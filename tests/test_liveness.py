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


def test_skill_path_with_spaces_passes(tmp_path: Path):
    skill = tmp_path / "skill with spaces"
    shutil.copytree(ROOT, skill)
    result = run_liveness(skill)
    assert result.returncode == 0, result.stdout + result.stderr


def test_corrupted_verifier_selftest_is_nonzero(tmp_path: Path):
    skill = tmp_path / "skill"
    shutil.copytree(ROOT, skill)
    verifier = skill / "scripts" / "verify_claim.py"
    verifier.write_text("#!/usr/bin/env python3\nraise SystemExit(0)\n", encoding="utf-8")

    result = run_liveness(skill)

    assert result.returncode != 0
    assert "verify_claim.py self-test failed" in result.stdout


def test_multiple_required_failures_remain_nonzero(tmp_path: Path):
    skill = tmp_path / "skill"
    shutil.copytree(ROOT, skill)
    (skill / "scripts" / "verify_claim.py").unlink()
    (skill / "scripts" / "check_v5_integrity.py").unlink()

    result = run_liveness(skill)

    assert result.returncode != 0
    assert "verify_claim.py missing" in result.stdout
    assert "check_v5_integrity.py unavailable" in result.stdout
    assert "end liveness check: FAIL" in result.stdout
