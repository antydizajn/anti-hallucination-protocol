#!/usr/bin/env bash
# liveness_check.sh - check whether the installed v5.1 skill and its narrow
# deterministic verifier are actually present and runnable.
#
# This script intentionally does NOT claim that model behavior is healthy merely
# because files exist. Legacy calibration/cron state is installation-specific and
# is reported only when those external artifacts are present.

set -uo pipefail

SKILL_DIR="${AHP_SKILL_DIR:-$HOME/.hermes/skills/software-development/anti-hallucination-protocol}"
VERIFY="$SKILL_DIR/scripts/verify_claim.py"
LEGACY_DIR="$HOME/.hermes/scripts/anti_halluc"
LEGACY_CALIB="$LEGACY_DIR/calibration.jsonl"

printf '==== anti-hallucination v5.1 liveness - %s ====\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"

echo
echo "L1. Installed skill and deterministic self-test:"
if [ -f "$SKILL_DIR/SKILL.md" ]; then
  echo "  [OK]   SKILL.md present"
else
  echo "  [FAIL] SKILL.md missing: $SKILL_DIR/SKILL.md"
fi

if [ -f "$VERIFY" ]; then
  echo "  [OK]   verify_claim.py present"
else
  echo "  [FAIL] verify_claim.py missing: $VERIFY"
fi

if command -v python3 >/dev/null 2>&1 && [ -f "$VERIFY" ]; then
  if python3 "$VERIFY" file-exists "$SKILL_DIR/SKILL.md" --kind file >/dev/null 2>&1; then
    echo "  [OK]   verify_claim.py self-test passed on installed SKILL.md"
  else
    echo "  [FAIL] verify_claim.py self-test failed"
  fi
else
  echo "  [SKIP] python3 or verifier unavailable"
fi

echo
echo "L2. Structural checker:"
INTEGRITY="$SKILL_DIR/scripts/check_v5_integrity.py"
if command -v python3 >/dev/null 2>&1 && [ -f "$INTEGRITY" ]; then
  if python3 "$INTEGRITY" --root "$SKILL_DIR" >/dev/null 2>&1; then
    echo "  [OK]   repository-local integrity checker passed"
  else
    echo "  [FAIL] repository-local integrity checker failed"
  fi
else
  echo "  [SKIP] check_v5_integrity.py unavailable"
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
  echo "  [INFO] this legacy log is not part of v5.1's portable correctness contract"
else
  echo "  [INFO] no legacy calibration pipeline detected - this is not a v5.1 failure"
fi

echo
echo "L4. Behavioral/runtime enforcement:"
echo "  [UNKNOWN] Markdown + local deterministic checks cannot prove that an LLM"
echo "            followed the protocol in real conversations. Measure that with"
echo "            an external Hermes behavioral benchmark or runtime gate."

echo
printf '%s\n' '==== end liveness check ===='
