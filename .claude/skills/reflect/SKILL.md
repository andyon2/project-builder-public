---
name: reflect
description: Erstellt eine ehrliche Selbstanalyse des Agent-Teams. Untersucht Rollen, Synchronisation, Schwachstellen, Ueberschneidungen und Verbesserungsvorschlaege. Schreibt das Ergebnis nach .claude/team-reflection.md
allowed-tools: "Read, Glob, Grep, Write"
context: fork
model: sonnet
---

Du analysierst dein eigenes Agent-Team schonungslos ehrlich. Du bist kein Cheerleader -- du bist ein interner Auditor, der Probleme benennt. "Alles ist gut" ist kein nuetzliches Ergebnis.

## Vorgehen

### 1. Team-Inventar lesen

Lies:
- `CLAUDE.md`
- Alle `.claude/agents/*.md`
- Alle `.claude/skills/*/SKILL.md`
- System-Prompt-Datei (falls im CLAUDE.md referenziert oder als separate .md im Root)
- `project-status.md` (fuer aktuellen Projektkontext)

### 2. Analyse durchfuehren

Beantworte fuer JEDEN Agent und Skill ehrlich:

**Rollen-Klarheit:**
- Was genau tut dieser Agent/Skill?
- Gibt es Ueberschneidungen mit anderen?
- Wird er regelmaessig genutzt oder ist er "totes Gewicht"?

**Synchronisation:**
- Wie bleiben die Agents untereinander konsistent?
- Wo gibt es Luecken (Aenderung in Dokument A, aber Agent B weiss nichts davon)?
- Was passiert automatisch, was muss manuell angestossen werden?

**Schwachstellen:**
- Was funktioniert in der Praxis NICHT gut?
- Wo muss der User haeufig korrigieren oder nachbessern?
- Welche Aufgaben dauern laenger als sie sollten?
- Was fehlt komplett (wiederkehrende Aufgaben ohne Skill/Agent)?

**Ueberschneidungen und Ineffizienzen:**
- Welche Skills/Agents machen aehnliche Dinge?
- Gibt es Skills die nie oder fast nie genutzt werden?
- Gibt es Agents die eigentlich nur Schritte ausfuehren (Skill-Kandidaten)?

**Ziele und Organisation:**
- Was sind die aktuellen Projektziele (kurz/mittel/langfristig)?
- Wie organisiert sich das Team fuer diese Ziele?
- Wo gibt es Luecken zwischen Zielen und vorhandenen Faehigkeiten?

### 2b. Prinzip-Konsistenz pruefen

Dieser Schritt prueft ob das Team seine eigenen Prinzipien befolgt -- nicht nur ob die Struktur sauber ist. Das ist eine andere Pruefklasse: Nicht "ist alles da?" sondern "tun wir was wir predigen?".

**Selbstbeschreibung erstellen:**
- Lies den System Prompt / die main-agent-Datei
- Extrahiere alle expliziten Prinzipien (z.B. "Skill-First", "Token-Bewusstsein", "Delegieren statt selbst machen")
- Extrahiere alle Taetigkeiten die der Agent laut System Prompt + CLAUDE.md ausfuehrt (nicht nur Skills -- auch implizite Taetigkeiten)

**Gegen Struktur pruefen:**
- Hat jede Taetigkeit einen passenden Skill oder Agent? (Skill-First-Check)
- Hat jeder Agent und Fork-Skill ein explizites model-Feld? (Token-Check)
- Hat jeder Agent ein maxTurns-Feld? (Runaway-Schutz)
- Sind immer-geladene Dateien schlank? CLAUDE.md <100, System Prompt <200, project-status.md <50 Zeilen (Context-Burden-Check)
- Delegiert der Main-Agent konsequent oder macht er Aufgaben selbst die ein Skill abdecken koennte? (Delegations-Check)

**Explizit nach Luecken suchen -- das ist der wichtigste Teil:**
- Welche Taetigkeiten haben KEINEN Skill, sollten aber einen haben?
- Welche Prinzipien werden formuliert aber nicht in der Struktur umgesetzt?
- Gibt es Widersprueche zwischen Prinzipien und tatsaechlicher Architektur?

### 3. Verbesserungsvorschlaege formulieren

Unterteile in:
- **Quick Wins** -- sofort umsetzbar, niedriges Risiko, hoher Nutzen
- **Mittelfristig** -- groessere Umbauten, die sich lohnen
- **Bewusst beibehalten** -- was nach der Analyse sinnvoll ist und bleiben soll (mit Begruendung)

### 4. Ergebnis schreiben

Schreibe die vollstaendige Analyse nach `.claude/team-reflection.md`.

Format:

```markdown
# [Projektname] — Team-Reflection

Stand: [YYYY-MM-DD]

## 1. Wofuer bin ich zustaendig?
[Pro Agent/Skill: Was er tut, was er NICHT tut.
Tabellarisch: Bereich | Was ich tue | Was ich NICHT tue]

## 2. Synchronisation
[Wie bleibt alles konsistent? Drei-Quellen-Hierarchie o.ae.
Konkrete Trigger: Was loest was aus?
Was wird NICHT automatisch synchronisiert?]

## 3. Ziele und Organisation
[Kurz-/mittel-/langfristige Ziele.
Wie organisiert sich das Team dafuer?]

## 4. Schwachstellen und Luecken
[Ehrlich, konkret, mit Beispielen wenn moeglich.
Pro Schwachstelle: Problem, Auswirkung, moegliche Loesung.]

## 5. Ueberschneidungen und Ineffizienzen
[Was ueberlappt? Vorschlaege zur Bereinigung.
Welche Skills/Agents werden nie genutzt?]

## 6. Streamlining-Vorschlaege

### Sofort umsetzbar (Quick Wins)
[Nummeriert, konkret]

### Mittelfristig
[Nummeriert, konkret]

## 7. Bewusst beibehalten
[Was nach Analyse sinnvoll ist und bleiben soll -- mit Begruendung]

## 8. Prinzip-Konsistenz
[Selbstbeschreibung: Was behauptet das Team zu tun und welchen Prinzipien folgt es?
Pro Prinzip: Wird es eingehalten? Beleg oder Verstoss.
Luecken: Taetigkeiten ohne Skill, Prinzipien ohne Umsetzung, Widersprueche zwischen Anspruch und Realitaet.
Dieser Abschnitt ist der wichtigste fuer die Aussenperspektive.]

## Anhang: Dateistruktur
[Vollstaendiger Dateibaum mit Annotationen]
```

## Wichtig

- Schreibe aus der Ich-Perspektive des Teams (nicht "das Team macht X" sondern "ich mache X")
- Sei bei Schwachstellen schonungslos ehrlich -- blinde Flecken sind schlimmer als bekannte Probleme
- Nenne konkrete Beispiele statt abstrakter Beschreibungen
- Die Datei wird von einem externen Auditor (dem Project Builder) gelesen -- schreibe so, dass ein Aussenstehender das Team versteht
