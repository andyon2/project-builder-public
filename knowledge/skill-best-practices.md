# Skill Best Practices

## WAT-Framework (Workflows, Agent, Tools)

[Neu: 2026-03-08]

Ein konkretes Build-Pattern fuer Claude Code Projekte. Die drei Ebenen:

- **Workflows:** Markdown-Dateien in natuerlicher Sprache. Beschreiben den Prozess Schritt fuer Schritt -- was wann zu tun ist, in welcher Reihenfolge welche Tools aufzurufen sind. Analogie: Das Rezept.
- **Tools:** Konkrete Ausfuehrungs-Skripte (Python etc.). Jedes Tool hat genau eine Aufgabe (recherchieren, formatieren, senden, archivieren). Analogie: Die Zutaten/Geraete.
- **Agent:** Der Claude Code Agent, der Workflows liest und Tools aufruft. Er verbindet Rezept und Zutaten.

**Schluessel-Eigenschaft:** Sowohl Workflows als auch Tools werden vom Agenten bei Fehlern und Korrekturen **automatisch aktualisiert**. Das System verbessert sich im Betrieb (verbindet sich mit dem Selbst-modifizierenden CLAUDE.md Muster).

**Deployment-Einschraenkung:** Das WAT-Framework deployt Workflows und Tools -- nicht den Agenten selbst. Im Produktionsbetrieb (Cron, Webhook) verhaelt sich das System deterministisch wie eine klassische Automation. Die Self-Healing-Faehigkeit existiert nur, wenn der Agent aktiv dabei ist (Entwicklungs-/Testphase).

**Konsequenz fuer Design:** Workflows und Tools muessen ausgiebig mit dem Agenten getestet werden, bevor sie deployed werden. Erst wenn das System zuverlaessig laeuft, aus dem aktiven Kontext entlassen. Deterministik im Deployment ist kein Nachteil -- sie ist das Ziel.

## CLAUDE.md als Projekt-System-Prompt

[Neu: 2026-03-08 -- konkretisiert bestehende Praxis]

Das CLAUDE.md im Projektverzeichnis ist der projektspezifische System-Prompt des Claude Code Agenten. Jede Anfrage liest es erneut. Inhalte:
- Ordnerstruktur und wo was liegt
- Welches Framework verwendet wird (z.B. WAT)
- API-Key-Verwaltung (Verweis auf `.env`, nie direkt)
- Projektziel und wichtigste Konventionen

Wichtig fuer Token-Budget: Das CLAUDE.md muss kompakt bleiben. Mit wachsenden gelernten Regeln periodisch konsolidieren (siehe Selbst-modifizierendes CLAUDE.md).

**Blueprint-Dateien als CLAUDE.md-Erweiterung:** [Neu: 2026-03-13] Fuer wiederkehrende Bauaufgaben (Dashboards, Wizards, Landing Pages) lohnt es sich, wiederverwendbare Architektur-Blueprints als separate Markdown-Dateien neben dem CLAUDE.md zu lagern (z.B. `dashboard-blueprint.md`, `wizard-blueprint.md`). Bei Projektinitialisierung werden sie dem Agenten mitgegeben -- kein Neuerfinden der Rad-Struktur. Dies ist eine Konkretisierung des bestehenden `reference/`-Patterns (On-Demand-Dateien statt CLAUDE.md-Bloat) auf Projektebene.

## Auto-Research-Pattern: Autonome Experimentier-Loops

[Neu: 2026-03-13]

Ein Agent laeuft in einer engen Feedback-Schleife: Hypothese formulieren → Experiment ausfuehren (per API/CLI) → objektive Metrik messen → Gewinner behalten → Erkenntnisse in Resource-Datei akkumulieren → naechste Hypothese auf Basis der Lernkurve.

**Drei Bedingungen fuer sinnvollen Einsatz:**
- **Objektive Metrik:** Eine Zahl die klar besser/schlechter sagt. Keine subjektiven Metrics.
- **API-Zugang fuer Input-Veraenderungen:** Der Agent muss den Stimulus aendern koennen. Ohne API: nur manuelle Varianten moeglich.
- **Schneller Feedback-Loop:** Je schneller die Messung (5 Min bis 4 Stunden), desto schneller konvergiert das System.

**Resource-Datei als Gedaechtnis:** Erkenntnisse aus allen Experimenten akkumulieren in einer strukturierten Datei. Spaetere Laeufe generieren Hypothesen auf Basis des Gelernten. Ab ~500 Runs: periodische Konsolidierung noetig.

**Deployment:** GitHub Actions Cron oder Modal. Siehe `/loop` und Scheduled Tasks in session-state.md fuer Claude-Code-interne Alternativen.

**Abgrenzung:** WAT deployt deterministische Workflows ("das Gleiche besser machen"). Auto-Research deployt explorative Experimente ("autonom herausfinden was besser ist").

Quelle: claude-code-autoresearch-self-improving-ai (2026-03-13)

