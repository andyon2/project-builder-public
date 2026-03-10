# Entscheidungshierarchie: Skill vs. Agent

## Die Kernfrage

Fuer jede Aufgabe im Projekt:

```
Ist es ein wiederholbarer Workflow MIT vorhersagbarem Output?
|
+-- JA --> SKILL
|   +-- Einfach (<5 Turns, wenig Kontext) --> Inline-Skill
|   +-- Komplex (viel Kontext, Hilfsskripte) --> Fork-Skill (haiku/sonnet)
|   +-- Kurz-Dialog (3-5 Fragen, festes Format) --> Interview-Skill
|
+-- NEIN --> Braucht es eine eigene Denkweise/Urteilsvermoegen?
    |
    +-- JA --> AGENT
    |   +-- Kein User-Dialog noetig --> Delegierter Agent (sonnet)
    |   +-- User-Dialog noetig (>5 Interaktionen) --> Agent + Direkt (sonnet)
    |
    +-- NEIN --> Kann der Main-Agent es inline erledigen?
        +-- JA (<3 Nachrichten) --> Main-Agent macht es selbst
        +-- NEIN --> Zurueck: Doch ein Skill oder Agent
```

## Der Denkweise-Test

Ein Agent braucht eine Denkweise, wenn die Aufgabe folgendes erfordert:

| Merkmal | Beispiel | Agent noetig? |
|---------|----------|---------------|
| Urteile faellen | "Ist dieses Angebot gut oder schlecht?" | Ja |
| Kontext verknuepfen | "Wie passt das zur Gesamtstrategie?" | Ja |
| Muster erkennen | "Welche Trends zeigen sich ueber mehrere Datenpunkte?" | Ja |
| Perspektive einnehmen | "Wie wuerde ein Kunde das sehen?" | Ja |
| Schritte ausfuehren | "Lies Datei A, formatiere als Tabelle, schreib in Datei B" | Nein -> Skill |
| Daten sammeln | "Hole Status aus 3 Quellen, fasse zusammen" | Nein -> Skill |
| Report erstellen | "Erstelle woechentlichen Bericht im Format X" | Nein -> Skill |
| Kurz-Interview | "Frage 5 Fragen zum Thema X, schreib Ergebnis in Datei Y" | Nein -> Skill |

## Warum Spezialisierung? (Intuition)

Ein generischer KI-Agent ist wie ein Genie, das alles aus dem Stand erarbeiten kann -- aber noch nie Steuern gemacht hat. Ein spezialisierter Skill ist wie der erfahrene Steuerberater, der Tausende Faelle kennt, jeden Edge Case und jeden Kniff.

Du willst den Steuerberater. Nicht weil der Generalist es nicht koennte -- sondern weil du nicht willst, dass er den Steuercode jedes Mal neu erarbeitet.

Skills sind dieser Spezialisierungssprung: Derselbe intelligente Generalist darunter, aber mit on-demand einladbarer Domain-Expertise.

[Neu: 2026-03-07]

## Grenzfaelle

### "Der Agent macht beides -- Urteile UND Workflow"
Aufteilen: Der Urteilsteil bleibt Agent, der Workflow-Teil wird Skill. Der Agent ruft den Skill auf oder der Main-Agent orchestriert beides.

### "Der Skill ist zu komplex fuer einen Skill"
Fork-Skill mit Hilfsskripten. Ein Fork-Skill kann genauso komplex arbeiten wie ein Agent -- er hat nur keine eigene "Persoenlichkeit" und keinen Eskalations-Mechanismus. Wenn beides nicht noetig ist, reicht ein Fork-Skill.

### "Ich bin unsicher"
Starte als Skill. Wenn sich herausstellt, dass die Aufgabe mehr Urteilsvermoegen braucht, promoviere zum Agent. Umgekehrt (Agent -> Skill) ist schwieriger, weil man organisch gewachsene Prompts kuerzen muss.

### "Der Agent wurde organisch erweitert und macht jetzt alles"
Typisches Zeichen fuer Wucherung. Zerlegen: Was davon braucht Urteilsvermoegen (bleibt Agent), was sind angehaegte Workflows (werden Skills)? Ein Agent, der 10 verschiedene Aufgaben macht, ist fast immer: 2-3 echte Agent-Aufgaben + 7-8 Skills.

## Faustregel fuer Team-Komposition

| Team-Groesse | Empfohlenes Verhaeltnis Skills:Agents |
|--------------|---------------------------------------|
| Klein (1-3 Agents) | Mindestens 1:1 (gleich viele Skills wie Agents) |
| Mittel (4-6 Agents) | Mindestens 1.5:1 (50% mehr Skills als Agents) |
| Gross (7+ Agents) | Pruefe: Braucht es wirklich 7+ Agents? Oft sind 4 Agents + 6 Skills besser. |

Wenn ein Team deutlich mehr Agents als Skills hat, ist das ein Warnsignal. Nicht jedes Warnsignal ist ein Problem -- aber es erfordert eine explizite Begruendung.

## Strategy-Agent-Pattern: Wann braucht ein Team einen Strategen?

[Neu: 2026-03-09]

Nicht jedes Team braucht einen Strategy-Agent -- aber jedes Team, das ein **verkauftes oder oeffentlich positioniertes Produkt** baut, braucht eine Strategie-Faehigkeit. Die Frage ist, wo sie sitzt.

### Drei Muster

