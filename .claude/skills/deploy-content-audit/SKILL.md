---
name: deploy-content-audit
description: Pflanzt den audit-content Skill und die Content-Humanization-Regeln in ein bestehendes Projekt ein. Aktualisiert Content-Agents mit Selbstcheck-Regeln. Aufrufen mit Projektpfad.
argument-hint: "[pfad-zum-projekt]"
allowed-tools: "Read, Glob, Grep, Write, Edit"
context: fork
model: sonnet
---

Du deployst die Content-Humanization-Erweiterung in ein bestehendes Projekt. NUR diese drei Dinge:

1. `/audit-content` Skill ins Projekt kopieren
2. `knowledge/content-humanization.md` ins Projekt kopieren
3. Content-generierende Agents mit Selbstcheck-Regel erweitern

## Vorgehen

### Phase 1: Projekt analysieren (read-only)

Lies im Zielprojekt `$ARGUMENTS`:

1. `CLAUDE.md` -- Verstehe Projektstruktur, vorhandene Agents und Skills
2. `.claude/skills/` -- Prüfe ob `/audit-content` schon existiert
3. `knowledge/` -- Prüfe ob `content-humanization.md` schon existiert
4. `.claude/agents/*.md` -- Identifiziere Content-generierende Agents (Texte, Web, Marketing, Blog, Social Media, Design)

Zeige dem User:
```
## Deploy-Plan: Content Audit fuer [Projekt]

Skill audit-content: [Neu anlegen / Existiert bereits]
Knowledge content-humanization.md: [Neu anlegen / Existiert bereits]

Content-Agents gefunden:
- [agent-name]: [Warum Content-Agent? Was generiert er?]
- [agent-name]: ...

Content-Skills gefunden:
- [skill-name]: [Warum Content-Skill?]

Aenderungen die ich vornehme:
1. [...]
2. [...]
```

Warte auf OK vom User.

### Phase 2: Deployen (nach User-OK)

**A. Audit-Content Skill anlegen**

Erstelle `$ARGUMENTS/.claude/skills/audit-content/SKILL.md` mit dem Inhalt aus `$CLAUDE_PROJECT_DIR/.claude/skills/audit-content/SKILL.md`.

Passe den Skill an das Projekt an:
- Wenn das Projekt bestimmte Content-Verzeichnisse hat, ergänze diese als Standard-Suchpfade
- Wenn das Projekt eine bestimmte Sprache hat (DE/EN), priorisiere die passende Blacklist

**B. Knowledge-Datei anlegen**

Erstelle `$ARGUMENTS/knowledge/content-humanization.md` -- kopiere den Inhalt aus `$CLAUDE_PROJECT_DIR/knowledge/content-humanization.md`.

Falls `$ARGUMENTS/knowledge/` nicht existiert, erstelle das Verzeichnis.

**C. Content-Agents erweitern**

Fuer jeden identifizierten Content-Agent, fuege im "Selbstcheck vor Abgabe"-Block hinzu:

```
- Habe ich die Wort-Blacklist aus knowledge/content-humanization.md beachtet? (Keine GPTisms, keine KI-Floskeln)
- Variiert meine Satzlaenge genuegend? (Mix aus kurzen Fragmenten und laengeren Saetzen)
- Habe ich Stellung bezogen statt neutral zu bleiben?
- [Bei Deutsch]: Nutze ich Modalpartikeln natuerlich?
- [Bei Web/Design]: Kein Purple-Gradient, kein Inter, kein 3-Spalten-Grid?
```

Wenn der Agent keinen "Selbstcheck vor Abgabe"-Block hat, fuege einen am Ende hinzu.

Fuer Content-generierende Skills: Fuege eine kurze Regel ein, die auf `knowledge/content-humanization.md` verweist.

**D. CLAUDE.md aktualisieren**

Fuege in der Skills-Tabelle hinzu:

```
| /audit-content [pfad] | Prueft Content auf KI-erkennbare Muster | fork |
```

Falls es eine Knowledge-Referenz in CLAUDE.md gibt, ergaenze `content-humanization.md`.

### Phase 3: Zusammenfassung

Zeige dem User:
```
## Erledigt

Neu angelegt:
- [Dateien die erstellt wurden]

Geaendert:
- [Dateien die editiert wurden, mit kurzer Beschreibung was sich aenderte]

Naechster Schritt:
Fuehre `/audit-content` auf deinem bestehenden Content aus, um aktuelle Probleme zu finden.
```
