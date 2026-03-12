# Session-State-Management

## Das Problem

Ohne klare Konvention entstehen verschiedene Ansaetze:
- `status.md` + `todo.md` + `buildlog.md` (drei Dateien, laufen auseinander)
- `memory/` (Claudes Auto-Memory, anderer Zweck)
- Gar keine Statusdatei (Wissen geht zwischen Sessions verloren)

Mehrere Dateien kosten bei jedem Sessionstart unnoetig Tokens und geraten aus dem Sync.

## Die Konvention: Eine `project-status.md`

Jedes Projekt hat genau EINE zentrale Statusdatei im Root:

```markdown
# Projektstatus

## Aktueller Stand
[2-3 Saetze: Wo stehen wir? Was wurde zuletzt gemacht?]

## Offene Aufgaben
- [ ] [Aufgabe 1]
- [ ] [Aufgabe 2]
- [x] [Erledigte Aufgabe -- bleibt kurz als Kontext]

## Entscheidungen
- [YYYY-MM-DD]: [Entscheidung + kurze Begruendung]

## Naechste Session
[Was sollte als erstes passieren? Gibt es Blocker?]
```

## Regeln

1. **Main-Agent liest** die Datei bei jedem Sessionstart als Erstes
2. **Main-Agent aktualisiert** sie bei jedem Sessionende
3. **Sub-Agents lesen** sie fuer Kontext, aber nur der Main-Agent schreibt
4. **Erledigte Aufgaben** werden nach 2-3 Sessions entfernt (Datei waechst nicht)
5. **Max ~50 Zeilen** -- Details gehoeren in Projektdateien, nicht in den Status
6. **Keine Duplikation** -- was in Projektdateien steht, wird im Status nur referenziert

## `/track` als Standard-Skill fuer Statusverwaltung

[Aktualisiert: 2026-03-09]

Die `project-status.md` bleibt die Single Source of Truth. Der Zugriff laeuft ueber einen `/track`-Skill -- **inline** (nicht Fork), weil der Skill den Session-Kontext braucht.

**Ein Befehl, keine Argumente:**
- `/track` -- aktualisiert project-status.md mit dem, was in der Session passiert ist
- Kein separater "Status-Report"-Modus. Fuer "wo stehen wir?" am Sessionstart liest der Main-Agent `project-status.md` direkt.

**Warum inline statt Fork:**
Der Skill muss wissen, was in der Session erarbeitet wurde. Ein Fork (eigener Kontext) hat diese Info nicht und muesste den User fragen -- das ist schlechte UX. Inline laeuft im Main-Agent-Kontext und hat die volle Session-Geschichte.

**Konsequenz fuer den Masterprompt:**
- Sessionstart-Regel bleibt: "Lies `project-status.md`"
- Sessionende-Regel wird: "Rufe `/track` auf"
- Die Datei-Konvention (Format, max 50 Zeilen) bleibt als Template -- der Skill setzt sie um
- Das Format von project-status.md kann projektspezifisch variieren (z.B. hat project-builder "Meta-Learnings" statt "Offene Aufgaben")

## Warum eine Datei statt mehrerer

| Ansatz | Reads pro Sessionstart | Sync-Risiko | Uebersichtlichkeit |
|--------|----------------------|-------------|-------------------|
| 1 Datei (project-status.md) | 1 | Keins | Hoch |
| 3 Dateien (status + todo + buildlog) | 3 | Hoch | Niedrig |
| Gar keine | 0 | n.a. | Agent startet blind |

## Abgrenzung zu Claudes Auto-Memory

| | project-status.md | Claudes Auto-Memory |
|---|---|---|
| **Zweck** | Wo steht das Projekt? | Wie arbeiten wir zusammen? |
| **Inhalt** | Aktueller Stand, Aufgaben, Entscheidungen | Muster, Praeferenzen, Architektur |
| **Wer schreibt** | Main-Agent (explizit) | Claude (automatisch) |
| **Wer liest** | Alle Agents | Nur Claude |
| **Persistenz** | Im Projektverzeichnis (versionierbar) | In Claudes eigenem Speicher |

Beide sind komplementaer. Die Statusdatei ist das "Was", Auto-Memory ist das "Wie".

## Iceberg-Technik: Strategisches Context Loading

[Neu: 2026-03-08]

Das Kontextfenster ist endlich (200k-1M Token je nach Modell; 1 Token ~ 0.7 Woerter). Naiver Ansatz: Alles in den Kontext laden (ganzes Codebase, alle Skills, alle Status-Dateien). Ergebnis: Kontext voll, bevor die eigentliche Arbeit beginnt.

