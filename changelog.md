# Changelog: Masterprompt Project Builder

### /track komplett neu: Inline, kein Argument, kein Fork (2026-03-09)
- **Redesign nach UX-Problem:** Fork-Skill auf Haiku hatte keinen Session-Kontext, fragte User nach Zusammenfassung statt sie selbst zu liefern. Loesung: Inline-Skill, kein Argument, Agent nutzt Session-Kontext direkt.
- **Drei Modi → ein Modus:** `/track status` und `/track update [was]` entfallen. `/track` macht nur noch eins: project-status.md mit Session-Fortschritt aktualisieren.
- **Sessionstart unveraendert:** Main-Agent liest project-status.md direkt (kein Skill noetig).
- **Alle 5 Projekte umgestellt:** SKILL.md (inline), CLAUDE.md (Skill-Tabelle), main-agent.md (Sessionende-Anweisung).
- **Project-builder hat eigenes Format:** Kein "Aktueller Stand" (redundant), dafuer Architektur-Entscheidungen, Meta-Learnings, offene Punkte.
- **Eigener /track-Skill fuer project-builder erstellt:** .claude/skills/track/SKILL.md + project-status.md (initial).
- Aktualisiert: knowledge/skill-best-practices.md, knowledge/session-state.md, masterprompt-project-builder-v5.md (Saeule 4 + Sessionende-Template), CLAUDE.md

### Architektur: Infrastruktur-Skills, /learn Umbenennung, Knowledge-Ingestion als Standard (2026-03-08)
- **`/integrate-source` umbenannt zu `/learn`:** Konsistentes Naming -- dasselbe Pattern ueberall, skalierte Implementierung. Skill-Datei, Scripts-Verzeichnis, CLAUDE.md, README.md, teams.md, dispatches.md, widersprueche.md aktualisiert. Changelog-Eintraege bleiben historisch bei `/integrate-source`.
- **Infrastruktur-Skills als Architektur-Baustein:** Drei Standard-Skills, die nicht projektspezifisch sind: `/track` (Statusverwaltung, Haiku), `/learn` (Knowledge-Ingestion, Sonnet), `/reflect` (Team-Selbstanalyse, Sonnet). Dokumentiert in knowledge/skill-best-practices.md.
- **`/track` als Standard-Skill:** Ersetzt direkte project-status.md-Verwaltung durch Fork-Skill auf Haiku. Drei Modi (kompakt, ausfuehrlich, update). Praxisbeispiel: ConTaktArt. Dokumentiert in knowledge/session-state.md.
- **Knowledge-Ingestion Stufen-Modell:** Stufe 0 (kein Domaenenwissen), Stufe 1 (knowledge/ + /learn), Stufe 2 (volle Pipeline mit Notion/Dispatching/Archivierung). Schwelle fuer Stufenfrage bewusst niedrig -- auch Branding-Teams koennen Stufe 2 brauchen.
- **Masterprompt-Aenderungen vorgeschlagen:** Saeule 4 Erweiterung (/track + /learn), Templates, Schritt 2+3, Qualitaetsprinzipien. Status: Offen.
- Aktualisiert: knowledge/skill-best-practices.md, knowledge/session-state.md, knowledge/masterprompt-aenderungen.md, CLAUDE.md, README.md, teams.md, dispatches.md, widersprueche.md

### Wissensupdate: WAT-Framework, Deployment-Determinismus, METR-Benchmark (2026-03-08)
- Quellen: 2026-03-08_how-to-build-10000-agentic-workflows-claude-code-tutorial.md (YouTube-Transcript), 2026-03-08_agi-ist-da-warum-spricht-niemand-drber.md (YouTube-Transcript)
- Aktualisiert: knowledge/skill-best-practices.md (WAT-Framework, CLAUDE.md als Projekt-System-Prompt, Deployment-Determinismus), knowledge/entscheidungshierarchie.md (Deployment-Determinismus als Designziel), knowledge/session-state.md (METR-Benchmark, Task-Horizon-Daten)
- Dispatches: ki-berater → dispatches/ki-berater/2026-03-08_agentic-workflows-markt-und-pricing.md
- Widersprueche: nein
- Masterprompt-Impact: nein

### Wissensupdate: Multi-Agent-Patterns, Context Management, Modell-Mix (2026-03-08)
- Quelle: 2026-03-08_ai-agents-full-course-2026-master-agentic-ai-2-hours.md (YouTube-Transcript, 2h Kurs)
- Aktualisiert: knowledge/skill-best-practices.md (Selbst-modifizierendes CLAUDE.md, Stochastic Consensus, Agent Chat Rooms, Sub-Agent Verification, Prompt Contracts/Reverse Prompting), knowledge/token-optimization.md (60/30/10 Modell-Mix, Batch API), knowledge/session-state.md (Iceberg-Technik, Auto-Compaction)
- Dispatches: keine
- Widersprueche: nein
- Masterprompt-Impact: ja -- masterprompt-aenderungen.md ergaenzt (Selbst-modifizierendes CLAUDE.md, Vorschlag Niedrig-Prioritaet)