| Muster | Wann | Beispiel |
|--------|------|----------|
| **Main-Agent IST der Stratege** | Strategie/Positionierung ist der Projektzweck | Beratungs-Team (Career Strategist), Content-Team (Creative Director) |
| **Separater Strategy-Agent** | Main-Agent ist primaer technisch/operativ, Produkt wird aber vermarktet | Software-Produkt mit Tech Lead als Main-Agent |
| **Kein Strategie-Bedarf** | Reines Infrastruktur-/Tooling-Projekt ohne Vermarktung | Build-Pipeline, interne Automation |

### Erkennungsfrage

> *"Wird dieses Produkt/Projekt verkauft, positioniert oder oeffentlich vermarktet? Wenn ja: Wer im Team entscheidet ueber Positionierung, Zielgruppe, Pricing, Feature-Priorisierung aus Marktsicht?"*

Wenn die Antwort "niemand" oder "der User alleine im Kopf" ist: Luecke.

### Warum ein separater Agent (nicht der Main-Agent)?

Wenn der Main-Agent ein Tech Lead ist, ist seine Denkweise technisch: Architektur, Code-Qualitaet, Delegation an Entwickler-Agents. Strategie-Denken ("Welches Feature zuerst, weil der Markt es verlangt?") ist eine **andere Denkweise** -- nicht eine Erweiterung der technischen.

Die Denkweisen kollidieren: Ein Tech Lead priorisiert nach technischer Schuld und Abhaengigkeiten. Ein Stratege priorisiert nach Markt-Impact und Differenzierung. Beides im selben Agent verwischt die Perspektive.

### Warum ein Agent (nicht ein Skill)?

Der Denkweise-Test:
- Eigenstaendige Urteile faellen ("Feature X vor Y, weil Marktsignal Z") → Ja
- Breiten Kontext verknuepfen (Wettbewerb + User-Needs + Tech-Constraints + Pricing) → Ja
- Eigene Perspektive hat Mehrwert ("denkt wie ein Indie-Product-Stratege") → Ja
- Output vorhersagbar? → Nein

→ Agent, nicht Skill.

### Design-Empfehlung fuer den separaten Strategy-Agent

**Modus:** `delegiert + direkt` -- Roadmap-Diskussionen und Positionierungs-Workshops sind explorativ und dialogisch. Delegiert fuer: "Priorisiere diese 5 Backlog-Items aus Marktsicht."

**Modell:** Sonnet. Braucht Reasoning-Tiefe fuer Strategie, aber kein Opus.

**Abgrenzung zum Main-Agent:**
- Strategy-Agent: Positionierung, Zielgruppe, Pricing, Roadmap-Priorisierung (Business-Sicht), Wettbewerbs-Analyse, Release-Scoping
- Main-Agent: Architektur, Code-Reviews, Agent-/Skill-Delegation, Session-Management

**Knowledge-Anbindung:** Liest `knowledge/competitors.md` (falls vorhanden) und bekommt eine eigene `knowledge/product-strategy.md` (Positionierung, Zielgruppe, Pricing-Modell, Differenzierung).

**Interaktion mit Tech Lead:**
1. Stratege liefert priorisierte Roadmap mit Business-Begruendung
2. Tech Lead setzt um oder meldet technische Constraints zurueck
3. Bei Konflikten (Business-Prio vs. Tech-Schuld): User entscheidet

### Pflicht-Prueffrage bei neuen Teams

Diese Frage gehoert in Schritt 1 (Anforderungen klaeren) des Architektur-Entwurfs. Nicht optional -- aktiv stellen.

### Quellen
- Analyse bestehender Teams (2026-03-09) -- Muster-Erkennung: Strategie-Besitz korreliert mit Projekt-Typ

## Deployment-Determinismus als Designziel

[Neu: 2026-03-08]

Ein verbreiteter Irrtum: Agentic Workflows seien im Deployment selbst-heilend. Das stimmt nur, solange der Agent aktiv dabei ist (Entwicklungs- und Testphase). Im Production-Deployment (Cron, Webhook, autonome Ausfuehrung) laeuft nur der Code -- nicht der Agent.

**Konsequenz:** Das Deployment-Ziel ist Deterministik, nicht Agilität. Ein sauber getesteter, deterministischer Workflow ist zuverlaessiger als ein "flexibler" Workflow, der viele Entscheidungen zur Laufzeit trifft.

**Designprinzip:**
- Alle Edge Cases in der Entwicklungsphase mit dem Agenten auflösen
- Erst wenn der Workflow sauber laeuft, deployen
- Im Deployment: Klar definierte Fehlerpfade (nicht "der Agent wird es schon finden")

**Abgrenzung:** Skills die lokal vom User getriggert werden (mit aktivem Agenten) koennen flexibler sein. Workflows die autonom laufen muessen maximal deterministisch sein.

## Quellen
- Rendle-Architektur (v3-v5) -- Grundlegende Hierarchie, Denkweise-Test
- improved-skill.md (2026-03-06) -- Grenzfaelle Agent-zu-Skill, Team-Kompositionsregeln
- AI_DESIGN_PATTERNS_REPORT.md (2026-03-06) -- Muster bei uebergrossen Agent-Teams
- stop-building-ai-agents-do-this-instead.md (2026-03-07) -- Genius-vs-Tax-Professional-Metapher als Intuition fuer den Wert von Spezialisierung
- 2026-03-08_how-to-build-10000-agentic-workflows-claude-code-tutorial.md (2026-03-08) -- Deployment-Determinismus, WAT-Framework Deployment-Einschraenkung, Self-Healing nur bei aktivem Agent.
