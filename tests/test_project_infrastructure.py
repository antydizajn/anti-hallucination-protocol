from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "scripts" / "canonicalize_agent_message.py"
VERIFY = ROOT / "scripts" / "verify_agent_signature.py"
INTAKE = ROOT / "scripts" / "check_external_submission.py"


def run(*args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT,
        timeout=20,
    )


def signed_message(signature_file: str = "payload.sig") -> dict:
    return {
        "schema": "ahp-agent-bus-signed-message-v1",
        "signed": {
            "protocol": "ahp-agent-bus-v1",
            "message_id": "MSG-1",
            "thread_id": "THREAD-1",
            "created_at": "2026-08-10T03:00:00+02:00",
            "sender_agent_id": "agent-test",
            "recipient_agent_id": "agent-other",
            "kind": "RESULT",
            "subject": "test",
            "payload": {"ok": True, "count": 2},
        },
        "signature": {
            "algorithm": "ssh-ed25519",
            "namespace": "ahp-agent-bus-v1",
            "key_id": "agent-test-2026-01",
            "signature_file": signature_file,
        },
    }


def test_agent_message_canonicalization_is_deterministic(tmp_path: Path) -> None:
    a = signed_message()
    b = json.loads(json.dumps(a))
    b["signed"] = dict(reversed(list(b["signed"].items())))
    pa = tmp_path / "a.json"
    pb = tmp_path / "b.json"
    pa.write_text(json.dumps(a), encoding="utf-8")
    pb.write_text(json.dumps(b), encoding="utf-8")
    ra = run(str(CANON), str(pa))
    rb = run(str(CANON), str(pb))
    assert ra.returncode == 0, ra.stderr.decode()
    assert rb.returncode == 0, rb.stderr.decode()
    assert ra.stdout == rb.stdout
    assert not ra.stdout.endswith(b"\n")


def test_agent_message_canonicalization_rejects_float(tmp_path: Path) -> None:
    msg = signed_message()
    msg["signed"]["payload"]["score"] = 0.5
    path = tmp_path / "m.json"
    path.write_text(json.dumps(msg), encoding="utf-8")
    result = run(str(CANON), str(path))
    assert result.returncode == 2
    assert b"floats are forbidden" in result.stderr


