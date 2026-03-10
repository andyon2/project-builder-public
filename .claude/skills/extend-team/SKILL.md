---
name: extend-team
description: "Erstellt einen fertigen Entwurf (SKILL.md oder Agent-Datei) fuer eine neue Aufgabe. Entscheidet selbststaendig ob Skill oder Agent die richtige Abstraktion ist. Nicht fuer Ja/Nein-Entscheidungen ohne Dateierstellung."
argument-hint: "[aufgabenbeschreibung]"
allowed-tools: "Read, Glob, Grep"
context: fork
model: sonnet
---

Der User oder Main-Agent hat eine Aufgabe identifiziert, fuer die es noch keinen Skill oder Agent gibt. Deine Aufgabe: Analysieren, die richtige Abstraktion waehlen, und einen fertigen Entwurf liefern.

# REGEL: NUR ENTWURF, KEINE UMSETZUNG

Du erstellst KEINE Dateien. Du aenderst NICHTS am Projekt. Du lieferst einen Entwurf im Chat. Der User entscheidet, ob und wie er umgesetzt wird.

## Aufgabe

$ARGUMENTS

## Vorgehen

### 1. Referenzmaterial und Projektkontext laden

Lies zuerst die Team-Building-Templates: `$CLAUDE_PROJECT_DIR/reference/team-building-templates.md`

Dann lies im aktuellen Projekt:
- `CLAUDE.md` -- um das Projekt, die bestehenden Agents und Skills zu verstehen
- `.claude/agents/` -- welche Agents gibt es schon?
- `.claude/skills/` -- welche Skills gibt es schon?
- System-Prompt des Main-Agents (falls auffindbar)

Pruefe: Gibt es bereits einen Agent oder Skill, der diese Aufgabe teilweise abdeckt? Falls ja, ist vielleicht eine Erweiterung besser als etwas Neues.

### 2. Entscheidung: Skill oder Agent?

Wende den Denkweise-Test an:

**Braucht die Aufgabe eigenes Urteilsvermoegen?**
- Muss eigenstaendig bewertet, priorisiert, strategisch eingeordnet werden? --> Agent
- Muss eine eigene Perspektive eingenommen werden ("denkt wie ein...")? --> Agent
- Muss breiter Kontext verknuepft werden (mehrere Wissensgebiete, Projekthistorie)? --> Agent

**Oder ist es ein wiederholbarer Workflow?**
- Gleiche Schritte, variables Input, vorhersagbarer Output? --> Skill
- Klare Abfolge von Lesen, Verarbeiten, Formatieren, Schreiben? --> Skill
- Strukturierter Kurz-Dialog (3-5 Fragen, festes Format)? --> Skill

**Im Zweifel: Skill.** Wenn sich spaeter zeigt, dass mehr Urteilsvermoegen noetig ist, kann man zum Agent promovieren.

### 3. Bei Skill: Details bestimmen

**Skill-Typ:**
- Encoded Preference (nutzerspezifischer Workflow, langlebig) -- bevorzugen
- Capability Uplift (kompensiert Modell-Schwaeche, fragil) -- nur wenn noetig

**Kontext:**
- Inline (im Hauptkontext): Wenn einfach, <5 Turns, wenig Dateizugriff
- Fork (isolierter Subagent): Wenn komplex, viele Dateien, wuerde Hauptkontext belasten

**Modell (bei Fork):**
- haiku: Wenn der Skill nur liest, formatiert, zusammenfasst
- sonnet: Wenn der Skill kreativ schreiben oder analysieren muss

**Skill-Suite pruefen:**
- Gehoert der neue Skill thematisch zu bestehenden Skills oder wuerden mehrere verwandte Skills entstehen?
- Falls ja: Als Skill-Suite vorschlagen -- ein uebergeordneter Ordner mit Unter-Skills (jeder mit eigenem `SKILL.md`)
- Beispiel: `/content` als Suite mit `write`, `edit`, `translate` als Unter-Skills
- Vorteil: Skaliert auf 10+ thematisch verbundene Skills, Progressive Disclosure bleibt erhalten

**Hilfsskripte noetig?**
- Braucht der Skill externe API-Calls, Daten-Fetching, PDF-Rendering?
- Falls ja: Hilfsskript-Entwurf mit angeben

### 4. Bei Agent: Details bestimmen

**Denkweise formulieren:**
- "Du denkst wie ein erfahrener [Analogie], der..."
- Was unterscheidet gute von schlechter Arbeit in dieser Rolle?

**Modell:**
- sonnet (Standard fuer die meisten Agents)
- haiku (nur wenn die Aufgabe einfach genug ist)
- Opus: NEIN -- das ist dem Main-Agent vorbehalten

**Modus:**
- Delegiert (Standard): Klarer Auftrag rein, Ergebnis zurueck
- Delegiert + Direkt: Nur wenn die Kernaufgabe nachweislich Dialog braucht

**maxTurns:** 15-25 (normal), 20-30 (dialogisch)

### 5. Entwurf erstellen

Liefere den vollstaendigen Entwurf im Chat. Format:

```
## Empfehlung: [Skill / Agent]

### Begruendung
[2-3 Saetze: Warum diese Abstraktion? Was war ausschlaggebend?]

### Einordnung ins bestehende Team
[Wie verhaelt sich das Neue zu bestehenden Agents/Skills? Gibt es Ueberschneidungen?]

### Datei: [Pfad wo die Datei hinkommen wuerde]

[Vollstaendiger Inhalt der Skill- oder Agent-Datei, copy-paste-ready]

### Hilfsskripte (falls noetig)
[Datei: Pfad]
[Inhalt]

### Aenderungen an CLAUDE.md
[Welche Zeile in der Agent- oder Skill-Tabelle ergaenzt werden muesste]

### Aenderungen am Main-Agent System Prompt
[Falls der Main-Agent den neuen Skill/Agent kennen muss: Welche Zeile ergaenzen?]
```

Am Ende: Expliziter Hinweis:
"Dies ist ein Entwurf. Es wurden keine Dateien erstellt oder geaendert. Zum Umsetzen: Kopiere die Dateien an die angegebenen Pfade und aktualisiere CLAUDE.md."
