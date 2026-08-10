#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: prepare_workspaces.sh <rep-slug>" >&2
}
[[ $# -eq 1 ]] || { usage; exit 64; }
REP="$1"
[[ "$REP" =~ ^[a-z0-9][a-z0-9_-]{0,31}$ ]] || { echo "ERROR: invalid rep-slug" >&2; exit 64; }

BENCH_HOME="${AHP_BENCH_HOME:-$HOME/ahp-benchmark-v01}"
ROOT="$BENCH_HOME/work/$REP"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for arm in A B C; do
  mkdir -p "$ROOT/$arm"
  python3 "$SCRIPT_DIR/setup_fixtures.py" "$ROOT/$arm" > "$ROOT/$arm/fixture-tree-sha256.txt"
done

cmp "$ROOT/A/fixture-tree-sha256.txt" "$ROOT/B/fixture-tree-sha256.txt"
cmp "$ROOT/A/fixture-tree-sha256.txt" "$ROOT/C/fixture-tree-sha256.txt"

echo "PASS: identical fixture trees prepared for $REP"
