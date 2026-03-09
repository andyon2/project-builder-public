# Token-Optimierung fuer Agent-Teams

## Die groessten Token-Fresser

### 1. Fehlende model-Felder (Opus-Vererbung)
**Problem:** Ohne explizites `model`-Feld erbt jeder Sub-Agent und jeder Fork-Skill das Modell des Main-Agents. Laeuft der auf Opus, verbrennen alle Opus-Tokens fuer Aufgaben, die Sonnet oder Haiku genauso gut erledigen.

**Fix:** `model`-Feld in JEDEM Agent und JEDEM Fork-Skill setzen. Keine Ausnahme.

**Impact:** Oft -50% Gesamtverbrauch allein durch diese Aenderung.

### 2. Agents statt Skills
**Problem:** Ein Agent braucht ein eigenes Context Window, laedt den vollstaendigen Agent-Prompt, und hat Overhead fuer Eskalation/Selbstcheck. Ein Fork-Skill laeuft in einem eigenen schlanken Kontext mit guenstigerem Modell.

**Fix:** Pruefe jeden Agent: Braucht er eine Denkweise oder fuehrt er nur Schritte aus? Letzteres -> Fork-Skill.

**Wichtig: Inline-Skill vs. Fork-Skill vs. Agent:**
- Inline-Skill: Laeuft auf Opus (Main-Agent-Kontext). NUR fuer winzige Tasks (<3 Turns).
- Fork-Skill (`context: fork, model: haiku`): Laeuft auf eigenem Modell. Kuerzerer Prompt, kein Agent-Overhead. **Fast immer guenstiger als ein Agent auf Sonnet.**
- Agent (sonnet): Laeuft auf Sonnet, aber langer Prompt + Eskalation + Selbstcheck.

Im Zweifel: Fork-Skill mit Haiku schlaegt Agent mit Sonnet -- billigeres Modell UND weniger Prompt-Overhead.

**Impact:** -60-80% pro konvertiertem Agent, besonders bei haeufig genutzten Agents.

### 3. Aufgeblaehte Agent-Prompts
**Problem:** Agent-Prompts wachsen organisch. Sektionen werden hinzugefuegt, aber nie entfernt. Ein 200-Zeilen-Prompt fuer einen Agent, der nur Dateien liest und formatiert, ist Verschwendung.

**Fix:** Prompt-Laenge muss proportional zur Aufgabenkomplexitaet sein. Haiku-Agents brauchen kurze, praezise Prompts.

**Impact:** -10-30% pro Agent.

### 4. Fehlende maxTurns
**Problem:** Ohne maxTurns kann ein Agent in Endlosschleifen geraten (Retry-Loops, unnoetige Recherche-Zyklen). Jeder zusaetzliche Turn kostet Tokens.

**Fix:** maxTurns als Pflichtfeld. 15-25 fuer normale Tasks, 20-30 fuer dialogische.

**Impact:** Verhindert Ausreisser, die eine ganze Session ruinieren koennen.

### 5a. Guenstiges Modell + Evaluations-Loop vs. teures Modell direkt

[Neu: 2026-03-08]

**Problem:** Bei hohen Fehlerraten ist der Reflex "groesseres Modell nehmen". Das ist teuer und loest das Problem oft nicht vollstaendig -- selbst das staerkste Modell macht Fehler.

**Alternative:** Guenstiges Modell (Mistral Small, lokales Modell) + Grounding-Execution-Evaluation-Loop.

**Praxis-Daten:**
- Guenstiges Modell direkt: 70.7% Fehlerrate (Japanisch), 8.2% (Englisch)
- Guenstiges Modell mit Evaluations-Loop: ~0.1% Fehlerrate
- Selbst Claude Opus direkt: Macht immer noch Fehler

**Wann welche Strategie:**
| Situation | Strategie |
|-----------|-----------|
| Einfache repetitive Tasks (Uebersetzung, Formatierung) | Guenstiges Modell + Evaluations-Loop |
| Komplexe Tasks mit eindeutigen Qualitaetskriterien | Sonnet + Evaluations-Loop |
| Echte strategische Analyse ohne Retry-Logik | Opus direkt |

**Achtung:** Der Loop kostet mehr Tokens pro Task (mehrere Runden moeglich). Wenn die Aufgabe sehr selten laeuft oder Zeit kritisch ist, kann ein staerkeres Modell direkt trotzdem sinnvoll sein. Bei Batch-Verarbeitung (1000+ Tasks/Tag) ueberwiegt die Kostenersparnis durch guenstiges Modell deutlich.

### 5b. 60/30/10 Modell-Mix fuer grosse Agent-Stacks

