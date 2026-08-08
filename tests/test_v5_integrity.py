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


def valid_skill(version: str = mod.EXPECTED_VERSION) -> str:
    states = "\n".join(mod.REQUIRED_STATES)
    refs = "\n".join(mod.ACTIVE_REFERENCES)
    return f'''---
name: anti-hallucination-protocol
description: Test fixture
version: {version}
author: "Paulina Janowska & Gniewisława AI"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [verification]
    category: software-development
---

{states}
{refs}
'''


def test_happy_path(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill())
    assert mod.validate(root) == []


def test_wrong_frontmatter_version_fails(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill("4.0.0"))
    errors = mod.validate(root)
    assert any("frontmatter version" in e for e in errors)


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


# Regression probes from GPT-5.6 Terra's forensic audit.

def test_no_frontmatter_fails_even_if_body_contains_version_string(tmp_path):
    fake = "version: 5.1.0\n" + "\n".join(mod.REQUIRED_STATES + mod.ACTIVE_REFERENCES)
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("must begin with YAML frontmatter" in e for e in errors)


def test_body_version_cannot_mask_wrong_frontmatter_version(tmp_path):
    fake = valid_skill("4.0.0") + "\nversion: 5.1.0\n"
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("frontmatter version" in e for e in errors)


def test_unclosed_frontmatter_fails(tmp_path):
    fake = valid_skill().replace("\n---\n\n", "\n", 1)
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("no closing" in e for e in errors)


def test_malformed_top_level_yaml_line_fails(tmp_path):
    fake = valid_skill().replace(
        "description: Test fixture",
        "description: Test fixture\nTHIS IS NOT YAML",
    )
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("malformed top-level YAML mapping" in e for e in errors)


def test_missing_required_frontmatter_key_fails(tmp_path):
    fake = valid_skill().replace("license: MIT\n", "")
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("frontmatter missing required key: license" in e for e in errors)
