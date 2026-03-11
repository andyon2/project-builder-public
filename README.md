# Project Builder

Ein Claude-Code-Agent der andere Agent-Teams entwirft, baut, auditiert und verbessert.

## Das Problem

Claude Code kann fast alles -- aber ohne Struktur entsteht Chaos. Agent-Teams werden zu groß, Kontextfenster laufen voll, Skills und Agents überlappen sich, und nach ein paar Sessions vergisst der Agent seine eigenen Regeln.

Project Builder löst das durch eine Architektur-Philosophie (das "Rendle-Prinzip") und ein Set von Skills, die diese Philosophie durchsetzen -- auch auf sich selbst.

## Was er kann

**Teams bauen:** Du beschreibst einen Anwendungsfall. Der Project Builder klärt mit dir die Anforderungen und erstellt das komplette Team: CLAUDE.md, System Prompt, Agents, Skills, Scripts, Verzeichnisstruktur.

**Teams auditieren:** Bestehende Agent-Teams auf Token-Verschwendung, fehlende Felder, falsche Skill/Agent-Balance und Anti-Patterns prüfen. Read-only -- ändert nichts ohne OK.

**Teams verbessern:** Audit-Ergebnisse anwenden: Backups, Safe Fixes, Agent-zu-Skill-Konvertierungen, CLAUDE.md-Update.

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

### Rückwärts-Suche bei Umbau

Hinzufügen und Umbauen sind fundamental verschiedene Operationen. Beim Hinzufügen (neuer Skill, neue Datei) reicht vorwärts denken: "Was muss ich erstellen?" Beim Umbau (Entfernen, Umbenennen, Verantwortlichkeit verschieben) ist Rückwärts-Suche Pflicht: "Was konsumiert das, was ich gerade ändere?"

Jedes Team bekommt diese Regel in seiner CLAUDE.md:

> Vor dem ersten Edit bei strukturellen Änderungen: `grep -r` nach allen Konsumenten des Geänderten. Erst dann editieren.

Nicht jedes Problem braucht einen neuen Skill. Manchmal fehlt dem Agent nur der Auslöser im richtigen Moment -- dann reicht ein Bedingungssatz in CLAUDE.md statt eines neuen Workflows.

## Drei Schutzschichten

Agent-Teams vergessen ihre Regeln. Je länger eine Session, desto stärker verdünnt sich der System Prompt. Dagegen gibt es drei Schichten:

| Schicht | Was sie tut | Vergisst bei langem Kontext? |
|---------|-------------|------------------------------|
| **System Prompt** | Identität + Prinzipien | Ja (verdünnt sich) |
| **Skills** | Workflows ausführen | Nein (frisch geladen bei Aufruf) |
| **Hooks** | Harte Schranken + Erinnerungen | Nein (extern, kein LLM) |

### Globaler Safety-Hook

Ein Shell-Script das deterministisch prüft und blockt. Drei Stufen:

- **deny:** `git push --force`, `rm -rf`, `git reset --hard`, `git clean -f` -- sofort blockiert, keine Rückfrage
- **ask:** `.env`-Zugriff, Commits in fremden Repos -- Bestätigung erforderlich
- **allow:** alles andere

Registriert in `~/.claude/settings.json`, gilt für alle Projekte auf allen Maschinen. Kein LLM-Call, kein Vergessen, kein Interpretieren.

### Post-Compaction-Reminder

Wenn das Kontextfenster voll wird, komprimiert Claude automatisch den älteren Kontext. Ein Hook injiziert danach die kritischsten Prinzipien zurück -- die, die am stärksten driften.

## Das Selbstentwicklungs-Paradox

Ein KI-Agent kann sich weiterentwickeln: neues Wissen lernen, neue Skills bauen, bestehende Teams auditieren. Aber er kann nicht zuverlässig prüfen, ob er seine eigenen Regeln einhält. Seine Prüfwerkzeuge haben dieselben blinden Flecken wie er selbst.

Entdeckt wurde das durch **Cross-Instance-Review**: Zwei Instanzen desselben Agents prüfen sich gegenseitig. Die eine baut, die andere reviewt. Kein gemeinsamer Bias, kein gemeinsames Vergessen.

Ergebnis: Der Agent predigte "Skill-First" (jede Aufgabe soll ein Skill sein), aber seine größte eigene Aufgabe -- Teams bauen -- war kein Skill. Keins seiner Audit-Tools hatte das beanstandet, weil sie nur prüfen was da ist, nicht was fehlt.

Die Lösung: `/reflect` wurde um einen Prinzip-Konsistenz-Check erweitert. Er extrahiert alle Prinzipien aus dem System Prompt, alle Tätigkeiten aus der Struktur, und sucht gezielt nach Lücken: "Was mache ich, wofür es keinen Skill gibt?"

