#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: collect_run.sh <rep-slug> <ARM> <profile> <session-id>" >&2
}
[[ $# -eq 4 ]] || { usage; exit 64; }
REP="$1"
ARM="$2"
PROFILE="$3"
SESSION="$4"
[[ "$REP" =~ ^[a-z0-9][a-z0-9_-]{0,31}$ ]] || { echo "ERROR: invalid rep-slug" >&2; exit 64; }
[[ "$ARM" =~ ^[ABC]$ ]] || { echo "ERROR: arm must be A/B/C" >&2; exit 64; }

EXPECTED_PROFILE="ahpbench-${REP}-$(tr 'ABC' 'abc' <<<"$ARM")"
[[ "$PROFILE" == "$EXPECTED_PROFILE" ]] || {
  echo "ERROR: profile/arm mismatch. Expected $EXPECTED_PROFILE, got $PROFILE" >&2
  exit 65
}

BENCH_HOME="${AHP_BENCH_HOME:-$HOME/ahp-benchmark-v01}"
OUT="$BENCH_HOME/runs/$REP/$ARM"
mkdir -p "$OUT"

command -v hermes >/dev/null || { echo "ERROR: hermes missing" >&2; exit 69; }
command -v python3 >/dev/null || { echo "ERROR: python3 missing" >&2; exit 69; }
hermes profile show "$PROFILE" >/dev/null 2>&1 || { echo "ERROR: profile not found: $PROFILE" >&2; exit 2; }

# Exact profile + exact session. No implicit latest/default session is accepted.
# JSONL is the machine-readable full session export. Trace is a separate
# redacted-by-default trajectory representation. HTML is the readable transcript.
hermes -p "$PROFILE" sessions export "$OUT/session.jsonl" --session-id "$SESSION" --format jsonl
hermes -p "$PROFILE" sessions export "$OUT/trace.jsonl" --session-id "$SESSION" --format trace
hermes -p "$PROFILE" sessions export "$OUT/transcript.html" --session-id "$SESSION" --format html --redact

for required in session.jsonl trace.jsonl transcript.html; do
  [[ -s "$OUT/$required" ]] || {
    echo "ERROR: missing or empty export artifact: $OUT/$required" >&2
    exit 3
  }
done

python3 - "$OUT" "$SESSION" <<'PY'
from pathlib import Path
import hashlib
import json
import sys
out = Path(sys.argv[1])
session_id = sys.argv[2]

# Verify that the JSONL export is exactly one object and that it resolves to
# the requested session id. Do not accept a successful command as evidence by itself.
lines = [x for x in (out / "session.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
if len(lines) != 1:
    raise SystemExit(f"ERROR: expected one session JSONL object, got {len(lines)}")
obj = json.loads(lines[0])
actual = str(obj.get("id") or obj.get("session_id") or "")
if actual != session_id:
    raise SystemExit(f"ERROR: exported session mismatch: expected {session_id}, got {actual!r}")

with (out / "artifact-sha256.txt").open("w", encoding="utf-8") as f:
    for name in ("session.jsonl", "trace.jsonl", "transcript.html"):
        p = out / name
        f.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {name}\n")
PY

cat > "$OUT/COLLECTION.txt" <<EOF
session_id=$SESSION
profile=$PROFILE
arm=$ARM
repetition=$REP
session_jsonl=session.jsonl
trace=trace.jsonl
transcript=transcript.html
collection_rule=explicit_profile_exact_session_and_post_export_identity_check
EOF

printf '%s\n' "Collected and identity-checked: $OUT"
