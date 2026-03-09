#!/bin/bash
# Setup-Script fuer neue Project-Builder-Instanzen.
# Kopiert Templates, fragt nach Integrationen, erstellt Instanz-Dateien.
#
# Usage: ./scripts/setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Project Builder Setup ==="
echo ""

# --- CLAUDE.md ---
if [ -f "$PROJECT_DIR/CLAUDE.md" ]; then
  echo "CLAUDE.md existiert bereits -- uebersprungen."
else
  cp "$PROJECT_DIR/CLAUDE.md.template" "$PROJECT_DIR/CLAUDE.md"
  echo "CLAUDE.md erstellt (aus Template)."
fi

# --- teams.md ---
if [ -f "$PROJECT_DIR/teams.md" ]; then
  echo "teams.md existiert bereits -- uebersprungen."
else
  cp "$PROJECT_DIR/teams.md.template" "$PROJECT_DIR/teams.md"
  echo "teams.md erstellt (aus Template). Trage deine Agent-Teams ein."
fi

# --- dispatches.md ---
if [ -f "$PROJECT_DIR/dispatches.md" ]; then
  echo "dispatches.md existiert bereits -- uebersprungen."
else
  cp "$PROJECT_DIR/dispatches.md.template" "$PROJECT_DIR/dispatches.md"
  echo "dispatches.md erstellt (aus Template)."
fi

# --- dispatches/ Verzeichnis ---
mkdir -p "$PROJECT_DIR/dispatches"
if [ ! -f "$PROJECT_DIR/dispatches/.gitkeep" ]; then
  touch "$PROJECT_DIR/dispatches/.gitkeep"
fi

# --- sources/ Verzeichnisse ---
mkdir -p "$PROJECT_DIR/sources/inbox"
mkdir -p "$PROJECT_DIR/sources/archive"
if [ ! -f "$PROJECT_DIR/sources/log.md" ]; then
  echo "# Integrationslog" > "$PROJECT_DIR/sources/log.md"
  echo "" >> "$PROJECT_DIR/sources/log.md"
  echo "| Datum | Quelle | Ziel | Aktion |" >> "$PROJECT_DIR/sources/log.md"
  echo "|-------|--------|------|--------|" >> "$PROJECT_DIR/sources/log.md"
  echo "sources/log.md erstellt."
fi

# --- config/ ---
mkdir -p "$PROJECT_DIR/config"

# --- Notion-Integration ---
echo ""
read -p "Notion-Integration einrichten? (j/n): " NOTION_ANSWER
if [[ "$NOTION_ANSWER" == "j" ]]; then
  if [ -f "$PROJECT_DIR/config/notion.md" ]; then
    echo "config/notion.md existiert bereits -- uebersprungen."
  else
    cp "$PROJECT_DIR/config/notion.md.example" "$PROJECT_DIR/config/notion.md"
    echo ""
    echo "config/notion.md erstellt. Bitte IDs eintragen:"
    echo "  1. Notion-Integration erstellen: https://www.notion.so/my-integrations"
    echo "  2. Datenbank-ID und Project-Relation-ID in config/notion.md eintragen"
    echo "  3. MCP-Server konfigurieren (siehe Notion MCP Docs)"
  fi
else
  echo "Notion uebersprungen. Kann spaeter mit config/notion.md.example eingerichtet werden."
fi

# --- Globaler Shortcut ---
echo ""
read -p "Globalen Shortcut 'project-builder' einrichten? (j/n): " SHORTCUT_ANSWER
if [[ "$SHORTCUT_ANSWER" == "j" ]]; then
  mkdir -p ~/.local/bin
  ln -sf "$PROJECT_DIR/scripts/project-builder" ~/.local/bin/project-builder
  echo "Symlink erstellt: ~/.local/bin/project-builder"
  if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo ""
    echo "HINWEIS: ~/.local/bin ist nicht im PATH. Fuege hinzu:"
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
  fi
else
  echo "Shortcut uebersprungen. Starte mit: ./scripts/project-builder"
fi

# --- Python-Umgebung ---
echo ""
read -p "Python-Umgebung fuer YouTube-Transcripts einrichten? (j/n): " PYTHON_ANSWER
if [[ "$PYTHON_ANSWER" == "j" ]]; then
  python3 -m venv "$PROJECT_DIR/scripts/.venv"
  "$PROJECT_DIR/scripts/.venv/bin/pip" install -q youtube-transcript-api yt-dlp faster-whisper "imageio[ffmpeg]"
  echo "Python-Umgebung eingerichtet."
else
  echo "Python uebersprungen. /learn funktioniert ohne -- nur YouTube-Transcripts sind eingeschraenkt."
fi

echo ""
echo "=== Setup abgeschlossen ==="
echo ""
echo "Naechste Schritte:"
echo "  1. teams.md: Trage deine Agent-Teams ein"
if [[ "$NOTION_ANSWER" == "j" ]]; then
  echo "  2. config/notion.md: Trage deine Notion-IDs ein"
fi
echo "  Starte mit: project-builder (oder ./scripts/project-builder)"
echo ""
echo "Weitere Integrationen koennen unter config/ als Markdown-Datei angelegt werden."
echo "Der Agent erkennt sie automatisch."
