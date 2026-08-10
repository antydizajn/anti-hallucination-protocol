#!/usr/bin/env python3
"""Verify an AHP signed agent message against the public-key registry.

A successful result establishes KEY_BOUND_IDENTITY only.
It does not establish factual truth, model identity, independence, or human non-intervention.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from canonicalize_agent_message import canonical_bytes

NAMESPACE = "ahp-agent-bus-v1"


def parse_time(value: Any) -> datetime | None:
    if value in (None, "", "UNKNOWN"):
        return None
    if not isinstance(value, str):
        raise ValueError("time value must be string/null")
    text = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("time value requires timezone")
    return parsed.astimezone(timezone.utc)


def find_key(registry: dict[str, Any], agent_id: str, key_id: str) -> dict[str, Any]:
    for agent in registry.get("agents", []):
        if agent.get("agent_id") == agent_id:
            for key in agent.get("keys", []):
                if key.get("key_id") == key_id:
                    return key
            raise ValueError(f"key_id {key_id!r} is not registered for agent {agent_id!r}")
    raise ValueError(f"agent_id {agent_id!r} is not registered")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--message", required=True, type=Path)
    p.add_argument("--signature", required=True, type=Path)
    p.add_argument("--registry", required=True, type=Path)
    args = p.parse_args()
    try:
        if shutil.which("ssh-keygen") is None:
            raise RuntimeError("ssh-keygen unavailable")
        message = json.loads(args.message.read_text(encoding="utf-8"))
        registry = json.loads(args.registry.read_text(encoding="utf-8"))
        signed = message.get("signed")
        sigmeta = message.get("signature")
        if not isinstance(signed, dict) or not isinstance(sigmeta, dict):
            raise ValueError("message requires signed and signature objects")
        if sigmeta.get("algorithm") != "ssh-ed25519":
            raise ValueError("signature.algorithm must be ssh-ed25519")
        if sigmeta.get("namespace") != NAMESPACE:
            raise ValueError(f"signature.namespace must equal {NAMESPACE!r}")
        if sigmeta.get("signature_file") != args.signature.name:
            raise ValueError("signature_file metadata does not match supplied signature filename")
        sender = signed.get("sender_agent_id")
        key_id = sigmeta.get("key_id")
        if not isinstance(sender, str) or not sender:
            raise ValueError("signed.sender_agent_id missing")
        if not isinstance(key_id, str) or not key_id:
            raise ValueError("signature.key_id missing")
        key = find_key(registry, sender, key_id)
        if key.get("algorithm") != "ssh-ed25519":
            raise ValueError("registered key algorithm mismatch")
        if key.get("status") != "ACTIVE":
            raise ValueError(f"registered key is not ACTIVE: {key.get('status')!r}")
        created_at = parse_time(signed.get("created_at"))
        if created_at is None:
            raise ValueError("signed.created_at is required for key-validity checks")
        valid_from = parse_time(key.get("valid_from"))
        valid_until = parse_time(key.get("valid_until"))
        revoked_at = parse_time(key.get("revoked_at"))
        if valid_from and created_at < valid_from:
            raise ValueError("message predates key validity")
        if valid_until and created_at > valid_until:
            raise ValueError("message postdates key validity")
        if revoked_at and created_at >= revoked_at:
            raise ValueError("message timestamp is at/after key revocation")
        public_key = key.get("public_key")
        if not isinstance(public_key, str) or not public_key.startswith("ssh-ed25519 "):
            raise ValueError("registered public_key is missing or not ssh-ed25519")
        canonical = canonical_bytes(message)
        with tempfile.TemporaryDirectory(prefix="ahp-agent-verify-") as td:
            td_path = Path(td)
            allowed = td_path / "allowed_signers"
            payload = td_path / "payload.json"
            allowed.write_text(f"{sender} {public_key}\n", encoding="utf-8")
            payload.write_bytes(canonical)
            proc = subprocess.run(
                [
                    "ssh-keygen", "-Y", "verify",
                    "-f", str(allowed),
                    "-I", sender,
                    "-n", NAMESPACE,
                    "-s", str(args.signature),
                ],
                stdin=payload.open("rb"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
        if proc.returncode != 0:
            raise ValueError("cryptographic signature verification failed")
        print("AGENT IDENTITY: KEY_BOUND_IDENTITY")
        print(f"agent_id: {sender}")
        print(f"key_id: {key_id}")
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"AGENT IDENTITY: UNVERIFIED - {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