### Wissensupdate: Evaluations-Loop, Diverse Reviews, Cross-Model-Reviews (2026-03-08)
- Quelle: 2026-03-08_ki-am-murksen-hindern.md (YouTube-Transcript)
- Aktualisiert: knowledge/skill-best-practices.md, knowledge/token-optimization.md
- Widersprueche: nein
- Masterprompt-Impact: ja -- knowledge/masterprompt-aenderungen.md angelegt (Grounding-Execution-Evaluation-Finalizing Pattern)

---

## v5 (2026-03-07)

### CLAUDE.md eingefuehrt
- **Trennung Projektkontext / Identitaet** jetzt auch im Project Builder selbst umgesetzt (eigene Saeule 1).
- **CLAUDE.md** im Projektroot: Wissensquellen-Liste, Projektstruktur, Skills-Tabelle, Konventionen, Wissens-Pipeline, Notion-Config.
- **Masterprompt entschlackt:** Hardcodierte Knowledge-Dateiliste durch Verweis auf CLAUDE.md ersetzt. Architektur-Prinzipien, Templates, Qualitaetsprinzipien bleiben unveraendert.
- **Systemweiter Shortcut:** README dokumentiert Setup fuer `project-builder`-Befehl (via `~/.local/bin`).

### Wissensupdate: Skill-Suites, MCP-Abgrenzung, Progressive Disclosure
- Quelle: 2026-03-07_stop-building-ai-agents-do-this-instead.md (YouTube-Transcript)
- Aktualisiert: knowledge/skill-best-practices.md, knowledge/entscheidungshierarchie.md
- `/extend-team` prueft jetzt bei neuen Skills, ob eine Skill-Suite sinnvoll waere

---

## v4.1 (2026-03-07)

### Notion-Integration in `/integrate-source`
- **Vier Modi:** `alle` (Notion + lokal), `notion` (nur Notion), `lokal` (nur lokale Inbox), `[dateiname]` (einzelne Datei).
- **`alle` holt zuerst aus Notion:** Query (inboxed=true, Created>=2026) → Titel auf KI-Relevanz pruefen → YouTube-Transcripts/Artikel fetchen → lokal in sources/inbox/ ablegen → Type (z.B. "video") + Project=algron in Notion setzen (macht inboxed automatisch false) → dann lokale Inbox verarbeiten.
- **KI-Relevanz-Erkennung:** Titel-basiert mit breiter Keyword-Liste (Claude, Agent, MCP, RAG, LLM, etc.). Im Zweifel eher verarbeiten.
- **Notion-DB:** All Notes [UB] (cd8b8484-6919-4e48-8cb1-be2c627a5ee5), Property-IDs fuer Title, URL, Type, Created, inboxed hardcoded.
- **Handy-Workflow:** YouTube-Video in Notion teilen → `/integrate-source alle`.
- **Separater `/notion-inbox` Skill entfernt** -- Notion-Logik ist jetzt Schritt N im integrate-source Skill.

### Sources-System: Inbox/Archive-Pipeline
- **Neue Verzeichnisstruktur:** `sources/inbox/` (unverarbeitete Quellen) + `sources/archive/[YYYY-MM]/` (integrierte Quellen).
- **Schlanke `sources/log.md`:** Eine Zeile pro Quelle (Datei, Typ, Datum, Archiv-Pfad). Bleibt selbst bei 500+ Eintraegen handhabbar.
- **Bestehende Quellen archiviert:** Alle 5 bisherigen Quelldateien nach `archive/2026-03/` verschoben.
- **`integrate-source` Skill komplett neu geschrieben:**
  - Inbox/Archive-Pipeline statt flacher Dateistruktur
  - Verdichtungs-Logik: Bestaetigung, Erweiterung, Widerspruch, Veraltung (statt nur "anfuegen")
  - Automatisches Archivieren nach Integration
  - Vier Modi: `alle` (Notion + lokal), `notion` (nur Notion), `lokal` (nur lokale Inbox), `[dateiname]` (einzelne Datei)