## Quellen
- Anthropic Skill Creator (offizieller Plugin, 2026) -- Grundlagen Skill-Architektur, YAML-Header, Trigger Tuning
- Anthropic PDF: Skill Best Practices (33 Seiten) -- Skill-Typen, Wartung, Evals
- improved-skill.md (2026-03-06) -- Fork-Skill-Patterns, Hilfsskripte-Auslagerung
- Claude 2.0 is finally here.md (2026-03-07) -- Skill Creator Plugin, context:fork Verhalten
- stop-building-ai-agents-do-this-instead.md (2026-03-07) -- MCP-Skills-Metapher, Skill-Suite-Muster (Ordner-Struktur fuer verwandte Skills), Progressive Disclosure Mechanismus, Non-Techniker-Zugang
- 2026-03-08_ki-am-murksen-hindern.md (2026-03-08) -- Grounding-Execution-Evaluation-Finalizing Pattern, Praxis-Fehlerdaten. Code-Review-spezifische Teile (diverse Reviewer, Cross-Model, DoD) dispatched an zustaendiges Team.
- 2026-03-08_ai-agents-full-course-2026-master-agentic-ai-2-hours.md (2026-03-08) -- Selbst-modifizierendes CLAUDE.md, Stochastic Multi-Agent Consensus, Agent Chat Rooms, Sub-Agent Verification Loops, Prompt Contracts, Reverse Prompting, Video-to-Action Pipeline.
- 2026-03-08_how-to-build-10000-agentic-workflows-claude-code-tutorial.md (2026-03-08) -- WAT-Framework als Build-Pattern, CLAUDE.md als Projekt-System-Prompt, Deployment-Determinismus als Designprinzip.
- 2026-03-08_agi-ist-da-warum-spricht-niemand-drber.md (2026-03-08) -- METR-Benchmark (Aufgabenhorizont 14,5h fuer Claude Opus 4.6), Multi-Agent-Parallelisierung, In-Context-Learning als AGI-Kriterium.
- Knowledge-Architektur-Analyse eines Content-Teams (2026-03-08) -- /learn als Standard-Skill, Infrastruktur-Skills als Architektur-Baustein, /track als Statusverwaltungs-Skill, Stufen-Modell fuer Knowledge-Ingestion, Naming-Konsistenz /integrate-source → /learn.
- 2026-03-12_claude-code-20-has-arrived-its-insane.md (2026-03-12) -- Skills 2.0 Eval-Workflow (kriterienbasiertes Scoring, HTML-Report, AB-Testing, Sub-Agent Parallelisierung), Leaner-Skills durch Eval-basiertes Reference-File-Pruning, Google Workspace CLI als Bestaetigung CLI>MCP.
- claude-code-autoresearch-self-improving-ai.md (2026-03-13) -- Auto-Research-Pattern: Autonome Experimentier-Loops mit objektiver Metrik, Bedingungen fuer sinnvollen Einsatz, Resource-Datei als Lern-Gedaechtnis.
- claude-code-baut-ein-vermieter-portal-in-37-min.md (2026-03-13) -- Blueprint-Dateien als CLAUDE.md-Erweiterung fuer wiederkehrende Bauaufgaben.

## Wann ist etwas ein Skill (nicht ein Agent)?

Ein Skill ist die richtige Abstraktion, wenn:
- Die Aufgabe einen **wiederholbaren Workflow** hat (gleiche Schritte, variables Input)
- Der Output **vorhersagbar strukturiert** ist (Report, Zusammenfassung, Checkliste)
- Keine **eigene Denkweise** noetig ist (kein Urteilsvermoegen, keine Bewertung)
- Die Aufgabe in **<15 Turns** abgeschlossen ist

Ein Agent ist noetig, wenn:
- **Eigenstaendige Urteile** gefaellt werden (Bewertung, Priorisierung, Strategie)
- **Breiter Kontext** verknuepft werden muss (mehrere Wissensgebiete, Projekthistorie)
- Die Ergebnisse **nicht vorhersagbar** sind (kreative Arbeit, Analyse mit unbekanntem Ausgang)
- Eine **eigene Perspektive** einen Mehrwert hat ("denkt wie ein...")

## Skill-Typen

### Encoded Preference (bevorzugen)
- Kodiert einen nutzerspezifischen Workflow mit fester Reihenfolge und Logik
- Das Modell kennt die Einzelteile, aber nicht die gewuenschte Kombination
- **Langlebig** -- bleibt relevant, weil der Workflow nutzerspezifisch ist
- Beispiele: Weekly Reports, Idea Mining, Daten-Pipelines, Onboarding-Interviews

### Capability Uplift (mit Vorsicht)
- Kompensiert eine Modell-Schwaeche durch Prompt-Engineering
- **Fragil** -- kann mit besseren Modellen obsolet werden
- Regelmaessig benchmarken: Ist das Basismodell inzwischen besser ohne den Skill?
- Beispiele: Frontend-Design-Skill, Excel-Formel-Skill

## Skill-Architektur

### Einfache Skills (inline)
- Laufen im Hauptkontext des Main-Agents
- Fuer schnelle Abfragen, Statusreports, Kurz-Dialoge (<5 Interaktionen)
- Belasten das Context Window des Main-Agents minimal

### Komplexe Skills (context: fork)
- Laufen in einem isolierten Subagent mit eigenem Context Window
- **Pflicht: `model`-Feld setzen!** Ohne erbt der Fork das Modell des Main-Agents
- Koennen Hilfsskripte aufrufen (unter `scripts/[skill-name]/`)
- Koennen parallele Agenten spawnen fuer unabhaengige Teilaufgaben
- Ergebnisse werden in Projektdateien geschrieben, nicht zurueck in den Chat

### Hilfsskripte
- Komplexe Logik gehoert in separate Skripte, nicht in den Skill-Body
- Liegen unter `scripts/[skill-name]/`
- Beispiele: Daten-Fetching, PDF-Rendering, API-Calls
- Der Skill orchestriert die Skripte, nicht umgekehrt

## CLI vs. MCP: Klare Faustregel

[Neu: 2026-03-12]

Wenn fuer ein Tool sowohl eine CLI als auch ein MCP existiert: **immer CLI bevorzugen.**

