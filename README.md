# Project Builder

Ein Claude-Code-Agent der andere Agent-Teams entwirft, baut, auditiert und migriert.

## Das Problem

Claude Code kann fast alles -- aber ohne Struktur entsteht Chaos. Agent-Teams werden zu gross, Kontextfenster laufen voll, Skills und Agents ueberlappen sich, und nach ein paar Sessions vergisst der Agent seine eigenen Regeln.

Project Builder loest das durch eine Architektur-Philosophie (das "Rendle-Prinzip") und ein Set von Skills, die diese Philosophie durchsetzen -- auch auf sich selbst.

## Was er kann

**Teams bauen:** Du beschreibst einen Anwendungsfall. Der Project Builder klaert mit dir die Anforderungen und erstellt das komplette Team: CLAUDE.md, System Prompt, Agents, Skills, Scripts, Verzeichnisstruktur.

**Teams auditieren:** Bestehende Agent-Teams auf Token-Verschwendung, fehlende Felder, falsche Skill/Agent-Balance und Anti-Patterns pruefen. Read-only -- aendert nichts ohne OK.

**Teams migrieren:** Audit + Plan + Umsetzung in einem Schritt. Backup, Safe Fixes, Agent-zu-Skill-Konvertierungen, CLAUDE.md-Update.

**Wissen aufbauen:** Integriert Wissensquellen (YouTube-Transcripts, Artikel, Notion-Inbox) in eine kuratierte Knowledge-Base. Verdichtet statt sammelt -- neues Wissen wird gegen den bestehenden Stand geprueft.

**Content pruefen:** Findet KI-erkennbare Muster in Texten (GPTisms, Claude-typische Formulierungen, strukturelle Tells) und gibt konkrete Fix-Vorschlaege.

## Architektur: Das Rendle-Prinzip

Sechs Saeulen, die jedes Team durchziehen:

1. **Trennung Kontext/Identitaet.** CLAUDE.md = Projektfakten (fuer alle Agents gleich). System Prompt = Identitaet (wer der Agent ist, wie er denkt). Nie vermischen.

2. **Agents mit Denkweise.** Nicht "Du machst X" sondern "Du denkst wie ein erfahrener X". Nur Rollen die eigenes Urteilsvermoegen brauchen werden Agents. Ein Agent denkt. Ein Skill fuehrt aus.

3. **Main-Agent als Orchestrator.** Delegiert, reviewed, challenged. Nicht selbst Spezialist.

4. **Dateien als Gedaechtnis.** Eine `project-status.md` pro Projekt. Markdown-Dateien als Kommunikation zwischen Sessions. Kurz gehalten (<50 Zeilen).

5. **Kontextschutz.** Das Kontextfenster ist die knappste Ressource. Referenzmaterial wird nur bei Bedarf geladen, nicht beim Start. Zwischenergebnisse in Dateien, nicht im Chat.

6. **Skill-First.** Jede Aufgabe startet als Skill-Kandidat. Agent nur bei eigenem Urteilsvermoegen. "Braucht das wirklich einen Agent?" ist die erste Frage.

## Drei Schutzschichten

Agent-Teams vergessen ihre Regeln. Je laenger eine Session, desto staerker verduennt sich der System Prompt. Dagegen gibt es drei Schichten:

| Schicht | Was sie tut | Vergisst bei langem Kontext? |
|---------|-------------|------------------------------|
| **System Prompt** | Identitaet + Prinzipien | Ja (verduennt sich) |
| **Skills** | Workflows ausfuehren | Nein (frisch geladen bei Aufruf) |
| **Hooks** | Harte Schranken + Erinnerungen | Nein (extern, kein LLM) |

**Command-Hooks sind Gesetze.** Ein Shell-Script das deterministisch blockt. Kein LLM-Call, kein Vergessen, kein Interpretieren. Beispiel: Der Foreign-Commit-Hook verhindert, dass der Agent in fremden Repos committet -- egal wie lang die Session ist.

**Post-Compaction-Reminder.** Wenn das Kontextfenster voll wird, komprimiert Claude automatisch den aelteren Kontext. Ein Hook injiziert danach die fuenf kritischsten Prinzipien zurueck -- die, die am staerksten driften.

## Das Selbstentwicklungs-Paradox

Ein KI-Agent kann sich weiterentwickeln: neues Wissen lernen, neue Skills bauen, bestehende Teams auditieren. Aber er kann nicht zuverlaessig pruefen, ob er seine eigenen Regeln einhaelt. Seine Pruefwerkzeuge haben dieselben blinden Flecken wie er selbst.

Entdeckt wurde das durch **Cross-Instance-Review**: Zwei Instanzen desselben Agents pruefen sich gegenseitig. Die eine baut, die andere reviewt. Kein gemeinsamer Bias, kein gemeinsames Vergessen.

