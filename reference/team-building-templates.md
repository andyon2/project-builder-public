# Team-Building: Templates, Prozeduren und Checklisten

Dieses Dokument wird von Team-Building-Skills on demand geladen. Es ist bewusst NICHT im System Prompt -- nur laden wenn du ein Team entwirfst, auditierst oder migrierst.

---

## Dateiformat-Spezifikation

### CLAUDE.md (Projektroot)
```markdown
# [Projektname]

## Ziel
[Klares, messbares Ziel mit Zeitrahmen und Constraints]

## Ich ([Name])
[Relevanter Hintergrund, Skills, aktuelle Situation -- nur was fuer den Kontext wichtig ist]

## Kommunikation
[Formatierungsregeln -- gelten fuer alle Agents gleichermassen:]
[Umlaut-Regel -- abhaengig vom Projekttyp:
- Deutschsprachige Endnutzer-Projekte: "Umlaute: ä, ö, ü verwenden, NICHT ae, oe, ue."
- Technische Projekte: "Umlaute: ae, oe, ue statt ä, ö, ü (Encoding-Sicherheit)."
- Mischprojekte: "ae/oe/ue in technischen Dateien. ä/ö/ü in Endnutzer-Dokumentation."]
[Ton, Sprache, Stil → gehoert in den System Prompt (Identitaet), nicht hier]

## Projektstruktur
[Dateipfade und was darin liegt -- als Referenz fuer alle Agents]

Zentrale Dateien:
- `project-status.md` -- Projektstatus (bei Sessionstart gelesen, bei Sessionende aktualisiert)
- `briefings/` -- Briefing-Dokumente fuer direkte Agent-Sessions

## Agenten

| Agent | Aufgabe | Modell | Modus |
|-------|---------|--------|-------|
| [name] | [Beschreibung] | sonnet | delegiert |
| [name] | [Beschreibung] | sonnet | delegiert + direkt |

## Skills

| Skill | Aufgabe | Kontext |
|-------|---------|---------|
| /[name] | [Beschreibung] | fork |
| /[name] | [Beschreibung] | inline |

## Custom Tools

Eigene CLI-Tools: siehe `~/.config/claude-tools/registry.md`. CLI-Tools immer bevorzugen vor MCP-Servern oder direkten API-Aufrufen. Bei Unklarheit: `<tool> --help`.

## Regeln
[Uebergreifende Regeln, die fuer alle Agents gelten. Mindestens diese Standard-Regeln:]
- **Rueckwaerts-Suche bei Umbau:** Vor dem ersten Edit bei strukturellen Aenderungen: `grep -r` nach allen Konsumenten des Geaenderten. Erst dann editieren. Strukturell = Entfernen, Umbenennen, Output-Format aendern, Verantwortlichkeit zwischen Komponenten verschieben. Nicht strukturell = Hinzufuegen, Erweitern, neue Datei anlegen.
```

**Laenge:** Ziel <100 Zeilen. Keine Templates, keine Prozeduren, keine historischen Entscheidungen. Nur Fakten und Struktur.

### System Prompt fuer Main-Agent (z.B. `main-agent.md`)

**Design-Prinzip: Kurz halten.** System Prompts werden in langen Konversationen "verduennt" -- je laenger, desto mehr vergisst der Agent. Nur Identitaet, Strategie und Delegationslogik. Alles Prozedurale gehoert in Skills (die bei jedem Aufruf frisch geladen werden).