**Iceberg-Prinzip:** Nur der sichtbare Eisberganteil liegt sofort im Kontext. Der groessere Teil liegt darunter und wird nur bei Bedarf abgerufen.

**Im Kontext (immer geladen, ~20-30%):**
- CLAUDE.md / Agents.md (Systemregeln)
- Aktuelle Task-Kontext (was passiert gerade?)
- Aktive Dateien (nur die aktuell relevanten)
- Memory-Datei (Praeferenzen, Architektur-Entscheidungen)

**Auf Demand (Tool-Calls, ~70-80%):**
- Read: Einzelne Dateien, erst wenn benoetigt
- Grep/Glob: Nur relevante Codestellen, nicht das gesamte Repo
- WebFetch: Internet-Inhalte
- Skills: Nur der YAML-Header ist initial geladen; der vollstaendige Skill-Body wird erst bei Aufruf eingeladen (Progressive Disclosure)

**Auto-Compaction:** Wenn das Kontextfenster voll laeuft (~80% belegt), komprimieren Modelle automatisch den aelteren Kontext. Das kann zu Informationsverlust fuehren (Tool-Outputs, fruehe Entscheidungen). Gegenstrategien:
- Wichtige Erkenntnisse in Dateien schreiben statt im Chat belassen
- Sessions gezielt neu starten bevor Compaction einsetzt
- Memory.md fuer dauerhafte Erkenntnisse nutzen

## Hooks als dritte Schutzschicht

[Neu: 2026-03-09]

Agent-Teams haben drei Schichten fuer Konsistenz und Qualitaet:

| Schicht | Was sie tut | Vergisst bei langem Kontext? | Typ |
|---------|-------------|------------------------------|-----|
| System Prompt | Identitaet + Prinzipien | Ja (verduennt sich) | Empfehlung |
| Skills | Workflows ausfuehren | Nein (frisch geladen bei Aufruf) | Frischer Kontext |
| Hooks | Harte Schranken + Erinnerungen | Nein (extern, kein LLM) | Gesetz / Wachmann |

**Command-Hooks sind Gesetze.** Ein Shell-Script mit exit 2 blockt deterministisch. Kein LLM-Call, kein Vergessen, kein Interpretieren. Ideal fuer Guardrails die nie gebrochen werden duerfen.

**Prompt-Hooks sind Wachmaenner.** Ein LLM-basierter Hook (type: prompt/agent) kann halluzinieren, Kontext missverstehen, false positives liefern. Nuetzlich aber nicht deterministisch. Kosten-Nutzen-Verhaeltnis pruefen.

### Relevante Hook-Events fuer Agent-Teams

| Event | Wann | Typischer Einsatz | Kontext-Injection? |
|-------|------|-------------------|--------------------|
| `PreToolUse` (matcher: Bash) | Vor jedem Bash-Befehl | Gefaehrliche Befehle blocken (JSON mit permissionDecision: deny) | Nein (nur allow/deny) |
| `SessionStart` (matcher: compact) | Nach Auto-Compaction | Kernprinzipien re-injizieren (JSON mit additionalContext) | Ja |
| `PreCompact` | Bevor Compaction startet | Nur Side Effects: Logging, State in Datei sichern | Nein |
| `Stop` | Agent beendet Antwort | Validierung (prompt-basiert, Kosten beachten) | Nein |

### Wann Hooks einsetzen

**Sofort sinnvoll:**
- Harte Guardrails die nie gebrochen werden duerfen (Command-Hook, PreToolUse)
- Post-Compaction-Reminder fuer Kernprinzipien (Command-Hook, SessionStart)

**Erst testen, dann entscheiden:**
- Prompt-basierte Stop-Hooks (Kosten pro Antwort, Zuverlaessigkeit unklar)

**Nicht moeglich:**
- Periodische Reminder (alle N Tool-Calls) -- Hooks sind eventbasiert, nicht intervallbasiert
- Skills aus Hooks heraus triggern

### Konfiguration

Hooks leben in `.claude/settings.json` (Projekt-Level, shareable) oder `~/.claude/settings.json` (User-Level). Shell-Scripts unter `.claude/hooks/` (konsistent mit `.claude/agents/` und `.claude/skills/`).

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"}]
    }],
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/reminder.sh"}]
    }]
  }
}
```

**Hook-Output-Formate (alle exit 0):**
- **PreToolUse blocken:** `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..."}}`
- **SessionStart injizieren:** `{"additionalContext": "Reminder-Text der in den Kontext geht"}`
- **PreCompact:** Kein Output-Format -- nur Side Effects (Datei schreiben, Logging)

`$CLAUDE_PROJECT_DIR` als Umgebungsvariable fuer portable Script-Pfade. Hooks koennen auch in Skill/Agent-YAML-Frontmatter definiert werden (scoped auf Lifecycle der Komponente).

