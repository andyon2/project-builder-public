---
name: apply-safe-fixes
description: Fuegt fehlende model- und maxTurns-Felder in Agent- und Skill-Dateien eines bestehenden Projekts ein. Zeigt jeden Fix als Diff und wartet auf Bestaetigung bevor etwas geaendert wird. Aufrufen mit dem Pfad zum Projektverzeichnis.
argument-hint: "[projekt-pfad]"
allowed-tools: "Read, Glob, Grep, Edit"
context: fork
model: sonnet
---

Du fuegst fehlende Pflichtfelder in Agent- und Skill-Dateien ein. NUR `model` und `maxTurns` -- nichts anderes.

# REGELN

1. Du aenderst NUR YAML-Header-Felder. Nie den Body/Inhalt eines Agents oder Skills.
2. Du fuegst NUR fehlende Felder hinzu. Du aenderst KEINE bestehenden Werte.
3. Du zeigst JEDEN Fix als Diff BEVOR du ihn ausfuehrst.
4. Du wartest auf explizites OK des Users BEVOR du irgendetwas aenderst.
5. Du machst EINE Datei nach der anderen -- nicht alles auf einmal.
6. Wenn der User "stopp" oder "nein" sagt, hoerst du sofort auf.

## Vorgehen

### 1. Inventar erstellen

Lies im Projektverzeichnis `$ARGUMENTS`:
- Alle Dateien unter `.claude/agents/`
- Alle Dateien unter `.claude/skills/`

Fuer jede Datei: Pruefe den YAML-Header auf:
- `model`-Feld vorhanden? Wenn ja: welcher Wert?
- `maxTurns`-Feld vorhanden? (nur bei Agents relevant)
- Bei Skills: Hat er `context: fork`? Wenn ja, ist `model` besonders kritisch.

### 2. Fix-Plan erstellen

Erstelle eine Uebersicht aller fehlenden Felder:

```
## Fix-Plan

| Datei | Fehlt | Vorgeschlagener Wert | Begruendung |
|-------|-------|---------------------|-------------|
| .claude/agents/x.md | model | sonnet | [Begruendung basierend auf Aufgabe] |
| .claude/agents/x.md | maxTurns | 20 | Standard fuer normale Tasks |
| .claude/agents/y.md | model | haiku | Liest nur Dateien, formatiert |
| .claude/skills/z/SKILL.md | model | haiku | Fork-Skill, nur Zusammenfassung |
```

**Modell-Empfehlung ableiten:**
- Lies den Agent/Skill-Body und verstehe, was er tut
- Kreative/analytische Arbeit --> sonnet
- Lesen/Formatieren/Zusammenfassen --> haiku
- Im Zweifel: sonnet (sicherer als haiku, guenstiger als opus)

**maxTurns-Empfehlung:**
- Normaler delegierter Agent: 20
- Dialogischer Agent: 25
- Komplexer Agent mit viel Recherche: 25
- Einfacher Agent: 15

Zeige dem User den vollstaendigen Fix-Plan und frage: "Soll ich diese Fixes einzeln durchgehen und anwenden? Du kannst jeden einzelnen ablehnen oder den Wert aendern."

### 3. Fixes einzeln anwenden

Fuer JEDEN Fix im Plan:

1. Zeige den konkreten Diff:
```
Datei: .claude/agents/[name].md
Aenderung: model-Feld einfuegen

Vorher:
---
name: [name]
description: [...]
tools: [...]
---

Nachher:
---
name: [name]
description: [...]
model: sonnet
tools: [...]
---
```

2. Frage: "OK? (ja / nein / anderer Wert)"

3. Nur bei explizitem "ja" oder "ok": Fuehre den Fix mit dem Edit-Tool aus.
   - Fuege das Feld im YAML-Header ein (nach `description`, vor `tools`)
   - Aendere NUR den Header, nie den Body

4. Bestaetigung: "Erledigt: model: sonnet in [datei] eingefuegt."

5. Weiter zum naechsten Fix.

### 4. Zusammenfassung

Am Ende:
```
## Safe Fixes abgeschlossen

Angewendet: [N] von [M] Fixes
Uebersprungen: [N] (vom User abgelehnt)

Geaenderte Dateien:
- [Liste]

Nicht geaenderte Dateien:
- [Liste mit Grund: "vom User abgelehnt" / "keine Fixes noetig"]
```