**Begruendung:** Claude Code lebt im Terminal. Ein CLI-Tool ist direkt ansprechbar via Bash -- kein Middleman, kein Config-Overhead, kein zusaetzlicher Prozess. MCPs versuchen dasselbe zu erreichen, haben aber inhaerent mehr Overhead, weil sie ausserhalb des Terminals liegen.

**Beispiele:**
- Supabase: Supabase CLI > Supabase MCP
- NotebookLM: NotebookLM-PI CLI > Kein offizielles MCP
- Firecrawl: Firecrawl CLI > Firecrawl MCP
- Google Workspace: GWS CLI > Google Workspace MCP

**Wenn nur MCP verfuegbar ist:** MCP bleibt sinnvoll als Fallback, besonders fuer Tools ohne CLI-Alternative.

**Caveat:** Jeder neue CLI braucht in der Regel eine begleitende **Skill-Datei**, die Claude Code beibringt wie der CLI zu nutzen ist. Pruefen ob der CLI-Anbieter bereits einen offiziellen Skill mitliefert (Supabase, Vercel, Playwright tun das).

Quellen: cli-anything-just-brought-claude-code (2026-03-12), 10-claude-code-plugins (2026-03-12), googles-new-tool-gws (2026-03-12)

## Tool-Registry: Dreischichtige Tool-Entkopplung

[Neu: 2026-03-12]

Wenn mehrere Teams dasselbe externe Tool nutzen (z.B. Notion), entsteht ein Wartungsproblem: API-Details in jedem Skill hardcoded, bei Tool-Wechsel N×M Migration.

**Loesung: Drei Schichten trennen**

| Schicht | Verantwortung | Wo |
|---------|--------------|-----|
| **Skill** | Workflow-Logik (WAS) | `.claude/skills/[name]/` |
| **Tool-Registry** | Faehigkeit → Werkzeug (WOMIT) | `~/.config/claude-tools/registry.md` |
| **Config** | IDs, Credentials, DB-Namen (WIE) | `~/.config/[tool]/` oder `config/` |

**Durchsetzung via Wissens-Entzug:** Skills enthalten keine API-Details (Endpoints, Property-IDs, Filter-Syntax). Der Agent KANN nicht direkt API-Calls machen, weil er die Details nicht hat. Staerker als Verhaltensregeln ("bitte schau erst in die Registry"), die ignoriert werden.

**Beispiel vorher:**
```
# Im Skill (hardcoded):
"PATCH page_id → properties: { 'oYqt': {'select': {'name': 'video'}} }"
```

**Beispiel nachher:**
```
# Im Skill (abstrakt):
"Setze Type und Project auf dem Eintrag"
```

Der Agent liest CLAUDE.md → findet "Custom Tools → Registry" → liest Registry → findet das CLI-Tool → liest Config fuer Details.

**CLAUDE.md-Konvention fuer alle Teams:**
```
## Custom Tools
Eigene CLI-Tools: siehe `~/.config/claude-tools/registry.md`.
CLI-Tools immer bevorzugen vor MCP-Servern oder direkten API-Aufrufen.
```

**Registry-Format:** Pro Tool: Name, Pfad, Befehle, Config-Verweis. Keine API-Details, nur CLI-Interface.

Quellen: Eigenentwicklung, validiert durch /learn-Migration (2026-03-12)

## MCP und Skills: Abgrenzung

MCP-Server und Skills erledigen verschiedene Dinge und erganzen sich:

- **MCP** = die Haende: Verbindet Claude mit der Aussenwelt (APIs, externe Tools, Datenquellen, Dateisystem-Zugriff).
- **Skills** = die Erfahrung: Sagt Claude, was es mit dem tun soll, was es durch MCP bekommt. Workflow, Reihenfolge, Qualitaetsstandards.

Erst zusammen entsteht ein vollstaendiger Spezialist: MCP gibt Reichweite, Skills geben Expertise.

[Neu: 2026-03-07]

## Progressive Disclosure (technischer Hintergrund)

Claude laedt Skills nicht alle auf einmal. Beim Start sieht Claude nur einen kurzen Beschreibungstext pro Skill -- wie den Titel auf einem Buch-Ruecken. Erst wenn Claude fuer eine Aufgabe einen spezifischen Skill benoetigt, laedt es den vollstaendigen Skill-Body.

Konsequenzen:
- Ein Projekt kann Hunderte Skills haben, ohne das Kontextfenster zu belasten.
- Die `description` im YAML-Header ist deshalb kritisch: Sie ist das, was Claude beim Auswaehlen sieht.
- Je praeziser die Description, desto treffsicherer waehlt Claude den richtigen Skill.

[Neu: 2026-03-07 -- praezisiert gegenueber bisheriger Beschreibung]

## Skill-Suites: Mehrere Skills als Ordner-Gruppe

Verwandte Skills koennen als Suite organisiert werden -- ein Hauptordner mit mehreren Unterordnern, jeder mit eigenem `skill.mmd`:

```
geo-audit/
  skill.mmd              # Haupt-Skill: orchestriert die Suite
  geo-citability/
    skill.mmd            # Teilaufgabe 1
  geo-score/
    skill.mmd            # Teilaufgabe 2
  ...
```

Der Haupt-Skill (z.B. `/geo-audit`) orchestriert die Teilskills. Claude kann aber auch einzelne Teilskills direkt aufrufen, wenn nur ein Aspekt benoetigt wird. Dieses Pattern skaliert auf 10+ zusammengehoerende Skills ohne Uebersicht zu verlieren.

[Neu: 2026-03-07]

