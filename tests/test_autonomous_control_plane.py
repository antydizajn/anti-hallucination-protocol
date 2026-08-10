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
        ROOT / "EXTERNAL-CONTRIBUTOR.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "PROJECT-MAP.json",
        ROOT / "PROJECT-HANDOFF.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    assert not missing, f"missing autonomous bootstrap files: {missing}"


def test_bootstrap_routes_repo_url_to_discover_work_and_external_mode():
    data = json.loads((ROOT / "AGENT-BOOTSTRAP.json").read_text(encoding="utf-8"))
    assert data["schema"] == "ahp-agent-bootstrap-v2"
    assert data["default_when_only_repo_url_is_given"] == "DISCOVER_WORK"
    assert data["no_work_result"] == "STOP_WITH_NO_ASSIGNED_WORK"
    assert data["live_work_ledger"]["system"] == "github_issues"
    assert data["live_work_ledger"]["ready_marker"] == "[AGENT-READY]"
    assert data["live_work_ledger"]["claim_ttl_minutes"] == 120
    assert data["capability_routing"]["external_contributor"] == "EXTERNAL-CONTRIBUTOR.md"
    assert data["capability_routing"]["unknown_permission_default"] == "EXTERNAL_CONTRIBUTOR"
    assert data["external_helper"]["start"] == "python3 scripts/external_contributor.py start"
    assert data["external_helper"]["submit"] == "python3 scripts/external_contributor.py submit"


def test_agents_md_points_repo_url_only_agents_to_bootstrap():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "If you were given only the repository URL" in text
    assert "AGENT-BOOTSTRAP.json" in text
    assert "EXTERNAL-CONTRIBUTOR.md" in text
    assert "AUTONOMOUS-AGENT.md" in text
    assert "STOP_WITH_NO_ASSIGNED_WORK" in text
    assert "[AGENT-READY]" in text


def test_autonomous_entrypoint_forbids_manufactured_work_and_routes_no_write():
    text = (ROOT / "AUTONOMOUS-AGENT.md").read_text(encoding="utf-8")
    assert "`TODO.md` is roadmap context, not proof that a task remains open" in text
    assert "STOP_WITH_NO_ASSIGNED_WORK" in text
    assert "Autonomy means following a durable work contract" in text
    assert "permission unknown               -> EXTERNAL_CONTRIBUTOR" in text
    assert "EXTERNAL-CONTRIBUTOR.md" in text


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


def test_handoff_records_external_contributor_flow_as_merged():
    text = (ROOT / "PROJECT-HANDOFF.md").read_text(encoding="utf-8")
    assert "PR #9  - one-link autonomous control plane" in text
    assert "PR #13 - zero-write external contributor fork/PR workflow" in text
    assert "ec7816daea6250ee10835acad9f11f95c1e30a70" in text
    assert "GitHub Issues are the live work ledger" in text
    assert "CI PASS != BEHAVIORAL EFFECTIVENESS" in text
    assert "external-contributor-v1" in text
    assert "HISTORICAL merged development branch" in text
    assert "CANDIDATE zero-write fork/PR contribution path until merged" not in text


def test_project_map_has_capability_routed_repo_entrypoint():
    data = json.loads((ROOT / "PROJECT-MAP.json").read_text(encoding="utf-8"))
    assert data["schema"] == "ahp-project-map-v2"
    assert data["entrypoints"]["repo_url_only"] == [
        "AGENTS.md",
        "AGENT-BOOTSTRAP.json",
    ]
    assert data["entrypoints"]["external_no_write"] == [
        "EXTERNAL-CONTRIBUTOR.md",
        "CONTRIBUTING.md",
        "scripts/external_contributor.py",
    ]
    assert data["entrypoints"]["trusted_upstream_writer"] == "AUTONOMOUS-AGENT.md"
    assert data["entrypoints"]["live_work_ledger"] == "GitHub Issues with [AGENT-READY] marker"
    assert data["permission_modes"]["unknown_defaults_to"] == "EXTERNAL_CONTRIBUTOR"
    branch = next(item for item in data["branches"] if item["name"] == "external-contributor-v1")
    assert branch["role"] == "HISTORICAL"
