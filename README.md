# Project Builder

Ein Claude-Code-Agent der andere Agent-Teams entwirft, baut, auditiert und verbessert.

## Das Problem

Claude Code kann fast alles -- aber ohne Struktur entsteht Chaos. Agent-Teams werden zu groß, Kontextfenster laufen voll, Skills und Agents überlappen sich, und nach ein paar Sessions vergisst der Agent seine eigenen Regeln.

Project Builder löst das durch eine Architektur-Philosophie (das "Rendle-Prinzip") und ein Set von Skills, die diese Philosophie durchsetzen -- auch auf sich selbst.

## Was er kann

**Teams bauen:** Du beschreibst einen Anwendungsfall. Der Project Builder klärt mit dir die Anforderungen, recherchiert die Domäne und erstellt das komplette Team: CLAUDE.md, System Prompt, Agents, Skills, Scripts, Verzeichnisstruktur. Vier Phasen mit zwei Gates -- du bestätigst bevor gebaut wird.

**Teams auditieren:** Bestehende Agent-Teams auf Token-Verschwendung, fehlende Felder, falsche Skill/Agent-Balance und Anti-Patterns prüfen. Read-only -- ändert nichts ohne OK.

**Teams verbessern:** Audit-Ergebnisse anwenden: Backups, Safe Fixes, Agent-zu-Skill-Konvertierungen, CLAUDE.md-Update.

**Teams rebuilden:** Operatives Wissen aus einem bestehenden Team extrahieren und als Grundlage für einen Neubau verwenden. Die Extraktion fließt in den 4-Phasen-Flow ein -- nichts geht verloren.

**Wissen aufbauen:** Integriert Wissensquellen (YouTube-Transcripts, Artikel, Notion-Inbox) in eine kuratierte Knowledge-Base. Verdichtet statt sammelt -- neues Wissen wird gegen den bestehenden Stand geprüft.

**Content prüfen:** Findet KI-erkennbare Muster in Texten (GPTisms, Claude-typische Formulierungen, strukturelle Tells) und gibt konkrete Fix-Vorschläge.

**Über Repos hinweg arbeiten:** `/cross-commit` committet und pusht Änderungen in allen verwalteten Projekten auf einmal. Der Agent weiß, welche Repos er verwaltet und welche nicht.

## Architektur: Das Rendle-Prinzip

Sechs Säulen, die jedes Team durchziehen:

1. **Trennung Kontext/Identität.** CLAUDE.md = Projektfakten (für alle Agents gleich). System Prompt = Identität (wer der Agent ist, wie er denkt). Nie vermischen.

2. **Agents mit Denkweise.** Nicht "Du machst X" sondern "Du denkst wie ein erfahrener X". Nur Rollen die eigenes Urteilsvermögen brauchen werden Agents. Ein Agent denkt. Ein Skill führt aus.

3. **Main-Agent als Orchestrator.** Delegiert, reviewed, challenged. Nicht selbst Spezialist.

4. **Dateien als Gedächtnis.** Eine `project-status.md` pro Projekt. Markdown-Dateien als Kommunikation zwischen Sessions. Kurz gehalten (<50 Zeilen).

5. **Kontextschutz.** Das Kontextfenster ist die knappste Ressource. Referenzmaterial wird nur bei Bedarf geladen, nicht beim Start. Zwischenergebnisse in Dateien, nicht im Chat.

6. **Skill-First.** Jede Aufgabe startet als Skill-Kandidat. Agent nur bei eigenem Urteilsvermögen. "Braucht das wirklich einen Agent?" ist die erste Frage.

### 4-Phasen-Flow für Team-Building

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

Vorher baute der Agent Teams direkt aus dem Interview -- ohne Domänenwissen, ohne Synthese-Schritt. Die Research-Phase schließt diese Lücke.

### Rückwärts-Suche bei Umbau

