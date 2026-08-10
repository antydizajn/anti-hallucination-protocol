#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: collect_run.sh <rep-slug> <ARM> <session-id>" >&2
}
[[ $# -eq 3 ]] || { usage; exit 64; }
REP="$1"
ARM="$2"
SESSION="$3"
[[ "$ARM" =~ ^[ABC]$ ]] || { echo "ERROR: arm must be A/B/C" >&2; exit 64; }

BENCH_HOME="${AHP_BENCH_HOME:-$HOME/ahp-benchmark-v01}"
OUT="$BENCH_HOME/runs/$REP/$ARM"
mkdir -p "$OUT"

command -v hermes >/dev/null || { echo "ERROR: hermes missing" >&2; exit 69; }

hermes sessions export --session-id "$SESSION" --format md > "$OUT/transcript.md"
hermes sessions export --session-id "$SESSION" --format jsonl > "$OUT/trace.jsonl"
hermes sessions export --session-id "$SESSION" --format json > "$OUT/session.json" || true

sha256sum "$OUT/transcript.md" "$OUT/trace.jsonl" "$OUT/session.json" 2>/dev/null > "$OUT/artifact-sha256.txt"

cat > "$OUT/COLLECTION.txt" <<EOF
session_id=$SESSION
arm=$ARM
repetition=$REP
transcript=transcript.md
trace=trace.jsonl
collection_rule=explicit_session_id_only
EOF

printf '%s\n' "Collected $OUT"