Ergebnis: Der Agent predigte "Skill-First" (jede Aufgabe soll ein Skill sein), aber seine groesste eigene Aufgabe -- Teams bauen -- war kein Skill. Keins seiner Audit-Tools hatte das beanstandet, weil sie nur pruefen was da ist, nicht was fehlt.

Die Loesung: `/reflect` wurde um einen Prinzip-Konsistenz-Check erweitert. Er extrahiert alle Prinzipien aus dem System Prompt, alle Taetigkeiten aus der Struktur, und sucht gezielt nach Luecken: "Was mache ich, wofuer es keinen Skill gibt?"

Mehr dazu: [`knowledge/self-evolution-paradox.md`](knowledge/self-evolution-paradox.md)

## Skills

| Skill | Was er tut |
|-------|-----------|
| `/build-team` | Neues Agent-Team erstellen (nach dialogischer Anforderungsklaerung) |
| `/extend-team` | Neuen Skill oder Agent fuer bestehendes Team entwerfen |
| `/skill-or-agent` | Schnelle Entscheidungshilfe: Skill oder Agent? |
| `/audit-team` | Team auf Best Practices pruefen (read-only) |
| `/audit-content` | Texte auf KI-erkennbare Muster pruefen |
| `/migrate-team` | Vollstaendige Team-Migration (Audit + Plan + Umsetzung) |
| `/convert-agent` | Agent-zu-Skill-Konvertierung entwerfen |
| `/apply-safe-fixes` | Fehlende model/maxTurns-Felder einfuegen |
| `/deploy-content-audit` | Content-Audit in bestehendes Projekt einpflanzen |
| `/reflect` | Team-Selbstanalyse (mit Prinzip-Konsistenz-Check) |
| `/learn` | Wissensquellen integrieren (Notion + lokal) |
| `/research-updates` | Aktuelle Entwicklungen recherchieren |
| `/track` | Projektstatus aktualisieren |

## Setup

```bash
git clone https://github.com/andyon2/project-builder.git ~/project-builder
cd ~/project-builder
./scripts/setup.sh
```

Das Setup-Script:
1. Erstellt deine Instanz-Dateien aus Templates (CLAUDE.md, teams.md, dispatches.md)
2. Fragt ob du Notion-Integration willst (optional)
3. Richtet den globalen `project-builder`-Shortcut ein (optional)
4. Installiert Python-Abhaengigkeiten fuer YouTube-Transcripts (optional)

Danach: `project-builder` (oder `./scripts/project-builder`) starten.

### Eigene Instanz konfigurieren

Nach dem Setup:
1. **teams.md** -- Trage deine Agent-Teams ein (Name, Pfad, Wissensgebiete)
2. **config/notion.md** -- Falls Notion: IDs eintragen (siehe `config/notion.md.example`)

Weitere Integrationen koennen unter `config/` als Markdown-Datei angelegt werden. Der Agent erkennt sie automatisch.

### Instanz-Dateien

Nach dem Setup entstehen Instanz-Dateien (CLAUDE.md, teams.md, project-status.md, config/), die deine persoenliche Konfiguration enthalten. Diese stehen in `.gitignore` und werden nicht ins Public Repo committed. Bei Nutzung auf mehreren Rechnern: Separates privates Repo oder Sync-Ordner.

## Projektstruktur

```
project-builder/
  CLAUDE.md                    # Projektkontext (fuer alle Agents gleich)
  main-agent.md                # System Prompt (Identitaet + Prinzipien)
  project-status.md            # Aktueller Stand (<50 Zeilen)
  knowledge/                   # Kuratierte Knowledge-Base
  reference/                   # On-Demand-Referenzmaterial
  sources/inbox/               # Neue Wissensquellen hier ablegen
  scripts/                     # Starter-Script, Tests, Hilfsskripte
  .claude/skills/              # 13 Skills
  .claude/hooks/               # Deterministische Sicherheits-Hooks
```

## Knowledge-Base

Verdichtetes Wissen zu KI-Agent-Architektur. Wird ueber `/learn` aktualisiert, nicht manuell editiert.

| Datei | Thema |
|-------|-------|
| `skill-best-practices.md` | Wann und wie Skills einsetzen |
| `token-optimization.md` | Token-Sparstrategien fuer Agent-Teams |
| `entscheidungshierarchie.md` | Skill vs. Agent: Entscheidungsbaum |
| `session-state.md` | Statusdateien, Hooks, Context Loading |
| `content-humanization.md` | Anti-GPTism-Regeln, Wort-Blacklists |
| `self-evolution-paradox.md` | Selbstentwicklung vs. Selbstkonsistenz |
| `widersprueche.md` | Offene Konflikte zwischen Quellen |

## Lizenz

MIT
