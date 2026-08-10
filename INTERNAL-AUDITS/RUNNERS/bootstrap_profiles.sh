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
WORKDIR="$BENCH_HOME/work/$REP"
A="ahpbench-${REP}-a"
B="ahpbench-${REP}-b"
C="ahpbench-${REP}-c"
PROFILES=("$A" "$B" "$C")

mkdir -p "$WORKDIR"

# A benchmark workspace must not inject project-level rules.
for f in AGENTS.md HERMES.md .hermes.md CLAUDE.md .cursorrules; do
  if [[ -e "$WORKDIR/$f" ]]; then
    echo "ERROR: contaminated benchmark workdir contains $f" >&2
    exit 2
  fi
done

for p in "${PROFILES[@]}"; do
  if hermes profile show "$p" >/dev/null 2>&1; then
    echo "ERROR: profile already exists: $p" >&2
    echo "Use a new repetition slug or explicitly delete this benchmark repetition." >&2
    exit 2
  fi
done

DEFAULT_CONFIG="$(hermes -p default config path)"
DEFAULT_ENV="$(hermes -p default config env-path)"

for p in "${PROFILES[@]}"; do
  hermes profile create "$p" --no-skills --no-alias >/dev/null

  CFG="$(hermes -p "$p" config path)"
  ENVF="$(hermes -p "$p" config env-path)"
  PHOME="$(dirname "$CFG")"

  # Carry the same model/provider/tool configuration and credentials into all arms,
  # but do not clone sessions, memory, SOUL, or skills.
  [[ -f "$DEFAULT_CONFIG" ]] && cp "$DEFAULT_CONFIG" "$CFG"
  [[ -f "$DEFAULT_ENV" ]] && cp "$DEFAULT_ENV" "$ENVF"

  : > "$PHOME/SOUL.md"
  mkdir -p "$PHOME/skills" "$PHOME/memories" "$PHOME/home"

  # --no-skills writes an opt-out marker. Preserve it, clear anything else.
  find "$PHOME/skills" -mindepth 1 -maxdepth 1 ! -name '.no-bundled-skills' -exec rm -rf {} + 2>/dev/null || true

  # A copied default config can point at external skill directories. That would
  # leak treatment into CONTROL even with an empty local skills directory.
  hermes -p "$p" config unset skills.external_dirs >/dev/null 2>&1 || true

  hermes -p "$p" memory off >/dev/null
  hermes -p "$p" memory reset --yes >/dev/null
  hermes -p "$p" config set terminal.cwd "$WORKDIR" >/dev/null
  hermes -p "$p" config set terminal.home_mode profile >/dev/null

done

cat <<EOF
Created fresh condition profiles for repetition: $REP
A CONTROL : $A
B LEGACY  : $B
C CURRENT : $C
workdir   : $WORKDIR

Next:
  bash INTERNAL-AUDITS/RUNNERS/install_frozen_ahp.sh $REP
EOF