```markdown
Du bist [Rolle] -- [Beziehung zum Nutzer und Zweck].

## Deine Rolle
[2-3 Saetze: Was du bist und was du NICHT bist]

## Wie du dich verhaeltst

### Strategisch mitdenken
[Wann und wie challengst du den Nutzer?]

### Konsistenz sichern
[Worauf achtest du uebergreifend?]

### Orchestrieren
[Delegationslogik: Skill → Agent → Eigenarbeit. Wie pruefst du Output?]

### Kontext schuetzen
- Skills vor Agents, Delegation vor Eigenarbeit
- Zwischenergebnisse in Dateien, nicht im Chat
- Direkte Sessions bei explorativen Dialogen (>5 Interaktionen)
- Knowledge/Referenz NICHT bei Sessionstart laden
- Wenn der User eine Aufgabe bringt die nicht vom bisherigen Session-Kontext profitiert: Neue Session vorschlagen. Eine frische Session mit vollem Kontextfenster ist oft besser als eine ueberfuellte.

## Deine Skills
[Bei kleinen Teams (3-5 Skills): Tabelle Name | Wann nutzen.
Bei grossen Teams (10+): Weglassen -- Progressive Disclosure ueber YAML-Descriptions uebernimmt das Routing. Die Skill-Tabelle in CLAUDE.md reicht.]

### Selbst-Erweiterung
Frage: "Dafuer gibt es noch keinen Skill/Agent. Soll ich einen erstellen?"
Wenn ja: Rufe /draft-extension auf. Pruefe den Entwurf, dann setze ihn selbst um.

## Sessionstart
1. Lies `project-status.md`
2. [Projektspezifisch]
3. Brief den User

## Sessionende
1. Zwischenergebnisse in Dateien
2. Rufe `/commit` auf

## Was du NICHT bist
[Explizite Abgrenzung]
```

**Laenge:** Ziel <120 Zeilen. Referenzmaterial (Templates, Checklisten) gehoert in On-Demand-Dateien.

### Sub-Agent-Dateien (in `.claude/agents/`)

#### Modellwahl pro Agent

| Modell | Wann einsetzen | Typische Rollen |
|--------|---------------|-----------------|
| `opus` | Main-Agent (via CLI-Flag). Fuer Sub-Agents nur in begruendeten Ausnahmen. |
| `sonnet` | Inhaltliche Arbeit, Texterstellung, Code, Recherche, Analyse |
| `haiku` | Einfache, mechanische Aufgaben, Statusabfragen, Daten-Fetching |

**Pflicht:** Jeder Agent und jeder Fork-Skill MUSS ein explizites `model`-Feld haben. Ohne model-Feld erbt der Sub-Agent das Modell des Main-Agents.

#### Standard-Sub-Agent (nur delegiert)
```markdown
---
name: [agent-name]
description: [Wann dieser Agent eingesetzt wird -- klar und spezifisch]
model: [sonnet / haiku -- Pflichtfeld]
tools: [Nur die Tools, die dieser Agent braucht]
maxTurns: [Pflichtfeld. 15-25 fuer normale Tasks.]
---

Du bist der [Rolle] im [Projektname].

## Wer du bist
[Denkweise, Perspektive, Expertise -- nicht nur Aufgaben, sondern Urteilsvermoegen.
"Du denkst wie ein erfahrener [Analogie], der..."]

## Kontext
[Welche Dateien zuerst lesen]

## [Hauptaufgaben-Sektion]
[Spezifische Arbeitsanweisungen, Formate, Prozesse]

## Strategische Eskalation
[Welche uebergeordneten Erkenntnisse zurueckmelden? Konkrete Trigger.]

## Wissensquellen
[Falls Fachwissen noetig: Welche Quellen, wann recherchieren, wie festhalten?]

## Selbstcheck vor Abgabe
[3-5 Prueffragen. Mindestens eine gegen Gesamtstrategie.]
```

#### Dialogischer Sub-Agent (delegiert + direkt)
```markdown
---
name: [agent-name]
description: [Wann dieser Agent eingesetzt wird]
model: [sonnet / haiku -- Pflichtfeld]
tools: [Nur die Tools, die dieser Agent braucht]
maxTurns: [Pflichtfeld. 20-30 fuer dialogische Tasks.]
---

Du bist der [Rolle] im [Projektname].

## Wer du bist
[Denkweise, Perspektive, Expertise -- Urteilsvermoegen, nicht nur Aufgaben.]

## Kontext
[Welche Dateien zuerst lesen]

## Interaktionsmodi

### Delegiert (One-Shot)
- Klar definierten Auftrag abarbeiten, Ergebnis zurueck

### Direkt (Interaktive Session)
- Briefing unter `briefings/[dein-name]-*.md` lesen (falls vorhanden)
- Dialog fuehren, Ergebnisse in Projektdateien schreiben
- Am Ende zusammenfassen: Was erarbeitet, was offen

## [Hauptaufgaben-Sektion]
[Arbeitsanweisungen. Fuer Direkt-Modus: Gespraechsfuehrung, Fragetechniken.]

## Strategische Eskalation
[Im Direkt-Modus: Erkenntnisse in `briefings/[dein-name]-insights.md`]

## Selbstcheck vor Abgabe
[3-5 Prueffragen. Im Direkt-Modus zusaetzlich:
- Alle Ergebnisse in Projektdateien?
- Strategische Erkenntnisse fuer Main-Agent?
- Offene Punkte dokumentiert?]
```

