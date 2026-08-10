#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: cleanup_profiles.sh <rep-slug>" >&2
}
[[ $# -eq 1 ]] || { usage; exit 64; }
REP="$1"
[[ "$REP" =~ ^[a-z0-9][a-z0-9_-]{0,31}$ ]] || { echo "ERROR: invalid rep-slug" >&2; exit 64; }

command -v hermes >/dev/null || { echo "ERROR: hermes missing" >&2; exit 69; }

for suffix in a b c; do
  p="ahpbench-${REP}-${suffix}"
  if hermes profile show "$p" >/dev/null 2>&1; then
    hermes profile delete "$p" --yes
    echo "deleted $p"
  else
    echo "absent $p"
  fi
done

echo "Benchmark cleanup completed for $REP"