- **`knowledge/widersprueche.md` eingefuehrt:** Sammelt Konflikte zwischen Quellen explizit. Widersprueche werden nicht leise aufgeloest, sondern dokumentiert bis sie durch Praxistest oder neue Quellen geklaert sind.
- **Quellen-Sektionen in allen Knowledge-Dateien:** Jede Knowledge-Datei hat am Ende eine `## Quellen`-Sektion, die nachvollziehbar macht, welche Quellen zu welchen Erkenntnissen beigetragen haben.
- **Alte Quellreferenz in `content-humanization.md` bereinigt:** Verweis auf `sources/`-Pfade entfernt (Dateien liegen jetzt im Archiv).
- **URL-Auto-Fetch:** Inbox-Dateien, die nur eine URL enthalten, werden automatisch aufgeloest:
  - YouTube-URLs: Transcript wird per `youtube-transcript-api` geholt (`scripts/integrate-source/fetch-transcript.py`)
  - Artikel-URLs: Inhalt wird per WebFetch geholt
- **Auto-Rename beim Archivieren:** Dateien werden zu `YYYY-MM-DD_[slug].md` umbenannt. Slug wird aus Titel/Thema abgeleitet.
- **Python-Venv:** `scripts/.venv/` mit `youtube-transcript-api` fuer Transcript-Fetching.

---

## v4 (2026-03-06)

### Content Humanization (Anti-GPTism / Anti-AI-Slop)
- **Knowledge-Datei:** `knowledge/content-humanization.md` -- Kuratiertes Wissen aus drei Tiefenrecherchen (GPTisms, Humanisierungstechniken, Design-Anti-Patterns).
- **Wort-Blacklists:** EN Tier 1/2/3, DE Floskeln, Uebergangsfluche -- jeweils mit konkreten Alternativen.
- **Strukturelle Regeln:** Was KI-Text verrät (gleichfoermige Satzlaenge, Intro-Liste-Fazit, Synonym-Ketten) vs. was menschlichen Text auszeichnet (wilde Variation, Konjunktions-Starter, Satzfragmente).
- **Deutsche Spezialregeln:** Modalpartikeln (doch, halt, eben, mal, eigentlich) als staerkster Einzelindikator, Komposita, Nebensatzstrukturen, Registerprobleme.
- **Design Anti-Patterns:** Purple Gradients, Inter/Roboto/Poppins, 3-Spalten-Icon-Grid, zentrierter Hero, spezifische Hex-Werte die "KI" signalisieren.
- **Pflicht-Bloecke fuer Content-Agents:** Kopierbare Prompt-Abschnitte (Text, Deutsch-Zusatz, Design-Zusatz) zum Einbau in Content-generierende Agents/Skills.
- **Voice Cloning Prozess:** Drei-Schichten-Analyse (Strukturell, Emotional, Semantisch) fuer markenspezifischen Content.
- **Masterprompt-Integration:** Neues Qualitaetsprinzip ("Content-Agents brauchen Anti-GPTism-Regeln"), Content-Check in Schritt 2, Knowledge-Referenz.
- **`/audit-content` Skill:** Prueft bestehenden Content auf KI-erkennbare Muster (Wort-Blacklist, Struktur, Ton, Design). Read-only, fork, sonnet.
- **`/deploy-content-audit` Skill:** Pflanzt audit-content + Knowledge + Selbstcheck-Regeln in ein bestehendes Projekt ein. Gezielt fuer bereits migrierte Teams. Fork, sonnet.
- **`/research-updates` Skill:** Recherchiert aktuelle Entwicklungen zu einem Thema und aktualisiert die relevante Knowledge-Datei. Fork, sonnet.
- **`/migrate-team` erweitert:** Neue Phase E deployt Content-Humanization automatisch bei zukuenftigen Migrationen.
- **Quellen:** 3 Recherche-Reports in `sources/` (GPTisms: 680+ Zeilen/30+ Quellen, Humanisierung: ~700 Zeilen/akademisch+Praxis, Design: ~520 Zeilen/spezifische CSS-Werte).

### Neue Saeule: Skill-First-Prinzip
- **Entscheidungshierarchie:** Jede Aufgabe startet als Skill-Kandidat. Nur wenn sie eigenes Urteilsvermoegen oder eine eigene Denkweise braucht, wird sie ein Agent.
- **Zwei Skill-Typen:** Encoded Preference (langlebig, bevorzugen) vs. Capability Uplift (fragil, benchmarken).
- **Skill-zu-Agent-Verhaeltnis** als Qualitaetsmetrik: Mindestens 1:1, idealerweise hoeher.
- **Quelle:** Anthropic Skill Creator, Analyse bestehender Agent-Teams (Token-Verschwendung durch zu viele Agents).

### Erweiterte Skill-Templates
- Drei Skill-Typen dokumentiert: Inline, Fork (context: fork), Interview-Skill.
- Hilfsskripte-Pattern dokumentiert.
- Agent-zu-Skill-Konvertierungsanleitung.
- YAML-Header-Optionen vollstaendig dokumentiert.