### Starter-Scripts (in `scripts/`)

#### Git-Sync-Check (Pflichtblock)

Jedes Starter-Script enthaelt vor dem `exec claude`-Aufruf:
```bash
# Git-Remote-Check: Warnung wenn Remote neuere Commits hat
if git rev-parse --git-dir &>/dev/null; then
    git fetch origin --quiet 2>/dev/null || true
    LOCAL=$(git rev-parse HEAD 2>/dev/null || true)
    REMOTE=$(git rev-parse origin/main 2>/dev/null || true)
    if [[ -n "$LOCAL" && -n "$REMOTE" && "$LOCAL" != "$REMOTE" ]]; then
        BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
        if [[ "$BEHIND" -gt 0 ]]; then
            echo ""
            echo "⚠  Remote hat $BEHIND neuere Commits. Willst du pullen? (j/n)"
            read -r ANSWER
            if [[ "$ANSWER" == "j" ]]; then
                git pull --ff-only origin main || echo "Pull fehlgeschlagen -- bitte manuell loesen."
            fi
            echo ""
        fi
    fi
fi
```

#### Main-Agent-Starter
```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# [Git-Sync-Check hier einfuegen]

PROMPT_FILE="$PROJECT_ROOT/[main-agent].md"
STARTER_PROMPT="Sessionstart: Lies project-status.md, [weitere Dateien], dann brief mich wo wir stehen. Reminder: Sessionende → Rufe /commit auf."

# --get-prompt: Nur den Starter-Prompt ausgeben (fuer externe Apps)
# --remote: Claude ohne Starter-Prompt starten (fuer Remote Control Flow)
if [[ "${1:-}" == "--get-prompt" ]]; then
  echo "$STARTER_PROMPT"
  exit 0
elif [[ "${1:-}" == "--remote" ]]; then
  exec claude --system-prompt-file "$PROMPT_FILE"
else
  exec claude --system-prompt-file "$PROMPT_FILE" "$STARTER_PROMPT"
fi
```

- Scripts liegen immer im Repo (`scripts/`), nie ausserhalb
- Globale Shortcuts via Symlink in `~/.local/bin/`
- Start-Prompt endet mit Commit+Push-Reminder
- `--remote` und `--get-prompt` Flags sind Pflicht (fuer Claude Launcher / Remote Control)

#### Sub-Agent-Starter (fuer dialogische Agents)

Sub-Agent-Scripts brauchen keinen Git-Check (Main-Agent-Start hat ihn bereits durchgefuehrt).
```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
AGENT_FILE="$PROJECT_ROOT/.claude/agents/[agent-name].md"

if [[ ! -f "$AGENT_FILE" ]]; then
    echo "Fehler: Agent-Datei nicht gefunden: $AGENT_FILE"
    exit 1
fi

BRIEFING_DIR="$PROJECT_ROOT/briefings"
if [[ -f "$BRIEFING_DIR/[agent-name]-"*.md ]]; then
    DYNAMIC_PROMPT="Lies Briefing: briefings/[agent-name]-*.md. Arbeite mit dem User. Reminder: Sessionende → /commit aufrufen."
else
    DYNAMIC_PROMPT="Kein Briefing. Frage den User. Lies CLAUDE.md. Reminder: Sessionende → /commit aufrufen."
fi

exec claude --append-system-prompt "$(cat "$AGENT_FILE")" "$DYNAMIC_PROMPT"
```

### Skills (in `.claude/skills/[name]/SKILL.md`)

**Token-Oekonomie:**
- **Inline-Skills:** Im Main-Agent-Kontext. Nur fuer winzige Tasks (<3 Turns).
- **Fork-Skills:** Eigener Kontext, eigenes Modell. Fast immer guenstiger als Agents. Im Zweifel: `context: fork` mit `model: haiku`.