Hinzufügen und Umbauen sind fundamental verschiedene Operationen. Beim Hinzufügen (neuer Skill, neue Datei) reicht vorwärts denken: "Was muss ich erstellen?" Beim Umbau (Entfernen, Umbenennen, Verantwortlichkeit verschieben) ist Rückwärts-Suche Pflicht: "Was konsumiert das, was ich gerade ändere?"

Jedes Team bekommt diese Regel in seiner CLAUDE.md:

> Vor dem ersten Edit bei strukturellen Änderungen: `grep -r` nach allen Konsumenten des Geänderten. Erst dann editieren.

Nicht jedes Problem braucht einen neuen Skill. Manchmal fehlt dem Agent nur der Auslöser im richtigen Moment -- dann reicht ein Bedingungssatz in CLAUDE.md statt eines neuen Workflows.

### Tool-Registry: CLI-Tools teamübergreifend teilen

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

## Das Selbstentwicklungs-Paradox

Ein KI-Agent kann sich weiterentwickeln: neues Wissen lernen, neue Skills bauen, bestehende Teams auditieren. Aber er kann nicht zuverlässig prüfen, ob er seine eigenen Regeln einhält. Seine Prüfwerkzeuge haben dieselben blinden Flecken wie er selbst.

Entdeckt wurde das durch **Cross-Instance-Review**: Zwei Instanzen desselben Agents prüfen sich gegenseitig. Die eine baut, die andere reviewt. Kein gemeinsamer Bias, kein gemeinsames Vergessen.

Ergebnis: Der Agent predigte "Skill-First" (jede Aufgabe soll ein Skill sein), aber seine größte eigene Aufgabe -- Teams bauen -- war kein Skill. Keins seiner Audit-Tools hatte das beanstandet, weil sie nur prüfen was da ist, nicht was fehlt.

Die Lösung: `/reflect` wurde um einen Prinzip-Konsistenz-Check erweitert. Er extrahiert alle Prinzipien aus dem System Prompt, alle Tätigkeiten aus der Struktur, und sucht gezielt nach Lücken: "Was mache ich, wofür es keinen Skill gibt?"

Mehr dazu: [`knowledge/self-evolution-paradox.md`](knowledge/self-evolution-paradox.md)

## Benutzung

### Starten

```bash
project-builder main     # Architektur-Orchestrator (Status, Dispatches, Infrastruktur)
project-builder team     # Neues Team bauen (direkt in 4-Phasen-Flow)
project-builder rebuild  # Bestehendes Team neu bauen (Extraktion + 4-Phasen-Flow)
```

Drei Rollen, ein Agent. `main` ist der Standardmodus. `team` und `rebuild` überspringen die Begrüßung und starten direkt im passenden Workflow.

### Natürliche Sprache

Sag dem Agent was du willst -- er wählt den richtigen Skill:

- *"Bau mir ein Team für mein Coaching-Business"*
- *"Prüf mal das Team in ~/mein-projekt"*
- *"Setz die Empfehlungen um"*
- *"Dieser Text klingt zu sehr nach KI"*

### Befehle

| Befehl | Wann |
|--------|------|
| `/track` | Projektstatus aktualisieren |
| `/commit` | Sessionende: /track + commit + push in einem Schritt |
| `/learn` | Neue Wissensquellen integrieren |
| `/cross-commit` | Änderungen in verwalteten Repos committen + pushen |

`/commit` ist der Standard für Sessionende. Pusht nur wenn ein Remote existiert -- ohne Remote wird nur lokal committed.

## Setup

```bash
git clone https://github.com/andyon2/project-builder-public.git ~/project-builder
cd ~/project-builder
./scripts/setup.sh
```

Das Setup-Script:
1. Erstellt deine Instanz-Dateien aus Templates (CLAUDE.md, teams.md, dispatches.md)
2. Fragt ob du Notion-Integration willst (optional)
3. Richtet den globalen `project-builder`-Shortcut ein (optional)
4. Installiert Python-Abhängigkeiten für YouTube-Transcripts (optional)

