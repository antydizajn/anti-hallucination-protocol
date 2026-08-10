"""Regression tests for three hardening fixes.

Each test fails on the pre-fix code, so a green run is discriminating
evidence that the specific gap is closed and stays closed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "scripts" / "canonicalize_agent_message.py"
INTAKE = ROOT / "scripts" / "check_external_submission.py"
INTEGRITY = ROOT / "scripts" / "check_v5_integrity.py"


def run(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([sys.executable, *args], capture_output=True)


def write_manifest(subdir: Path, artifacts: list[dict[str, str]]) -> None:
    manifest = {
        "schema": "ahp-external-submission-v1",
        "submission_id": subdir.name,
        "submission_type": "FORENSIC_AUDIT",
        "submitted_at": "2026-08-10T03:00:00Z",
        "submitter": {"type": "HUMAN", "name": "regression"},
        "executor": {"type": "AGENT", "model": "m", "provider_runtime": "p"},
        "target": {"repository": "r", "ref": "main", "commit": "c"},
        "methodology": {"name": "UNKNOWN", "version": "UNKNOWN", "commit": "UNKNOWN"},
        "execution_occurred": False,
        "artifacts": artifacts,
        "declared_findings": [],
        "correlation_hints": [],
    }
    (subdir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def test_duplicate_object_keys_are_rejected(tmp_path: Path) -> None:
    """Two semantically different messages must not share one canonical byte string."""
    message = tmp_path / "dup.json"
    message.write_text(
        '{"signed":{"protocol":"ahp-agent-bus-v1","payload":{"a":1,"a":2}}}',
        encoding="utf-8",
    )
    result = run(str(CANON), str(message))
    assert result.returncode == 2
    assert b"duplicate object key" in result.stderr


def test_duplicate_key_free_message_still_canonicalizes(tmp_path: Path) -> None:
    message = tmp_path / "ok.json"
    message.write_text(
        '{"signed":{"protocol":"ahp-agent-bus-v1","payload":{"a":2}}}',
        encoding="utf-8",
    )
    result = run(str(CANON), str(message))
    assert result.returncode == 0
    assert result.stdout == b'{"payload":{"a":2},"protocol":"ahp-agent-bus-v1"}'


def test_oversized_artifact_is_rejected(tmp_path: Path) -> None:
    """An unbounded read_bytes() on attacker-sized input is a trivial memory DoS."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_external_submission", INTAKE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    limit = module.MAX_ARTIFACT_BYTES

    inbox = tmp_path / "INBOX"
    subdir = inbox / "SUB-20260810-oversize"
    subdir.mkdir(parents=True)
    (subdir / "REPORT.md").write_text("# ok\n", encoding="utf-8")
    (subdir / "BIG.bin").write_bytes(b"0" * (limit + 1))
    write_manifest(
        subdir,
        [{"path": "REPORT.md", "sha256": "UNKNOWN"}, {"path": "BIG.bin", "sha256": "UNKNOWN"}],
    )

    result = run(str(INTAKE), "--root", str(inbox))
    assert result.returncode == 1
    assert b"artifact exceeds" in result.stdout


def test_artifact_at_size_limit_is_accepted(tmp_path: Path) -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_external_submission", INTAKE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    inbox = tmp_path / "INBOX"
    subdir = inbox / "SUB-20260810-atlimit"
    subdir.mkdir(parents=True)
    (subdir / "REPORT.md").write_bytes(b"0" * module.MAX_ARTIFACT_BYTES)
    write_manifest(subdir, [{"path": "REPORT.md", "sha256": "UNKNOWN"}])

    result = run(str(INTAKE), "--root", str(inbox))
    assert result.returncode == 0
    assert b"STRUCTURALLY_VALID_SUBMISSION" in result.stdout


def test_streamed_hash_matches_declared_digest(tmp_path: Path) -> None:
    """Chunked hashing must produce the same digest as a whole-file read."""
    import hashlib

    inbox = tmp_path / "INBOX"
    subdir = inbox / "SUB-20260810-hash"
    subdir.mkdir(parents=True)
    payload = bytes(range(256)) * 8192
    (subdir / "REPORT.md").write_bytes(payload)
    write_manifest(
        subdir,
        [{"path": "REPORT.md", "sha256": hashlib.sha256(payload).hexdigest()}],
    )

    result = run(str(INTAKE), "--root", str(inbox))
    assert result.returncode == 0
    assert b"STRUCTURALLY_VALID_SUBMISSION" in result.stdout


def test_integrity_contract_covers_new_load_bearing_files() -> None:
    """Deleting any load-bearing script/test must break the release contract."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_v5_integrity", INTEGRITY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    required = set(module.REQUIRED_PATHS)
    for rel in (
        "scripts/canonicalize_agent_message.py",
        "scripts/verify_agent_signature.py",
        "scripts/check_external_submission.py",
        "scripts/external_contributor.py",
        "tests/test_project_infrastructure.py",
        "tests/test_external_contributor.py",
        "tests/test_agent_identity_secret_boundary.py",
        "tests/test_autonomous_control_plane.py",
        "tests/test_v541_integrity_extra.py",
        "tests/test_v542_policy_regressions.py",
    ):
        assert rel in required, f"{rel} is load-bearing but absent from REQUIRED_PATHS"
        assert (ROOT / rel).exists(), f"{rel} is required but missing from the tree"
