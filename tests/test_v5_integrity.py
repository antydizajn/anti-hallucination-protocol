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


def valid_skill(version: str = "5.4.0") -> str:
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


def test_other_v5_semver_is_rejected_by_release_checker(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill("5.9.3"))
    errors = mod.validate(root)
    assert any("expected exact release version '5.4.0'" in e for e in errors)


def test_previous_v5_release_is_rejected(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill("5.3.0"))
    errors = mod.validate(root)
    assert any("expected exact release version '5.4.0'" in e for e in errors)


def test_wrong_major_version_fails(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill("4.0.0"))
    errors = mod.validate(root)
    assert any("expected exact release version '5.4.0'" in e for e in errors)


def test_non_semver_version_fails(tmp_path):
    root = write_minimal_tree(tmp_path, valid_skill("five-point-four"))
    errors = mod.validate(root)
    assert any("expected exact release version '5.4.0'" in e for e in errors)


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


def test_no_frontmatter_fails_even_if_body_contains_version_string(tmp_path):
    fake = "version: 5.4.0\n" + "\n".join(mod.REQUIRED_STATES + mod.ACTIVE_REFERENCES)
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("must begin with YAML frontmatter" in e for e in errors)


def test_body_version_cannot_mask_wrong_frontmatter_version(tmp_path):
    fake = valid_skill("5.3.0") + "\nversion: 5.4.0\n"
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("expected exact release version '5.4.0'" in e for e in errors)


def test_unclosed_frontmatter_fails(tmp_path):
    fake = valid_skill().replace("\n---\n\n", "\n", 1)
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("no closing" in e for e in errors)


def test_malformed_top_level_line_fails_yaml_parse(tmp_path):
    fake = valid_skill().replace(
        "description: Test fixture",
        "description: Test fixture\nTHIS IS NOT A MAPPING",
    )
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert errors


def test_leading_unterminated_flow_sequence_fails(tmp_path):
    fake = valid_skill().replace("description: Test fixture", "description: [")
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("not valid YAML" in e for e in errors)


def test_trailing_unterminated_flow_sequence_fails(tmp_path):
    fake = valid_skill().replace("description: Test fixture", "description: Test fixture [")
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("not valid YAML" in e for e in errors)


def test_unterminated_quoted_scalar_fails(tmp_path):
    fake = valid_skill().replace("description: Test fixture", 'description: "broken')
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("not valid YAML" in e for e in errors)


def test_scalar_cannot_become_nested_mapping(tmp_path):
    fake = valid_skill().replace(
        "  hermes:\n    tags: [verification]",
        "  hermes: scalar\n    tags: [verification]",
    )
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("not valid YAML" in e for e in errors)


def test_colon_rich_plain_scalar_is_rejected_if_yaml_reinterprets_it(tmp_path):
    fake = valid_skill().replace(
        "description: Test fixture",
        "description: malformed: scalar",
    )
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert errors


def test_platforms_must_parse_as_list(tmp_path):
    fake = valid_skill().replace(
        "platforms: [linux, macos, windows]",
        'platforms: "[linux, macos, windows]"',
    )
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("platforms must be a non-empty string list" in e for e in errors)


def test_metadata_hermes_must_be_mapping(tmp_path):
    fake = valid_skill().replace("  hermes:\n", "  hermes: nope\n")
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("metadata.hermes must be a mapping" in e for e in errors)


def test_duplicate_top_level_key_fails(tmp_path):
    fake = valid_skill().replace(
        "version: 5.4.0",
        "version: 5.4.0\nversion: 5.4.1",
    )
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("duplicate top-level key: version" in e for e in errors)


def test_missing_required_frontmatter_key_fails(tmp_path):
    fake = valid_skill().replace("license: MIT\n", "")
    root = write_minimal_tree(tmp_path, fake)
    errors = mod.validate(root)
    assert any("frontmatter missing required key: license" in e for e in errors)
