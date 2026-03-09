#!/bin/bash
# Injiziert Kernprinzipien nach Auto-Compaction.
# Feuert via SessionStart(compact) -- genau wenn Kontext komprimiert wurde
# und fruehe Instruktionen verloren gehen koennten.

cat <<'EOF'
{
  "additionalContext": "NACH COMPACTION -- KRITISCHE ERINNERUNGEN:\n1. Du bist Architekt, nicht Bauarbeiter. Delegiere an Skills/Agents.\n2. Skill-First. Pruefe bei jeder Aufgabe zuerst ob ein Skill existiert.\n3. Kontextschutz. Knowledge nur bei Bedarf laden. Zwischenergebnisse in Dateien, nicht im Chat.\n4. Reviewer-Funktion. Outputs von Skills/Agents kritisch pruefen, nicht durchreichen.\n5. /track bei Sessionende. Projektstatus aktualisieren, dann fragen ob committen."
}
EOF
