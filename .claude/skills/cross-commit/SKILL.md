---
name: cross-commit
description: Committed und pusht uncommitted Aenderungen in allen fremden Repos aus teams.md. Nur auf expliziten User-Befehl. Committet NUR bereits getrackte Dateien (git add -u), keine untracked files.
argument-hint: "[commit message]"
context: fork
model: haiku
allowed-tools: "Read, Bash"
---

Du fuehrst Cross-Repo-Git-Operationen durch. NUR getrackte Dateien committen. NUR auf expliziten User-Befehl (dieser Skill wurde bereits aufgerufen, also ist der Befehl erteilt).

## Commit-Message bestimmen

- Falls `$ARGUMENTS` nicht leer: Verwende `[PB] $ARGUMENTS`
- Falls `$ARGUMENTS` leer: Verwende `[PB] Cross-project update via Project Builder`

## Schritt 1: Repos aus teams.md lesen

Lies `teams.md`. Extrahiere alle Pfade aus der Pfad-Spalte (Format: `~/projektname`).
Expandiere `~` zu absolutem Pfad (HOME-Verzeichnis des Users).

## Schritt 2: Aenderungen pruefen

Fuer jedes Repo: Pruefe ob uncommitted Aenderungen an bereits getrackten Dateien vorliegen:

```bash
git -C /pfad/zum/repo status --porcelain
```

Interpretiere das Ergebnis:
- Zeilen mit `M`, `D`, `R` im ersten oder zweiten Zeichen: getrackte Aenderungen (relevant)
- Zeilen mit `??`: untracked files (IGNORIEREN)
- Repo nicht vorhanden oder kein Git-Repo: Notieren, ueberspringen

Sammle: Liste der Repos MIT Aenderungen (nur getrackte), Liste der Repos ohne Aenderungen, Liste der Repos die nicht gefunden wurden.

## Schritt 3: Uebersicht anzeigen

Zeige dem User BEVOR du irgendwas committed:

```
## Cross-Commit Uebersicht

**Repos mit Aenderungen (werden committed):**
- ~/projekt-a: M scripts/starter
- ~/projekt-b: M CLAUDE.md

**Repos ohne Aenderungen (werden uebersprungen):**
- ~/projekt-c, ~/projekt-d

**Commit-Message:** "[PB] Cross-project update via Project Builder"
```

Warte auf Bestaetigung vom User bevor du weitermachst.

## Schritt 4: Committen und Pushen

Fuer jedes Repo mit Aenderungen:

```bash
git -C /pfad/zum/repo add -u
git -C /pfad/zum/repo commit -m "[PB] <commit-message>"
git -C /pfad/zum/repo push
```

Fehlerbehandlung:
- Commit schlaegt fehl: Warnung ausgeben, naechstes Repo
- Push schlaegt fehl: Warnung ausgeben, naechstes Repo
- Nie abbrechen wegen eines einzelnen Fehlers

## Schritt 5: Ergebnis-Report

```
## Cross-Commit Ergebnis

**Erfolgreich:** ~/projekt-a, ~/projekt-b (je 1 Datei)
**Fehlgeschlagen:** ~/projekt-e (Push fehlgeschlagen)
**Uebersprungen:** ~/projekt-c, ~/projekt-d (keine Aenderungen)
```