## Non-Techniker-Zugang

Skills erfordern keine Programmierkenntnisse. Wer Markdown schreiben kann, kann einen Skill erstellen:
- Recruiter: Schreiben einen Skill fuer den unternehmensinternen Bewerbungsprozess.
- Finance: Schreiben einen Skill fuer Reports im Hausformat.
- Legal: Schreiben einen Skill fuer die Vertragspruefung nach Kanzlei-Standard.

Komplexere Skills mit Python-Skripten und Sub-Agenten brauchen technisches Wissen -- aber der Einstieg ist bewusst niedrigschwellig.

[Neu: 2026-03-07]

## Write vs. Edit in Skills: Datenverlust vermeiden

[Neu: 2026-03-08]

**Kritischer Bug-Typ:** Ein Skill hat `Write` in `allowed-tools` und nutzt das Write-Tool um bestehende Dateien zu aktualisieren (z.B. Log-Dateien, Feedback-Logs, Publishing-Logs). Write **ueberschreibt die gesamte Datei** -- alle vorherigen Eintraege sind weg.

**Regel:** Wenn ein Skill in eine bestehende Datei **ergaenzen** soll (neue Eintraege hinzufuegen, Zeilen aendern), muss er `Edit` statt `Write` verwenden. Write ist nur sicher fuer:
- Neue Dateien erstellen (die vorher nicht existierten)
- Dateien komplett neu schreiben (bewusster Full Overwrite)

**In Skill-Prompts explizit machen:**
```
# FALSCH
### 1. In `feedback/log.md` schreiben (neue Eintraege oben)

# RICHTIG
### 1. In `feedback/log.md` ergaenzen (neue Eintraege oben, IMMER mit Edit -- NIE mit Write, das ueberschreibt bestehende Eintraege)
```

**Checkliste fuer Skill-Design:**
- Hat der Skill `Write` in `allowed-tools`? Pruefe: Schreibt er in bestehende Dateien?
- Wenn ja: `Edit` statt `Write` verwenden, oder beides in `allowed-tools` und im Body explizit unterscheiden
- Log-Dateien, Feedback-Dateien, Status-Dateien: **Immer Edit**
- Neue Reports, neue Content-Dateien: Write ist OK

## YAML-Header-Optionen

```yaml
name: skill-name              # Pflicht
description: "Wann und wofuer" # Pflicht - bestimmt natuerlichsprachliche Erkennung
argument-hint: "[parameter]"  # Optional - Autocomplete-Hinweis
allowed-tools: "Read, Bash"   # Optional - Tools ohne Permission-Prompt
context: fork                  # Optional - isolierter Subagent
model: haiku                   # Pflicht bei fork - sonst erbt Main-Agent-Modell
agent: my-agent                # Optional - referenziert Agent aus .claude/agents/ (fuer maxTurns o.ae.)
```

**Hinweis:** Fork-Skills unterstuetzen kein `maxTurns`-Feld direkt. Bei Skills mit Runaway-Risiko: eigenen Agent unter `.claude/agents/` mit `maxTurns` anlegen und via `agent:`-Feld referenzieren. Fuer endliche Skills (lesen → analysieren → schreiben) ist das nicht noetig.

## Trigger Tuning

Bei 10+ Skills in einem Projekt:
- False Triggers (falscher Skill) und Misfires (kein Skill) werden wahrscheinlicher
- Die `description` im YAML-Header optimieren fuer hoehere Treffergenauigkeit
- Jede Description sollte klar und spezifisch sein, nicht generisch
- Der Skill Creator Plugin kann Trigger Tuning automatisch durchfuehren

## Skill-Wartung

1. Regelmaessig Evals laufen lassen, besonders nach Modell-Updates
2. Capability-Uplift-Skills gegen das Basismodell benchmarken
3. Feedback-Schleife nutzen: Je oefter ein Skill verwendet wird, desto besser wird er
4. Veraltete Skills archivieren statt loeschen (fuer Referenz)

## Skill Creator (Anthropic Plugin)

Seit 2026 verfuegbar. Kann:
- Skills aus vager Beschreibung erstellen (inkl. YAML, Body, Hilfsskripte)
- Bestehende Skills optimieren
- Evals und Benchmarks durchfuehren
- Trigger Tuning automatisieren

Installation: `/plugins -> Manage Plugins -> skill-creator -> Install`

### Skill Performance Measurement (AB-Testing)

[Neu: 2026-03-12]

Der Skill Creator kann nicht nur Skills erstellen, sondern auch **messen ob ein Skill tatsaechlich besser ist** als der Zustand ohne ihn. Konkret:
- AB-Test: Aufgabe mit Skill vs. ohne Skill
- Vergleich: neue Version eines Skills vs. alte Version (vor/nach Aenderungen)

**Warum wichtig:** Ohne Messung ist Skill-Optimierung Bauchgefuehl. Mit AB-Testing gibt es echte Daten. Ein schlechterer Skill kann jetzt erkannt und zurueckgesetzt werden.

**Anwendung:** Vor allem bei Capability-Uplift-Skills sinnvoll (die fragil sind und mit Modell-Updates obsolet werden koennen). Siehe Skill-Typen-Abschnitt.

Quelle: 10-claude-code-plugins (2026-03-12)

### Skills 2.0: Strukturierte Evals mit kriterienbasiertem Scoring

[Neu: 2026-03-12]

Der Skill Creator hat mit Skills 2.0 strukturierte Evaluierungen bekommen. Nicht mehr nur "Passt/Passt nicht" -- sondern kriterienbasiertes Scoring mit HTML-Report.