Danach: `project-builder main` starten.

### Eigene Instanz konfigurieren

Nach dem Setup:
1. **teams.md** -- Trage deine Agent-Teams ein (Name, Pfad, Wissensgebiete)
2. **config/notion.md** -- Falls Notion: `notion-cli config init` einrichten, IDs in config/notion.md eintragen

Weitere Integrationen können unter `config/` als Markdown-Datei angelegt werden. Der Agent erkennt sie automatisch.

### Instanz-Dateien

Nach dem Setup entstehen Instanz-Dateien (CLAUDE.md, teams.md, project-status.md, config/), die deine persönliche Konfiguration enthalten. Diese stehen in `.gitignore` und werden nicht ins Public Repo committed. Bei Nutzung auf mehreren Rechnern: Separates privates Repo oder Sync-Ordner.

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
    project-builder            # Starter-Script (main|team|rebuild)
    starter-main.md            # Sessionstart-Routine: Orchestrator
    starter-team.md            # Sessionstart-Routine: Team-Building
    starter-rebuild.md         # Sessionstart-Routine: Team-Rebuild
    notion/notion-cli.py       # Notion API CLI (ersetzt MCP Server)
    notion/notion-cli          # Shell-Wrapper (Symlink: ~/.local/bin/notion-cli)
  .claude/skills/              # 15 Skills
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

## Für Fortgeschrittene

### Multi-Environment-Workflow

Agent-Teams können auf mehreren Maschinen laufen (lokal + Server). Git ist das einzige Sync-Medium -- kein SSH-Sync, keine geteilten Dateisysteme.

```
Lokal:   Sessionstart → git pull → arbeiten → commit → push
Server:  Sessionstart → git pull → arbeiten → commit → push
```

Jeder Agent ist selbst dafür verantwortlich, bei Sessionstart den neuesten Stand zu holen. Das Starter-Script fragt automatisch, ob gepullt werden soll, wenn der Remote neuere Commits hat.

**Umgebungserkennung:** Eine Datei `~/.environment` (Inhalt: `local` oder `server`) sagt dem Agent, wo er läuft. Einmal pro Maschine gesetzt, außerhalb aller Repos.

### Dezentrale Dispatches: Wissen zwischen Teams routen

Wenn `/learn` eine Quelle verarbeitet, kann das Wissen für mehrere Teams relevant sein. Das Dispatch-System routet Erkenntnisse an die richtigen Empfänger:

```
Quelle → /learn → Routing:
  KI-Architektur    → eigene knowledge/
  Für anderes Team  → [team-repo]/dispatches/inbox/
  Beides            → knowledge/ + Dispatch
```

Dispatch-Dateien leben in den Team-Repos, nicht zentral im Project Builder. Bei Sessionstart prüft der Ziel-Agent, ob neue Dispatches in seinem `dispatches/inbox/` vorliegen, und verarbeitet sie automatisch. `dispatches.md` im PB-Repo ist ein Write-Only-Log (was wurde wann wohin gesendet).

**Routing-Tabelle:** `teams.md` definiert pro Team die Wissensgebiete. `/learn` matcht Erkenntnisse gegen diese Gebiete und routet automatisch.

### Cross-Commit: Mehrere Repos gleichzeitig verwalten

`/cross-commit` iteriert über alle verwalteten Repos (aus `teams.md`), committet ausstehende Änderungen und pusht. Nützlich wenn der Project Builder Dateien in mehreren fremden Repos geändert hat (z.B. nach einem Dispatch-Rollout oder einem Framework-Update).

Wichtig: Committet nur bereits getrackte Dateien (`git add -u`). Neue Dateien müssen vorher explizit `git add`-ed werden -- der Agent warnt, wenn untracked Files vorliegen.

## Lizenz

MIT
