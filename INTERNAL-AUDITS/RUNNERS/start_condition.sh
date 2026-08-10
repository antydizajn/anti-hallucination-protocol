#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  start_condition.sh <rep-slug> <A|B|C> <provider> <model>

Example:
  bash INTERNAL-AUDITS/RUNNERS/start_condition.sh q5r001 A openrouter openai/gpt-5.6
EOF
}
[[ $# -eq 4 ]] || { usage; exit 64; }
REP="$1"; ARM="$2"; PROVIDER="$3"; MODEL="$4"
[[ "$REP" =~ ^[a-z0-9][a-z0-9_-]{0,31}$ ]] || { echo "ERROR: invalid rep-slug" >&2; exit 64; }
[[ "$ARM" =~ ^[ABC]$ ]] || { echo "ERROR: arm must be A, B, or C" >&2; exit 64; }

BENCH_HOME="${AHP_BENCH_HOME:-$HOME/ahp-benchmark-v01}"
WORKDIR="$BENCH_HOME/work/$REP/$ARM"
PROFILE="ahpbench-${REP}-$(tr 'ABC' 'abc' <<<"$ARM")"

[[ -d "$WORKDIR/fixtures" ]] || {
  echo "ERROR: fixtures missing for arm $ARM. Run prepare_workspaces.sh $REP" >&2
  exit 2
}
hermes profile show "$PROFILE" >/dev/null 2>&1 || {
  echo "ERROR: missing profile $PROFILE" >&2
  exit 2
}

for f in AGENTS.md HERMES.md .hermes.md CLAUDE.md .cursorrules; do
  [[ ! -e "$WORKDIR/$f" ]] || { echo "ERROR: contaminated workspace contains $f" >&2; exit 3; }
done

# Do not use --safe-mode or --ignore-rules: current Hermes semantics can skip
# preloaded skills, which would destroy the B/C treatment.
ARGS=(-p "$PROFILE" --in "$WORKDIR" chat --provider "$PROVIDER" --model "$MODEL" -v)
case "$ARM" in
  A) ;;
  B|C) ARGS+=(-s anti-hallucination-protocol) ;;
esac

cat <<EOF
Starting benchmark condition
  repetition : $REP
  arm        : $ARM
  profile    : $PROFILE
  provider   : $PROVIDER
  model      : $MODEL
  cwd        : $WORKDIR
  AHP preload: $([[ "$ARM" == A ]] && echo NO || echo YES)

IMPORTANT:
- Use only the pre-registered operator prompts.
- Do not use --ignore-rules or --safe-mode.
- Do not resume another session.
- Record the Session ID printed by Hermes. collect_run.sh requires that exact ID.
EOF

exec hermes "${ARGS[@]}"