[Neu: 2026-03-08]

Bei multi-Agent-Setups mit hohem Token-Volumen lohnt sich ein bewusster Modell-Mix statt eines einheitlichen Modells:

| Anteil | Modell | Fuer |
|--------|--------|------|
| 60% | Haiku / Flash | Masse-Tasks: Scraping, Extraktion, Klassifikation, Formatierung |
| 30% | Sonnet | Mid-Tier: Anreicherung, Recherche, Entwurf |
| 10% | Opus | Routing-Entscheidungen, Orchestrierung, Review, finale Synthese |

**Praxis-Kalkulation (Beispiel Lead-Generierung):**
- 100% Opus: ~12 Cent/Lead
- 60/30/10 Mix: ~3 Cent/Lead (75% Kostenreduktion bei ~5% Qualitaetsabfall)

**Batch API:** Fuer nicht-zeitkritische Aufgaben bieten Anbieter (Anthropic, Google, OpenAI) Batch-Verarbeitung mit ~50% Kostenreduktion. Anfragen werden in Niedrig-Last-Perioden (z.B. nachts) ausgefuehrt -- fuer Datenverarbeitungs-Pipelines ideal.

### 5. Opus fuer einfache Tasks
**Problem:** Opus ist deutlich teurer als Sonnet und Haiku. Wenn ein Agent nur Dateien liest und zusammenfasst, ist Opus Verschwendung.

**Fix:** Modellwahl nach Aufgabenkomplexitaet:

| Aufgabe | Modell | Begruendung |
|---------|--------|-------------|
| Strategische Analyse, Review, Urteilsvermoegen | sonnet | Braucht Reasoning-Tiefe |
| Texterstellung, Code, Recherche | sonnet | Braucht kreative Qualitaet |
| Datei-Reads, Zusammenfassungen, Status-Reports | haiku | Braucht nur Struktur |
| Daten-Fetching, Format-Konvertierung | haiku | Mechanische Aufgabe |

### 6. Main-Agent macht Arbeit selbst
**Problem:** Jede Nachricht im Main-Agent-Kontext ist teuer (Opus + wachsendes Context Window). Wenn der Main-Agent selbst arbeitet statt zu delegieren, frisst das den wertvollsten Kontext.

**Fix:** Der Main-Agent delegiert IMMER. Skills fuer Schnelles, Agents fuer Komplexes. Eigenarbeit nur bei strategischen Entscheidungen (<3 Nachrichten).

## Token-Impact pro Abstraktion

| Abstraktion | Relativer Token-Overhead pro Aufruf |
|-------------|--------------------------------------|
| Inline-Skill | Minimal (laeuft im bestehenden Kontext) |
| Fork-Skill (haiku) | Niedrig |
| Fork-Skill (sonnet) | Mittel |
| Agent (haiku) | Mittel (Agent-Prompt + Kontext + Eskalation + Selbstcheck) |
| Agent (sonnet) | Hoch |
| Agent (opus, geerbt) | Sehr hoch |

Die Hierarchie ist gleichzeitig eine Kosten-Hierarchie: Von oben nach unten wird es teurer. Deshalb: Skill-First.

## Checkliste: Token-Audit

- [ ] Hat JEDER Agent ein explizites `model`-Feld?
- [ ] Hat JEDER Fork-Skill ein explizites `model`-Feld?
- [ ] Hat JEDER Agent ein `maxTurns`-Feld?
- [ ] Gibt es Agents, die eigentlich Skills sein sollten?
- [ ] Sind die Agent-Prompts proportional zur Aufgabenkomplexitaet?
- [ ] Laeuft kein Agent auf Opus, der es nicht braucht?
- [ ] Delegiert der Main-Agent konsequent statt selbst zu arbeiten?
- [ ] Gibt es wiederkehrende Aufgaben ohne Skill?

## Quellen
- Rendle-Architektur (v3-v5) -- Grundprinzipien Opus-Vererbung, Modellwahl-Tabelle
- improved-skill.md (2026-03-06) -- Fork-Skill vs. Agent Token-Vergleich, Inline-Skill-Warnung
- Claude 2.0 is finally here.md (2026-03-07) -- Modell-Vererbungsverhalten bei context:fork
- 2026-03-08_ki-am-murksen-hindern.md (2026-03-08) -- Guenstiges Modell + Evaluations-Loop vs. teures Modell direkt, Praxis-Fehlerdaten aus Morphreader-Produktion
- 2026-03-08_ai-agents-full-course-2026-master-agentic-ai-2-hours.md (2026-03-08) -- 60/30/10 Modell-Mix, Batch-API-Rabatte, Praxis-Kalkulation Lead-Generierung
