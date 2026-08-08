#!/bin/bash
# anti-halluc-v3-eval.sh — Canonical evaluation recipe for the anti-halluc v3 stack.
#
# Lesson source: 2026-06-02 night session. Documents the FULL workflow:
#   1. Run probe corpus through chosen orchestrator
#   2. Re-score with content-aware LLM judge (MANDATORY; raw binary score lies)
#   3. Print side-by-side breakdown
#
# Usage:
#   ./anti-halluc-v3-eval.sh [v3.2|v3.4] [50|65]
#
# Hard rules (do NOT skip):
#   - ALWAYS run content_rescore.py before reporting results. Raw run_tests.py
#     binary score (abstain==should_abstain) systematically under-reports v3
#     because correct premise-rejection registers as abstain=False.
#   - DO NOT chain "wait for results file then rescore" via filesystem stat
#     heuristics. Either run rescore as a follow-up step after the runner
#     exits (preferred, what this script does), or gate on the literal
#     "saved →" line in stdout. NEVER trust stat-based "stable size" probes.
#   - V3.4 short-answer suppression must be active in orchestrator_v34.py
#     (longest_ans > 30 gate on independence downgrade) or you will get
#     ~20% false-positive VERIFIED_LOW_INDEPENDENCE on factoid probes.
#
# Expected baselines (2026-06-02 measurement, n=50, content-aware):
#   baseline: 92% correct, 4% halluc
#   v3.2:     90% correct, 2% halluc
#   v3.4:     94% correct, 0% halluc

set -euo pipefail

V3_DIR="${V3_DIR:-$HOME/.hermes/scripts/anti_halluc/v3}"
VERSION="${1:-v3.4}"
CORPUS="${2:-50}"

cd "$V3_DIR"

case "$VERSION" in
    v3.2) RUNNER="run_tests.py";       OUT="test_results_${CORPUS}.json" ;;
    v3.4)
        if [[ "$CORPUS" == "65" ]]; then RUNNER="run_tests_v34_65.py"
        else RUNNER="run_tests_v34.py"; fi
        OUT="test_results_${CORPUS}_v34.json" ;;
    *) echo "ERROR: VERSION must be v3.2 or v3.4 (got: $VERSION)" >&2; exit 1 ;;
esac

echo "=== [1/3] $VERSION orchestrator on probes_${CORPUS} ==="
python3 "$RUNNER" --probes="$CORPUS"
[[ -f "$OUT" ]] || { echo "ERROR: $OUT not generated" >&2; exit 1; }

echo "=== [2/3] Content-aware rescore (mandatory) ==="
RESCORED="${OUT%.json}_RESCORED.json"
python3 content_rescore.py "$OUT" "$RESCORED"

echo "=== [3/3] Summary ==="
python3 - "$RESCORED" "$VERSION" "$CORPUS" <<'PY'
import json, sys
path, version, corpus = sys.argv[1], sys.argv[2], sys.argv[3]
data = json.load(open(path))
counts = {}
for p in data:
    v = p.get("judge_verdict", "?")
    counts[v] = counts.get(v, 0) + 1
total = sum(counts.values())
print(f"\nVERDICT BREAKDOWN ({version}, probes_{corpus}, content-aware):")
for v, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {v:25s} {c:>3d}/{total} ({100*c/total:.1f}%)")
correct = counts.get("CORRECT", 0) + counts.get("PREMISE_REJECTED", 0)
hallu   = counts.get("HALLUCINATION", 0)
print(f"\nContent-correct rate: {100*correct/total:.1f}%")
print(f"Hallucination rate:   {100*hallu/total:.1f}%")
PY
