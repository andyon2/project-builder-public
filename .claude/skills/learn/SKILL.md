---
name: learn
description: Integriert neues Wissen in die Knowledge-Base. "alle" holt zuerst aus Notion, dann lokale Inbox. "notion" nur Notion. "lokal" nur lokale Inbox. Oder einzelne Datei angeben.
argument-hint: "[alle | notion | lokal | dateiname]"
allowed-tools: "Read, Write, Edit, Glob, Bash, Grep, WebFetch, mcp__notionApi__API-query-data-source, mcp__notionApi__API-patch-page"
context: fork
model: sonnet
---

Du integrierst neues Wissen in die Knowledge-Base des Project Builders.

## Kontext zuerst

Lies bei jedem Aufruf:
1. `knowledge/widersprueche.md` -- offene Konflikte kennen
2. `sources/log.md` -- was wurde bereits integriert
3. `teams.md` -- Routing-Tabelle (welche Teams gibt es, welche Wissensgebiete)

## Modus bestimmen

- `$ARGUMENTS` = **"alle"**: Zuerst Notion-Inbox abholen (Schritt N), dann lokale Inbox verarbeiten
- `$ARGUMENTS` = **"notion"**: Nur Notion-Inbox abholen (Schritt N), lokale Inbox ueberspringen
- `$ARGUMENTS` = **"lokal"**: Nur lokale Inbox verarbeiten (Schritt N ueberspringen)
- `$ARGUMENTS` = **[dateiname]**: Nur `sources/inbox/$ARGUMENTS` verarbeiten (Schritt N ueberspringen)

**Dateiformat:** Jedes lesbare Textformat wird akzeptiert (.md, .txt, ohne Extension). Beim Archivieren wird immer zu `.md` umbenannt.

---

## Schritt N: Notion-Inbox abholen (nur bei "alle")

### N.1 Notion abfragen

Query die Notes-DB `cd8b8484-6919-4e48-8cb1-be2c627a5ee5` mit:
```json
{
  "and": [
    {"property": "inboxed", "formula": {"checkbox": {"equals": true}}},
    {"property": "Created", "created_time": {"on_or_after": "2026-01-01"}}
  ]
}
```

Nur diese Properties abfragen (Token sparen): `title`, `G%3D%5C%5E` (URL), `oYqt` (Type), `kimN` (Created), `ugyE` (inboxed).
Sortierung: Created descending.

Falls keine Ergebnisse: Melde "Notion-Inbox leer" und weiter zu Schritt 0.

### N.2 KI-Relevanz pruefen

Fuer jeden Eintrag: Pruefe anhand des **Titels**, ob er KI-relevant ist.

**KI-relevant** wenn der Titel Begriffe enthaelt wie:
- KI, AI, Claude, Anthropic, OpenAI, GPT, ChatGPT, Gemini, LLM, ML
- Agent, Agentic, MCP, RAG, Prompt, Embedding, Token, Fine-Tuning, Transformer
- Cursor, Copilot, Windsurf, Coding Assistant, Vibe Coding
- Neural, Deep Learning, Machine Learning, NLP, Computer Vision
- Automation, Workflow + AI, API + AI

**Nicht KI-relevant:** Titel deutet klar auf andere Themen (Kochen, Musik, Gaming, etc.).

**Im Zweifelsfall:** Eher als KI-relevant einstufen.

### N.3 Inhalte fetchen und lokal ablegen

Fuer jeden KI-relevanten Eintrag mit URL:

**YouTube-URLs** (youtube.com/watch, youtu.be, youtube.com/shorts):
```bash
VENV_PYTHON="scripts/.venv/bin/python3"
FETCH_SCRIPT="scripts/learn/fetch-transcript.py"
$VENV_PYTHON $FETCH_SCRIPT "<url>" --meta 2>slug.tmp > "sources/inbox/notion-tmp.md"
SLUG=$(grep "^SLUG:" slug.tmp | cut -d: -f2)
mv "sources/inbox/notion-tmp.md" "sources/inbox/${SLUG}.md"
```

**Nicht-YouTube-URLs:** WebFetch, dann als Datei mit `url:` und `type: Artikel` Header schreiben.

**Kein URL:** Ueberspringen, in Zusammenfassung notieren.

**Bei Fetch-Fehler:** Ueberspringen, NICHTS in Notion setzen.