### Zusammenspiel mit bestehenden Massnahmen

Hooks ersetzen keine strukturellen Massnahmen -- sie ergaenzen sie:
- **Schlanker System Prompt** bleibt die beste Anti-Dilution-Massnahme (weniger Text = weniger zu vergessen)
- **Skill-First** bedeutet: Komplexe Arbeit in frischen Kontexten, nicht im verduennten Hauptkontext
- **Kurze Sessions** = Neustart mit voller Prompt-Gewichtung
- **Hooks** = Sicherheitsnetz fuer den Fall dass die strukturellen Massnahmen nicht greifen

## Migration bestehender Teams

Wenn ein Team bereits status.md / todo.md / buildlog.md nutzt:
1. Inhalte in eine neue `project-status.md` konsolidieren
2. Dabei kuerzen: Nur den aktuellen Stand uebernehmen, nicht die komplette Historie
3. Alte Dateien in einen `archive/`-Ordner verschieben (nicht loeschen)
4. CLAUDE.md und Main-Agent System Prompt aktualisieren

## METR-Benchmark: Aufgabenhorizont als Planungsgrundlage

[Neu: 2026-03-08]

Der METR-Benchmark misst den "Task Horizon" von KI-Modellen: Wie lang darf eine Aufgabe sein (in Mensch-Stunden), damit ein Modell sie mit 50% Erfolgswahrscheinlichkeit loest?

**Aktuelle Werte (Stand 2026-03-08):**
- GPT-4 (2023): ~4 Minuten
- Claude Opus 4.6: ~14,5 Stunden

**Wachstumskurve:** Der Anstieg ist nicht linear, sondern exponentiell (oder schneller). Prognose: Ende 2026 koennte der Horizont bei 4 ganzen Tagen liegen (entspricht 12 Arbeitstagen, da KI 24/7 arbeitet).

**Konsequenz fuer Agent-Design:**
- Aufgaben muessen nicht mehr kleiner als ein halber Tag sein, um an KI delegiert zu werden
- Multi-Agent-Orchestrierung hebelt die Grenze weiter aus: Wenn jeder Sub-Agent 14,5h-Aufgaben loest und mehrere parallel laufen, erledigt ein Team theoretisch wochenlange Arbeit in einem Durchgang
- **Entscheidungsregel:** Aufgaben in Einheiten aufteilen, die jeweils kleiner als der aktuelle Task-Horizon sind. Dann lassen sich auch sehr grosse Aufgaben sicher delegieren.

**Wichtig fuer Kontext-Planung:** Laengere Aufgaben = mehr Tool-Calls = hoeherer Kontext-Verbrauch. Bei langen Agenten-Runs die Auto-Compaction im Blick behalten (siehe Iceberg-Technik).

## /loop und Scheduled Tasks: Zwei Ebenen der Session-Automatisierung

[Neu: 2026-03-12]

Claude Code unterscheidet zwei Mechanismen fuer automatisierte Aufgaben -- sie haben unterschiedliche Lebenszeiten und Einsatzbereiche:

### /loop (Kurzfristig, session-gebunden)
- Erstellt einen Cron-Job innerhalb der laufenden Session
- Syntax: `/loop every 10 minutes [prompt]` oder `/loop everyday [prompt]`
- Laeuft in **derselben Kontext-Instanz** wie die aktuelle Session
- **Ablauf:** Nach 3 Tagen automatisch. Deterministisch als Safetyguard.
- **Session-gebunden:** Wenn die Session geschlossen wird, ist der Loop weg. Kein Catch-up.
- **Anwendungsfaelle:** Inbox-Monitoring, Sprint-Tracking, alles wo Claude fuer die naechsten Stunden/Tage im Blick halten soll
- Tools: `CronCreate`, `CronList`, `CronDelete`

### Scheduled Tasks (Dauerhaft, fresh context)
- Konfiguration ueber Desktop App (nicht Terminal/VSCode-Extension)
- Laeuft in einer **neuen Kontext-Instanz** bei jeder Ausfuehrung -- liest Projektdateien frisch
- **Persistent:** Laeuft auch wenn die laufende Session beendet wurde. Holt verpasste Runs nach.
- **Anwendungsfaelle:** Daily Routinen (YouTube-Check + Content repurposing), Weekly Reports, alles was dauerhaft automatisiert laufen soll
- Computer muss an, App muss offen sein

