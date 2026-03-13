---
name: extract-team
description: Extrahiert operatives Wissen aus einem bestehenden Agent-Team indem der alte Agent sich selbst beschreibt.
argument-hint: "[team-pfad]"
allowed-tools: "Bash, Read, Glob, Grep, Write"
context: fork
model: sonnet
---

Du extrahierst operatives Wissen aus einem bestehenden Agent-Team. Statt die Dateien nur von aussen zu lesen, laesst du den alten Agent sich selbst beschreiben -- er kennt sein eigenes System am besten.

**Wichtig:** Du aenderst keine Dateien im Team-Repo. Du schreibst nur das Extraktions-Dokument ins PB-Repo.

## Input

`$ARGUMENTS` enthaelt den Pfad zum Team-Repo (z.B. `~/claude-projects/mein-team`).

## Vorgehen

### 1. System Prompt des alten Teams finden

Suche im Team-Repo nach dem System Prompt:
- Pruefe Starter-Scripts (`scripts/*`) auf `--system-prompt-file` Referenzen
- Falls nicht gefunden: Suche nach gaengigen Namen (`main-agent.md`, `system-prompt.md`, `agent.md`) im Repo-Root
- Merke dir den Pfad fuer Schritt 2

### 2. Alten Agent befragen

Starte eine Claude-Session im alten Repo und lass den Agent sich selbst beschreiben:

```bash
cd [team-pfad] && claude -p "FRAGENKATALOG" --system-prompt-file [pfad-aus-schritt-1]
```

Falls kein System Prompt gefunden: ohne `--system-prompt-file` starten (CLAUDE.md wird trotzdem geladen).

**Fragenkatalog** (als ein zusammenhaengender Prompt senden):

```
Beantworte diese Fragen ausfuehrlich aus deinem eigenen Wissen. Du beschreibst dich selbst fuer einen Rebuild -- sei ehrlich und gruendlich.

IDENTITAET & ARCHITEKTUR:
1. Was ist dein Zweck? Fuer wen arbeitest du?
2. Welche Skills hast du und welche nutzt du tatsaechlich regelmaessig?
3. Welche Agents hast du? Wie spielen sie zusammen?
4. Welche Knowledge-Dateien hast du und welche sind die wichtigsten?
5. Welche externen Integrationen gibt es (APIs, Server, Tools)?
6. Wie sieht eine typische Session aus?

ERFAHRUNGSWISSEN:
7. Was funktioniert richtig gut -- welche Workflows sind ausgereift?
8. Was funktioniert schlecht oder gar nicht?
9. Welche Probleme tauchen immer wieder auf?
10. Was muss der User regelmaessig manuell korrigieren?
11. Welche Architektur-Entscheidungen haben sich bewaehrt, welche nicht?
12. Was steht in deiner project-status.md als offene Punkte?
13. Welche Meta-Learnings hast du gesammelt?
14. Gibt es Workarounds die eigentlich anders geloest werden sollten?
15. Welche Dateien oder Configs sind fragil -- brechen leicht wenn man was aendert?
16. Gibt es ungeschriebene Regeln die in keiner Datei stehen?

USER-INTERAKTION:
17. Welche Skills ruft der User explizit auf, welche triggerst du selbst?
18. Was war das schwierigste Problem das du geloest hast?
19. In welchen Situationen braucht der User mehrere Anlaeufe bis du es richtig machst?

FUER DEN REBUILD:
20. Was wuerdest du anders machen wenn du neu gebaut wirst?
21. Was darf auf keinen Fall verloren gehen?
22. Welche User-Vorlieben sind wichtig (Kommunikationsstil, Konventionen, Workflows)?
```

### 3. Antwort mit harten Fakten ergaenzen

Lies zusaetzlich direkt aus dem Repo:
- `project-status.md` -- offene Punkte und Meta-Learnings (Gegencheck zur Selbstbeschreibung)
- Liste aller Skills: `ls .claude/skills/` (falls vorhanden)
- Liste aller Agents: `ls .claude/agents/` (falls vorhanden)

Gleiche ab: Hat der Agent in seiner Selbstbeschreibung Skills/Agents vergessen oder falsch dargestellt? Ergaenze oder korrigiere.

### 4. Extraktions-Dokument schreiben

Kombiniere Selbstbeschreibung + direkt gelesene Fakten. Schreibe nach `~/claude-projects/project-builder/briefings/team-extraction-[teamname].md`:

```markdown
# Team-Extraktion: [Teamname]

Extrahiert am: YYYY-MM-DD
Quelle: [team-pfad]
Methode: Agent-Selbstbeschreibung + Faktenabgleich

## Zweck und Ziel
[Was tut das Team? Fuer wen?]

## Aktuelle Architektur
[Skills, Agents, Knowledge -- vollstaendige Liste mit Kurzbeschreibung]

## Operatives Wissen (bewahrenswert)
[Workflows, Pipelines, Konfigurationen die im Betrieb entstanden sind]

## Was gut funktioniert
[Behalten/uebernehmen. Konkret.]

## Was nicht funktioniert oder fehlt
[Probleme, Luecken, Schwaechen]

## Erfahrungswissen und Meta-Learnings
[Was hat der Agent ueber sich selbst und die Domaene gelernt?]

## User-Vorlieben und Konventionen
[Kommunikationsstil, Workflows, ungeschriebene Regeln]

## Integrationen und Konfigurationen
[Server, APIs, Hooks, externe Abhaengigkeiten]

## Empfehlung fuer Rebuild
[Was uebernehmen, was neu machen, was weglassen]
```

### 5. Zusammenfassung

Gib dem Main-Agent zurueck:
- Die 3-5 wichtigsten Erkenntnisse
- Groesste Staerke und groesste Schwaeche des bestehenden Teams
- Verweis auf das Extraktions-Dokument
