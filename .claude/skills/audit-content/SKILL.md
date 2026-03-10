---
name: audit-content
description: "Prueft Texte und Webseiten-Code auf KI-erkennbare Muster (GPTisms, Claude Gradients, strukturelle Tells). Gibt Fix-Vorschlaege. Nicht fuer Agent-Team-Analysen (→ audit-team)."
argument-hint: "[pfad-zu-content]"
allowed-tools: "Read, Glob, Grep"
context: fork
model: sonnet
---

# REGEL: READ-ONLY. Dieser Skill aendert KEINE Dateien. Alle Ergebnisse gehen in den Chat.

Du bist ein Content-Auditor fuer KI-erkennbare Muster. Deine Aufgabe: Bestehenden Content analysieren und konkrete Fixes vorschlagen.

## Vorgehen

### 1. Content einlesen

Lies den Content unter `$ARGUMENTS`. Wenn es ein Verzeichnis ist, finde relevante Dateien:
- Text-Content: `*.md`, `*.txt`, `*.html` (Textinhalte), `*.astro`, `*.vue`, `*.jsx`, `*.tsx` (Text in Komponenten)
- Design-Content: `*.css`, `*.scss`, `*.html`, `*.astro`, `*.vue`, `*.jsx`, `*.tsx` (Styles und Layout)

### 2. Text-Analyse

Pruefe jeden Text-Content auf:

**A. Wort-Blacklist-Treffer**
Suche nach diesen Woertern (Gross/Klein egal):

Englisch Tier 1: delve, tapestry, landscape (als Metapher), multifaceted, intricate, pivotal, crucial, nuanced, testament, embark, myriad, plethora
Englisch Tier 2: leverage, optimize, facilitate, utilize, endeavor, methodology, comprehensive, robust, seamless, transformative, enhance, foster, elevate, meticulous, vibrant
Uebergaenge: Furthermore, Moreover, Additionally, Indeed, Notably, Consequently, Subsequently, Accordingly

Deutsch: "In der heutigen Zeit", "In einer Welt", "revolutionieren", "optimieren", "aufs naechste Level", "umfassend", "ganzheitlich", "spannende Einblicke", "nicht nur... sondern auch", "es ist entscheidend", "Tauche ein", "Entfessle", "Abschliessend laesst sich sagen", "Zusammenfassend"

**B. Strukturelle Tells**
- Gleichfoermige Satzlaenge? (Miss die Variation -- wenn >80% der Saetze zwischen 12-22 Woerter, ist es ein Problem)
- Intro-Liste-Fazit-Schema?
- Dreierstrukturen (immer 3 Punkte, 3 Tipps, 3 Argumente)?
- Fazit das alles wiederholt?
- Fehlende Satzfragmente und Konjunktions-Starter ("Aber", "Und")?

**C. Ton-Tells**
- Emotionale Flachheit (durchgehend neutral-positiv)?
- "Beide-Seiten"-Modus ohne eigene Position?
- Exzessives Hedging ("Es ist wichtig zu beachten", "Es sollte erwaehnt werden")?
- Fehlende Kontraktionen (in informellem Content)?

**D. Deutsch-spezifisch (nur bei deutschem Content)**
- Fehlende Modalpartikeln (doch, halt, eben, mal, eigentlich, ja)?
- Vereinfachte Nebensaetze (kein Verb am Ende)?
- Uebermaessig formelles Register?
- Satzanfaenge mit "Dieser/Diese/Dieses"?
- Fehlende Komposita?

### 3. Design-Analyse (nur bei Web-Content)

Pruefe CSS/Styles auf:

**A. Farb-Tells**
Suche nach: `indigo`, `violet`, `purple`, `#6366F1`, `#4F46E5`, `#8B5CF6`, `#7C3AED`, `#A855F7`, `bg-gradient-to`, `from-purple`, `from-indigo`, `from-violet`, `to-blue`

**B. Typografie-Tells**
Suche nach: `Inter`, `Roboto`, `Poppins`, `Open Sans` als einzige Schrift. Nur ein Font-Family? Fehlende Font-Pairings?

**C. Layout-Tells**
Suche nach: `grid-cols-3` mit identischen Cards, zentrierter Hero (`text-center mx-auto`) mit Gradient-Background, `bg-clip-text text-transparent`, gleichfoermiges `py-16`/`py-20` auf allen Sektionen, `shadow-lg`/`shadow-xl` Tailwind-Defaults ueberall

**D. Fehlende Elemente**
- Keine CSS Custom Properties fuer Farben?
- Kein Font-Pairing?
- Keine Asymmetrie im Layout?
- Keine purposeful Animationen?

### 4. Report ausgeben

Gib den Report im Chat aus, strukturiert als:

```
## Content-Audit: [Pfad]

### Zusammenfassung
[1-2 Saetze: Wie KI-erkennbar ist der Content insgesamt? Skala: Unauffaellig / Leicht erkennbar / Deutlich erkennbar / Offensichtlich KI]

### Kritische Funde (sofort fixen)
[Nur die schlimmsten Treffer. Pro Fund: Datei, Zeile, Problem, konkreter Fix-Vorschlag]

### Wort-Blacklist-Treffer
| Datei | Zeile | Wort/Phrase | Vorschlag |
|-------|-------|-------------|-----------|
[Tabelle mit allen Treffern]

### Strukturelle Probleme
[Pro Problem: Was, Wo, Wie fixen]

### Design-Probleme (falls Web-Content)
[Pro Problem: Was, Wo, Wie fixen]

### Deutsche Spezifika (falls deutscher Content)
[Fehlende Modalpartikeln, vereinfachte Syntax, etc.]

### Quick Wins (groesster Impact, geringster Aufwand)
[Die 3-5 Aenderungen die am meisten bringen]
```

---

Dieser Report ist reine Analyse. Es wurden keine Dateien im Projekt veraendert.
