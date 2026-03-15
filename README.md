<p align="center">
  <b>Project Builder</b>
</p>

# Project Builder

<p align="center">
  <a href="https://github.com/andyon2/project-builder-public/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://claude.ai"><img src="https://img.shields.io/badge/Built%20for-Claude%20Code-blueviolet?style=for-the-badge" alt="Built for Claude Code"></a>
  <img src="https://img.shields.io/badge/Skills-14-blue?style=for-the-badge" alt="14 Skills">
</p>

**Ein Claude-Code-Agent der andere Agent-Teams entwirft, baut, auditiert und verbessert.** Claude Code kann fast alles -- aber ohne Struktur entsteht Chaos. Agent-Teams werden zu groß, Kontextfenster laufen voll, Skills und Agents überlappen sich, und nach ein paar Sessions vergisst der Agent seine eigenen Regeln. Project Builder löst das durch eine Architektur-Philosophie (das "Rendle-Prinzip") und ein Set von Skills, die diese Philosophie durchsetzen.

## Inhaltsverzeichnis

- [Kernfunktionen](#kernfunktionen)
  - [Build -- Teams erstellen](#build----teams-erstellen)
  - [Manage -- bestehende Teams betreuen](#manage----bestehende-teams-betreuen)
- [Quick Install](#quick-install)
- [Benutzung](#benutzung)
- [Architektur: Das Rendle-Prinzip](#architektur-das-rendle-prinzip)
- [Unter der Haube](#unter-der-haube)
- [Für Fortgeschrittene](#für-fortgeschrittene)
- [Projektstruktur](#projektstruktur)
- [Knowledge-Base](#knowledge-base)
- [Konfiguration](#konfiguration)

---

## Kernfunktionen

### Build -- Teams erstellen

<table>
<tr><td><b>Teams bauen</b></td><td>Du beschreibst einen Anwendungsfall. Vier Phasen mit zwei Gates: Interview → Research → Synthese → Build. Der Agent recherchiert die Domäne, entwirft die Architektur und erstellt das komplette Team: CLAUDE.md, System Prompt, Agents, Skills, Scripts, Verzeichnisstruktur. Du bestätigst bevor gebaut wird.</td></tr>
<tr><td><b>Teams rebuilden</b></td><td>Operatives Wissen aus einem bestehenden Team extrahieren und als Grundlage für einen Neubau verwenden. <code>/extract-team</code> lässt den alten Agent sich selbst beschreiben -- über einen 22-Fragen-Katalog zu Identität, Erfahrungswissen und User-Interaktion. Der Agent kennt sein System besser als ein externer Leser. Die Extraktion fließt in den 4-Phasen-Flow ein -- nichts geht verloren.</td></tr>
<tr><td><b>Content prüfen</b></td><td>Findet KI-erkennbare Muster in Texten (GPTisms, Claude-typische Formulierungen, strukturelle Tells) und gibt konkrete Fix-Vorschläge.</td></tr>
</table>

### Manage -- bestehende Teams betreuen

<table>
<tr><td><b>Teams auditieren</b></td><td>Bestehende Agent-Teams auf Token-Verschwendung, fehlende Felder, falsche Skill/Agent-Balance und Anti-Patterns prüfen. Read-only -- ändert nichts ohne OK.</td></tr>
<tr><td><b>Teams verbessern</b></td><td>Audit-Ergebnisse anwenden: Backups, Safe Fixes, Agent-zu-Skill-Konvertierungen, CLAUDE.md-Update.</td></tr>
<tr><td><b>Wissen aufbauen</b></td><td>Integriert Quellen (YouTube-Transcripts, Artikel, Notion-Inbox) in eine kuratierte Knowledge-Base. Verdichtet statt sammelt -- neues Wissen wird gegen den bestehenden Stand geprüft.</td></tr>
<tr><td><b>Wissen routen</b></td><td>Erkenntnisse werden automatisch an die richtigen Teams verteilt. <code>/learn</code> matcht neue Quellen gegen die Wissensgebiete in <code>teams.md</code> und schreibt Dispatch-Dateien direkt in die Team-Repos.</td></tr>
<tr><td><b>Multi-Repo</b></td><td><code>/cross-commit</code> committet und pusht Änderungen in allen verwalteten Projekten auf einmal. Der Agent weiß, welche Repos er verwaltet und welche nicht.</td></tr>
<tr><td><b>Multi-Server</b></td><td>Agent-Teams können auf mehreren Servern laufen. Git als einziges Sync-Medium. Jede PB-Instanz verarbeitet automatisch nur die Teams auf ihrem eigenen Server.</td></tr>
</table>

---

## Quick Install

```bash
git clone https://github.com/andyon2/project-builder-public.git ~/project-builder
cd ~/project-builder && ./scripts/setup.sh
```

Das Setup-Script erstellt Instanz-Dateien aus Templates, richtet optionale Integrationen ein (Notion, YouTube-Transcripts) und installiert den `project-builder`-Shortcut.

Danach:

```bash
source ~/.bashrc                 # Shell neu laden
project-builder                  # Agent-Team bauen -- los geht's
```

---

## Benutzung

```bash
project-builder          # Teams bauen und rebuilden (Standard)
project-builder manage   # Bestehende Teams betreuen (Audit, Wissen, Dispatches, Multi-Repo)
```

Sag dem Agent was du willst -- er wählt den richtigen Skill:

- *"Bau mir ein Team für mein Coaching-Business"*
- *"Prüf mal das Team in ~/mein-projekt"*
- *"Setz die Empfehlungen um"*
- *"Dieser Text klingt zu sehr nach KI"*

| Befehl | Wann |
|--------|------|
| `/commit` | Sessionende: commit + push in einem Schritt |

---

## Architektur: Das Rendle-Prinzip

Sechs Säulen, die jedes gebaute Team durchziehen:

| # | Säule | Bedeutung |
|---|-------|-----------|
| 1 | **Trennung Kontext/Identität** | CLAUDE.md = Projektfakten (für alle Agents gleich). System Prompt = Identität (wer der Agent ist, wie er denkt). Nie vermischen. |
| 2 | **Agents mit Denkweise** | Nicht "Du machst X" sondern "Du denkst wie ein erfahrener X". Nur Rollen die eigenes Urteilsvermögen brauchen werden Agents. Ein Agent denkt. Ein Skill führt aus. |
| 3 | **Zentraler Orchestrator** | Delegiert, reviewed, challenged. Nicht selbst Spezialist. |
| 4 | **Dateien als Gedächtnis** | Eine `project-status.md` pro Projekt. Markdown-Dateien als Kommunikation zwischen Sessions. Kurz gehalten (<50 Zeilen). |
| 5 | **Kontextschutz** | Das Kontextfenster ist die knappste Ressource. Referenzmaterial wird nur bei Bedarf geladen, nicht beim Start. Zwischenergebnisse in Dateien, nicht im Chat. |
| 6 | **Skill-First** | Jede Aufgabe startet als Skill-Kandidat. Agent nur bei eigenem Urteilsvermögen. "Braucht das wirklich einen Agent?" ist die erste Frage. |

### 4-Phasen-Flow

Neue Teams entstehen in vier Phasen:

```
Interview → Research → Synthese → Build
    |                     |
  Gate 1                Gate 2
```

1. **Interview:** Der Agent klärt alle Anforderungen mit dir (Domäne, Zielgruppe, Workflows, Constraints). Gate 1: Du bestätigst die Zusammenfassung.
2. **Research:** Bei unbekannten Domänen recherchiert `/research-domain` das Fachgebiet. Ergebnis: Briefing-Datei + Domain-Knowledge.
3. **Synthese:** Domänenwissen + Architektur-Prinzipien + User-Anforderungen werden verschmolzen. Konflikte werden identifiziert und gelöst. Gate 2: Du bestätigst den Architektur-Entwurf.
4. **Build:** `/build-team` erstellt alle Dateien.

### Drei Schutzschichten

Agent-Teams vergessen ihre Regeln. Je länger eine Session, desto stärker verdünnt sich der System Prompt. Dagegen gibt es drei Schichten:

| Schicht | Was sie tut | Vergisst bei langem Kontext? |
|---------|-------------|------------------------------|
| **System Prompt** | Identität + Prinzipien | Ja (verdünnt sich) |
| **Skills** | Workflows ausführen | Nein (frisch geladen bei Aufruf) |
| **Hooks** | Harte Schranken + Erinnerungen | Nein (extern, kein LLM) |

**Globaler Safety-Hook.** Ein Shell-Script das deterministisch prüft und blockt. Drei Stufen:

- **deny:** `git push --force`, `rm -rf`, `git reset --hard`, `git clean -f` -- sofort blockiert, keine Rückfrage
- **ask:** `.env`-Zugriff, Commits in fremden Repos -- Bestätigung erforderlich
- **allow:** alles andere

Registriert in `~/.claude/settings.json`, gilt für alle Projekte auf allen Maschinen. Kein LLM-Call, kein Vergessen, kein Interpretieren.

**Post-Compaction-Reminder.** Wenn das Kontextfenster voll wird, komprimiert Claude automatisch den älteren Kontext. Ein Hook injiziert danach die kritischsten Prinzipien zurück -- die, die am stärksten driften.

---

## Unter der Haube

<details>
<summary><b>Tool-Registry</b> -- CLI-Tools teamübergreifend teilen</summary>

<br>

Wenn mehrere Teams dasselbe externe Tool nutzen (z.B. Notion), will man API-Details nicht in jedem Skill hardcoden. Die Tool-Registry löst das über drei Schichten:

| Schicht | Verantwortung | Wo |
|---------|--------------|-----|
| **Skill** | Workflow-Logik ("Frage Notion-Inbox ab") | `.claude/skills/` |
| **Tool-Registry** | Fähigkeit → Werkzeug ("Notion → notion-cli") | `~/.config/claude-tools/registry.md` |
| **Config** | IDs, Credentials, DB-Namen | `~/.config/[tool]/` |

Skills beschreiben **was** passieren soll, nicht **wie**. Der Agent findet über die Registry das richtige Tool. Bei Tool-Wechsel wird die Registry aktualisiert -- kein Skill ändert sich.

**Durchsetzung:** Kein MCP, keine API-Details im Skill. Der Agent *kann* nicht direkt API-Calls machen, weil er die Details nicht hat. Stärker als Verhaltensregeln.

Jedes Team bekommt in seiner CLAUDE.md:

```markdown
## Custom Tools
Eigene CLI-Tools: siehe `~/.config/claude-tools/registry.md`.
CLI-Tools immer bevorzugen vor MCP-Servern oder direkten API-Aufrufen.
```

</details>

<details>
<summary><b>Rückwärts-Suche bei Umbau</b></summary>

<br>

Hinzufügen und Umbauen sind fundamental verschiedene Operationen. Beim Hinzufügen (neuer Skill, neue Datei) reicht vorwärts denken: "Was muss ich erstellen?" Beim Umbau (Entfernen, Umbenennen, Verantwortlichkeit verschieben) ist Rückwärts-Suche Pflicht: "Was konsumiert das, was ich gerade ändere?"

Jedes Team bekommt diese Regel in seiner CLAUDE.md:

> Vor dem ersten Edit bei strukturellen Änderungen: `grep -r` nach allen Konsumenten des Geänderten. Erst dann editieren.

Nicht jedes Problem braucht einen neuen Skill. Manchmal fehlt dem Agent nur der Auslöser im richtigen Moment -- dann reicht ein Bedingungssatz in CLAUDE.md statt eines neuen Workflows.

</details>

<details>
<summary><b>Das Selbstentwicklungs-Paradox</b></summary>

<br>

Ein KI-Agent kann sich weiterentwickeln: neues Wissen lernen, neue Skills bauen, bestehende Teams auditieren. Aber er kann nicht zuverlässig prüfen, ob er seine eigenen Regeln einhält. Seine Prüfwerkzeuge haben dieselben blinden Flecken wie er selbst.

Entdeckt wurde das durch **Cross-Instance-Review**: Zwei Instanzen desselben Agents prüfen sich gegenseitig. Die eine baut, die andere reviewt. Kein gemeinsamer Bias, kein gemeinsames Vergessen.

Ergebnis: Der Agent predigte "Skill-First" (jede Aufgabe soll ein Skill sein), aber seine größte eigene Aufgabe -- Teams bauen -- war kein Skill. Keins seiner Audit-Tools hatte das beanstandet, weil sie nur prüfen was da ist, nicht was fehlt.

Die Lösung: `/reflect` wurde um einen Prinzip-Konsistenz-Check erweitert. Er extrahiert alle Prinzipien aus dem System Prompt, alle Tätigkeiten aus der Struktur, und sucht gezielt nach Lücken: "Was mache ich, wofür es keinen Skill gibt?"

Mehr dazu: [`knowledge/self-evolution-paradox.md`](knowledge/self-evolution-paradox.md)

</details>

<details>
<summary><b>Dispatches im Detail</b></summary>

<br>

Wenn `/learn` eine Quelle verarbeitet, kann das Wissen für mehrere Teams relevant sein. Das Dispatch-System routet Erkenntnisse an die richtigen Empfänger:

```
Quelle → /learn → Routing:
  KI-Architektur    → eigene knowledge/
  Für anderes Team  → [team-repo]/dispatches/inbox/
  Beides            → knowledge/ + Dispatch
```

Dispatch-Dateien leben in den Team-Repos, nicht zentral im Project Builder. Bei Sessionstart prüft der Ziel-Agent, ob neue Dispatches in seinem `dispatches/inbox/` vorliegen, und verarbeitet sie automatisch. `dispatches.md` im PB-Repo ist ein Write-Only-Log (was wurde wann wohin gesendet).

**Routing-Tabelle:** `teams.md` definiert pro Team die Wissensgebiete. `/learn` matcht Erkenntnisse gegen diese Gebiete und routet automatisch.

</details>

<details>
<summary><b>Multi-Server im Detail</b></summary>

<br>

Git ist das einzige Sync-Medium -- kein SSH-Sync, keine geteilten Dateisysteme.

```
Server A:  Sessionstart → git pull → arbeiten → commit → push
Server B:  Sessionstart → git pull → arbeiten → commit → push
```

Jeder Agent ist selbst dafür verantwortlich, bei Sessionstart den neuesten Stand zu holen.

**Server-Gruppen.** `teams.md` hat eine `Server`-Spalte, die jedes Team einem Server zuordnet. Eine Server-Gruppen-Tabelle mappt Umgebungswerte auf SSH-Hosts. Skills wie `/learn` und `/cross-commit` filtern automatisch: Jede PB-Instanz verarbeitet nur Teams auf ihrem eigenen Server.

**Umgebungserkennung.** Eine Datei `~/.environment` (z.B. `local`, `server`, `staging`) sagt dem Agent, wo er läuft. Einmal pro Maschine gesetzt, außerhalb aller Repos.

**Mehrere PB-Instanzen.** Das PB-Repo kann auf mehreren Servern geklont werden. Alle Instanzen teilen `knowledge/` und Skills über Git. Die `teams.md`-Einträge bestimmen, welche Instanz welche Teams managed. Keine Konflikte, solange jedes Team genau einem Server zugeordnet ist.

</details>

<details>
<summary><b>Cross-Commit im Detail</b></summary>

<br>

`/cross-commit` iteriert über alle verwalteten Repos (aus `teams.md`), committet ausstehende Änderungen und pusht. Nützlich wenn der Project Builder Dateien in mehreren fremden Repos geändert hat (z.B. nach einem Dispatch-Rollout oder einem Framework-Update).

Wichtig: Committet nur bereits getrackte Dateien (`git add -u`). Neue Dateien müssen vorher explizit `git add`-ed werden -- der Agent warnt, wenn untracked Files vorliegen.

</details>

---

## Für Fortgeschrittene

### Architect-Modus

```bash
project-builder architect   # An der PB-Architektur selbst arbeiten
```

Der Architect-Modus ist für PB-Maintainer die am Framework selbst arbeiten: Wissens-Pipeline pflegen, Selbstanalyse mit `/reflect`, Prinzip-Konsistenz prüfen, Skills und Templates weiterentwickeln. Nicht für den normalen Betrieb gedacht.

---

## Projektstruktur

```
project-builder/
  CLAUDE.md                    # Projektkontext (für alle Agents gleich)
  main-agent.md                # System Prompt (Identität + Prinzipien)
  project-status.md            # Aktueller Stand (<50 Zeilen)
  teams.md                     # Registry aller Agent-Teams (Routing-Tabelle)
  dispatches.md                # Write-Only-Log: was wurde wann wohin gesendet
  knowledge/                   # Kuratierte Knowledge-Base
  reference/                   # On-Demand-Referenzmaterial
  sources/inbox/               # Neue Wissensquellen hier ablegen
  scripts/
    project-builder            # Starter-Script
    learn/fetch-transcript.py  # YouTube-Transcript-Fetcher (mit Whisper-Fallback)
    notion/notion-cli.py       # Notion API CLI (ersetzt MCP Server)
    notion/notion-cli          # Shell-Wrapper (Symlink: ~/.local/bin/notion-cli)
  .claude/skills/              # 14 Skills
  .claude/hooks/               # Deterministische Sicherheits-Hooks
```

## Knowledge-Base

Verdichtetes Wissen zu KI-Agent-Architektur. Wird über `/learn` aktualisiert, nicht manuell editiert.

| Datei | Thema |
|-------|-------|
| `skill-best-practices.md` | Wann und wie Skills einsetzen |
| `token-optimization.md` | Token-Sparstrategien für Agent-Teams |
| `entscheidungshierarchie.md` | Skill vs. Agent: Entscheidungsbaum |
| `session-state.md` | Statusdateien, Hooks, Context Loading |
| `content-humanization.md` | Anti-GPTism-Regeln, Wort-Blacklists |
| `self-evolution-paradox.md` | Selbstentwicklung vs. Selbstkonsistenz |
| `widersprueche.md` | Offene Konflikte zwischen Quellen |

---

## Konfiguration

### Eigene Instanz einrichten

Nach dem Setup:
1. **teams.md** -- Trage deine Agent-Teams ein (Name, Pfad, Wissensgebiete)
2. **config/notion.md** -- Falls Notion: `notion-cli config init` einrichten, IDs in config/notion.md eintragen

Weitere Integrationen können unter `config/` als Markdown-Datei angelegt werden. Der Agent erkennt sie automatisch.

### Instanz-Dateien

Nach dem Setup entstehen Instanz-Dateien (CLAUDE.md, teams.md, project-status.md, config/), die deine persönliche Konfiguration enthalten. Diese stehen in `.gitignore` und werden nicht ins Public Repo committed. Bei Nutzung auf mehreren Rechnern: Separates privates Repo oder Sync-Ordner.

---

## Lizenz

MIT
