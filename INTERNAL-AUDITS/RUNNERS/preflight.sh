#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

fail() { echo "FAIL: $*" >&2; exit 1; }

command -v python3 >/dev/null || fail "python3 missing"
command -v hermes >/dev/null || fail "hermes missing"
command -v git >/dev/null || fail "git missing"

python3 --version
hermes --version
git -C "$ROOT" rev-parse HEAD

[[ -f "$ROOT/INTERNAL-AUDITS/RUNNERS/validate_benchmark.py" ]] || fail "validator missing"
[[ -f "$ROOT/INTERNAL-AUDITS/SCHEMAS/run-manifest.schema.json" ]] || fail "manifest schema missing"

for forbidden in AGENTS.md .hermes.md CLAUDE.md .cursorrules; do
  [[ ! -e "$PWD/$forbidden" ]] || fail "contaminating context file in current directory: $forbidden"
done

python3 "$ROOT/INTERNAL-AUDITS/RUNNERS/validate_benchmark.py"

echo "PASS: AHP benchmark preflight"
