#!/usr/bin/env python3
"""Canonicalize the signed portion of an AHP agent message.

Produces deterministic UTF-8 JSON bytes suitable for detached signing.
Fails closed on floats to avoid cross-runtime representation ambiguity.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from typing import Any


def reject_floats(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise ValueError(f"{path}: floats are forbidden in signed agent payloads")
    if isinstance(value, list):
        for i, item in enumerate(value):
            reject_floats(item, f"{path}[{i}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_floats(item, f"{path}.{key}")


def canonical_bytes(message: dict[str, Any]) -> bytes:
    if not isinstance(message, dict):
        raise ValueError("message must be a JSON object")
    signed = message.get("signed")
    if not isinstance(signed, dict):
        raise ValueError("message must contain object field 'signed'")
    if signed.get("protocol") != "ahp-agent-bus-v1":
        raise ValueError("signed.protocol must equal 'ahp-agent-bus-v1'")
    reject_floats(signed)
    return json.dumps(
        signed,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("message", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    try:
        data = json.loads(args.message.read_text(encoding="utf-8"))
        out = canonical_bytes(data)
        if args.output:
            args.output.write_bytes(out)
        else:
            sys.stdout.buffer.write(out)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
