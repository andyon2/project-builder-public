# Offene Widersprueche & Ungeklaerte Fragen

Dieses Dokument sammelt Konflikte zwischen Quellen und offene Fragen, die nicht leise aufgeloest werden duerfen. Jeder Eintrag bleibt stehen, bis er durch Praxistest, neue Quellen oder eine bewusste Entscheidung aufgeloest wird.

## Format

```
## [Kurztitel]
- **Position A** ([Quelle]): [Zusammenfassung]
- **Position B** ([Quelle]): [Zusammenfassung]
- **Aktueller Stand:** [Ungeloest / Tendenz zu A/B / Aufgeloest]
- **Naechster Schritt:** [Was wuerde die Frage klaeren?]
- **Aufgeloest am:** [Datum, falls erledigt -- dann in "Aufgeloeste" Sektion verschieben]
```

---

## Offene Widersprueche

_Aktuell keine offenen Widersprueche._

---

## Aufgeloeste Widersprueche

### Supabase CLI vs. MCP in Dispatches

- **Position A** (skill-best-practices.md, CLI>MCP-Prinzip): Supabase CLI > Supabase MCP. Immer CLI bevorzugen.
- **Position B** (Dispatch, 2026-03-13): Empfahl urspruenglich Supabase MCP-Server direkt, ohne CLI-Abgleich.
- **Loesung:** Dispatch korrigiert: CLI bevorzugen, MCP als Fallback fuer Features ohne CLI-Aequivalent. Fehlrouting behoben.
- **Learning fuer /learn:** Bei Dispatches immer gegen eigene Knowledge pruefen. Bestehende Prinzipien haben Vorrang.
- **Aufgeloest am:** 2026-03-13

### maxTurns als Pflicht fuer Fork-Skills

- **Position A** (main-agent.md, build-team, team-reflection): "maxTurns ist Pflicht in jedem Agent und Fork-Skill."
- **Position B** (Anthropic-Doku, Skill-YAML-Spezifikation): Fork-Skills unterstuetzen kein maxTurns-Feld im YAML-Header. Nur Agents haben maxTurns.
- **Loesung:** Prinzip korrigiert: model ist Pflicht fuer Agents + Fork-Skills, maxTurns ist Pflicht nur fuer Agents. Bei Fork-Skills mit Runaway-Risiko: agent:-Feld als Escape Hatch (referenziert Agent mit maxTurns).
- **Learning:** Prinzipien gegen die tatsaechliche API validieren bevor sie in Knowledge landen. Nicht aus der Agent-Welt auf Skills uebertragen ohne Pruefung.
- **Aufgeloest am:** 2026-03-13