### Token-Bewusstsein als Architekturprinzip
- `model`-Feld ist jetzt Pflicht (nicht optional) fuer jeden Agent und Fork-Skill.
- `maxTurns` ist jetzt Pflicht fuer jeden Agent.
- Neue Qualitaetsprinzipien: Token-Bewusstsein, Skills keine zweite Klasse.

### Veraendertes Vorgehen (Schritt 1 + 2)
- Schritt 1 fragt jetzt: "Welche Aufgaben sind Workflows vs. Denkarbeit?"
- Schritt 2: Skills werden VOR Agents identifiziert (nicht als Nachgedanke).
- Architektur-Check: Skill-zu-Agent-Verhaeltnis wird explizit geprueft.

### Saeule 2 verschaerft
- Explizite Unterscheidung: "Ein Agent denkt. Ein Skill fuehrt aus."
- Nur Rollen mit eigener Denkweise werden Agents.

### Knowledge-Base eingefuehrt
- `knowledge/` Verzeichnis mit kuratierten Best Practices.
- Masterprompt referenziert Knowledge-Base: "Lies vor Architekturentscheidungen."
- Unabhaengig vom Masterprompt aktualisierbar.

### Eigene Skills fuer den Project Builder
- `/audit-team` -- Analysiert bestehende Agent-Teams auf Effizienz.
- `/integrate-source` -- Integriert neue Wissensquellen in die Knowledge-Base.
- `/skill-or-agent` -- Schnelle Entscheidungshilfe fuer einzelne Aufgaben.

### Migration-System
- `migration-guides/` Verzeichnis fuer Versions-Uebergaenge.
- Erster Guide: v3 -> v4.

### Selbst-Erweiterung
- Neue Regel im Main-Agent-Template: Wenn keine Skill/Agent fuer eine Aufgabe existiert, User fragen und /extend-team aufrufen.
- `/extend-team` Skill: Analysiert Aufgabe, entscheidet Skill vs. Agent, erstellt Entwurf (read-only).

### Safe Migration Skills
- `/apply-safe-fixes` -- Fuegt fehlende model/maxTurns-Felder ein. Zeigt Diff, wartet auf OK, eine Datei nach der anderen.
- `/convert-agent` -- Liest bestehenden Agent, erstellt Skill-Entwurf als Alternative. Aendert nichts am Agent.

### Autonome Migration
- `/migrate-team` Skill: Fuehrt nach Audit-Analyse die komplette Migration durch -- Safe Fixes, Skill-Konvertierungen mit Backup, CLAUDE.md-Update. Zeigt Plan, wartet auf OK, setzt dann alles um.
- Backup-System: Konvertierte Agents werden nach `.claude/agents/backup/` verschoben, nicht geloescht. Reaktivierung jederzeit moeglich.

### Token-Oekonomie-Klarstellung
- Expliziter Hinweis im Masterprompt: Inline-Skills laufen auf Opus (nur fuer Einzeiler!). Fork-Skills laufen auf eigenem Modell (typisch Haiku) -- DAS ist der Token-Sparer.
- Fork-Skills sind fast immer guenstiger als Agents auf Sonnet.

### Session-State-Konvention
- Neue Konvention: Eine `project-status.md` pro Projekt (statt status.md + todo.md + buildlog.md).
- Vier Sektionen: Aktueller Stand, Offene Aufgaben, Entscheidungen, Naechste Session.
- Main-Agent liest bei Sessionstart, aktualisiert bei Sessionende.
- Abgrenzung zu Claudes Auto-Memory dokumentiert.
- Knowledge-Datei: `knowledge/session-state.md`.
- Migrate-Team-Skill um Phase D (Statusdatei-Konsolidierung) erweitert.

### System-Prompt Design-Prinzip
- Expliziter Hinweis im Masterprompt: System Prompt kurz halten. Nur Identitaet/Strategie/Delegation. Alles Prozedurale in Skills, die frisch geladen werden und nicht "vergessen" werden koennen.

---

## v3 (frueher als "v2" im Header bezeichnet)

### Fuenf Saeulen
- Trennung Projektkontext/Identitaet
- Spezialisierte Sub-Agents mit Persoenlichkeit
- Main-Agent als Orchestrator
- Dateien als Gedaechtnis
- Kontextschutz und Interaktionsmodi (inkl. Direkt-Modus)

### Modellwahl als Architekturentscheidung
- Opus/Sonnet/Haiku-Empfehlungen pro Rolle.
- Warnung vor Opus-Vererbung ohne model-Feld.

### Dialogische Agents
- Starter-Scripts fuer Direkt-Modus.
- Briefing-System fuer Session-Uebergaben.

---

## v1

- Vier Saeulen (ohne Kontextschutz).
- Grundlegende Agent-Templates.
- Rendle-Prinzip als Basis.
