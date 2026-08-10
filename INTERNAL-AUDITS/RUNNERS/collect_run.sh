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
[[ "$ARM" =~ ^[ABC]$ ]] || { echo "ERROR: arm must be A/B/C" >&2; exit 64; }

BENCH_HOME="${AHP_BENCH_HOME:-$HOME/ahp-benchmark-v01}"
OUT="$BENCH_HOME/runs/$REP/$ARM"
mkdir -p "$OUT"

command -v hermes >/dev/null || { echo "ERROR: hermes missing" >&2; exit 69; }

# Never export an implicit latest/default session. The profile is part of the
# evidence boundary and the exact session ID must belong to that Hermes state.
hermes -p "$PROFILE" sessions export --session-id "$SESSION" --format md > "$OUT/transcript.md"
hermes -p "$PROFILE" sessions export --session-id "$SESSION" --format jsonl > "$OUT/trace.jsonl"
hermes -p "$PROFILE" sessions export --session-id "$SESSION" --format json > "$OUT/session.json" || true

python3 - "$OUT" <<'PY'
from pathlib import Path
import hashlib
import sys
out = Path(sys.argv[1])
with (out / "artifact-sha256.txt").open("w", encoding="utf-8") as f:
    for p in sorted(out.glob("*.md")) + sorted(out.glob("*.json")) + sorted(out.glob("*.jsonl")):
        f.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n")
PY

cat > "$OUT/COLLECTION.txt" <<EOF
session_id=$SESSION
profile=$PROFILE
arm=$ARM
repetition=$REP
transcript=transcript.md
trace=trace.jsonl
collection_rule=explicit_profile_and_session_id_only
EOF

printf '%s\n' "Collected $OUT"
