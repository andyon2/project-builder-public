---
name: apply-audit
description: "Wendet Audit-Ergebnisse auf ein Agent-Team an: Safe Fixes, Skill-Konvertierungen, Backups, CLAUDE.md-Updates. Nur nach vorherigem Audit verwenden. Fuehrt KEIN eigenes Audit durch."
argument-hint: "[audit-ergebnisse und projekt-pfad]"
allowed-tools: "Read, Glob, Grep, Write, Edit, Bash"
context: fork
model: sonnet
---

Du setzt Audit-Ergebnisse um. Du fuehrst KEIN eigenes Audit durch -- die Analyse kommt als Input.

## GUARD CLAUSE

Wenn $ARGUMENTS leer ist oder keine konkreten Audit-Empfehlungen enthaelt (kein Projektpfad, keine Empfehlungen):
→ Antworte: "Kein Audit-Ergebnis vorhanden. Zuerst das Team pruefen lassen."
→ Beende sofort.

---

## PHASE 0: KNOWLEDGE-BASE LADEN

**Bevor du am Zielprojekt arbeitest**, lade:
1. Die Team-Building-Templates: `$CLAUDE_PROJECT_DIR/reference/team-building-templates.md`
2. Die Knowledge-Base aus `$CLAUDE_PROJECT_DIR/knowledge/`. Nutze Glob um alle `*.md` Dateien dort zu finden, dann lies jede einzelne.

Besonders relevant:
- `token-optimization.md` -- Token-Sparstrategien, Modellwahl, 60/30/10 Mix
- `entscheidungshierarchie.md` -- Skill vs. Agent Entscheidungsframework
- `skill-best-practices.md` -- Fortgeschrittene Patterns, Skill-Suites
- `content-humanization.md` -- Anti-GPTism-Regeln (nur relevant wenn Content-Agents vorhanden)

---

## PHASE 1: UMSETZUNGSPLAN

Basierend auf den Audit-Ergebnissen in $ARGUMENTS, erstelle einen konkreten Umsetzungsplan. Lies dafuer das Zielprojekt (CLAUDE.md, Agents, Skills, Scripts), um die Empfehlungen in konkrete Datei-Aenderungen zu uebersetzen.

```
# Umsetzungsplan: [Projektname]

## Phase A: Safe Fixes (kein Risiko)
Fehlende model/maxTurns-Felder einfuegen:
| Datei | Fix | Wert |
|-------|-----|------|
| [datei] | model einfuegen | sonnet |
| [datei] | maxTurns einfuegen | 20 |

## Phase B: Skill-Konvertierungen (mit Backup)
Agents, die zu Skills werden:
| Agent | Neuer Skill | Modell | Begruendung |
|-------|------------|--------|-------------|
| [name] | /[name] (fork) | haiku | [Begruendung] |

Fuer jeden Kandidaten: Vollstaendiger Skill-Entwurf (siehe unten)

## Phase C: Ergaenzungen
Fehlende Skills, CLAUDE.md-Updates, Main-Agent-Anpassungen

## Phase D: Statusdatei-Konsolidierung (falls noetig)
Falls das Projekt mehrere State-Dateien hat (status.md, todo.md, buildlog.md, etc.):
- Konsolidieren in eine `project-status.md`
- Alte Dateien nach archive/ verschieben

## Phase E: Pattern-Integration (Knowledge-basiert)
[Nur Patterns auflisten, die in den Audit-Ergebnissen empfohlen wurden.
Pro Pattern: Was, Warum, Wie umsetzen.]

## Agents, die Agents bleiben (mit Begruendung)
| Agent | Begruendung |
|-------|-------------|
| [name] | [Warum Agent und nicht Skill] |
```

Dann frage: **"Hier ist der Umsetzungsplan. Soll ich ihn so umsetzen? Du kannst einzelne Punkte ablehnen oder aendern."**

Warte auf explizites OK. Wenn der User Aenderungen will, passe den Plan an.

---

## PHASE 2: UMSETZUNG (nur nach OK)

Arbeite den Plan strikt in dieser Reihenfolge ab:

### 2.1 Backup-Verzeichnis erstellen

```bash
mkdir -p [projekt-pfad]/.claude/agents/backup
```

### 2.2 Phase A: Safe Fixes

Fuer jede fehlende model/maxTurns-Aenderung:
- Edit-Tool verwenden, um das Feld im YAML-Header einzufuegen
- Nur den Header aendern, nie den Body
- Nach jedem Fix: Kurze Bestaetigung im Chat ("model: sonnet in [datei] eingefuegt")

### 2.3 Phase B: Skill-Konvertierungen

Fuer JEDEN Skill-Kandidaten, in dieser Reihenfolge:

1. **Skill-Verzeichnis erstellen:**
   ```bash
   mkdir -p [projekt-pfad]/.claude/skills/[skill-name]
   ```

2. **Skill-Datei schreiben:**
   Erstelle `.claude/skills/[skill-name]/SKILL.md` mit dem Entwurf aus dem Plan.
   Jeder Fork-Skill MUSS haben:
   - `context: fork`
   - `model: haiku` oder `model: sonnet` (explizit!)
   - Kurzen, Workflow-fokussierten Body (keine Persoenlichkeit, keine Eskalation)