### N.4 In Notion als verarbeitet markieren

Fuer jeden erfolgreich geholten Eintrag zwei Properties setzen:
1. **Project** als Relation auf algron (`eb9b7f96-a925-4cb8-a113-1ac8d6acb1d6`) -- **das ist der kritische Schritt, der inboxed=false macht**
2. **Type** auf den passenden Wert aus der TYPE LIST (siehe unten) -- reine Kategorisierung, aendert inboxed nicht

NUR nach erfolgreichem Fetch + lokalem Speichern. Nie vorher.
Wenn der PATCH fuer Project fehlschlaegt, bleibt der Eintrag in der Inbox (gewuenschtes Verhalten).

```
PATCH page_id → properties: {
  "oYqt": {"select": {"name": "<type>"}},
  "%7CUS%7C": {"relation": [{"id": "eb9b7f96-a925-4cb8-a113-1ac8d6acb1d6"}]}
}
```

**TYPE LIST** (waehle genau 1):
`audiobook, book, fachartikel, game, glaubenssatz, idea, information, podcast, software, video, web clip`

Typische Zuordnung:
- YouTube-Video → `video`
- Blogartikel / Webseite → `web clip`
- Fachartikel / Paper → `fachartikel`
- Podcast-Transcript → `podcast`
- Software-Dokumentation → `software`
- Buch-Zusammenfassung → `book`
- Alles andere → `information`

### N.5 Notion-Zusammenfassung notieren

Merke dir fuer die finale Zusammenfassung (Schritt 9):
- Wie viele Eintraege in Notion gefunden
- Welche als KI-relevant geholt
- Welche uebersprungen (mit Grund)
- Welche Fehler auftraten

---

## Schritt 0: Lokale Inbox-Dateien vorbereiten

Pruefe JEDE Datei in `sources/inbox/`:

### URL-Only-Dateien erkennen

Eine Datei gilt als URL-Only, wenn sie:
- Nur eine URL enthaelt (ggf. mit Whitespace)
- Oder nur eine URL + wenige Woerter (z.B. "schau dir das an https://...")

### YouTube-URLs: Transcript automatisch holen

Wenn die Datei eine YouTube-URL enthaelt (youtube.com/watch, youtu.be, youtube.com/shorts) aber KEIN vollstaendiges Transcript:

```bash
VENV_PYTHON="scripts/.venv/bin/python3"
FETCH_SCRIPT="scripts/learn/fetch-transcript.py"
$VENV_PYTHON $FETCH_SCRIPT "<url>" --meta 2>slug.tmp > transcript.tmp
SLUG=$(grep "^SLUG:" slug.tmp | cut -d: -f2)
```

Ersetze den Inhalt der Inbox-Datei mit dem geholten Transcript (inkl. Metadaten-Header).

Falls das Fetching fehlschlaegt: Melde den Fehler, ueberspringe diese Datei, lass sie in der Inbox.

### Artikel-URLs: Inhalt per WebFetch holen

Wenn die Datei eine nicht-YouTube-URL enthaelt aber keinen substantiellen Inhalt:
- Nutze WebFetch um den Artikelinhalt zu holen
- Ersetze den Inhalt der Inbox-Datei mit dem geholten Text
- Fuege `url: [URL]` und `type: Artikel` am Anfang ein

### Bereits vorhandene Metadaten erkennen

Wenn die Datei bereits am Anfang optionale Metadaten-Zeilen hat, uebernimm sie:
```
url: https://...
title: ...
type: ...
date: ...
```
Diese Zeilen sind OPTIONAL. Aber wenn sie da sind, nutze sie.

### YouTube-URLs im Fliesstext

Wenn die Datei ein vollstaendiges Transcript enthaelt UND eine YouTube-URL darin vorkommt:
- Extrahiere die URL als Metadatum
- Das Transcript ist bereits vorhanden, kein Fetching noetig

Wenn `sources/inbox/` nach Schritt N und Schritt 0 immer noch leer ist: Melde das und beende.

---

## Verarbeitungs-Pipeline (pro Datei)

### 1. Quelle lesen und klassifizieren

Lies die Datei vollstaendig. Bestimme den Typ:
- YouTube-Transcript
- Artikel / Blogpost
- Report / Whitepaper
- Dokumentation
- Research / Studie
- Sonstiges

