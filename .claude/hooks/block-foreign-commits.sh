#!/bin/bash
# Blockt git commit/push in fremden Repos.
# Regel: Dateien editieren OK, aber NIE committen/pushen ausserhalb des eigenen Projekts.
# Keine jq-Abhaengigkeit -- parst JSON mit python3 (ueberall verfuegbar).

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)
CWD=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null)

# Nur git commit/push pruefen
if echo "$COMMAND" | grep -qE 'git\s+(commit|push)'; then
  # Repo-Root des Hooks (= unser Projekt)
  OUR_REPO="$(cd "$CLAUDE_PROJECT_DIR" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null)"
  # Fallback wenn CLAUDE_PROJECT_DIR nicht gesetzt
  if [[ -z "$OUR_REPO" ]]; then
    HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
    OUR_REPO="$(cd "$HOOK_DIR" && git rev-parse --show-toplevel 2>/dev/null)"
  fi

  # Repo-Root des Zielverzeichnisses
  TARGET_REPO="$(cd "$CWD" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null)"

  if [[ -n "$OUR_REPO" && -n "$TARGET_REPO" && "$OUR_REPO" != "$TARGET_REPO" ]]; then
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "BLOCKED: Git commit/push in fremdem Repo ($TARGET_REPO). Starte den Agent in dem Projekt und lass ihn selbst committen."
  }
}
EOF
    exit 0
  fi
fi

exit 0
