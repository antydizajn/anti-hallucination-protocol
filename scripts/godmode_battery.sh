#!/usr/bin/env bash
# godmode_battery.sh - LEGACY installation-specific diagnostic.
#
# This script is retained for existing installations that still have the old
# ~/.hermes/scripts/anti_halluc corpus + hard_assert.py stack. It is NOT part of
# the portable v5.4 correctness/liveness contract.
#
# Safety changes introduced in v5.3 and retained in v5.4:
#   - read-only by default;
#   - no implicit calibration.jsonl append;
#   - prints attempted/skipped/errors separately;
#   - false probes or execution errors produce non-zero exit status;
#   - optional logging requires an explicit --calibration-log PATH.

set -uo pipefail

DIR="$HOME/.hermes/scripts/anti_halluc"
CORPUS="$DIR/adversarial_corpus.json"
CALIB_LOG=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)
            [[ $# -ge 2 ]] || { echo "ERROR: --dir requires a path" >&2; exit 2; }
            DIR="$2"; CORPUS="$DIR/adversarial_corpus.json"; shift 2 ;;
        --corpus)
            [[ $# -ge 2 ]] || { echo "ERROR: --corpus requires a path" >&2; exit 2; }
            CORPUS="$2"; shift 2 ;;
        --calibration-log)
            [[ $# -ge 2 ]] || { echo "ERROR: --calibration-log requires a path" >&2; exit 2; }
            CALIB_LOG="$2"; shift 2 ;;
        -h|--help)
            cat <<'EOF'
Usage: godmode_battery.sh [--dir PATH] [--corpus FILE] [--calibration-log FILE]

Read-only by default. --calibration-log explicitly opts into writing one
summary record after a run with zero execution errors.
EOF
            exit 0 ;;
        *) echo "ERROR: unknown argument: $1" >&2; exit 2 ;;
    esac
done

if [[ ! -f "$CORPUS" ]]; then
    echo "FAIL: adversarial corpus missing at $CORPUS" >&2
    exit 2
fi

export AHP_LEGACY_DIR="$DIR"
export AHP_LEGACY_CORPUS="$CORPUS"
export AHP_LEGACY_CALIB_LOG="$CALIB_LOG"

echo "==== LEGACY adversarial battery - $(date '+%Y-%m-%d %H:%M:%S %Z') ===="
echo "corpus: $CORPUS"
[[ -n "$CALIB_LOG" ]] && echo "explicit calibration log: $CALIB_LOG" || echo "calibration log: disabled (read-only mode)"
echo

python3 - <<'PY'
import datetime
import json
import os
import sys
from pathlib import Path

base = Path(os.environ["AHP_LEGACY_DIR"])
corpus_path = Path(os.environ["AHP_LEGACY_CORPUS"])
calib_raw = os.environ.get("AHP_LEGACY_CALIB_LOG", "")
calib_log = Path(calib_raw) if calib_raw else None

try:
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"ERROR: cannot load corpus: {exc}", file=sys.stderr)
    raise SystemExit(2)

sys.path.insert(0, str(base))
try:
    import hard_assert as ha
except Exception as exc:
    print(f"ERROR: cannot import hard_assert: {exc}", file=sys.stderr)
    raise SystemExit(2)

probes = corpus.get("probes", corpus) if isinstance(corpus, dict) else corpus
if not isinstance(probes, list):
    print("ERROR: corpus must be a list or an object containing list field 'probes'", file=sys.stderr)
    raise SystemExit(2)

correct = 0
attempted = 0
skipped = 0
errors = 0
falses = []

for p in probes:
    if not isinstance(p, dict):
        errors += 1
        print("  ?  ERR: probe is not an object")
        continue

    pid = str(p.get("id", p.get("name", "?")))
    kind = p.get("class") or p.get("kind") or "unknown"
    target = p.get("target") or p.get("query") or p.get("input") or ""
    expected = p.get("expected", p.get("ground_truth", "?"))
    verdict = "SKIP"
    actual = "n/a"

    try:
        if kind in ("arxiv_id_lookup", "arxiv_id_nonexistent"):
            attempted += 1
            r = ha.check_arxiv(target)
            actual = r.get("status", "?")
            ok = (expected == "exists" and actual == "ok") or (
                expected == "nonexistent" and actual != "ok"
            )
            if ok:
                verdict = "PASS"; correct += 1
            else:
                verdict = "FAIL"; falses.append((pid, target, expected, actual))
        elif kind == "path_exists":
            attempted += 1
            r = ha.check_path(target)
            actual = r.get("status", "?")
            ok = (expected == "exists" and actual == "ok") or (
                expected == "nonexistent" and actual != "ok"
            )
            if ok:
                verdict = "PASS"; correct += 1
            else:
                verdict = "FAIL"; falses.append((pid, target, expected, actual))
        else:
            skipped += 1
    except Exception as exc:
        errors += 1
        verdict = f"ERR:{exc}"

    print(
        f"  {pid:24s} kind={str(kind):24s} expected={str(expected):14s} "
        f"actual={str(actual):12s} {verdict}"
    )

print()
rate = 100 * correct / max(attempted, 1)
print(
    f"==== SUMMARY: attempted={attempted} correct={correct} "
    f"failed={len(falses)} skipped={skipped} errors={errors} "
    f"attempted_accuracy={rate:.1f}% ===="
)
if falses:
    print("FALSE CLAIMS:")
    for item in falses:
        print(f"  {item}")

if calib_log is not None:
    if errors:
        print("NOT WRITING calibration log because execution errors occurred", file=sys.stderr)
    else:
        entry = {
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "source": "legacy_godmode_battery",
            "claim": f"legacy supported-subset battery {correct}/{attempted} correct",
            "attempted": attempted,
            "correct": correct,
            "failed": len(falses),
            "skipped": skipped,
            "errors": errors,
        }
        calib_log.parent.mkdir(parents=True, exist_ok=True)
        with calib_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
        print(f"appended explicit summary to {calib_log}")

if errors:
    raise SystemExit(2)
if falses:
    raise SystemExit(1)
raise SystemExit(0)
PY
status=$?

echo
echo "==== end legacy battery (exit=$status) ===="
exit "$status"
