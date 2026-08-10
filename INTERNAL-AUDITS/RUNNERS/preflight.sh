#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

fail() { echo "FAIL: $*" >&2; exit 1; }

command -v python3 >/dev/null || fail "python3 missing"
command -v hermes >/dev/null || fail "hermes missing"
command -v git >/dev/null || fail "git missing"
command -v bash >/dev/null || fail "bash missing"

python3 --version
hermes --version
git -C "$ROOT" rev-parse HEAD

python3 - <<'PY' || fail "PyYAML missing; install with: python3 -m pip install PyYAML"
import yaml
print("PyYAML", getattr(yaml, "__version__", "UNKNOWN"))
PY

[[ -f "$ROOT/INTERNAL-AUDITS/RUNNERS/validate_benchmark.py" ]] || fail "validator missing"
[[ -f "$ROOT/INTERNAL-AUDITS/SCHEMAS/run-manifest.schema.json" ]] || fail "manifest schema missing"

for forbidden in AGENTS.md HERMES.md .hermes.md CLAUDE.md .cursorrules; do
  [[ ! -e "$PWD/$forbidden" ]] || fail "contaminating context file in current directory: $forbidden"
done

while IFS= read -r script; do
  bash -n "$script" || fail "shell syntax failed: $script"
done < <(find "$ROOT/INTERNAL-AUDITS/RUNNERS" -maxdepth 1 -type f -name '*.sh' | sort)

python3 -m py_compile \
  "$ROOT/INTERNAL-AUDITS/RUNNERS/setup_fixtures.py" \
  "$ROOT/INTERNAL-AUDITS/RUNNERS/validate_benchmark.py" \
  "$ROOT/INTERNAL-AUDITS/RUNNERS/score_run.py"

python3 "$ROOT/INTERNAL-AUDITS/RUNNERS/validate_benchmark.py"

echo "PASS: AHP benchmark preflight"