Bestimme einen **Archivnamen** fuer die Datei:
- Format: `YYYY-MM-DD_[slug].md`
- Der Slug wird aus dem Titel/Thema abgeleitet (lowercase, Bindestriche, max 60 Zeichen)
- Bei YouTube-Transcripts: Das Fetch-Script liefert den Slug via stderr
- Bei anderen Dateien: Aus der ersten Ueberschrift oder dem dominanten Thema ableiten

### 2. Erkenntnisse extrahieren und routen

Welche konkreten, verwertbaren Erkenntnisse enthaelt die Quelle? Filtere:
- **Behalten:** Neue Fakten, Techniken, Muster, Empfehlungen, Daten
- **Verwerfen:** Allgemeinplaetze, Marketing-Sprache, Wiederholungen von bereits Bekanntem

**Routing:** Lies `teams.md` und pruefe fuer jede Erkenntnis: Wer profitiert davon?

**A) Eigenes Wissen** (KI-Architektur, Prompting, Agent-Design, Skill-Design):
Bestimme die Ziel-Knowledge-Datei:
- `skill-best-practices.md` -- Skill-Design, -Architektur, -Wartung
- `token-optimization.md` -- Token-Sparstrategien, Modellwahl
- `entscheidungshierarchie.md` -- Skill vs. Agent Entscheidungen
- `content-humanization.md` -- Anti-GPTism, Textqualitaet, Design
- `session-state.md` -- Session-Management, Statusdateien
- `widersprueche.md` -- Konflikte zwischen Quellen
- Neue Datei unter `knowledge/[thema].md` falls kein Ziel passt
→ Weiter mit Schritt 3 (Verdichten).

**B) Fremdwissen** (betrifft Wissensgebiete eines anderen Teams, NICHT KI-Architektur):

1. Schreibe eine Dispatch-Notiz in `dispatches/[team-name]/YYYY-MM-DD_[slug].md`:
```markdown
# [Titel]

Quelle: [archivname] ([datum])

[3-5 Bullet Points: konkrete, verwertbare Erkenntnisse fuer dieses Team]

Vollstaendige Quelle: ~/project-builder/sources/archive/[monat]/[archivname]
```

2. Trage eine Zeile in `dispatches.md` ein (unter `## Offene Dispatches`):
```
- [ ] | YYYY-MM-DD | [team-name] | [Titel] | dispatches/[team-name]/YYYY-MM-DD_[slug].md
```

→ **NICHT** in `knowledge/` verdichten. Schritt 3 ueberspringen fuer diese Erkenntnis.

**C) Beides** (betrifft KI-Architektur UND ein anderes Team):
→ `knowledge/` verdichten (Schritt 3) UND Dispatch-Notiz + Zeile in `dispatches.md` schreiben.

**Harte Regel:** Wenn eine Erkenntnis nur ein anderes Team betrifft (z.B. Code-Review-Patterns fuer mr-review, Tanz-Didaktik fuer contaktart), gehoert sie NICHT in `knowledge/`. Nur Dispatch.

**Dispatch-Zustellung mr-review:** mr-review laeuft auf einem externen Server. Nach dem Schreiben einer Dispatch-Notiz fuer mr-review, synchronisiere NUR die neue Dispatch-Datei:
```bash
rsync -av dispatches/mr-review/[neue-datei].md andreas@77.42.39.93:~/claude-projects/mr-review/dispatches/
```
**Harte Regeln fuer Server-Zugriff:**
- NUR `dispatches/` beschreiben, NIE andere Dateien auf dem Server aendern
- NIE `--delete` verwenden (Server-Dateien koennten vom dortigen Team stammen)
- NIE `main-agent.md`, `scripts/`, `knowledge/` oder andere Dateien ueberschreiben

### 3. Verdichten, nicht nur ablegen (nur fuer eigenes Wissen)

Fuer jede Erkenntnis pruefe gegen den bestehenden Knowledge-Stand:

**A) Bestaetigung:** Die Erkenntnis deckt sich mit bestehendem Wissen.
- Nicht redundant einfuegen. Stattdessen: In der Quellen-Sektion die neue Quelle als zusaetzlichen Beleg ergaenzen.
- Nur wenn die neue Quelle eine *praezisere Formulierung* oder *konkretere Zahlen* liefert, den bestehenden Text aktualisieren.

