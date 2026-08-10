#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: bash INTERNAL-AUDITS/RUNNERS/bootstrap_profiles.sh <rep-slug>" >&2
  echo "Example: bash INTERNAL-AUDITS/RUNNERS/bootstrap_profiles.sh q5r001" >&2
}

[[ $# -eq 1 ]] || { usage; exit 64; }
REP="$1"
[[ "$REP" =~ ^[a-z0-9][a-z0-9_-]{0,31}$ ]] || {
  echo "ERROR: rep-slug must match ^[a-z0-9][a-z0-9_-]{0,31}$" >&2
  exit 64
}

command -v hermes >/dev/null || { echo "ERROR: hermes not found in PATH" >&2; exit 69; }

BENCH_HOME="${AHP_BENCH_HOME:-$HOME/ahp-benchmark-v01}"
REP_ROOT="$BENCH_HOME/work/$REP"
A="ahpbench-${REP}-a"
B="ahpbench-${REP}-b"
C="ahpbench-${REP}-c"
PROFILES=("$A" "$B" "$C")
ARMS=(A B C)

mkdir -p "$REP_ROOT"

for arm in "${ARMS[@]}"; do
  mkdir -p "$REP_ROOT/$arm"
  for f in AGENTS.md HERMES.md .hermes.md CLAUDE.md .cursorrules; do
    if [[ -e "$REP_ROOT/$arm/$f" ]]; then
      echo "ERROR: contaminated benchmark workdir contains $arm/$f" >&2
      exit 2
    fi
  done
done

for p in "${PROFILES[@]}"; do
  if hermes profile show "$p" >/dev/null 2>&1; then
    echo "ERROR: profile already exists: $p" >&2
    echo "Use a new repetition slug or explicitly delete this benchmark repetition." >&2
    exit 2
  fi
done

DEFAULT_ENV="$(hermes -p default config env-path)"

for i in 0 1 2; do
  p="${PROFILES[$i]}"
  arm="${ARMS[$i]}"
  hermes profile create "$p" --no-skills --no-alias >/dev/null

  CFG="$(hermes -p "$p" config path)"
  ENVF="$(hermes -p "$p" config env-path)"
  PHOME="$(dirname "$CFG")"
  ARM_WORKDIR="$REP_ROOT/$arm"

  # Do not clone/copy the default config. A full config copy can import custom
  # skills, MCP/plugin/hook state, memory providers, or other treatment confounds.
  # Only credentials are copied; provider/model are supplied explicitly at launch.
  [[ -f "$DEFAULT_ENV" ]] && cp "$DEFAULT_ENV" "$ENVF"

  : > "$PHOME/SOUL.md"
  mkdir -p "$PHOME/skills" "$PHOME/memories" "$PHOME/home"

  # --no-skills writes an opt-out marker. Preserve it and remove anything else.
  find "$PHOME/skills" -mindepth 1 -maxdepth 1 ! -name '.no-bundled-skills' -exec rm -rf {} + 2>/dev/null || true

  hermes -p "$p" config unset skills.external_dirs >/dev/null 2>&1 || true
  hermes -p "$p" memory off >/dev/null
  hermes -p "$p" memory reset --yes >/dev/null
  hermes -p "$p" config set terminal.cwd "$ARM_WORKDIR" >/dev/null
  hermes -p "$p" config set terminal.home_mode profile >/dev/null

done

cat <<EOF
Created fresh condition profiles for repetition: $REP
A CONTROL : $A -> $REP_ROOT/A
B LEGACY  : $B -> $REP_ROOT/B
C CURRENT : $C -> $REP_ROOT/C

Default config was NOT copied.
Only the default .env credential file was copied when present.

Next:
  bash INTERNAL-AUDITS/RUNNERS/install_frozen_ahp.sh $REP
  python3 INTERNAL-AUDITS/RUNNERS/setup_fixtures.py $REP_ROOT/A
  python3 INTERNAL-AUDITS/RUNNERS/setup_fixtures.py $REP_ROOT/B
  python3 INTERNAL-AUDITS/RUNNERS/setup_fixtures.py $REP_ROOT/C
EOF