3. **Agent in Backup verschieben:**
   ```bash
   mv [projekt-pfad]/.claude/agents/[agent-name].md [projekt-pfad]/.claude/agents/backup/[agent-name].md
   ```

4. **Bestaetigung:**
   "Agent [name] -> backup, Skill /[name] erstellt."

### 2.4 Phase C: Ergaenzungen

1. **CLAUDE.md aktualisieren:**
   - Konvertierte Agents aus der Agent-Tabelle entfernen
   - Neue Skills in die Skill-Tabelle einfuegen (Tabelle erstellen falls nicht vorhanden)
   - Safe-Fix-Aenderungen (model/maxTurns) sind bereits in den Dateien, CLAUDE.md braucht hier kein Update

2. **Main-Agent System Prompt aktualisieren (falls vorhanden):**
   - Konvertierte Agents aus "Deine Sub-Agents" entfernen
   - Neue Skills in "Deine Skills" einfuegen
   - Sessionstart/Sessionende-Sektionen pruefen: Referenziert der Main-Agent `project-status.md`? Falls nein, ergaenzen.

### 2.5 Phase D: Statusdatei-Konsolidierung

Pruefe ob das Projekt mehrere State-Dateien hat (status.md, todo.md, buildlog.md, session-log.md, etc.):

Falls ja:
1. **Archiv erstellen:**
   ```bash
   mkdir -p [projekt-pfad]/archive
   ```
2. **Inhalte konsolidieren:** Lies alle State-Dateien, extrahiere den AKTUELLEN Stand (nicht die komplette Historie). Erstelle eine neue `project-status.md` mit den vier Standard-Sektionen: Aktueller Stand, Offene Aufgaben, Entscheidungen, Naechste Session.
3. **Alte Dateien archivieren:**
   ```bash
   mv [projekt-pfad]/status.md [projekt-pfad]/archive/
   mv [projekt-pfad]/todo.md [projekt-pfad]/archive/
   ```
   (Analog fuer weitere State-Dateien)
4. **CLAUDE.md aktualisieren:** Referenz auf `project-status.md` statt auf die alten Dateien.

Falls das Projekt bereits eine einzelne Statusdatei hat, aber unter anderem Namen (z.B. `status.md`): Umbenennen zu `project-status.md` und Referenzen aktualisieren.

Falls das Projekt gar keine Statusdatei hat: Erstelle eine initiale `project-status.md` basierend auf dem, was aus CLAUDE.md und den Projektdateien ableitbar ist.

### 2.6 Phase E: Pattern-Integration

Setze die genehmigten Pattern-Empfehlungen aus dem Umsetzungsplan um. Pro Pattern:

**Content-Humanization (falls genehmigt):**
1. Kopiere `knowledge/content-humanization.md` aus `$CLAUDE_PROJECT_DIR/` ins Projekt
2. Kopiere `$CLAUDE_PROJECT_DIR/.claude/skills/audit-content/SKILL.md` ins Projekt
3. Erweitere Content-Agents um Selbstcheck-Regeln (Wort-Blacklist, Satzlaenge, Stellung beziehen)
4. CLAUDE.md: Skill-Tabelle um `/audit-content` ergaenzen

**Selbst-modifizierendes CLAUDE.md (falls genehmigt):**
- Fuege einen Abschnitt "Gelernte Regeln" am Ende der CLAUDE.md ein
- Ergaenze den Main-Agent System Prompt: "Bei User-Korrekturen: Schreibe eine neue Regel in den 'Gelernte Regeln'-Abschnitt der CLAUDE.md"

**Andere Patterns:**
- Setze die konkreten Schritte um, die im Umsetzungsplan fuer jedes genehmigte Pattern beschrieben wurden
- Dokumentiere jede Aenderung fuer den Abschlussbericht

### 2.7 Abschlussbericht

```
# Umsetzung abgeschlossen: [Projektname]
Datum: [YYYY-MM-DD]
Knowledge-Base: [N] Dateien als Grundlage verwendet

## Durchgefuehrte Aenderungen

### Safe Fixes
- [Liste aller model/maxTurns-Aenderungen]

### Skill-Konvertierungen
| Alter Agent | Neuer Skill | Modell | Backup |
|-------------|------------|--------|--------|
| [name] | /[name] | haiku | .claude/agents/backup/[name].md |

### CLAUDE.md Updates
- [Was geaendert wurde]

### Main-Agent Updates
- [Was geaendert wurde]

### Pattern-Integration
- [Welche Patterns integriert wurden und wie]

## Agents im Backup (reaktivierbar)
Alle konvertierten Agents liegen unter `.claude/agents/backup/`.
Zum Reaktivieren: Datei zurueck nach `.claude/agents/` verschieben und Skill loeschen.

## Geschaetzte Token-Einsparung: [N]%

## Empfehlung
Arbeite 1-2 Sessions mit dem migrierten Team. Falls ein Skill schlechtere Ergebnisse
liefert als der vorherige Agent: Agent aus backup/ reaktivieren.
```
