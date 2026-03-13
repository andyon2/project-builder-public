---
name: cross-commit
description: Committed und pusht uncommitted Aenderungen in allen fremden Repos aus teams.md (nur Repos mit PB-Managed=ja), dann pullt auf dem Server. Nur auf expliziten User-Befehl. Committet NUR bereits getrackte Dateien (git add -u), keine untracked files.
argument-hint: "[commit message]"
context: fork
model: haiku
allowed-tools: "Read, Bash"
---

Du fuehrst Cross-Repo-Git-Operationen durch. NUR getrackte Dateien committen. Der User hat diesen Skill explizit aufgerufen -- das ist die Bestaetigung.

## Commit-Message bestimmen

- Falls `$ARGUMENTS` nicht leer: Verwende `[PB] $ARGUMENTS`
- Falls `$ARGUMENTS` leer: Verwende `[PB] Cross-project update via Project Builder`

## Schritt 1: Repos aus teams.md lesen

Lies `teams.md`. Extrahiere alle Zeilen aus der Teams-Tabelle.

**Umgebungsfilter:**
```bash
ENV=$(cat $HOME/.environment)
```
Nur Teams verarbeiten, deren `Server`-Spalte in `teams.md` zur aktuellen Umgebung passt. Das Mapping von Umgebungswert zu Server-Gruppe steht in der Server-Gruppen-Tabelle in `teams.md`.

Zusaetzlich: Nur Repos mit `ja` in der PB-Managed-Spalte sind relevant. Repos mit `nein` oder `--` werden komplett ignoriert.
Expandiere `~` zu absolutem Pfad (HOME-Verzeichnis des Users).

## Schritt 2: Aenderungen pruefen

Fuer jedes berechtigte Repo: Pruefe ob uncommitted Aenderungen an bereits getrackten Dateien vorliegen:

```bash
git -C /pfad/zum/repo status --porcelain
```

Interpretiere das Ergebnis:
- Zeilen mit `M`, `D`, `R` im ersten oder zweiten Zeichen: getrackte Aenderungen (relevant)
- Zeilen mit `??`: untracked files (NICHT committen, aber fuer Warnung merken)
- Repo nicht vorhanden oder kein Git-Repo: Notieren, ueberspringen

Sammle: Liste der Repos MIT Aenderungen (nur getrackte), Liste der Repos ohne Aenderungen, Liste der Repos die nicht gefunden wurden, Liste der Repos mit untracked files.

## Schritt 3: Committen und Pushen

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

## Schritt 4: Server-Sync

Nach erfolgreichem Push: Lies `config/server.md` und die Server-Gruppen-Tabelle in `teams.md`.

Bestimme den SSH-Host anhand der aktuellen Umgebung und der Server-Gruppen-Tabelle in `teams.md`.

Fuer jedes erfolgreich gepushte Repo: Pruefe ob es auf dem Server existiert und pullen:

```bash
ssh [SSH-HOST] "cd ~/claude-projects/[projekt] && git pull --ff-only origin main" 2>&1
```

Regeln:
- Nur Repos die in Schritt 3 erfolgreich gepusht wurden
- `--ff-only` verwenden — bei Divergenz Warnung ausgeben, NICHT force-pullen
- SSH-Fehler (Timeout, Connection refused): Warnung, nicht abbrechen
- Server nicht erreichbar: Gesamten Sync-Schritt ueberspringen mit Hinweis

## Schritt 5: Ergebnis-Report

```
## Cross-Commit Ergebnis

**Erfolgreich:** ~/projekt-a, ~/projekt-b (je 1 Datei)
**Fehlgeschlagen:** ~/projekt-e (Push fehlgeschlagen)
**Uebersprungen:** ~/projekt-c, ~/projekt-d (keine Aenderungen)
**Nicht berechtigt:** ~/projekt-f (PB-Managed=nein)

**Server-Sync ([ssh-host]):**
  ✓ projekt-a, projekt-b (gepullt)
  ✗ projekt-e (Divergenz — manuell loesen)
  — projekt-c (nicht gepusht, kein Sync)

**⚠ Untracked files (nicht committed!):**
  ~/projekt-a: scripts/new-script, .claude/agents/new-agent.md
  ~/projekt-b: (keine)
```
