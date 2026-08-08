from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_v5_integrity.py"

spec = importlib.util.spec_from_file_location("check_v5_integrity", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def write_minimal_tree(tmp_path: Path, skill_text: str) -> Path:
    root = tmp_path / "skill"
    root.mkdir()
    (root / "SKILL.md").write_text(skill_text, encoding="utf-8")
    for rel in mod.REQUIRED_PATHS:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("placeholder", encoding="utf-8")
    return root


def valid_skill() -> str:
    states = "\n".join(mod.REQUIRED_STATES)
    refs = "\n".join(
        [
            "references/research-foundations.md",
            "references/v5-gap-map.md",
            "references/evidence-state-model.md",
            "references/untrusted-evidence-boundary.md",
        ]
    )
    return f"version: 5.0.0\n{states}\n{refs}\n"


def test_happy_path(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill())
    assert mod.validate(root) == []


def test_wrong_version_fails(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill().replace("5.0.0", "4.0.0"))
    errors = mod.validate(root)
    assert any("does not declare version 5.0.0" in e for e in errors)


def test_missing_required_file_fails(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill())
    (root / "references" / "v5-gap-map.md").unlink()
    errors = mod.validate(root)
    assert any("required file missing" in e for e in errors)


def test_missing_state_fails(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill().replace("CONFLICT\n", ""))
    errors = mod.validate(root)
    assert any("required evidence state missing" in e for e in errors)


def test_missing_major_reference_from_skill_fails(tmp_path):
    root = write_minimal_tree(
        tmp_path,
        valid_skill().replace("references/v5-gap-map.md\n", ""),
    )
    errors = mod.validate(root)
    assert any("does not reference references/v5-gap-map.md" in e for e in errors)


def test_dead_backtick_path_fails(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill() + "`references/ghost.md`\n")
    errors = mod.validate(root)
    assert any("references missing local path: references/ghost.md" in e for e in errors)