**B) Erweiterung:** Die Erkenntnis ist neu und ergaenzt bestehendes Wissen.
- In die passende Sektion einfuegen, mit `[Neu: YYYY-MM-DD]` markieren.
- In der Quellen-Sektion die Quelle mit Kurzbeschreibung ergaenzen.

**C) Widerspruch:** Die Erkenntnis widerspricht bestehendem Wissen.
- NICHT leise ueberschreiben.
- Neuen Eintrag in `knowledge/widersprueche.md` erstellen:
  ```
  ## [Kurztitel]
  - **Position A** ([bestehende Quelle]): [Zusammenfassung]
  - **Position B** ([neue Quelle]): [Zusammenfassung]
  - **Aktueller Stand:** Ungeloest
  - **Naechster Schritt:** [Was wuerde die Frage klaeren?]
  ```
- Im betroffenen Knowledge-Abschnitt einen Verweis ergaenzen: `[Widerspruch: siehe widersprueche.md#kurztitel]`

**D) Veraltung:** Die Erkenntnis macht bestehendes Wissen obsolet (z.B. neues Modellverhalten).
- Bestehenden Text mit `[Veraltet seit YYYY-MM-DD, siehe: Quelle]` markieren.
- Neue Information direkt darunter einfuegen.
- In der Quellen-Sektion dokumentieren.

### 4. Knowledge-Dateien aktualisieren

Fuehre die in Schritt 3 bestimmten Aenderungen durch. Halte dich an die bestehende Struktur jeder Datei.

**Quellen-Sektion:** Jede Knowledge-Datei hat am Ende eine `## Quellen`-Sektion. Ergaenze dort die neue Quelle im Format:
```
- [archivname] (YYYY-MM-DD) -- [Was diese Quelle zu dieser Datei beigetragen hat]
```

### 5. Masterprompt-Impact pruefen

Lies die aktuelle Masterprompt-Version (Datei mit hoechstem `v`-Suffix im Root).

Pruefe: Erfordern die neuen Erkenntnisse Aenderungen am Masterprompt?
- Neue Prinzipien fuer die Saeulen?
- Aenderungen an Templates?
- Neue Qualitaetsprinzipien?
- Veraltete Empfehlungen?

Falls ja: Schreibe Aenderungsvorschlaege in `knowledge/masterprompt-aenderungen.md`.

### 6. Datei archivieren und umbenennen

```bash
MONTH=$(date +%Y-%m)
mkdir -p sources/archive/$MONTH
mv "sources/inbox/[originaldatei]" "sources/archive/$MONTH/[archivname]"
```

### 7. Log aktualisieren

Fuege eine neue Zeile in `sources/log.md` ein:
```
| [archivname] | [Typ] | [YYYY-MM-DD] | [YYYY-MM]/ |
```

### 8. Changelog-Eintrag

Fuege einen Eintrag in `changelog.md` ein:
```
### Wissensupdate: [Thema] (YYYY-MM-DD)
- Quelle: [archivname] ([Typ])
- Aktualisiert: [Liste der geaenderten knowledge/-Dateien]
- Dispatches: [Team-Name → Datei, oder "keine"]
- Widersprueche: [ja/nein -- falls ja, Kurztitel]
- Masterprompt-Impact: [ja/nein]
```

### 9. Zusammenfassung

Gib im Chat zurueck:

Falls Notion abgefragt wurde (Modus "alle"):
```
## Notion-Inbox
- Gefunden: [Anzahl] Eintraege
- KI-relevant geholt: [Liste mit Titel]
- Uebersprungen: [Liste mit Grund]
- Fehler: [Liste, falls vorhanden]
```

Pro verarbeiteter Datei:
- **Verarbeitet:** [Archivname] ([Typ])
- **Erkenntnisse:** [3-5 Bullet Points]
- **Eigenes Wissen:** [Knowledge-Dateien, die aktualisiert wurden]
- **Dispatches:** [Team-Name → Dispatch-Datei, fuer jedes Team das etwas bekam]
- **Verdichtung:** [Bestaetigung/Erweiterung/Widerspruch/Veraltung]
- **Widersprueche:** [Neue Eintraege, falls vorhanden]
- **Masterprompt:** [Aenderungsvorschlaege, falls vorhanden]
- **Offene Fragen:** [Falls vorhanden]
