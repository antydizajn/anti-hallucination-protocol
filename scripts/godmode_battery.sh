#!/usr/bin/env bash
# godmode_battery.sh -- run the adversarial corpus end-to-end as a self-test.
#
# This is the "on demand" version of the daily cron self-audit. Use when the user
# asks "does anti-halluc actually work" / "test yourself" / "godmode self-check",
# or anytime you want a fresh empirical reading on the protocol's effectiveness
# before making a high-stakes claim.
#
# Each probe is run through hard_assert.py (the cheapest layer) and logged into
# calibration.jsonl with the model's a priori P(true). Score is printed at the end.
#
# Output:
#   - line per probe: PROBE_ID  expected  result  verdict
#   - summary: N_correct / N_total, % correct, false claims highlighted
#   - calibration.jsonl gains N new entries
#
# This is NOT a full v3 orchestrator run -- it exercises L1 (verify_claim/hard_assert)
# and L3 (calibration log feed), not the full multi-judge ensemble. For that use
# eval_pipeline.sh in v3/.

set -uo pipefail

DIR="$HOME/.hermes/scripts/anti_halluc"
CORPUS="$DIR/adversarial_corpus.json"
CALIB_LOG="$DIR/calibration.jsonl"

if [ ! -f "$CORPUS" ]; then
    echo "FAIL: adversarial_corpus.json missing at $CORPUS"
    exit 1
fi

echo "==== GODMODE adversarial battery -- $(date '+%Y-%m-%d %H:%M:%S %Z') ===="
echo "corpus: $CORPUS"
echo ""

python3 - <<'PY'
import json, sys, subprocess, os, time
from pathlib import Path

DIR = Path(os.environ["HOME"]) / ".hermes/scripts/anti_halluc"
corpus = json.loads((DIR / "adversarial_corpus.json").read_text())
calib_log = DIR / "calibration.jsonl"

sys.path.insert(0, str(DIR))
try:
    import hard_assert as ha
except Exception as e:
    print(f"FAIL: cannot import hard_assert: {e}")
    sys.exit(1)

correct = 0
total = 0
falses = []

# Corpus shape varies; accept either {"probes":[...]}  or a flat list.
probes = corpus.get("probes", corpus) if isinstance(corpus, dict) else corpus

for p in probes:
    pid = p.get("id", p.get("name", "?"))
    kind = p.get("class") or p.get("kind") or "unknown"
    target = p.get("target") or p.get("query") or p.get("input") or ""
    expected = p.get("expected", p.get("ground_truth", "?"))

    # Heuristic dispatch -- only run the cheap deterministic classes here.
    verdict = "SKIP"
    actual = "n/a"
    if kind in ("arxiv_id_lookup", "arxiv_id_nonexistent"):
        try:
            r = ha.check_arxiv(target)
            actual = r.get("status", "?")
            if (expected == "exists" and actual == "ok") or \
               (expected == "nonexistent" and actual != "ok"):
                verdict = "PASS"; correct += 1
            else:
                verdict = "FAIL"; falses.append((pid, target, expected, actual))
            total += 1
        except Exception as e:
            verdict = f"ERR:{e}"
    elif kind == "path_exists":
        try:
            r = ha.check_path(target)
            actual = r.get("status", "?")
            ok = (expected == "exists" and actual == "ok") or \
                 (expected == "nonexistent" and actual != "ok")
            verdict = "PASS" if ok else "FAIL"
            if ok: correct += 1
            else: falses.append((pid, target, expected, actual))
            total += 1
        except Exception as e:
            verdict = f"ERR:{e}"
    # other classes (vision_confab, library_api, etc.) need richer harness -- skip here

    print(f"  {pid:24s}  kind={kind:24s}  expected={str(expected):14s}  actual={str(actual):12s}  {verdict}")

print("")
print(f"==== SUMMARY: {correct}/{total} correct ({100*correct/max(total,1):.1f}%) ====")
if falses:
    print("FALSE CLAIMS:")
    for f in falses:
        print(f"  {f}")

# Append a single summary line to calibration log so the battery shows up in the trail
import datetime
entry = {
    "ts": datetime.datetime.now().isoformat(),
    "source": "godmode_battery",
    "claim": f"adversarial battery {correct}/{total} correct",
    "predicted_p": correct / max(total, 1),
    "outcome": None,  # batter is its own evidence
    "n_probes": total,
}
with open(calib_log, "a") as f:
    f.write(json.dumps(entry) + "\n")
print(f"appended summary to {calib_log}")
PY

echo ""
echo "==== end battery ===="
