from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_research_provenance.py"

spec = importlib.util.spec_from_file_location("check_research_provenance", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

Paper = mod.Paper


def paper(pid: str = "2305.14251", title: str = "FActScore", url: str | None = None):
    return Paper(pid, title, url or f"https://arxiv.org/abs/{pid}")


def test_manifest_requires_minimum_30():
    errors = mod.validate_manifest([paper()], minimum=30)
    assert any("minimum is 30" in e for e in errors)


def test_duplicate_id_is_rejected():
    p1 = paper("2305.14251", "FActScore A")
    p2 = paper("2305.14251", "FActScore B")
    errors = mod.validate_manifest([p1, p2], minimum=0)
    assert any("duplicate arXiv id" in e for e in errors)


def test_wrong_canonical_url_is_rejected():
    p = paper("2305.14251", "FActScore", "https://arxiv.org/abs/2305.99999")
    errors = mod.validate_manifest([p], minimum=0)
    assert any("non-canonical URL" in e for e in errors)


def test_correct_id_with_wrong_title_fails_skill_comparison():
    p = paper("2305.14251", "Canonical Title")
    skill = "[Wrong Title - arXiv:2305.14251](https://arxiv.org/abs/2305.14251)"
    errors = mod.compare_skill_to_manifest([p], skill)
    assert any("title mismatch" in e for e in errors)


def test_manifest_paper_missing_from_skill_is_rejected():
    p = paper("2305.14251", "Canonical Title")
    errors = mod.compare_skill_to_manifest([p], "no research citations here")
    assert any("SKILL.md missing manifest paper" in e for e in errors)


def test_duplicate_skill_citation_is_rejected():
    p = paper("2305.14251", "Canonical Title")
    entry = "[Canonical Title - arXiv:2305.14251](https://arxiv.org/abs/2305.14251)"
    errors = mod.compare_skill_to_manifest([p], entry + "\n" + entry)
    assert any("expected exactly once" in e for e in errors)


def test_unmanifested_skill_paper_is_rejected():
    p = paper("2305.14251", "Canonical Title")
    skill = (
        "[Canonical Title - arXiv:2305.14251](https://arxiv.org/abs/2305.14251)\n"
        "[Phantom provenance - arXiv:9999.99999](https://arxiv.org/abs/9999.99999)"
    )
    errors = mod.compare_skill_to_manifest([p], skill)
    assert any("not present in manifest" in e for e in errors)


def test_foundations_must_contain_exact_manifest_reference_once():
    p = paper("2305.14251", "Canonical Title")
    missing = mod.compare_foundations_to_manifest([p], "nothing")
    assert missing

    exact = "[2305.14251](https://arxiv.org/abs/2305.14251)"
    assert mod.compare_foundations_to_manifest([p], exact) == []

    duplicate = mod.compare_foundations_to_manifest([p], exact + "\n" + exact)
    assert any("expected 1" in e for e in duplicate)


def test_happy_path_for_one_v4_entry():
    p = paper("2305.14251", "Canonical Title")
    skill = "[Canonical Title - arXiv:2305.14251](https://arxiv.org/abs/2305.14251)"
    foundations = "[2305.14251](https://arxiv.org/abs/2305.14251)"
    assert mod.validate_manifest([p], minimum=1) == []
    assert mod.compare_skill_to_manifest([p], skill) == []
    assert mod.compare_foundations_to_manifest([p], foundations) == []


def test_v5_gap_exact_manifest_order_passes():
    displays = [
        "Source A - arXiv:1111.11111: https://arxiv.org/abs/1111.11111",
        "Source B: https://example.com/b",
    ]
    gap = """# x
## New research sources used for v5

1. Source A - arXiv:1111.11111: https://arxiv.org/abs/1111.11111
2. Source B: https://example.com/b

## What v5 must NOT claim
"""
    assert mod.compare_v5_gap_to_manifest(displays, gap) == []


def test_v5_gap_wrong_title_for_same_arxiv_id_fails():
    displays = [
        "Reliable Post-Retrieval Assembly for Agent Memory: Separating Evidence Extraction from Policy Execution - arXiv:2606.01435: https://arxiv.org/abs/2606.01435"
    ]
    gap = """## New research sources used for v5
1. Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution - arXiv:2606.01435: https://arxiv.org/abs/2606.01435
## What v5 must NOT claim
"""
    errors = mod.compare_v5_gap_to_manifest(displays, gap)
    assert any("v5 research source #1 mismatch" in e for e in errors)


def test_v5_gap_missing_source_fails():
    displays = ["A: https://example.com/a", "B: https://example.com/b"]
    gap = """## New research sources used for v5
1. A: https://example.com/a
## What v5 must NOT claim
"""
    errors = mod.compare_v5_gap_to_manifest(displays, gap)
    assert errors


def test_v5_manifest_loader_rejects_missing_display(tmp_path: Path):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"sources": [{"url": "https://example.com"}]}), encoding="utf-8")
    try:
        mod.load_v5_manifest(path)
    except ValueError as exc:
        assert "display" in str(exc)
    else:
        raise AssertionError("invalid v5 manifest should fail")
