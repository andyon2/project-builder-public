---
name: build-team
description: Erstellt alle Dateien fuer ein neues Agent-Team basierend auf einem strukturierten Brief. Wird vom Main-Agent aufgerufen NACHDEM Anforderungen dialogisch mit dem User geklaert wurden. Aufrufen mit dem Ergebnis der Anforderungsklaerung.
argument-hint: "[strukturierter brief]"
allowed-tools: "Read, Write, Bash, Glob, Grep"
context: fork
model: sonnet
---

Du erstellst ein vollstaendiges Agent-Team basierend auf einem strukturierten Brief. Der Main-Agent hat bereits Interview, Research und Synthese durchgefuehrt (Phasen 1-3) -- du fuehrst Phase 4 (Build) aus.

**Wichtig:** Du erstellst Dateien. Du triffst keine strategischen Entscheidungen -- die stehen im Brief. Wenn der Brief unklar oder unvollstaendig ist, schreibe was du hast und notiere offene Punkte im Output.

## Vorgehen

### 0. Vorbereitung

Lies `reference/team-building-templates.md` -- darin stehen alle Templates, Formate und die Qualitaets-Checkliste.

Lies den Brief ($ARGUMENTS) und extrahiere:
- Projektname und Ziel
- Geplante Agents (mit Denkweise, Modell, Modus)
- Geplante Skills (mit Typ, Kontext, Modell)
- Knowledge-Stufe (0/1/2)
- Domain-Knowledge-Dateien (falls Research stattfand, Pfade zu den Dateien)
- Content-Check: Endnutzer-Texte? → Anti-GPTism-Regeln noetig
- Strategy-Check: Wird vermarktet? → Strategie-Rolle geklaert?
- Umlaut-Regel (ae/oe/ue oder ae/oe/ue)
- Sonstige Konventionen

### 1. Architektur pruefen

Bevor du Dateien erstellst, pruefe den Brief gegen die Qualitaets-Checkliste:
- Skill-zu-Agent-Verhaeltnis: mindestens 1:1?
- Jeder Agent hat Denkweise (nicht nur Aufgaben)?
- model fuer jeden Agent und Fork-Skill? maxTurns fuer jeden Agent?
- Context-Burden: Geplante CLAUDE.md + System Prompt + project-status.md <400 Zeilen?
- /reflect als Pflicht-Skill enthalten?

Wenn etwas fehlt: Ergaenze es selbst nach Best Practice und notiere es im Output.

### 2. Dateien erstellen

Erstelle im Projektverzeichnis (falls nicht angegeben: aktuelles Verzeichnis):

**Reihenfolge:**
1. `.gitignore` (Secrets, Node-Modules, etc.)
2. `CLAUDE.md` -- nach Template, <100 Zeilen. Enthaelt: Ziel, Kommunikation (inkl. Umlaut-Regel), Projektstruktur, Agent-Tabelle, Skill-Tabelle, Regeln.
3. `[main-agent].md` -- System Prompt nach Template, <120 Zeilen. Nur Identitaet + Prinzipien + Verhalten + Skill-Tabelle + Sessionstart/ende.
4. `.claude/agents/[name].md` -- Pro Agent, nach Template. Pflichtfelder: model, maxTurns, Denkweise, Eskalation, Selbstcheck.
5. `.claude/skills/[name]/SKILL.md` -- Pro Skill, nach Template. Fork-Skills: Pflichtfeld model.
6. `.claude/skills/commit/SKILL.md` -- Pflicht. Inline. Atomisches Sessionende: /track + commit + push. Push nur wenn Remote existiert. Siehe Template in `reference/team-building-templates.md`.
7. `.claude/skills/reflect/SKILL.md` -- Pflicht. Fork, Sonnet. Inkl. Prinzip-Konsistenz-Sektion.
8. `scripts/[main-agent]` -- Starter-Script mit Git-Sync-Check und Sessionstart-Prompt. `chmod +x`.
9. `scripts/[agent-name]` -- Fuer jeden dialogischen Agent. `chmod +x`.
10. `project-status.md` -- Initial: Ziel + erste offene Aufgaben.
11. `briefings/.gitkeep`

**Domain-Knowledge:** Wenn der Brief Domain-Knowledge-Dateien referenziert (aus Phase 2 Research):
- Kopiere die Dateien ins neue Team unter `knowledge/`
- Knowledge-Stufe wird automatisch mindestens Stufe 1 (falls im Brief niedriger angegeben)
- Erstelle `knowledge/index.md` mit Verweis auf die Domain-Knowledge-Datei(en)

**Content-Agents:** Wenn der Brief Content-Generierung erwaehnt, lies `knowledge/content-humanization.md` und integriere Anti-GPTism-Regeln in die relevanten Agent-Prompts.

**Knowledge-System:** Je nach Stufe:
- Stufe 0: Nichts
- Stufe 1: `knowledge/` + `knowledge/index.md` + `/learn`-Skill (Fork, Sonnet)
- Stufe 2: Wie Stufe 1 + `sources/inbox/` + `sources/archive/` + `sources/log.md` + Notion-Integration in /learn

### 3. Git-Repository

```bash
git init
git add -A
git commit -m "Initial commit: [Projektname] Agent-Team"
gh repo create [projektname] --private --source . --remote origin --push
```

Wenn `gh` nicht verfuegbar oder Fehler: Notiere im Output, User soll manuell erstellen.

### 4. Output

Gib dem Main-Agent eine **Onboarding-Summary** zurueck -- strukturiert, copy-paste-faehig fuer den User:

```markdown
## Dein neues Team: [Projektname]

### Quick Start
[starter-command]           # Session starten
[starter-command] --remote  # Remote-Modus (Claude Launcher)

# Symlink einrichten (einmalig):
ln -sf ~/[projekt]/scripts/[starter] ~/.local/bin/[starter]

### Skills
| Befehl | Was es tut |
|--------|------------|
| `/skill-1` | [Wann und wofuer] |
| `/commit` | Session beenden (Status speichern + commit + push) |

### Agents
| Agent | Aufgabe | Modus |
|-------|---------|-------|
| [name] | [Was er tut] | delegiert / `scripts/[name]` fuer direkte Sessions |

### Session-Workflow
1. `[starter-command]` -- Agent liest Status und briefed dich
2. Arbeiten -- Agent delegiert an Skills und Sub-Agents
3. `/commit` -- speichert Status, committed, pusht
```

Darunter (technisch, fuer den Main-Agent):
- Erstellte Dateien mit Zeilenanzahl
- Abweichungen vom Brief (was ergaenzt/angepasst wurde)
- Offene Punkte (was im Brief unklar war)

## Qualitaets-Selbstcheck

Bevor du das Ergebnis zurueckgibst:
- [ ] Jeder Agent hat model + maxTurns?
- [ ] Jeder Fork-Skill hat model?
- [ ] CLAUDE.md <100 Zeilen?
- [ ] System Prompt <120 Zeilen?
- [ ] /commit existiert (Inline, Pflicht-Skill)?
- [ ] /reflect existiert mit Prinzip-Konsistenz-Sektion?
- [ ] Starter-Scripts sind executable?
- [ ] Umlaut-Regel in CLAUDE.md?
- [ ] Kein Referenzmaterial in immer-geladenen Dateien?
- [ ] .gitignore schliesst Secrets aus?
- [ ] Rueckwaerts-Suche-Regel in CLAUDE.md `## Regeln`?
