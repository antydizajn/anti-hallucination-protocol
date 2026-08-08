#!/usr/bin/env bash
# liveness_check.sh — answer "dzialaja mechanizmy antyhalucynacji?" with evidence.
#
# Checks the THREE separate things:
#   L1. Files/scripts present and functional (self-test).
#   L2. Scheduled jobs have actually executed (last_run_at fresh).
#   L3. Behavioral pipeline is being fed (calibration.jsonl growing).
#
# Self-apply rule: do not return "OK" just because the skill file exists.
# Each layer is reported independently with a verdict and the evidence string.

set -uo pipefail

DIR="$HOME/.hermes/scripts/anti_halluc"
SKILL_DIR="$HOME/.hermes/skills/software-development/anti-hallucination-protocol"
CRON_JOB_ID="1b4a422f7443"   # anti-halluc-self-audit (canonical job)
CALIB_LOG="$DIR/calibration.jsonl"
MAX_CALIB_STALE_HOURS=48     # if calibration log untouched for >48h, the habit died
MAX_CRON_STALE_HOURS=48      # daily cron should have run in last 48h

echo "==== anti-halluc liveness check — $(date '+%Y-%m-%d %H:%M:%S %Z') ===="

# ---- L1. Files / functional ----
echo ""
echo "L1. Files and self-test:"
[ -f "$SKILL_DIR/SKILL.md" ] && echo "  [OK]   skill SKILL.md present" \
                              || echo "  [FAIL] skill SKILL.md missing"
[ -x "$HOME/.hermes/scripts/verify_claim.sh" ] && echo "  [OK]   verify_claim.sh present and executable" \
                              || echo "  [FAIL] verify_claim.sh missing or not executable"
python3 -c "import sys; sys.path.insert(0, '$DIR'); import hard_assert" 2>/dev/null \
    && echo "  [OK]   hard_assert.py imports cleanly" \
    || echo "  [FAIL] hard_assert.py broken"
timeout 15 "$HOME/.hermes/scripts/verify_claim.sh" arxiv 2309.11495 >/dev/null 2>&1 \
    && echo "  [OK]   verify_claim.sh arxiv self-test passes (CoVe paper)" \
    || echo "  [FAIL] verify_claim.sh arxiv self-test failed"

# ---- L2. Cron actually running ----
echo ""
echo "L2. Scheduled cron last_run freshness:"
# Use hermes CLI to query the cron job; if not available, leave the check inconclusive.
if command -v hermes >/dev/null 2>&1; then
    LAST_RUN=$(hermes cron list 2>/dev/null | grep -A1 "$CRON_JOB_ID" | grep -oE 'last_run[^,]*' || true)
    echo "  job_id=$CRON_JOB_ID  $LAST_RUN"
    if echo "$LAST_RUN" | grep -q "null"; then
        echo "  [FAIL] cron job has last_run=null — never actually fired since creation"
        echo "         remedy: cronjob action=run job_id=$CRON_JOB_ID  (seed first run manually)"
    fi
else
    echo "  [SKIP] hermes CLI not on PATH; can't query cron state from shell."
    echo "         from agent: cronjob action=list, look for $CRON_JOB_ID last_run_at"
fi

# ---- L3. Behavioral pipeline ----
echo ""
echo "L3. Behavioral pipeline (calibration log fed):"
if [ -f "$CALIB_LOG" ]; then
    LINES=$(wc -l < "$CALIB_LOG" | tr -d ' ')
    # macOS stat -f, Linux stat -c
    if MTIME=$(stat -f %m "$CALIB_LOG" 2>/dev/null); then :; else MTIME=$(stat -c %Y "$CALIB_LOG"); fi
    NOW=$(date +%s)
    AGE_H=$(( (NOW - MTIME) / 3600 ))
    echo "  calibration.jsonl: $LINES entries, last modified ${AGE_H}h ago"
    if [ "$AGE_H" -gt "$MAX_CALIB_STALE_HOURS" ]; then
        echo "  [FAIL] calibration log untouched for >${MAX_CALIB_STALE_HOURS}h"
        echo "         the habit of logging claims has broken; verifiers exist but nobody calls them"
        echo "         remedy: this session, before any strong factual claim, run"
        echo "         python3 $DIR/calibration_log.py log \"<claim>\" <P_true>"
    else
        echo "  [OK]   calibration log fresh"
    fi
    if [ "$LINES" -lt 10 ]; then
        echo "  [WARN] only $LINES total entries — sample size too small for meaningful Brier score"
    fi
else
    echo "  [FAIL] calibration.jsonl missing entirely"
fi

# ---- L1 bonus: actual self-audit alert output ----
echo ""
echo "L1+. daily_self_audit.sh dry-run (alerts only):"
OUT=$(bash "$DIR/daily_self_audit.sh" 2>&1 || true)
if [ -z "$OUT" ]; then
    echo "  [OK]   silent — nothing to alert"
else
    echo "$OUT" | sed 's/^/  /'
fi

echo ""
echo "==== end liveness check ===="
