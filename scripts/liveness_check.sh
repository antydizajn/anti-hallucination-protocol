#!/usr/bin/env bash
# liveness_check.sh - check whether the installed v5.4.1 skill and its narrow
# deterministic verifier are actually present and runnable.
#
# Required portable checks are L1/L2. Any failure or inability to execute a
# required check makes this script exit nonzero. L3 is optional legacy telemetry.
# L4 remains UNKNOWN by design because file presence cannot prove model behavior.

set -uo pipefail

SKILL_DIR="${AHP_SKILL_DIR:-$HOME/.hermes/skills/software-development/anti-hallucination-protocol}"
VERIFY="$SKILL_DIR/scripts/verify_claim.py"
INTEGRITY="$SKILL_DIR/scripts/check_v5_integrity.py"
LEGACY_DIR="$HOME/.hermes/scripts/anti_halluc"
LEGACY_CALIB="$LEGACY_DIR/calibration.jsonl"
STATUS=0

fail_required() {
  printf '  [FAIL] %s\n' "$1"
  STATUS=1
}

printf '==== anti-hallucination v5.4.1 liveness - %s ====\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"

echo
echo "L1. Installed skill and deterministic self-tests:"
if [ -f "$SKILL_DIR/SKILL.md" ]; then
  echo "  [OK]   SKILL.md present"
else
  fail_required "SKILL.md missing: $SKILL_DIR/SKILL.md"
fi

if [ -f "$VERIFY" ]; then
  echo "  [OK]   verify_claim.py present"
else
  fail_required "verify_claim.py missing: $VERIFY"
fi

if ! command -v python3 >/dev/null 2>&1; then
  fail_required "python3 unavailable; required verifier self-tests cannot run"
elif [ ! -f "$VERIFY" ]; then
  fail_required "verifier unavailable; required self-tests cannot run"
else
  python3 "$VERIFY" file-exists "$SKILL_DIR/SKILL.md" --kind file >/dev/null 2>&1
  EXISTS_CODE=$?
  python3 "$VERIFY" file-contains "$SKILL_DIR/SKILL.md" "anti-hallucination-protocol" >/dev/null 2>&1
  CONTAINS_CODE=$?
  python3 "$VERIFY" file-contains "$SKILL_DIR/SKILL.md" "" >/dev/null 2>&1
  EMPTY_CONTAINS_CODE=$?
  python3 "$VERIFY" file-line "$SKILL_DIR/SKILL.md" 1 "" >/dev/null 2>&1
  EMPTY_LINE_CODE=$?

  if [ "$EXISTS_CODE" -eq 0 ] && [ "$CONTAINS_CODE" -eq 0 ] && [ "$EMPTY_CONTAINS_CODE" -eq 2 ] && [ "$EMPTY_LINE_CODE" -eq 2 ]; then
    echo "  [OK]   verify_claim.py self-tests passed (existence, content, empty-match rejection)"
  else
    fail_required "verify_claim.py self-test failed (exists=$EXISTS_CODE contains=$CONTAINS_CODE empty_contains=$EMPTY_CONTAINS_CODE empty_line=$EMPTY_LINE_CODE)"
  fi
fi

echo
echo "L2. Structural checker:"
if ! command -v python3 >/dev/null 2>&1; then
  fail_required "python3 unavailable; structural checker cannot run"
elif [ ! -f "$INTEGRITY" ]; then
  fail_required "check_v5_integrity.py unavailable: $INTEGRITY"
elif python3 "$INTEGRITY" --root "$SKILL_DIR" >/dev/null 2>&1; then
  echo "  [OK]   v5.4.1 repository-local integrity checker passed"
else
  fail_required "v5.4.1 repository-local integrity checker failed"
fi

echo
echo "L3. Optional legacy installation telemetry:"
if [ -f "$LEGACY_CALIB" ]; then
  LINES=$(wc -l < "$LEGACY_CALIB" | tr -d ' ')
  if MTIME=$(stat -f %m "$LEGACY_CALIB" 2>/dev/null); then :; else MTIME=$(stat -c %Y "$LEGACY_CALIB" 2>/dev/null || echo 0); fi
  NOW=$(date +%s)
  if [ "$MTIME" -gt 0 ]; then
    AGE_H=$(( (NOW - MTIME) / 3600 ))
    echo "  [INFO] legacy calibration.jsonl: $LINES entries, modified ${AGE_H}h ago"
  else
    echo "  [INFO] legacy calibration.jsonl exists; mtime unavailable"
  fi
  echo "  [INFO] this legacy log is not part of v5.4.1's portable correctness contract"
else
  echo "  [INFO] no legacy calibration pipeline detected - this is not a v5.4.1 failure"
fi

echo
echo "L4. Behavioral/runtime enforcement:"
echo "  [UNKNOWN] Markdown + local deterministic checks cannot prove that an LLM"
echo "            followed the protocol in real conversations. Measure that with"
echo "            an external Hermes behavioral benchmark or runtime gate."

echo
if [ "$STATUS" -eq 0 ]; then
  printf '%s\n' '==== end liveness check: PASS (portable L1/L2) ===='
else
  printf '%s\n' '==== end liveness check: FAIL (portable L1/L2) ===='
fi
exit "$STATUS"
