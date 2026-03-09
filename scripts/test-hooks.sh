#!/bin/bash
# Tier A: Mechanische Hook-Tests
# Automatisiert alle deterministischen Tests fuer block-foreign-commits.sh
# und post-compaction-reminder.sh
#
# Usage: ./scripts/test-hooks.sh
# Kann von ueberall ausgefuehrt werden.

set -euo pipefail

PASS=0
FAIL=0
EXPECTED_FAIL=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
HOOK_DIR="$PROJECT_DIR/.claude/hooks"

# Temp-Repo als "fremdes Repo" fuer Tests
FOREIGN_REPO=$(mktemp -d)
git -C "$FOREIGN_REPO" init --quiet
trap "rm -rf $FOREIGN_REPO" EXIT

pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }
expected_fail() { echo "  EXPECTED FAIL: $1"; EXPECTED_FAIL=$((EXPECTED_FAIL + 1)); }

# Helper: Simuliert Hook-Input mit variablen Pfaden
run_hook() {
  local cmd="$1" cwd="$2" env_project_dir="${3:-$PROJECT_DIR}"
  echo "{\"tool_input\":{\"command\":\"$cmd\"},\"cwd\":\"$cwd\"}" | \
    CLAUDE_PROJECT_DIR="$env_project_dir" \
    "$HOOK_DIR/block-foreign-commits.sh" 2>/dev/null
}

echo "=== Tier A: Mechanische Hook-Tests ==="
echo ""

# --- A1-A5: block-foreign-commits.sh ---
echo "--- A1-A5: block-foreign-commits.sh ---"

echo ""
echo "A1: Commit in fremdem Repo..."
OUTPUT=$(run_hook "git commit -m test" "$FOREIGN_REPO")
if echo "$OUTPUT" | grep -q '"permissionDecision".*"deny"'; then
  pass "A1 -- commit in fremdem Repo geblockt"
else
  fail "A1 -- commit in fremdem Repo NICHT geblockt. Output: $OUTPUT"
fi

echo "A2: Commit im eigenen Repo..."
OUTPUT=$(run_hook "git commit -m test" "$PROJECT_DIR")
if [ -z "$OUTPUT" ]; then
  pass "A2 -- commit im eigenen Repo erlaubt"
else
  fail "A2 -- commit im eigenen Repo unerwartet geblockt. Output: $OUTPUT"
fi

echo "A3: Nicht-git-Command..."
OUTPUT=$(run_hook "rm -rf /" "$FOREIGN_REPO")
if [ -z "$OUTPUT" ]; then
  pass "A3 -- nicht-git-Command passiert"
else
  fail "A3 -- nicht-git-Command unerwartet geblockt. Output: $OUTPUT"
fi

echo "A4: Push in fremdem Repo..."
OUTPUT=$(run_hook "git push origin main" "$FOREIGN_REPO")
if echo "$OUTPUT" | grep -q '"permissionDecision".*"deny"'; then
  pass "A4 -- push in fremdem Repo geblockt"
else
  fail "A4 -- push in fremdem Repo NICHT geblockt. Output: $OUTPUT"
fi

echo "A5: Compound command..."
OUTPUT=$(run_hook "git add . && git commit -m test" "$FOREIGN_REPO")
if echo "$OUTPUT" | grep -q '"permissionDecision".*"deny"'; then
  pass "A5 -- compound command geblockt"
else
  fail "A5 -- compound command NICHT geblockt. Output: $OUTPUT"
fi

# --- A6-A7: post-compaction-reminder.sh ---
echo ""
echo "--- A6-A7: post-compaction-reminder.sh ---"

echo "A6: JSON + 5 Prinzipien..."
RESULT=$("$HOOK_DIR/post-compaction-reminder.sh" | python3 -c "
import sys, json
data = json.load(sys.stdin)
ctx = data.get('additionalContext','')
checks = ['Architekt', 'Skill-First', 'Kontextschutz', 'Reviewer', '/track']
missing = [c for c in checks if c not in ctx]
if missing: print(f'MISSING:{missing}'); sys.exit(1)
print('OK')
" 2>&1) || true
if [ "$RESULT" = "OK" ]; then
  pass "A6 -- valides JSON, alle 5 Prinzipien enthalten"
else
  fail "A6 -- $RESULT"
fi

echo "A7: Prinzipien-Alignment mit main-agent.md -- MANUELL pruefen"

# --- A8: Hook-Konfiguration ---
echo ""
echo "--- A8: Hook-Konfiguration ---"

echo "A8: settings.json + executable..."
CONFIG_OK=$(python3 -c "
import json
with open('$PROJECT_DIR/.claude/settings.json') as f: data = json.load(f)
hooks = data.get('hooks', {})
pre = hooks.get('PreToolUse', [])
sess = hooks.get('SessionStart', [])
ok = True
if not pre or pre[0].get('matcher') != 'Bash': print('FAIL: PreToolUse matcher'); ok = False
if not sess or sess[0].get('matcher') != 'compact': print('FAIL: SessionStart matcher'); ok = False
if ok: print('OK')
" 2>&1)
if [ "$CONFIG_OK" = "OK" ]; then
  pass "A8a -- settings.json Matcher korrekt"
else
  fail "A8a -- $CONFIG_OK"
fi

if test -x "$HOOK_DIR/block-foreign-commits.sh"; then
  pass "A8b -- block-foreign-commits.sh executable"
else
  fail "A8b -- block-foreign-commits.sh nicht executable"
fi

if test -x "$HOOK_DIR/post-compaction-reminder.sh"; then
  pass "A8c -- post-compaction-reminder.sh executable"
else
  fail "A8c -- post-compaction-reminder.sh nicht executable"
fi

# --- D1-D3: Edge Cases ---
echo ""
echo "--- D1-D3: Edge Cases ---"

echo "D1: Fallback ohne CLAUDE_PROJECT_DIR..."
OUTPUT=$(run_hook "git commit -m test" "$FOREIGN_REPO" "")
if echo "$OUTPUT" | grep -q '"permissionDecision".*"deny"'; then
  pass "D1 -- Fallback funktioniert, trotzdem deny"
else
  fail "D1 -- Fallback versagt. Output: $OUTPUT"
fi

echo "D2: Malformed JSON..."
OUTPUT=$(echo 'not json' | \
  CLAUDE_PROJECT_DIR="$PROJECT_DIR" \
  "$HOOK_DIR/block-foreign-commits.sh" 2>/dev/null)
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] && [ -z "$OUTPUT" ]; then
  pass "D2 -- malformed JSON: kein Crash, exit 0, kein Output"
else
  fail "D2 -- malformed JSON: exit=$EXIT_CODE, output=$OUTPUT"
fi

echo "D3: git -C Flag (Expected Failure)..."
OUTPUT=$(run_hook "git -C $FOREIGN_REPO commit -m test" "$PROJECT_DIR")
if echo "$OUTPUT" | grep -q '"permissionDecision".*"deny"'; then
  pass "D3 -- git -C wurde unerwartet erkannt (Blindspot behoben?)"
else
  expected_fail "D3 -- git -C nicht erkannt (bekannter Blindspot, Hook prueft CWD nicht -C Flag)"
fi

# --- Zusammenfassung ---
echo ""
echo "==============================="
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  EXPECTED FAIL: $EXPECTED_FAIL"
echo "==============================="

if [ $FAIL -gt 0 ]; then
  exit 1
fi
exit 0
