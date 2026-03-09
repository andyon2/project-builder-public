---
name: skill-or-agent
description: Schnelle Entscheidungshilfe ob eine bestimmte Aufgabe als Skill oder Agent umgesetzt werden sollte. Aufrufen mit einer Aufgabenbeschreibung.
argument-hint: "[aufgabenbeschreibung]"
---

Entscheide ob die folgende Aufgabe ein Skill oder ein Agent werden sollte:

**Aufgabe:** $ARGUMENTS

## Pruefschema

Beantworte diese drei Fragen:

1. **Wiederholbarer Workflow?** Gleiche Schritte, variables Input, vorhersagbarer Output?
   - Ja = Skill-Kandidat

2. **Eigene Denkweise noetig?** Urteile faellen, breiten Kontext verknuepfen, Perspektive einnehmen?
   - Ja = Agent-Kandidat

3. **User-Dialog noetig?** Explorativer Dialog, >5 Interaktionen, unvorhersehbare Tiefe?
   - Ja = Agent mit Direkt-Modus

## Ergebnis

Antworte in exakt diesem Format:

**Empfehlung:** [Skill / Agent / Agent+Direkt]
**Skill-Typ:** [Encoded Preference / Capability Uplift / n.a.] (nur bei Skill)
**Kontext:** [inline / fork / n.a.] (nur bei Skill)
**Modell:** [haiku / sonnet]
**Begruendung:** [2-3 Saetze, warum diese Entscheidung]
**Skizze:** [5-Zeilen-Entwurf des Skill-Bodies oder Agent-"Wer du bist"-Blocks]