#### Einfacher Skill
```markdown
---
name: [skill-name]
description: [Wann getriggert -- klar fuer natuerlichsprachliche Erkennung]
argument-hint: [Optional: "[firma]" oder "[thema]"]
allowed-tools: [Optional: "Read, Grep, Bash"]
---

[Anweisungen. $ARGUMENTS als Platzhalter fuer Argumente.]
```

#### Fork-Skill
```markdown
---
name: [skill-name]
description: [Wann getriggert]
context: fork
model: [haiku / sonnet -- Pflichtfeld!]
---

[Anweisungen fuer isolierten Subagent. Kann:
- Mehrere Dateien lesen/analysieren
- Hilfsskripte aufrufen
- Reports in Projektdateien schreiben
- Parallele Agenten spawnen]
```

#### Interview-Skill (strukturierter Kurz-Dialog)
```markdown
---
name: [skill-name]
description: [Wann getriggert]
---

[Strukturierter Dialog mit 3-5 Fragen und definiertem Output-Format.]
```

#### Pflicht-Skill: `/commit`

Jedes Team bekommt `/commit` (Inline). Atomisches Sessionende: /track + commit + push.
```markdown
---
name: commit
description: "Session-Commit: /track ausfuehren, dann committen und pushen. Standard fuer Sessionende."
---

Fuehre einen Session-Commit durch:

1. Rufe `/track` auf -- aktualisiert project-status.md mit dem Session-Fortschritt.
2. `git add -u` -- alle getrackten Aenderungen stagen.
3. `git diff --cached --stat` -- Ueberblick zeigen.
4. Commit-Message aus den Aenderungen ableiten (kurz, deutsch, beschreibend).
5. `git commit` mit der Message.
6. Pruefe ob ein Remote existiert (`git remote`). Wenn ja: `git push`. Wenn nein: "Kein Remote konfiguriert, nur lokal committed." melden.

Wenn nichts zu committen ist (keine staged changes nach Schritt 2), melde das und ueberspringe Schritt 3-6.
```

#### Pflicht-Skill: `/reflect`

Jedes Team bekommt `/reflect` (Fork, Sonnet). Output: `.claude/team-reflection.md`.
```markdown
---
name: reflect
description: Ehrliche Selbstanalyse des Agent-Teams
allowed-tools: "Read, Glob, Grep, Write"
context: fork
model: sonnet
---

Analysiere das eigene Team schonungslos ehrlich.
1. Lies: CLAUDE.md, alle Agents, alle Skills, System-Prompt, project-status.md
2. Analysiere: Rollen-Klarheit, Ueberschneidungen, Nutzungshaeufigkeit
3. Prinzip-Konsistenz: Extrahiere Prinzipien aus System Prompt, pruefe ob jede Taetigkeit einen Skill hat, suche nach Luecken (was sollte da sein, ist aber nicht)
4. Identifiziere: Schwachstellen, fehlende Skills, Ineffizienzen
5. Schreibe nach `.claude/team-reflection.md`
```

#### Agent-zu-Skill-Konvertierung

Wenn ein Agent eigentlich ein Skill sein sollte:
1. Hat er eine echte Denkweise oder nur Aufgaben?
2. Trifft er eigenstaendige Urteile oder folgt er einem Workflow?
3. Wenn beides Nein → Konvertiere: Body kuerzen, Workflow-fokussiert, fork/haiku, "Wer du bist" und Eskalation entfallen.

### Hooks und Permissions

Permissions werden **global** gehandhabt -- nicht pro Projekt.

**Globaler Safety-Hook** (`~/.claude/hooks/safety-hook.sh`):
- **deny:** `git push --force`, `rm -rf`, `git reset --hard`, `git clean -f`, `git checkout -- .`, `git restore .`
- **ask:** `.env`-Zugriff, Commits in fremden Repos
- **allow:** alles andere

Registriert in `~/.claude/settings.json` (global). Gilt fuer alle Projekte auf allen Maschinen.

