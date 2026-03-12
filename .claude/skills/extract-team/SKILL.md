---
name: extract-team
description: Extrahiert operatives Wissen aus einem bestehenden Agent-Team fuer einen Rebuild. Liest alle Team-Dateien inkl. System Prompt und liefert ein verdichtetes Extraktions-Dokument.
argument-hint: "[team-pfad]"
allowed-tools: "Read, Glob, Grep, Write"
context: fork
model: sonnet
---

Du extrahierst operatives Wissen aus einem bestehenden Agent-Team. Das Ergebnis dient als Input fuer einen Team-Rebuild mit dem 4-Phasen-Flow.

**Wichtig:** Du bist read-only gegenueber dem alten Team. Du aenderst keine Dateien im Team-Repo. Du schreibst nur das Extraktions-Dokument.

## Input

`$ARGUMENTS` enthaelt den Pfad zum Team-Repo (z.B. `~/claude-projects/mein-team`).

## Vorgehen

### 1. Team vollstaendig lesen

Lies in dieser Reihenfolge:

1. `CLAUDE.md` -- Projektkontext, Ziel, Struktur
2. `[main-agent].md` (System Prompt) -- **Kritisch:** Gibt dir das Verstaendnis wie die Teile zusammenspielen
3. `project-status.md` -- Operative Erkenntnisse, offene Punkte, Meta-Learnings
4. `.claude/agents/*.md` -- Alle Sub-Agents (Denkweisen, Workflows)
5. `.claude/skills/*/SKILL.md` -- Alle Skills (Prozeduren, Workflows)
6. `knowledge/*` -- Gesamtes Fachwissen
7. `briefings/*` -- Falls vorhanden: Erfahrungen aus direkten Sessions
8. `dispatches/` -- Falls vorhanden: Was wurde von aussen reingetragen

### 2. Analysieren

Mit dem Wissen aus dem System Prompt als Kontext, bewerte:

**Was funktioniert gut?**
- Welche Workflows/Pipelines sind ausgereift?
- Welche Skills werden offensichtlich aktiv genutzt (Detailgrad, Reife)?
- Welche Architektur-Entscheidungen haben sich bewaehrt?

**Was funktioniert nicht / fehlt?**
- Welche Agents/Skills wirken unreif oder ungenutzt?
- Welche Luecken gibt es (z.B. fehlendes Domaenenwissen, fehlende Skills)?
- Wo weicht die Architektur von Best Practices ab?

**Operatives Wissen:**
- Welche konkreten Erkenntnisse stehen in project-status.md?
- Welches Fachwissen steckt in knowledge/?
- Welche Konfigurationen/Integrationen existieren?

### 3. Extraktions-Dokument schreiben

Schreibe nach `briefings/team-extraction-[teamname].md` (im PB-Repo, nicht im Team-Repo):

```markdown
# Team-Extraktion: [Teamname]

Extrahiert am: YYYY-MM-DD
Quelle: [team-pfad]

## Zweck und Ziel
[Was tut das Team? Fuer wen?]

## Aktuelle Architektur
[Agents, Skills, Knowledge -- Kurzuebersicht]

## Operatives Wissen (bewahrenswert)
[Workflows, Pipelines, Konfigurationen die im Betrieb entstanden sind]
[Konkrete Erkenntnisse aus realen Tests -- aus project-status.md und Knowledge]

## Bestehendes Fachwissen
[Zusammenfassung der knowledge/-Dateien -- verdichtet, nicht kopiert]

## Was gut funktioniert
[Behalten/uebernehmen ins neue Team. Konkrete Dateien/Passagen referenzieren.]

## Was nicht funktioniert oder fehlt
[Verbesserungspotential, Luecken, Architektur-Schwaechen]

## Integrationen und Konfigurationen
[Server-Anbindungen, Hooks, externe Abhaengigkeiten]

## Empfehlung fuer Rebuild
[Was uebernehmen, was neu machen, was weglassen]
```

### 4. Zusammenfassung

Gib dem Main-Agent zurueck:
- Anzahl gelesener Dateien
- Die 3-5 wichtigsten Erkenntnisse
- Groesste Staerke und groesste Schwaeche des bestehenden Teams
- Verweis auf das Extraktions-Dokument
