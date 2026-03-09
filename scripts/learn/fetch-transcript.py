#!/usr/bin/env python3
"""
Holt ein YouTube-Transcript anhand einer Video-URL oder Video-ID.
Gibt das Transcript als Fliesstext auf stdout aus.

Strategie:
  1. Versucht YouTube-Captions ueber die API zu holen
  2. Bei TranscriptsDisabled: Audio via yt-dlp herunterladen und
     mit faster-whisper lokal transkribieren (GPU/CUDA bevorzugt)

Usage:
    fetch-transcript.py <url_or_id> [--lang de,en] [--whisper-model small]
"""

import sys
import re
import os
import argparse
import tempfile

# Adjust path for venv
SCRIPT_DIR = __import__("pathlib").Path(__file__).resolve().parent
VENV_PACKAGES = SCRIPT_DIR.parent / ".venv" / "lib"
# Find the python version directory dynamically
for p in VENV_PACKAGES.glob("python*/site-packages"):
    sys.path.insert(0, str(p))
    # CUDA-Libs aus pip-installierten nvidia-Paketen vorladen.
    # LD_LIBRARY_PATH wirkt nur bei Prozessstart -- daher muessen wir die
    # Shared Libraries explizit via ctypes laden, damit ctranslate2 sie findet.
    import ctypes
    _nvidia_libs_loaded = False
    for nvidia_lib in sorted(p.glob("nvidia/*/lib")):
        for so_file in sorted(nvidia_lib.glob("*.so*")):
            try:
                ctypes.CDLL(str(so_file), mode=ctypes.RTLD_GLOBAL)
                _nvidia_libs_loaded = True
            except OSError:
                pass  # Manche .so-Dateien sind Symlinks oder inkompatibel
    break

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def extract_video_id(url_or_id: str) -> str:
    """Extrahiert die Video-ID aus verschiedenen YouTube-URL-Formaten."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id  # Fallback: assume it's already an ID


def fetch_transcript_api(video_id: str, languages: list[str]) -> str:
    """Holt das Transcript via YouTube API und gibt es als Fliesstext zurueck.
    Wirft TranscriptsDisabled/NoTranscriptFound wenn keine Captions verfuegbar."""
    api = YouTubeTranscriptApi()
    try:
        transcript = api.fetch(video_id, languages=languages)
    except (TranscriptsDisabled, NoTranscriptFound):
        raise  # Caller handles fallback
    except Exception:
        # Fallback: try without language preference
        transcript = api.fetch(video_id)

    return _segments_to_text(transcript)


def _segments_to_text(segments) -> str:
    """Wandelt Transcript-Segmente in Fliesstext um."""
    lines = []
    for segment in segments:
        text = segment.text.strip() if hasattr(segment, 'text') else str(segment.get("text", "")).strip()
        if text and text not in ("[Music]", "[Musik]", "[Applause]"):
            lines.append(text)
    return " ".join(lines)


def _get_ffmpeg_path() -> str:
    """Findet den ffmpeg-Pfad -- erst System, dann imageio_ffmpeg."""
    import shutil
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise RuntimeError("ffmpeg nicht gefunden. Installiere: apt install ffmpeg ODER pip install imageio[ffmpeg]")


def fetch_transcript_whisper(video_id: str, languages: list[str], whisper_model: str = "small") -> str:
    """Fallback: Audio herunterladen und mit faster-whisper transkribieren."""
    import subprocess
    import shutil

    url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"[whisper-fallback] Captions nicht verfuegbar -- starte Audio-Transkription...", file=sys.stderr)
    print(f"[whisper-fallback] Modell: {whisper_model}, Sprache: {languages[0] if languages else 'auto'}", file=sys.stderr)

    # ffmpeg fuer faster-whisper im PATH bereitstellen
    ffmpeg_path = _get_ffmpeg_path()
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    env = os.environ.copy()
    env["PATH"] = ffmpeg_dir + os.pathsep + env.get("PATH", "")

    with tempfile.TemporaryDirectory(prefix="yt-whisper-") as tmpdir:
        audio_template = os.path.join(tmpdir, "audio.%(ext)s")

        # 1. Audio herunterladen via yt-dlp (ohne Konvertierung -- kein ffprobe noetig)
        print(f"[whisper-fallback] Audio wird heruntergeladen...", file=sys.stderr)
        yt_dlp_cmd = [
            sys.executable, "-m", "yt_dlp",
            "-f", "bestaudio",
            "-o", audio_template,
            "--no-playlist",
            "--quiet",
        ]

        # JS-Runtime: node nutzen falls vorhanden
        node_path = shutil.which("node")
        if node_path:
            yt_dlp_cmd.extend(["--js-runtimes", f"nodejs:{node_path}"])

        yt_dlp_cmd.append(url)
        result = subprocess.run(yt_dlp_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp fehlgeschlagen: {result.stderr.strip()}")

        # Audio-Datei finden (Extension variiert: webm, m4a, opus, ...)
        audio_path = None
        for f in os.listdir(tmpdir):
            if f.startswith("audio"):
                audio_path = os.path.join(tmpdir, f)
                break

        if not audio_path or not os.path.exists(audio_path):
            raise RuntimeError(f"Audio-Datei nicht gefunden in {tmpdir}")

        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"[whisper-fallback] Audio heruntergeladen ({size_mb:.1f} MB), starte Transkription...", file=sys.stderr)

        # 2. Transkribieren mit faster-whisper
        # ffmpeg muss im PATH sein, damit faster-whisper Audio dekodieren kann
        os.environ["PATH"] = env["PATH"]

        from faster_whisper import WhisperModel

        # CUDA bevorzugen, Fallback auf CPU
        try:
            model = WhisperModel(whisper_model, device="cuda", compute_type="float16")
            print(f"[whisper-fallback] Nutze GPU (CUDA, float16)", file=sys.stderr)
        except Exception as e:
            print(f"[whisper-fallback] GPU nicht verfuegbar ({e}), nutze CPU (int8)", file=sys.stderr)
            model = WhisperModel(whisper_model, device="cpu", compute_type="int8")

        lang = languages[0] if languages and languages[0] != "auto" else None
        segments, info = model.transcribe(audio_path, language=lang, beam_size=5)

        print(f"[whisper-fallback] Erkannte Sprache: {info.language} (p={info.language_probability:.2f})", file=sys.stderr)

        # Segmente sammeln
        lines = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                lines.append(text)

        transcript_text = " ".join(lines)
        print(f"[whisper-fallback] Transkription abgeschlossen ({len(lines)} Segmente)", file=sys.stderr)

        return transcript_text


def fetch_transcript(video_id: str, languages: list[str], whisper_model: str = "small") -> str:
    """Holt Transcript: erst API, bei Fehler Whisper-Fallback."""
    try:
        return fetch_transcript_api(video_id, languages)
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"[info] YouTube-Captions nicht verfuegbar ({type(e).__name__}), versuche Whisper-Fallback...", file=sys.stderr)
        return fetch_transcript_whisper(video_id, languages, whisper_model)


def get_video_title(video_id: str) -> str:
    """Versucht den Videotitel per oembed API zu holen."""
    try:
        import urllib.request
        import json
        url = f"https://www.youtube.com/oembed?url=https://youtube.com/watch?v={video_id}&format=json"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("title", "")
    except Exception:
        return ""


def slugify(text: str, max_len: int = 60) -> str:
    """Erzeugt einen URL-freundlichen Slug aus einem Titel."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    text = text.strip('-')
    return text[:max_len].rstrip('-')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript")
    parser.add_argument("url_or_id", help="YouTube URL or video ID")
    parser.add_argument("--lang", default="de,en", help="Comma-separated language preferences (default: de,en)")
    parser.add_argument("--meta", action="store_true", help="Include metadata header (url, title)")
    parser.add_argument("--whisper-model", default="small", help="Whisper model size: tiny/base/small/medium/large (default: small)")
    args = parser.parse_args()

    video_id = extract_video_id(args.url_or_id)
    languages = [l.strip() for l in args.lang.split(",")]

    title = get_video_title(video_id)
    transcript_text = fetch_transcript(video_id, languages, args.whisper_model)

    if args.meta:
        url = f"https://youtube.com/watch?v={video_id}"
        print(f"url: {url}")
        if title:
            print(f"title: {title}")
        print(f"type: YouTube-Transcript")
        print()

    if title:
        print(f"# {title}")
        print()

    print(transcript_text)

    # Output slug suggestion to stderr (for the calling skill)
    slug = slugify(title) if title else video_id
    print(f"SLUG:{slug}", file=sys.stderr)
