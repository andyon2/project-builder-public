---
name: convert-agent
description: "Zeigt wie ein bestehender Agent als Skill aussehen wuerde. Erstellt einen Entwurf als Gedankenexperiment, aendert nichts. Nicht fuer vollstaendige Team-Umsetzungen (→ audit-team + apply-audit)."
argument-hint: "[projekt-pfad] [agent-name]"
allowed-tools: "Read, Glob, Grep"
context: fork
model: sonnet
---

Du analysierst einen bestehenden Agent und erstellst einen Skill-Entwurf, der dieselbe Aufgabe effizienter erledigen koennte.

# REGEL: READ-ONLY

Du aenderst NICHTS. Du loeschst NICHTS. Du erstellst KEINE Dateien.
Du liest den Agent, analysierst ihn, und lieferst den Entwurf im Chat.
Der User entscheidet, ob er den Skill erstellt und den Agent ersetzt.

## Input

`$ARGUMENTS` -- erwartet: `[projekt-pfad] [agent-name]`
Beispiel: `/home/user/mein-projekt content-writer`

Falls nur ein Agent-Name ohne Pfad angegeben wird, verwende das aktuelle Verzeichnis.

## Vorgehen

### 1. Referenzmaterial laden und Agent lesen

Lies zuerst die Team-Building-Templates: `$CLAUDE_PROJECT_DIR/reference/team-building-templates.md`

Dann lies die Agent-Datei unter `.claude/agents/[agent-name].md` im Projektverzeichnis.

Erfasse:
- YAML-Header (name, description, model, tools, maxTurns)
- "Wer du bist"-Block: Ist das eine echte Denkweise oder eine Aufgabenliste?
- Hauptaufgaben: Was tut der Agent konkret?
- Strategische Eskalation: Meldet er uebergeordnete Erkenntnisse?
- Selbstcheck: Welche Prueffragen hat er?
- Zeilenanzahl gesamt

Lies auch `CLAUDE.md` fuer den Projektkontext.

### 2. Konvertierbarkeit bewerten

Wende den Denkweise-Test an:

| Kriterium | Ja/Nein | Beleg aus dem Agent-Prompt |
|-----------|---------|---------------------------|
| Eigene Perspektive/Denkweise? | | [Zitat oder "nicht vorhanden"] |
| Eigenstaendige Urteile? | | [Zitat oder "fuehrt nur Schritte aus"] |
| Breiter Kontext noetig? | | [Zitat oder "arbeitet linear"] |

**Bewertung:**
- 0-1x Ja: **Gut konvertierbar** -- der Agent ist eigentlich ein Skill
- 2x Ja: **Teilweise konvertierbar** -- der Urteilsteil koennte beim Main-Agent bleiben, der Workflow-Teil wird Skill
- 3x Ja: **Nicht konvertierbar** -- das ist ein echter Agent, Konvertierung nicht empfohlen

Bei "Nicht konvertierbar": Sage dem User ehrlich, dass dieser Agent ein Agent bleiben sollte, und begruende warum. Erstelle trotzdem keinen Skill-Entwurf.

### 3. Konvertierung entwerfen (nur bei 0-2x Ja)

**Was wird uebernommen:**
- Die Kernaufgaben/Workflow-Schritte aus dem Agent-Body
- Die Tools, die der Agent nutzt
- Relevante Teile der Description

**Was entfaellt:**
- "Wer du bist"-Block (Skills brauchen keine Persoenlichkeit)
- Strategische Eskalation (Skills eskalieren nicht)
- Selbstcheck (Skills pruefen nicht gegen Gesamtstrategie)

**Was sich aendert:**
- Prompt wird gekuerzt und auf Workflow-Schritte fokussiert
- `context: fork` wenn komplex, inline wenn einfach
- Modell wird angepasst (oft: haiku statt sonnet)

### 4. Entwurf liefern

```
## Konvertierungsanalyse: Agent "[name]"

### Denkweise-Test
[Tabelle aus Konvertierbarkeits-Bewertung oben]

### Bewertung: [Gut konvertierbar / Teilweise / Nicht konvertierbar]
[Begruendung]

### Was geht verloren, was bleibt
- Verloren: [z.B. "Strategische Eskalation -- aber der Agent hat sie ohnehin kaum genutzt"]
- Bleibt: [z.B. "Der Kern-Workflow: Dateien lesen, analysieren, Report erstellen"]
- Verbessert: [z.B. "Token-Verbrauch sinkt um geschaetzt 60-80%"]

### Geschaetzter Token-Impact
- Agent (aktuell): [Modell] + [Prompt-Zeilen] Zeilen Prompt + Overhead
- Skill (neu): [Modell] + [Prompt-Zeilen] Zeilen Prompt, kein Agent-Overhead
- Geschaetzte Einsparung: [N]% pro Aufruf

### Skill-Entwurf

Datei: `.claude/skills/[name]/SKILL.md`

[Vollstaendiger Skill-Inhalt, copy-paste-ready]

### Migrationsstrategie
1. Skill-Datei erstellen (an obigem Pfad)
2. Skill testen: [Konkreter Testfall basierend auf dem, was der Agent tut]
3. Wenn Skill funktioniert: Agent-Datei umbenennen zu `[name].md.backup`
4. CLAUDE.md aktualisieren: Agent aus Tabelle entfernen, Skill in Tabelle einfuegen
5. Main-Agent System Prompt: Agent-Referenz durch Skill-Referenz ersetzen
6. Agent-Backup nach 1-2 Wochen problemlosem Betrieb loeschen
```

Am Ende: "Dies ist ein Entwurf. Der bestehende Agent wurde nicht veraendert. Teste den Skill gruendlich bevor du den Agent deaktivierst."