### Konsequenz fuer Skill-Design
- Skills die von Scheduled Tasks aufgerufen werden, duerfen keinen Session-Kontext voraussetzen
- Sie muessen ihren Kontext komplett aus Projektdateien laden (CLAUDE.md, project-status.md)
- Scheduled-Task-Skills sind faktisch Deploy-Ready: Sie verhalten sich deterministisch wie klassische Automatisierungen
- Verbuendet sich mit dem **WAT-Framework**: Workflows und Tools muessen vollstaendig selbsterklaerend sein -- der Agent-Kontext ist fresh, nicht die Fortsetzung einer menschlichen Session

## Context Engineering: Fuenf-Ebenen-Modell (Claude Code)

[Neu: 2026-03-12]

Strukturiertes Kontext-Management in Claude Code laesst sich in 5 Ebenen aufteilen, die von aussen nach innen immer spezifischer werden:

| Ebene | Was | Wann geladen | Tipp |
|-------|-----|-------------|------|
| 1. CLAUDE.md | Projektbeschreibung, Tech-Stack, Struktur, allgemeine Regeln | Immer, bei jeder Session | Max. 1 Seite. Kurz halten. |
| 2. Rules | Konventionen fuer bestimmte Dateitypen/Bereiche | Automatisch, wenn Claude im zugehoerigen Verzeichnis arbeitet | Verhindert redundante Wiederholung von Regeln in jedem Skill |
| 3. Skills | Schritt-fuer-Schritt-Workflows | Bei Aufruf (explizit oder automatisch via YAML-Header) | Claude liest nur den Header, bis er den Skill braucht |
| 4. Subagents | Isolierte Teilaufgaben mit eigenem Kontext | Wenn Main-Agent sie spawnt | Parallel startbar fuer unabhaengige Aufgaben |
| 5. MCP Server | Externe Tool-Anbindungen | Wenn Tool aufgerufen wird | CLI bevorzugen wo verfuegbar |

**Rules als Wartungs-Sparer:** Wenn mehrere Skills dieselbe Konvention benoetigen, gehoert sie in eine Rule-Datei -- nicht in jeden Skill kopiert. Aenderungen muessen dann nur einmal gemacht werden.

### ETH-Zuerich-Studie: Weniger Kontext kann besser sein

[Neu: 2026-03-12]

Eine Studie der ETH Zuerich untersuchte, wie Instruktionsdateien (CLAUDE.md, agents.md etc.) die Performance von Coding-Agents beeinflussen:

- Zu viele Anweisungen machen die Aufgabe in den Augen des Agents **komplexer**: Er exploriert mehr, denkt laenger, braucht mehr Schritte.
- Gilt fuer Claude Code, GitHub Copilot, Cursor und andere Coding Agents.
- **Automatisch generierte** Kontextdateien verschlechtern die Performance im Schnitt leicht.
- Empfehlung der ETH: Instruktionsdateien **manuell schreiben** und **so kurz wie moeglich** halten.

**Konsequenz fuer CLAUDE.md-Design:**
- Nur schreiben, was der Agent bei **jeder Aufgabe** wissen muss
- Alles andere in Rules, Skills oder Subagents auslagern
- Periodisch aufraumen: Was hat sich bewaehrt? Was ist redundant?

Quelle: warum-dein-claude-code-agent-wichtigen-kontext-vergisst (2026-03-12)

## Quellen
- Rendle-Architektur (v3-v5) -- Grundprinzip "Dateien als Gedaechtnis", project-status.md Konvention
- Praxiserfahrung aus Team-Migrationen -- Sync-Probleme bei mehreren Statusdateien
- 2026-03-08_ai-agents-full-course-2026-master-agentic-ai-2-hours.md (2026-03-08) -- Iceberg-Technik, Auto-Compaction, strategisches vs. naives Context Loading
- 2026-03-08_agi-ist-da-warum-spricht-niemand-drber.md (2026-03-08) -- METR-Benchmark, Task-Horizon-Daten fuer GPT-4 und Claude Opus 4.6, exponentielle Wachstumskurve.
- Praxis-Team /track-Skill (2026-03-08, aktualisiert 2026-03-09) -- Praxisbeispiel: Zuerst Fork auf Haiku, dann nach UX-Problemen auf Inline umgestellt (Fork hatte keinen Session-Kontext, fragte User nach Zusammenfassung)
- 2026-03-12_warum-dein-claude-code-agent-wichtigen-kontext-vergisst.md (2026-03-12) -- Fuenf-Ebenen-Modell (CLAUDE.md, Rules, Skills, Subagents, MCP), ETH-Zuerich-Studie zu Instruktionsdatei-Laenge, Rules als Wartungs-Sparer
- 2026-03-12_claude-code-20-has-arrived-its-insane.md (2026-03-12) -- /loop vs. Scheduled Tasks als zwei Automatisierungsebenen, Session-Binding und Ablauf-Logik, Konsequenzen fuer Skill-Design bei Scheduled-Task-Einsatz
