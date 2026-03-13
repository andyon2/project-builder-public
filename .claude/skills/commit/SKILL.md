---
name: commit
description: "Session-Commit: /track ausfuehren, dann committen und pushen. Standard fuer Sessionende."
---

Fuehre einen Session-Commit durch:

1. Rufe `/track` auf -- aktualisiert project-status.md mit dem Session-Fortschritt.
2. `git add -u` -- alle getrackten Aenderungen stagen.
3. `git diff --cached --stat` -- Ueberblick zeigen.
4. **Rueckwaertssuche-Check:** Pruefe den Diff (`git diff --cached`) auf strukturelle Aenderungen:
   - Dateien geloescht oder umbenannt
   - Funktions-/Skill-/Agent-Namen geaendert
   - Output-Formate geaendert (JSON-Struktur, Rueckgabewerte)
   - Verantwortlichkeiten zwischen Komponenten verschoben
   - Import-Pfade oder Referenzen auf andere Dateien geaendert
   Wenn strukturelle Aenderungen gefunden: `grep -r` nach allen Konsumenten der geaenderten Dateien/Namen/Pfade. Ergebnisse dem User zeigen. Probleme VOR dem Commit fixen.
   Wenn keine strukturellen Aenderungen (nur Hinzufuegen, Erweitern, neue Dateien): weiter.
5. Commit-Message aus den Aenderungen ableiten (kurz, deutsch, beschreibend).
6. Marker schreiben: `touch .git/commit-via-skill` -- entsperrt den Pre-Commit-Hook.
7. `git commit` mit der Message.
8. Pruefe ob ein Remote existiert (`git remote`). Wenn ja: `git push`. Wenn nein: "Kein Remote konfiguriert, nur lokal committed." melden.

Wenn nichts zu committen ist (keine staged changes nach Schritt 2), melde das und ueberspringe Schritt 3-8.