**Workflow:**
1. Skill aufbauen (Name, Trigger-Description, Goal, Tools, Reference Files, Step-by-Step-Prozess)
2. Eval mit **spezifischen Kriterien** starten (nicht "teste alles auf einmal"):
   - Beispiel: "Pruefe ob der Skill immer die Persuasion-Toolkit-Referenz einsetzt, Curiosity Gaps nutzt und Founder-Stories einbaut"
   - 1-3 Kriterien pro Eval-Lauf -- mehr machen Auswertung unscharf
3. Skill Creator spawnt N Sub-Agenten parallel (z.B. 5), jeder fuehrt den Skill aus
4. HTML-Report mit: Score pro Kriterium, Beispiele fuer Pass/Fail, Token/Zeit-Benchmarks
5. Feedback geben → Skill Creator editiert `skill.md` → Eval erneut starten
6. Iteration bis ~90% Pass-Rate (danach ist weiteres Tuning Grenznutzen)

**AB-Test-Varianten:**
- Mit Skill vs. ohne Skill: Beweist ob der Skill ueberhaupt Mehrwert bringt
- Mit vs. ohne bestimmte Reference Files: Findet heraus welche Referenzen tatsaechlich wirken

**Leaner Skills durch Eval:** Bestehende Skills koennen verschlankt werden -- wenn sich herausstellt, dass 2 von 3 Reference Files keinen Score-Unterschied machen, koennen sie entfernt werden. Spart Tokens pro Skill-Aufruf.

**Goldene Regel:** Stop guessing, start testing. Evals ersetzen das naive "run und hoffen" durch einen datengetriebenen Lernzyklus.

## Grounding-Execution-Evaluation-Finalizing Pattern (4-Agenten-Loop)

[Neu: 2026-03-08]

Wenn ein Agent wiederholt Fehler produziert, ist die Loesung selten ein staerkeres Modell -- sondern ein strukturierter Evaluations-Loop. Das Pattern:

```
Grounding Agent --> Execution Agent --> Evaluation Agent
                         ^                     |
                         |_____ Retry falls Fehler __|
                                                     |
                                            Finalizing Agent (bei Erfolg)
```

**Grounding Agent:** Beschafft alle Informationen, die das ausfuehrende Modell braucht. Bei einfachen Tasks (Uebersetzung): reine Prompt-Engineering-Arbeit. Bei komplexen Tasks (Software-Issue): eigener KI-Agent, der Code liest, Web-Suche macht, Kontext aufbaut.

**Execution Agent:** Hat nur EINE Aufgabe. Kein Multitasking, keine Entscheidungen. Beispiel: "Uebersetze exakt das, was gegeben wird." Oder: "Implementiere exakt die Loesung, die das Grounding-Dokument beschreibt."

**Evaluation Agent:** Prueft den Output gegen klar definierte Kriterien. Gibt entweder "Passt" oder strukturiertes Feedback zurueck. Startet bei Fehler den Execution Agent neu (mit Fehlerbeschreibung).

**Finalizing Agent:** Kann auch hardcoded (nicht-KI) sein. Wenn der Evaluation Agent sagt "Passt", reicht oft ein direkter DB-Write oder Git-Commit. Nur bei komplexen Abschluss-Aktionen einen echten KI-Agenten einsetzen.

**Praxis-Daten (Morphreader-Uebersetzungen):**
- Fehlerrate ohne Loop: 8.2% (Englisch), 70.7% (Japanisch) mit guenstigem Modell
- Fehlerrate mit Evaluations-Loop: ~0.1% -- vergleichbar mit professionellen Uebersetzern
- Iteration count: Kann bis zu 11 Runden benoetigen (Praxisbeispiel Software-Issue)

**Wichtig: Diverse Evaluatoren schlagen einfache Mehrfach-Evaluation**

Nicht denselben Evaluator zweimal laufen lassen, sondern mehrere Evaluatoren mit **verschiedenem Fokus** parallel einsetzen. Jeder prueft einen anderen Aspekt des Outputs. Erst wenn alle gruen geben, wird der Output freigegeben.

Fuer domainspezifische Anwendungen dieses Prinzips (z.B. Code-Reviews): Siehe Dispatches an die jeweiligen Projekte.

## Selbst-modifizierendes CLAUDE.md / Agents.md

[Neu: 2026-03-08]

Agenten koennen ihre eigene Konfigurationsdatei (CLAUDE.md, gemini.md, agents.md) bei Fehlern oder Korrekturen durch den User automatisch aktualisieren. Das Ziel: Wissen akkumuliert sich ueber Sessions, die Fehlerquote sinkt mit jeder Iteration.

**Mechanismus:**
- Am Sessionende (oder nach jeder User-Korrektur) schreibt der Agent eine neue Regel in die Konfigurationsdatei.
- Format: `[Kategorie] Nie/Immer X, weil Y.`
- Beim naechsten Sessionstart sind die gelernten Regeln bereits im Kontext.

**Zwei Ebenen:**
- **Global** (z.B. `~/.claude/CLAUDE.md`): User-weite Praeferenzen und Regeln, gelten fuer alle Projekte.
- **Lokal** (Projektverzeichnis `CLAUDE.md`): Projektspezifische Regeln und Skills.

**Praxis-Effekt:** Die Fehlerquote relativ zu User-Praeferenzen sinkt mit jeder Session. Ab ~20-30 gelernten Regeln wird das System sehr praezise. Limit: Bei 1000+ Regeln beginnen Konflikte zwischen Regeln aufzutreten.