@pytest.mark.skipif(shutil.which("ssh-keygen") is None, reason="ssh-keygen unavailable")
def test_real_ed25519_agent_signature_verifies_and_tamper_fails(tmp_path: Path) -> None:
    key = tmp_path / "agent_key"
    subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
    )
    public_key = key.with_suffix(".pub").read_text(encoding="utf-8").strip()
    payload = tmp_path / "payload"
    sig = tmp_path / "payload.sig"
    message = signed_message(signature_file=sig.name)
    message_path = tmp_path / "message.json"
    message_path.write_text(json.dumps(message), encoding="utf-8")
    canon = run(str(CANON), str(message_path))
    assert canon.returncode == 0, canon.stderr.decode()
    payload.write_bytes(canon.stdout)
    subprocess.run(
        ["ssh-keygen", "-Y", "sign", "-f", str(key), "-n", "ahp-agent-bus-v1", str(payload)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
    )
    produced = Path(str(payload) + ".sig")
    produced.replace(sig)
    registry = {
        "schema": "ahp-agent-identity-registry-v1",
        "agents": [
            {
                "agent_id": "agent-test",
                "assurance": "KEY_BOUND_IDENTITY",
                "keys": [
                    {
                        "key_id": "agent-test-2026-01",
                        "algorithm": "ssh-ed25519",
                        "public_key": public_key,
                        "status": "ACTIVE",
                        "valid_from": "2026-01-01T00:00:00Z",
                        "valid_until": None,
                        "revoked_at": None,
                        "revocation_reason": None,
                    }
                ],
            }
        ],
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    ok = run(
        str(VERIFY),
        "--message", str(message_path),
        "--signature", str(sig),
        "--registry", str(registry_path),
    )
    assert ok.returncode == 0, ok.stderr.decode()
    assert b"KEY_BOUND_IDENTITY" in ok.stdout

    message["signed"]["payload"]["ok"] = False
    message_path.write_text(json.dumps(message), encoding="utf-8")
    bad = run(
        str(VERIFY),
        "--message", str(message_path),
        "--signature", str(sig),
        "--registry", str(registry_path),
    )
    assert bad.returncode == 2
    assert b"UNVERIFIED" in bad.stderr


@pytest.mark.skipif(shutil.which("ssh-keygen") is None, reason="ssh-keygen unavailable")
def test_revoked_agent_key_fails_closed(tmp_path: Path) -> None:
    key = tmp_path / "agent_key"
    subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
    )
    public_key = key.with_suffix(".pub").read_text(encoding="utf-8").strip()
    payload = tmp_path / "payload"
    sig = tmp_path / "payload.sig"
    message = signed_message(signature_file=sig.name)
    mp = tmp_path / "message.json"
    mp.write_text(json.dumps(message), encoding="utf-8")
    canon = run(str(CANON), str(mp))
    payload.write_bytes(canon.stdout)
    subprocess.run(
        ["ssh-keygen", "-Y", "sign", "-f", str(key), "-n", "ahp-agent-bus-v1", str(payload)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
    )
    Path(str(payload) + ".sig").replace(sig)
    registry = {
        "agents": [{
            "agent_id": "agent-test",
            "keys": [{
                "key_id": "agent-test-2026-01",
                "algorithm": "ssh-ed25519",
                "public_key": public_key,
                "status": "REVOKED",
                "valid_from": "2026-01-01T00:00:00Z",
                "valid_until": None,
                "revoked_at": "2026-08-01T00:00:00Z",
                "revocation_reason": "test",
            }],
        }],
    }
    rp = tmp_path / "registry.json"
    rp.write_text(json.dumps(registry), encoding="utf-8")
    result = run(str(VERIFY), "--message", str(mp), "--signature", str(sig), "--registry", str(rp))
    assert result.returncode == 2
    assert b"not ACTIVE" in result.stderr


def make_submission(root: Path, submission_id: str = "SUB-20260810-test-a1") -> Path:
    sub = root / submission_id
    sub.mkdir(parents=True)
    report = sub / "REPORT.md"
    report.write_text("# external report\n", encoding="utf-8")
    digest = hashlib.sha256(report.read_bytes()).hexdigest()
    manifest = {
        "schema": "ahp-external-submission-v1",
        "submission_id": submission_id,
        "submission_type": "FORENSIC_AUDIT",
        "submitted_at": "2026-08-10T03:00:00+02:00",
        "submitter": {"type": "HUMAN", "name": "test"},
        "executor": {"type": "AGENT", "model": "test-model", "provider_runtime": "test"},
        "target": {"repository": "https://github.com/antydizajn/anti-hallucination-protocol", "ref": "main", "commit": "UNKNOWN"},
        "methodology": {"name": "UNKNOWN", "version": "UNKNOWN", "commit": "UNKNOWN"},
        "execution_occurred": True,
        "artifacts": [{"path": "REPORT.md", "sha256": digest}],
        "declared_findings": [{"id": "F-001", "severity": "P2", "title": "test"}],
        "correlation_hints": [],
    }
    (sub / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return sub


def test_external_submission_validates_hash_and_shape(tmp_path: Path) -> None:
    inbox = tmp_path / "INBOX"
    make_submission(inbox)
    result = run(str(INTAKE), "--root", str(inbox))
    assert result.returncode == 0, result.stdout.decode() + result.stderr.decode()
    assert b"STRUCTURALLY_VALID_SUBMISSION" in result.stdout


def test_external_submission_hash_mismatch_fails(tmp_path: Path) -> None:
    inbox = tmp_path / "INBOX"
    sub = make_submission(inbox)
    (sub / "REPORT.md").write_text("tampered\n", encoding="utf-8")
    result = run(str(INTAKE), "--root", str(inbox))
    assert result.returncode == 1
    assert b"SHA-256 mismatch" in result.stdout


def test_external_submission_path_traversal_fails(tmp_path: Path) -> None:
    inbox = tmp_path / "INBOX"
    sub = make_submission(inbox)
    manifest_path = sub / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"] = [{"path": "../outside.txt", "sha256": "UNKNOWN"}]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    result = run(str(INTAKE), "--root", str(inbox))
    assert result.returncode == 1
    assert b"path traversal" in result.stdout
