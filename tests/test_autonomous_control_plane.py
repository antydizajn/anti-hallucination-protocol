from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_one_link_bootstrap_files_exist():
    required = [
        ROOT / "AGENTS.md",
        ROOT / "AGENT-BOOTSTRAP.json",
        ROOT / "AUTONOMOUS-AGENT.md",
        ROOT / "PROJECT-MAP.json",
        ROOT / "PROJECT-HANDOFF.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    assert not missing, f"missing autonomous bootstrap files: {missing}"


def test_bootstrap_routes_repo_url_to_discover_work():
    data = json.loads((ROOT / "AGENT-BOOTSTRAP.json").read_text(encoding="utf-8"))
    assert data["schema"] == "ahp-agent-bootstrap-v1"
    assert data["default_when_only_repo_url_is_given"] == "DISCOVER_WORK"
    assert data["no_work_result"] == "STOP_WITH_NO_ASSIGNED_WORK"
    assert data["live_work_ledger"]["system"] == "github_issues"
    assert data["live_work_ledger"]["ready_marker"] == "[AGENT-READY]"
    assert data["live_work_ledger"]["claim_ttl_minutes"] == 120


def test_agents_md_points_repo_url_only_agents_to_bootstrap():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "If you were given only the repository URL" in text
    assert "AGENT-BOOTSTRAP.json" in text
    assert "AUTONOMOUS-AGENT.md" in text
    assert "STOP_WITH_NO_ASSIGNED_WORK" in text
    assert "[AGENT-READY]" in text


def test_autonomous_entrypoint_forbids_manufactured_work():
    text = (ROOT / "AUTONOMOUS-AGENT.md").read_text(encoding="utf-8")
    assert "Do not treat `TODO.md` as proof that an item is still open" in text
    assert "STOP_WITH_NO_ASSIGNED_WORK" in text
    assert "Autonomy means following a durable work contract" in text


def test_custom_agent_profiles_have_valid_frontmatter():
    names = {
        "ahp-router.md": "ahp-router",
        "ahp-forensic-auditor.md": "ahp-forensic-auditor",
        "ahp-reproducer.md": "ahp-reproducer",
        "ahp-remediator.md": "ahp-remediator",
        "ahp-release-verifier.md": "ahp-release-verifier",
    }
    for filename, expected_name in names.items():
        path = ROOT / ".github" / "agents" / filename
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        _, frontmatter, body = text.split("---", 2)
        parsed = yaml.safe_load(frontmatter)
        assert parsed["name"] == expected_name
        assert isinstance(parsed["description"], str) and parsed["description"].strip()
        assert body.strip()


def test_submission_triage_workflow_is_non_executing_and_deduplicated():
    path = ROOT / ".github" / "workflows" / "submission-triage.yml"
    text = path.read_text(encoding="utf-8")
    parsed = yaml.safe_load(text)
    assert parsed["permissions"]["contents"] == "read"
    assert parsed["permissions"]["issues"] == "write"
    assert "AHP_SUBMISSION_ID:" in text
    assert "gh issue list" in text
    assert "gh issue create" in text
    assert "SUBMISSIONS/INBOX" in text
    forbidden = [
        "chmod +x SUBMISSIONS",
        "bash SUBMISSIONS/",
        "sh SUBMISSIONS/",
        "python SUBMISSIONS/",
        "./SUBMISSIONS/",
    ]
    assert not any(token in text for token in forbidden)


def test_handoff_records_new_control_plane_without_claiming_merge():
    text = (ROOT / "PROJECT-HANDOFF.md").read_text(encoding="utf-8")
    assert "autonomous-control-plane-v1" in text
    assert "Until merged, these are candidate infrastructure" in text
    assert "GitHub Issues = LIVE OPERATIONAL WORK LEDGER" in text
    assert "CI PASS != BEHAVIORAL EFFECTIVENESS" in text


def test_project_map_has_repo_url_only_entrypoint():
    data = json.loads((ROOT / "PROJECT-MAP.json").read_text(encoding="utf-8"))
    assert data["entrypoints"]["repo_url_only"] == [
        "AGENTS.md",
        "AGENT-BOOTSTRAP.json",
        "AUTONOMOUS-AGENT.md",
    ]
    assert data["entrypoints"]["live_work_ledger"] == "GitHub Issues with [AGENT-READY] marker"