Mehr dazu: [`knowledge/self-evolution-paradox.md`](knowledge/self-evolution-paradox.md)

## Benutzung

Sag dem Agent was du willst -- er wählt den richtigen Skill:

- *"Bau mir ein Team für mein Coaching-Business"*
- *"Prüf mal das Team in ~/mein-projekt"*
- *"Setz die Empfehlungen um"*
- *"Dieser Text klingt zu sehr nach KI"*

Befehle die du selbst aufrufst:

| Befehl | Wann |
|--------|------|
| `/track` | Sessionende: Projektstatus sichern |
| `/learn` | Neue Wissensquellen integrieren |
| `/cross-commit` | Änderungen in verwalteten Repos committen + pushen |

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

Danach: `project-builder` (oder `./scripts/project-builder`) starten.

### Eigene Instanz konfigurieren

Nach dem Setup:
1. **teams.md** -- Trage deine Agent-Teams ein (Name, Pfad, Wissensgebiete)
2. **config/notion.md** -- Falls Notion: IDs eintragen (siehe `config/notion.md.example`)

Weitere Integrationen können unter `config/` als Markdown-Datei angelegt werden. Der Agent erkennt sie automatisch.

### Instanz-Dateien

Nach dem Setup entstehen Instanz-Dateien (CLAUDE.md, teams.md, project-status.md, config/), die deine persönliche Konfiguration enthalten. Diese stehen in `.gitignore` und werden nicht ins Public Repo committed. Bei Nutzung auf mehreren Rechnern: Separates privates Repo oder Sync-Ordner.

## Projektstruktur

```
project-builder/
  CLAUDE.md                    # Projektkontext (für alle Agents gleich)
  main-agent.md                # System Prompt (Identität + Prinzipien)
  project-status.md            # Aktueller Stand (<50 Zeilen)
  knowledge/                   # Kuratierte Knowledge-Base
  reference/                   # On-Demand-Referenzmaterial
  sources/inbox/               # Neue Wissensquellen hier ablegen
  scripts/                     # Starter-Script, Tests, Hilfsskripte
  .claude/skills/              # 11 Skills
  .claude/hooks/               # Deterministische Sicherheits-Hooks
```

## Knowledge-Base

Verdichtetes Wissen zu KI-Agent-Architektur. Wird über `/learn` aktualisiert, nicht manuell editiert.

| Datei | Thema |
|-------|-------|
| `skill-best-practices.md` | Wann und wie Skills einsetzen |
| `token-optimization.md` | Token-Sparstrategien für Agent-Teams |
| `entscheidungshierarchie.md` | Skill vs. Agent: Entscheidungsbaum + Verhaltensänderung vs. Systemerweiterung |
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

Jeder Agent ist selbst dafür verantwortlich, bei Sessionstart den neuesten Stand zu holen. Das Script im Starter fragt automatisch, ob gepullt werden soll, wenn der Remote neuere Commits hat.

**Umgebungserkennung:** Eine Datei `~/.environment` (Inhalt: `local` oder `server`) sagt dem Agent, wo er läuft. Einmal pro Maschine gesetzt, außerhalb aller Repos.

**Unified Starter Scripts:** Ein Script pro Team, das als Argument die Rolle annimmt (`./scripts/mein-team reviewer`). Ohne Argument zeigt es die verfügbaren Rollen. So startet man auf jeder Maschine gleich.

### Dispatch-System: Wissen zwischen Teams routen

Wenn `/learn` eine Quelle verarbeitet, kann das Wissen für mehrere Teams relevant sein. Das Dispatch-System routet Erkenntnisse an die richtigen Empfänger:

```
Quelle → /learn → Routing:
  KI-Architektur    → eigene knowledge/
  Für anderes Team  → dispatches/[team-name]/
  Beides            → knowledge/ + Dispatch
```

Jedes Team hat ein Verzeichnis unter `dispatches/`. Bei Sessionstart prüft der Ziel-Agent, ob neue Dispatches vorliegen. Eine zentrale `dispatches.md` trackt, welche gelesen und welche offen sind.

**Routing-Tabelle:** `teams.md` definiert pro Team die Wissensgebiete. `/learn` matcht Erkenntnisse gegen diese Gebiete und routet automatisch.

### Cross-Commit: Mehrere Repos gleichzeitig verwalten

`/cross-commit` iteriert über alle verwalteten Repos (aus `teams.md`), committet ausstehende Änderungen und pusht. Nützlich wenn der Project Builder Dateien in mehreren fremden Repos geändert hat (z.B. nach einem Dispatch-Rollout oder einem Framework-Update).

Wichtig: Committet nur bereits getrackte Dateien (`git add -u`). Neue Dateien müssen vorher explizit `git add`-ed werden -- der Agent warnt, wenn untracked Files vorliegen.

## Lizenz

MIT
