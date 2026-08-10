from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "external_contributor.py"

spec = importlib.util.spec_from_file_location("external_contributor", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_target_ref_is_parsed_from_agent_ready_issue_body():
    body = """Target branch:\n\n```text\naudit-methodology-v6\n```\n"""
    assert mod.target_ref_from_issue(body) == "audit-methodology-v6"


def test_unknown_target_defaults_to_main():
    assert mod.target_ref_from_issue("no target declared") == "main"


def test_audit_like_work_is_submission_work():
    assert mod.infer_submission_type("[AGENT-READY][P1][METHODOLOGY] Blind review") == "FORENSIC_AUDIT"
    assert mod.infer_submission_type("[AGENT-READY][P2][REPRODUCER] Case") == "REPRODUCER"
    assert mod.infer_submission_type("[AGENT-READY][P2] Code cleanup") is None


def test_findings_extraction_does_not_invent_missing_fields(tmp_path: Path):
    path = tmp_path / "FINDINGS.json"
    path.write_text(json.dumps({"findings": [
        {"finding_id": "F-1", "title": "real", "severity": "P1"},
        {"finding_id": "F-2", "severity": "P0"},
        {"finding_id": "F-3", "title": "odd", "severity": "NOT_A_SEVERITY"},
    ]}), encoding="utf-8")
    assert mod.extract_findings(path) == [
        {"id": "F-1", "title": "real", "severity": "P1"},
        {"id": "F-3", "title": "odd", "severity": "UNKNOWN"},
    ]


def test_external_helper_never_pushes_to_upstream_remote():
    text = SCRIPT.read_text(encoding="utf-8")
    assert '"git", "push", "-u", "fork"' in text
    assert '"git", "push", "-u", "upstream"' not in text
    assert '"git", "push", "upstream"' not in text


def test_audit_target_is_separate_from_delivery_base():
    text = SCRIPT.read_text(encoding="utf-8")
    assert 'delivery_base = "main" if stype else target_ref' in text
    assert '"--base", state["delivery_base"]' in text
    assert "target_workspace" in text
    assert "git\", \"worktree\", \"add" in text


def test_completion_requires_real_upstream_pr_url():
    assert mod.PR_URL_RE.fullmatch("https://github.com/antydizajn/anti-hallucination-protocol/pull/123")
    assert not mod.PR_URL_RE.fullmatch("https://github.com/someone/anti-hallucination-protocol/pull/123")
    assert not mod.PR_URL_RE.fullmatch("PR prepared")


def test_external_workflows_do_not_use_pull_request_target():
    workflows = ROOT / ".github" / "workflows"
    for path in workflows.glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        if "submission" in path.name:
            assert "pull_request_target" not in text


def test_external_entrypoint_has_minimum_friction_commands():
    text = (ROOT / "EXTERNAL-CONTRIBUTOR.md").read_text(encoding="utf-8")
    assert "gh repo clone antydizajn/anti-hallucination-protocol" in text
    assert "python3 scripts/external_contributor.py start" in text
    assert "python3 scripts/external_contributor.py submit" in text
    assert "You do **not** need collaborator access" in text