**Wichtig fuer Token-Budget:** Das CLAUDE.md darf nicht unbegrenzt wachsen. Regeln periodisch konsolidieren und redundante entfernen.

## Stochastic Multi-Agent Consensus

[Neu: 2026-03-08]

Statt einen Agenten einmal zu fragen, werden N Agenten mit leicht variierten Prompt-Frames parallel gespawnt. Die Ergebnisse werden durch einen Orchestrator aggregiert.

**Warum:** Jedes LLM-Modell ist stochastisch -- bei identischem Prompt liefert es leicht unterschiedliche Antworten. Diese Varianz laesst sich ausnutzen, um einen groesseren Teil des "Loesungsraums" abzudecken.

**Aufbau:**
```
Orchestrator --> [Agent 1: konservative Perspektive]
             --> [Agent 2: nutzerfokussierte Perspektive]
             --> [Agent 3: messbare-Fakten-Perspektive]
             --> [Agent N: ...]
Orchestrator <-- Aggregation via Modus (Haeufigkeit) + Median + Ausreisser-Analyse
```

**Output-Kategorien:**
- **Consensus-Items:** Von den meisten Agenten geteilt -- hohes Vertrauen, priorisieren.
- **Divergente Items:** Nur von manchen geteilt -- manuell evaluieren.
- **Ausreisser:** Nur von 1-2 Agenten -- koennen brillant oder Halluzination sein.

**Sinnvoll fuer:** Ideation, strategische Analysen, Keyword-Recherche, Titelgenerierung, Entscheidungen mit vielen moeglichen Loesungen.

**Kostenpunkt:** N Agenten * Kosten pro Durchlauf. Empfehlung: 5-10 Agenten fuer die meisten Anwendungen.

## Agent Chat Rooms (Debattier-Muster)

[Neu: 2026-03-08]

Statt paralleler unabhaengiger Analyse debattieren Agenten mit verschiedenen Persoenlichkeiten/Rollen in einer gemeinsamen Datei (z.B. `chat.json`).

**Aufbau:**
```
Orchestrator --> [Systems Thinker] \
             --> [Pragmatist]      |  --> chat.json (gemeinsames Protokoll)
             --> [Edge Case Finder]|
             --> [User Advocate]   |
             --> [Contrarian]      /
             <-- Synthese-Agent liest chat.json und erstellt Zusammenfassung
```

**Unterschied zu Stochastic Consensus:**
- Consensus: Agenten arbeiten parallel, berichten unabhaengig.
- Chat Room: Agenten reagieren aufeinander, schraerfen Argumente durch Debatte.

**Vorteil:** Agenten "sehen" gegenseitig ihre Argumente und muessen sich positionieren. Das fuehrt zu praeziseren, nuancierteren Ergebnissen als reine Parallelarbeit.

**Implementierung:** Jeder Agent schreibt seinen Turn in `chat.json`, liest vorherige Turns. Round-Robin oder parallele Ausfuehrung innerhalb jeder Runde.

## Sub-Agent Verification Loops (Unvoreingenommener Reviewer)

[Neu: 2026-03-08]

Ein Implementierungs-Agent akkumuliert "Sunk-Cost-Bias": Er glaubt, seine Loesung sei die beste, weil er alle Umwege kennt. Ein frischer Agent bewertet nur den Output, nicht den Weg.

**Pattern:**
```
Implementierer --> [Output: Code/Dokument/Workflow]
                         |
                   Reviewer Agent (fresh context, zero bias)
                   -- sieht nur Output, nicht die Reasoning-Geschichte
                         |
                +--- OK: Finalizing Agent / direkte Ausgabe
                |
                +--- Fehler: Resolver Agent (fresh context)
                     --> neuer Output --> zurueck zu Reviewer
```

**Warum fresh context:** Der Reviewer-Agent hat keine emotionale Bindung an Designentscheidungen. Er bewertet wie ein externer Peer Reviewer -- erkennt, was der Implementierer "blind" sieht.

**Praxis-Empfehlung:** Nach groesseren Implementierungsaufgaben immer einen separaten Review-Agenten spawnen, nicht denselben nach seiner eigenen Arbeit fragen.

**Verwandt mit:** Grounding-Execution-Evaluation-Finalizing Pattern (siehe oben).

## Prompt Contracts und Reverse Prompting

[Neu: 2026-03-08]

Die haeufigste Ursache fuer schlechte Agent-Outputs ist eine zu vage "Definition of Done".

### Prompt Contracts
Ein Skill, der vor jeder nicht-trivialen Aufgabe einen strukturierten Vertrag erstellt:
```
- Ziel: Was soll am Ende vorliegen?
- Constraints: Was darf NICHT passieren?
- Format: Wie soll der Output aussehen?
- Failure-Kriterien: Wann ist der Output abzulehnen?
```
Der Agent legt den Contract zur Bestätigung vor, bevor er beginnt. Aehnlich wie "Plan Mode" in Claude Code, aber formaler.

### Reverse Prompting
Vor dem Contract stellt der Agent 5 dynamisch generierte Klaerungsfragen:
- Nicht-offensichtliche Annahmen identifizieren
- Geschmacks-abhaengige Entscheidungen klaeren (Design, Ton, Umfang)
- Erst nach den Antworten wird der Prompt Contract erstellt

**Wann einsetzen:** Bei Aufgaben mit subjektiven Qualitaetskriterien (Design, Texte, komplexe Builds) oder hohen One-Shot-Anforderungen.

## Agent-zu-Skill-Konvertierung

Wenn ein bestehender Agent eigentlich ein Skill sein sollte:

