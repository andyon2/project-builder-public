---
name: track
description: "Aktualisiert project-status.md mit Architektur-Entscheidungen, Meta-Learnings und offenen Punkten aus der aktuellen Session. Keine Argumente noetig."
allowed-tools: Read, Edit, Grep, Glob
---

Du aktualisierst den Projektstatus des Project Builders basierend auf dem, was in dieser Session passiert ist.

## Was du trackst

Project-builder ist ein Meta-Projekt. Es gibt keinen klassischen Task-Backlog. Stattdessen drei Kategorien:

1. **Architektur-Entscheidungen**: Grundsaetzliche Entscheidungen die alle Teams betreffen (z.B. "Track ist jetzt inline statt fork"). Mit Datum und kurzem Ausloeser/Begruendung.
2. **Meta-Learnings**: Erkenntnisse ueber die eigene Arbeitsweise (z.B. "Architektur verteidigen statt zuhoeren ist ein Anti-Pattern"). Nur Dinge die sich auf zukuenftige Sessions auswirken.
3. **Offene Punkte**: Dinge die die eigene Architektur betreffen aber noch nicht umgesetzt sind. Mit Herkunft (welches Projekt/Gespraech hat den Punkt ausgeloest).

## Vorgehen

1. Lies `project-status.md`
2. Fasse zusammen, was in dieser Session erarbeitet wurde
3. Aktualisiere die drei Sektionen:
   - **Architektur-Entscheidungen (letzte 5)**: Neue ergaenzen, aelteste entfernen wenn >5
   - **Meta-Learnings**: Neue ergaenzen. Keine Duplikate -- wenn eine Erkenntnis eine bestehende erweitert, bestehende aktualisieren statt neue anlegen.
   - **Offene Punkte**: Erledigte entfernen, neue ergaenzen
4. **Naechste Session** aktualisieren: Was sollte als erstes passieren?
5. **Karteileichen-Pruefung (PFLICHT):** Offene Punkte gegen den aktuellen Stand abgleichen. Erledigte entfernen.
6. Schreibe die aktualisierte Datei zurueck (Edit, nie Write)

## Regeln
- Halte die Datei unter 50 Zeilen
- Keine Meinung, keine Bewertung -- nur Fakten
- Keine Duplikation: Was in knowledge/ oder changelog.md steht, wird hier nicht wiederholt
- Architektur-Entscheidungen brauchen immer [YYYY-MM-DD] + Ausloeser