**Lokale `.claude/settings.json`:** Nur fuer projektspezifische Hooks (z.B. SessionStart-Hooks, Compaction-Reminder). Keine Permissions -- die deckt der globale Hook ab.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-compaction-reminder.sh"}]
      }
    ]
  }
}
```

Neue Teams bekommen **keine** lokale `settings.json`, ausser sie brauchen projektspezifische Hooks.

### Briefings (in `briefings/`)
```markdown
# Briefing: [Agent-Name] -- [Thema]

## Erstellt von
Main-Agent, [Datum]

## Ziel dieser Session
[Was soll als Ergebnis vorliegen?]

## Kontext
[Relevanter Hintergrund]

## Leitplanken
[Grenzen, nicht verhandelbare Entscheidungen]

## Offene Fragen
[Konkrete Fragen fuer den Dialog]

## Ergebnis-Dateien
[Wohin die Ergebnisse geschrieben werden]
```

---

## Vorgehen beim Team-Entwurf

### Phasen-Uebersicht

**Phase 1 Interview → Phase 2 Research → Phase 3 Synthese → Phase 4 Build**

### Phase 1: Interview (Main-Agent)

Alle Punkte durchgehen, nichts ueberspringen:
- Was ist das konkrete Ziel?
- **Greenfield oder Maintenance?** (Bestandscode, Wartungsvertrag, fremde Codebase → Maintenance. Beeinflusst Research-Trigger in Phase 2.)
- Welche Aufgabentypen: wiederholbare Workflows (Skill) vs. eigenstaendige Denkarbeit (Agent)?
- Welche Experten braucht man? Welche sind "Denker" vs. "Ausfuehrer"?
- Wie soll der Main-Agent sich verhalten?
- Welche Dateien als Gedaechtnis?
- Welches Fachwissen brauchen die Agents?
- Welche Aufgaben erfordern laengeren Dialog?
- Wird das Produkt vermarktet? → Strategy-Check
- **Ist die Domaene bekannt oder unbekannt?** → Research-Trigger (Phase 2)
- **User-Kontext fuer das neue Team:** Wer arbeitet mit dem Team? Welcher technische Hintergrund? Welche Vorlieben bei Ton/Stil/Sprache? Was sollte das Team ueber den User wissen? (Fuettert `CLAUDE.md ## Ich` des neuen Teams.)

**Gate 1:** Strukturierte Zusammenfassung aller geklaerten Punkte zeigen. User bestaetigt oder korrigiert. Erst dann weiter.

### Phase 2: Research (optional, /research-domain)

**Trigger:** Unbekannte Domaene, fremde Codebase, neues Fachgebiet.

Der Main-Agent delegiert an `/research-domain` mit:
- Domaene und Ziel
- Konkrete Fragen aus Phase 1
- Was bereits bekannt ist (vermeidet Doppelarbeit)

Ergebnis: Zwei Dateien unter `briefings/`:
- `research-[domaene].md` -- Briefing fuer die Synthese
- `domain-knowledge-[domaene].md` -- Geht spaeter ins neue Team

### Phase 3: Synthese (Main-Agent)

Der Main-Agent verschmilzt drei Wissensquellen:
1. **Domaenenwissen** aus dem Research-Briefing (Phase 2)
2. **Architektur-Wissen** aus eigener `knowledge/` (Skill-First, Token-Optimierung, etc.)
3. **User-Anforderungen** aus dem Interview (Phase 1)

Dabei:

**Zuerst Skills identifizieren:**
- Jede Aufgabe durchgehen: Kann das ein Skill sein?
- Typ (Encoded Preference / Capability Uplift) und Kontext (inline / fork) bestimmen
- Begruenden: Warum reicht ein Skill?

**Dann Agents identifizieren:**
- Nur Rollen die nach Skill-Pruefung uebrig bleiben
- Pro Agent begruenden: Warum reicht kein Skill? Welche Denkweise?
- Modell zuweisen (sonnet / haiku), Modus (delegiert / delegiert + direkt)

**Content-Check:** Endnutzer-Texte → Anti-GPTism-Regeln aus `knowledge/content-humanization.md`

**Strategy-Check:**
- Produkt wird vermarktet? → Wer hat Strategie-Hoheit?
- Main-Agent IST Stratege / Separater Strategy-Agent / Kein Strategie-Bedarf

**Architektur-Check:**
- Skill-zu-Agent-Verhaeltnis: mindestens 1:1, idealerweise 1.5:1+
- Token-Impact schaetzen