1. **Pruefe:** Hat der Agent eine echte "Denkweise" oder nur eine Aufgabenliste?
2. **Pruefe:** Trifft der Agent eigenstaendige Urteile oder folgt er einem Workflow?
3. **Wenn beides Nein --> Konvertiere:**
   - Agent-Prompt wird zum Skill-Body (gekuerzt, Workflow-fokussiert)
   - "Wer du bist" und "Strategische Eskalation" entfallen
   - `context: fork` wenn der Skill komplex ist
   - Modell auf Haiku setzen, wenn der Skill nur liest/formatiert
   - Hilfsskripte auslagern, wenn der Workflow externe Tools braucht

## Infrastruktur-Skills: Standard-Bausteine fuer jedes Team

[Neu: 2026-03-08]

Neben projektspezifischen Skills gibt es **Infrastruktur-Skills**, die nicht vom Anwendungsfall abhaengen, sondern zur Architektur selbst gehoeren. Drei sind Standard:

| Skill | Pflicht? | Modell | Was er tut |
|-------|----------|--------|-----------|
| `/track` | Ja, fuer jedes Team | Inline | Aktualisiert `project-status.md` mit Session-Fortschritt -- Karteileichen pruefen, Erledigtes abhaken |
| `/learn` | Ja, fuer Stufe-1+-Teams | Sonnet (Fork) | Integriert externes Fachwissen in `knowledge/` -- destillieren, verdichten, Index aktualisieren |
| `/reflect` | Ja, fuer jedes Team | Sonnet (Fork) | Team-Selbstanalyse nach `.claude/team-reflection.md` |

### `/track` -- Statusverwaltung als Skill

Ersetzt die direkte Verwaltung von `project-status.md` durch den Main-Agent. Ein Befehl, keine Argumente:
- `/track` -- aktualisiert project-status.md mit dem, was in der Session passiert ist

Laeuft **inline** (nicht als Fork), weil der Skill den Session-Kontext braucht um zu wissen, was erarbeitet wurde. Der Agent ruft `/track` am Sessionende auf (oder nach groesseren Meilensteinen). Kein Argument noetig -- der Agent hat die Info im Kopf.

Fuer "wo stehen wir?" am Sessionstart liest der Main-Agent einfach `project-status.md` direkt -- dafuer braucht es keinen Skill.

### `/learn` -- Knowledge-Ingestion als Skill

Standardisierter Workflow fuer "externes Fachwissen aufnehmen". Ein Pattern, skalierte Implementierung:

**Stufe 0:** Kein `/learn`, kein `knowledge/`. Fuer rein technische Teams ohne Domaenenwissen (z.B. Build-Pipeline, Deployment-Automation).

**Stufe 1 (Standard):** `knowledge/` Verzeichnis + `knowledge/index.md` + `/learn`-Skill (Fork, Sonnet).
- Quelle lesen (URL fetchen, Text verarbeiten)
- Gegen bestehenden Wissensstand pruefen
- Prinzipien destillieren und in die richtige Knowledge-Datei schreiben
- Quellen-Nachweis am Ende jeder Knowledge-Datei
- Index aktualisieren (welche Datei, welches Thema, welche Agents lesen sie)

**Stufe 2 (Wissensintensive Teams):** Wie Stufe 1, plus:
- Notion-Integration (externe Inbox fuer unterwegs)
- Dispatch-Routing (Erkenntnisse an andere Teams weiterleiten)
- Archivierung mit Log (`sources/inbox/` → `sources/archive/`)
- Separate `widersprueche.md` fuer Konflikt-Tracking

**Wann welche Stufe:**
- Stufe 0: Team braucht kein Domaenenwissen (selten)
- Stufe 1: Team arbeitet mit externem Fachwissen -- Content, Beratung, Branding, Strategie, Design, Coaching. **Im Zweifel: nachfragen statt annehmen.** Auch bei vermeintlich "einfachen" Teams kann der User komplexe Wissensanforderungen haben.
- Stufe 2: Team ist primaer ein Wissensverwaltungs-Projekt, oder verarbeitet regelmaessig viele Quellen, oder routet Wissen an mehrere andere Teams.

**Die Schwelle fuer die Stufenfrage ist bewusst niedrig:** Bei der Erstellung eines neuen Teams immer fragen, welche Stufe das Knowledge-System haben soll -- es sei denn, Stufe 0 oder Stufe 1 ist offensichtlich. Branding-Teams koennen Stufe 2 brauchen, Code-Teams koennen Stufe 1 brauchen.

**Verdichtungslogik (in jeder Stufe):**
Vier Typen, die der `/learn`-Skill bei jeder Integration prueft:
- **Bestaetigung:** Deckt sich mit bestehendem Wissen → nur Quelle ergaenzen, nicht redundant einfuegen
- **Erweiterung:** Neues Wissen → einfuegen mit Quellen-Tag `[Quelle: Titel, Datum]`
- **Widerspruch:** Widerspricht bestehendem Wissen → beide Positionen dokumentieren, Main-Agent informieren
- **Veraltung:** Macht bestehendes Wissen obsolet → altes markieren, neues einfuegen

In Stufe 1 stehen Widersprueche direkt in der Knowledge-Datei (mit `⚠ WIDERSPRUCH`-Marker). In Stufe 2 gibt es eine separate `widersprueche.md`.

**Naming-Konvention:** Der Skill heisst in jeder Stufe `/learn`. Die project-builder-Implementierung (Stufe 2) heisst ebenfalls `/learn` -- mit zusaetzlichen Modi (`alle`, `notion`, `lokal`). So ist das Pattern ueberall erkennbar, auch wenn die Implementierung skaliert.

