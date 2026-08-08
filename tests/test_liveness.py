from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "liveness_check.sh"


def run_liveness(skill_dir: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["AHP_SKILL_DIR"] = str(skill_dir)
    return subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_real_candidate_portable_checks_pass():
    result = run_liveness(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "end liveness check: PASS" in result.stdout


def test_missing_verifier_is_nonzero(tmp_path: Path):
    skill = tmp_path / "skill"
    shutil.copytree(ROOT, skill)
    (skill / "scripts" / "verify_claim.py").unlink()

    result = run_liveness(skill)

    assert result.returncode != 0
    assert "[FAIL] verify_claim.py missing" in result.stdout
    assert "end liveness check: FAIL" in result.stdout


def test_missing_integrity_checker_is_nonzero(tmp_path: Path):
    skill = tmp_path / "skill"
    shutil.copytree(ROOT, skill)
    (skill / "scripts" / "check_v5_integrity.py").unlink()

    result = run_liveness(skill)

    assert result.returncode != 0
    assert "[FAIL] check_v5_integrity.py unavailable" in result.stdout


def test_missing_skill_file_is_nonzero(tmp_path: Path):
    skill = tmp_path / "skill"
    shutil.copytree(ROOT, skill)
    (skill / "SKILL.md").unlink()

    result = run_liveness(skill)

    assert result.returncode != 0
    assert "[FAIL] SKILL.md missing" in result.stdout