**Context-Burden-Check:**
- Immer-geladene Dateien (CLAUDE.md + System Prompt + project-status.md) <400 Zeilen
- Keine Templates/Prozeduren in immer-geladenen Dateien

**Gate 2:** Architektur-Entwurf zeigen (Agents, Skills, Knowledge-Stufe, Begruendungen). User bestaetigt oder korrigiert. Erst dann weiter.

### Phase 4: Build (/build-team)

Der Main-Agent delegiert an `/build-team` mit strukturiertem Brief:
- Alle Ergebnisse aus Interview + Synthese
- Falls Research: Domain-Knowledge-Dateien angeben

/build-team erstellt:
- `CLAUDE.md` (mit Agent-Tabelle, Skill-Tabelle, Umlaut-Regel)
- `[main-agent].md` (System Prompt, <120 Zeilen)
- `.claude/agents/[name].md` (mit model, maxTurns)
- `.claude/skills/[name]/SKILL.md` (mit model bei fork)
- `.claude/skills/reflect/SKILL.md` (Pflicht)
- `scripts/[main-agent]` (chmod +x, Git-Sync-Check, Commit-Reminder)
- `scripts/[agent-name]` (fuer dialogische Agents)
- `project-status.md` (initial)
- `briefings/` (mit .gitkeep)
- `config/` (optional, mit .gitkeep) -- Instanz-spezifische Integrationen (Server-Zugang, API-Configs). In .gitignore, On-Demand gelesen. Referenz in CLAUDE.md.
- `.gitignore`
- `.claude/settings.json` nur wenn projektspezifische Hooks noetig (keine Permissions -- globaler Hook deckt das ab)

**Git-Repository:**
1. `git init`
2. `.gitignore` pruefen (keine Secrets)
3. Initial Commit
4. `gh repo create --private --source . --remote origin --push`

**Remote-Server-Deployment** (optional):
Falls ein Remote-Server konfiguriert ist, Repo dort klonen und Shortcut einrichten. Falls kein SSH-Zugang: Dem User die Befehle ausgeben.

**Startanleitung:**
- Main-Agent starten: `scripts/[name]`
- Skills: `/skill-name`
- Session beenden: Agent aktualisiert Status, fragt nach Commit+Push
- Direkte Sessions: Main-Agent sagt wann, `scripts/[agent-name]` starten

---

## Qualitaetsprinzipien (Checkliste)

- Jeder Agent braucht eine Denkweise, nicht nur Aufgaben
- Eskalation ist Pflicht: Sub-Agents melden strategisch relevante Erkenntnisse
- Selbstcheck verhindert Drift: Output gegen Gesamtstrategie pruefen
- "Was du NICHT bist" ist wichtig: Ohne Abgrenzung → generisches Assistenten-Verhalten
- Dateien sind das Gedaechtnis: Was nur im Chat steht ist nach der Session weg
- Fachwissen definieren: Wo holt der Agent es her, wie haelt er es fest?
- Direkt-Modus ist Eskalationsstufe, nicht Default
- Reviewer-Schleife darf nicht brechen: Kein Output ohne Review
- maxTurns ist Pflicht: Sicherheitsnetz gegen Endlos-Schleifen
- Content-Agents brauchen Anti-GPTism-Regeln aus `knowledge/content-humanization.md`
- Git ist Infrastruktur: Private Repo, .gitignore, Starter-Scripts mit Git-Sync-Check
- Umlaut-Regel ist Pflicht in CLAUDE.md
- `/commit` ist Pflicht in jedem Team (atomisches Sessionende, graceful ohne Remote)
- `/reflect` ist Pflicht in jedem Team
- **Rueckwaerts-Suche bei Umbau ist Pflicht in jeder CLAUDE.md:** Standard-Regel fuer alle Teams (siehe CLAUDE.md-Template)
- **Immer-geladene Dateien schlank halten:** CLAUDE.md <100 Zeilen, System Prompt <200 Zeilen, project-status.md <50 Zeilen. Referenzmaterial in On-Demand-Dateien.
- **Keine lokalen Permissions:** Globaler Safety-Hook regelt deny/ask/allow. Lokale settings.json nur fuer projektspezifische Hooks.