### Standard-Template: `/track`

Parametrisierte Vorlage. `[PROJEKTNAME]` projektspezifisch anpassen.

```markdown
---
name: track
description: "Aktualisiert project-status.md mit dem, was in der aktuellen Session erarbeitet wurde. Keine Argumente noetig."
allowed-tools: Read, Edit, Grep, Glob
---

Du aktualisierst den Projektstatus von [PROJEKTNAME] basierend auf dem, was in dieser Session passiert ist.

## Vorgehen

1. Lies `project-status.md`
2. Fasse zusammen, was in dieser Session erarbeitet wurde
3. Aktualisiere:
   - **Aktueller Stand**: Passe die 2-3 Saetze an
   - **Offene Aufgaben**: Hake erledigte ab, fuege neue hinzu
   - **Entscheidungen**: Trage neue Entscheidungen ein mit Datum
   - **Naechste Session**: Was sollte als naechstes passieren?
4. **Karteileichen-Pruefung (PFLICHT):** Alle offenen Aufgaben gegen den aktuellen Stand
   abgleichen. Erledigte nach "Erledigt" verschieben mit Datum.
5. Erledigte Aufgaben aelter als 2-3 Sessions entfernen
6. Schreibe die aktualisierte Datei zurueck (Edit, nie Write)

## Regeln
- Halte die Datei unter 50 Zeilen
- Keine Meinung, keine Bewertung -- nur Fakten
```

### Standard-Template: `/learn` (Stufe 1)

Parametrisierte Vorlage fuer Stufe-1-Teams. `[PROJEKTNAME]`, `[WISSENSGEBIET]` und die Ziel-Dateien projektspezifisch anpassen. Stufe 2 erweitert dieses Template um Notion-Integration, Dispatch-Routing und Archivierung (siehe project-builder `/learn` als Referenz).

```markdown
---
name: learn
description: "Integriert neues Fachwissen aus einer Quelle (URL, Text, Transkript) in die Knowledge-Base. Destilliert anwendbare Prinzipien fuer das Team."
argument-hint: "[URL oder Thema]"
allowed-tools: "Read, Edit, Write, Glob, Grep, WebFetch"
context: fork
model: sonnet
---

Du integrierst neues Fachwissen in die [PROJEKTNAME] Knowledge-Base.

## Kontext zuerst

1. Lies `knowledge/index.md` -- Uebersicht aller Knowledge-Dateien
2. Lies die Knowledge-Datei(en), die thematisch am naechsten liegen
3. Lies `CLAUDE.md` -- Projektkontext

## Quelle beschaffen

- $ARGUMENTS enthaelt eine URL → WebFetch (Artikel holen, YouTube-URL: Inhalt holen)
- $ARGUMENTS enthaelt keinen URL → als direkten Text-Input behandeln
- Falls Quelle nicht lesbar: Melden und abbrechen

## Prinzipien destillieren

Filtere rigoros:
- **Behalten:** Konkrete Techniken, Prinzipien, Frameworks, die [PROJEKTNAME]-Agents
  bei ihrer Arbeit anwenden koennen
- **Verwerfen:** Allgemeinplaetze, Motivationsfloskeln, Kontext der fuer
  [PROJEKTNAME] irrelevant ist

Formuliere jedes Prinzip als **anwendbare Regel**, nicht als Zusammenfassung:
- FALSCH: "Die Quelle sagt, dass X wichtig ist"
- RICHTIG: "[Konkreter Test/Regel/Technik die ein Agent direkt anwenden kann]"

## Einordnen (Verdichtungslogik)

Pruefe jede Erkenntnis gegen den bestehenden Wissensstand:

- **Bestaetigung:** Deckt sich mit bestehendem Wissen → nur Quelle ergaenzen, nicht redundant einfuegen
- **Erweiterung:** Neues Wissen → einfuegen mit `[Quelle: Titel, Datum]`
- **Widerspruch:** Widerspricht bestehendem Wissen → NICHT leise ueberschreiben.
  Beide Positionen dokumentieren mit `⚠ WIDERSPRUCH`-Marker. Main-Agent informieren.
- **Veraltung:** Macht bestehendes Wissen obsolet → altes mit `[Veraltet seit YYYY-MM-DD]`
  markieren, neues direkt darunter einfuegen

## Ziel-Datei bestimmen

[PROJEKTSPEZIFISCH: Welche Knowledge-Dateien gibt es und welche Themen gehoeren wohin?
Beispiele:
- Copywriting, Textqualitaet, Stil → content-principles.md
- Branding, Positionierung → brand-strategy.md
- Technische Patterns → architecture.md
- Markt, Wettbewerb → market-insights.md]

Neue Datei nur erstellen, wenn kein bestehendes Thema passt.

## Schreiben

1. Prinzipien in die Ziel-Datei einfuegen (Edit, nie Write bei bestehenden Dateien)
2. Quellen-Nachweis am Ende der Datei ergaenzen:
   `- [Titel] (YYYY-MM-DD) -- Was diese Quelle beigetragen hat`
3. `knowledge/index.md` aktualisieren falls neue Datei oder neue Agent-Zuordnung

## Zusammenfassung

Gib zurueck:
- Was wurde extrahiert (3-5 Prinzipien, als anwendbare Regeln formuliert)
- Wohin geschrieben (welche Knowledge-Datei)
- Welche Agents profitieren davon
- Verdichtungstyp (Bestaetigung/Erweiterung/Widerspruch/Veraltung)
- Ob es Widersprueche zum bestehenden Wissen gibt
```
