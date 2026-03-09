# Migration Guide: v3 -> v4 (Skill-First-Update)

## Was sich geaendert hat

### Neue Saeule: Skill-First-Prinzip
- Jede Aufgabe startet als Skill-Kandidat, nicht als Agent-Kandidat
- Entscheidungshierarchie: Skill -> Agent -> Agent+Direkt
- Zwei Skill-Typen: Encoded Preference (langlebig) vs. Capability Uplift (fragil)
- Skill-zu-Agent-Verhaeltnis als Qualitaetsmetrik (Ziel: mindestens 1:1)

### Pflichtfelder verschaerft
- `model`-Feld ist jetzt Pflicht fuer JEDEN Agent und Fork-Skill (vorher: empfohlen)
- `maxTurns` ist jetzt Pflicht fuer JEDEN Agent (vorher: optional)

### Erweiterte Skill-Architektur
- Drei Skill-Typen: Inline, Fork (`context: fork`), Interview-Skill
- Hilfsskripte-Pattern (`scripts/[skill-name]/`)
- Agent-zu-Skill-Konvertierungsanleitung
- Skills-Tabelle in CLAUDE.md (neben Agents-Tabelle)

### Saeule 2 verschaerft
- Explizite Unterscheidung: "Ein Agent denkt. Ein Skill fuehrt aus."
- Nur Rollen mit eigener Denkweise werden Agents

### Knowledge-Base
- `knowledge/` Verzeichnis mit kuratierten Best Practices
- Masterprompt referenziert Knowledge-Base bei Architekturentscheidungen

---

## Auf bestehende Teams anwendbar

### Universell (IMMER anwenden -- kein Risiko)

Diese Fixes sind rein technisch und koennen nichts kaputtmachen:

- [ ] **model-Feld in jeden Agent einfuegen, der keins hat.**
  Schaue in `.claude/agents/` -- jede Datei, die kein `model:` im YAML-Header hat, erbt das Modell des Main-Agents (vermutlich Opus). Setze `model: sonnet` als Default, `model: haiku` wenn der Agent nur liest/formatiert.

- [ ] **model-Feld in jeden Fork-Skill einfuegen, der keins hat.**
  Schaue in `.claude/skills/` -- jede Datei mit `context: fork` ohne `model:` erbt ebenfalls.

- [ ] **maxTurns in jeden Agent einfuegen, der keins hat.**
  Standard: `maxTurns: 20` fuer normale Agents, `maxTurns: 25` fuer dialogische.

- [ ] **Skills-Tabelle in CLAUDE.md ergaenzen.**
  Falls die CLAUDE.md nur eine Agents-Tabelle hat, ergaenze eine Skills-Tabelle (auch wenn sie anfangs leer ist -- das macht das Fehlen von Skills sichtbar).

### Empfohlen (pruefen, dann anwenden)

Diese Aenderungen erfordern eine Einschaetzung pro Agent:

- [ ] **Jeden Agent auf Skill-Kandidatur pruefen.**
  Der Denkweise-Test: (1) Eigene Perspektive? (2) Eigenstaendige Urteile? (3) Breiter Kontext?
  Wenn 0-1x Ja: Skill-Kandidat. Konvertierung nach dem Pattern in `knowledge/skill-best-practices.md`.

- [ ] **Agent-Prompts auf Proportionalitaet pruefen.**
  >150 Zeilen fuer eine einfache Aufgabe = aufgeblaeht. Straffen.

- [ ] **Modell-Angemessenheit pruefen.**
  Agents, die nur Dateien lesen und zusammenfassen: Haiku reicht.
  Agents, die kreativ schreiben oder analysieren: Sonnet.
  Kein Sub-Agent braucht Opus (das ist dem Main-Agent vorbehalten).

- [ ] **Fehlende Skills identifizieren.**
  Wiederkehrende Aufgaben, die kein Skill abdeckt? Status-Reports, Daten-Aggregation, Kurz-Interviews?

### Situativ (nur wenn passend)

- [ ] **Agents ohne Denkweise: Entweder Denkweise ergaenzen oder zu Skill konvertieren.**
  Manche Agents haben keinen "Wer du bist"-Block oder nur eine Aufgabenliste. Entweder den Block ergaenzen (wenn eine Denkweise Sinn macht) oder konvertieren.

- [ ] **Wissensquellen-Sektion ergaenzen, falls Agent Fachwissen braucht.**

- [ ] **Main-Agent System Prompt: Skills-Sektion ergaenzen.**
  Der Main-Agent sollte wissen, welche Skills er hat und wann er sie statt Agents nutzt.

### NICHT anwenden (wuerde Team brechen)

- **CLAUDE.md-Struktur NICHT erzwingen**, wenn das Team eigene Sektionen hat. Die v4-Vorlage ist fuer neue Teams. Bestehende Teams haben ihren eigenen Kontext.
- **Organisch gewachsene Agent-Inhalte NICHT umschreiben**, nur weil sie nicht ins Template passen. Die Denkweisen und Workflows in den Agents sind projektspezifisch. Nur die Infrastruktur (model, maxTurns, Skill-Balance) wird aktualisiert.
- **Agents NICHT loeschen**, bevor der Ersatz-Skill getestet ist. Erst Skill erstellen, testen, dann Agent entfernen.

---

## Empfohlene Reihenfolge fuer die Migration

1. **`/audit-team [projekt-pfad]` laufen lassen** -- gibt dir den vollstaendigen Report
2. **Universelle Fixes anwenden** (model, maxTurns, Skills-Tabelle) -- 10 Minuten pro Team
3. **Audit-Report durchgehen** -- Skill-Kandidaten und Token-Hotspots pruefen
4. **Skill-Konvertierungen einzeln umsetzen** -- pro Kandidat: Skill erstellen, testen, Agent entfernen
5. **Fehlende Skills erstellen** -- neue Skills fuer wiederkehrende Aufgaben
6. **Main-Agent System Prompt aktualisieren** -- Skills-Sektion, Delegationslogik

---

## Checkliste: Migration abgeschlossen?

- [ ] Jeder Agent hat `model`-Feld
- [ ] Jeder Agent hat `maxTurns`-Feld
- [ ] Jeder Fork-Skill hat `model`-Feld
- [ ] CLAUDE.md hat Skills-Tabelle
- [ ] Alle Skill-Kandidaten evaluiert (konvertiert oder begruendet beibehalten)
- [ ] Main-Agent kennt seine Skills
- [ ] Skill-zu-Agent-Verhaeltnis ist mindestens 1:1 (oder begruendet nicht)
