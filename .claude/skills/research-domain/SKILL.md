---
name: research-domain
description: Recherchiert Domaenenwissen fuer ein neues Agent-Team. Wird vom Main-Agent nach dem Interview aufgerufen, wenn die Domaene unbekannt ist.
argument-hint: "[domaene + ziel + konkrete fragen]"
allowed-tools: "Read, Write, Bash, Glob, Grep, WebSearch, WebFetch"
context: fork
model: sonnet
---

Du recherchierst Domaenenwissen fuer ein geplantes Agent-Team. Dein Ziel: Dem Main-Agent eine fundierte Grundlage liefern, damit er Domaenenwissen und Architektur-Wissen verschmelzen kann (Phase 3: Synthese).

## Input

Du bekommst als $ARGUMENTS:
- Die Domaene (z.B. "Rails-Codebase-Maintenance", "E-Commerce-Content")
- Das Ziel des Teams
- Konkrete Fragen aus dem Interview (Phase 1)
- Was bereits bekannt ist (optional)

## Vorgehen

### 1. Bestehende Erfahrung pruefen

Lies `reference/domain-learnings.md` (falls vorhanden). Wurde fuer eine aehnliche Domaene schon recherchiert? Falls ja: Nutze als Ausgangsbasis, recherchiere nur Luecken.

### 2. Recherchieren

Suche im Web nach:
- **Best Practices** fuer die Domaene (etablierte Workflows, bewaehrte Methoden)
- **Tools und Standards** (was nutzt die Community, welche Standards gelten)
- **Typische Fallstricke** (was geht oft schief, welche Anti-Patterns gibt es)
- **Bewertete Ansaetze** (was funktioniert gut, was wird kritisiert)

Fokus auf **verwertbare** Erkenntnisse -- keine allgemeinen Einfuehrungstexte. Suche gezielt nach den konkreten Fragen aus dem Interview.

### 3. Zwei Outputs schreiben

**Output 1: Research-Briefing** (fuer den Main-Agent zur Synthese)
→ `briefings/research-[domaene-slug].md`

```markdown
# Research-Briefing: [Domaene]

## Kernerkenntnisse
[5-10 Bullets: konkrete, verwertbare Erkenntnisse]

## Relevante Tools und Standards
[Was sollte das Team kennen/nutzen? Mit Kurzbeschreibung.]

## Typische Fallstricke
[Was geht oft schief? Konkrete Szenarien.]

## Architektur-Impulse
[Was bedeutet das fuer die Team-Struktur? Welche Rollen/Skills ergeben sich aus der Recherche?]

## Offene Fragen
[Was konnte nicht geklaert werden? Wo braeuchte man mehr Kontext?]
```

**Output 2: Domain-Knowledge** (geht ins neue Team)
→ `briefings/domain-knowledge-[domaene-slug].md`

```markdown
# [Domaene]: Wissensgrundlage

## Best Practices
[Verdichtetes Domaenenwissen -- das Team soll damit arbeiten koennen]

## Tools und Standards
[Relevante Werkzeuge mit Kurzbeschreibung und wann einsetzen]

## Bekannte Fallstricke
[Was vermeiden, worauf achten -- konkrete Warnsignale]

## Quellen
- [URL] -- [Kurzbeschreibung, was diese Quelle beigetragen hat]
```

### 4. Zusammenfassung

Gib dem Main-Agent zurueck:
- Anzahl recherchierter Quellen
- Die 3-5 wichtigsten Erkenntnisse (Bullets)
- Vorschlaege fuer die Team-Architektur die sich aus der Recherche ergeben
- Verweis auf beide Output-Dateien
- Offene Fragen (falls vorhanden)
