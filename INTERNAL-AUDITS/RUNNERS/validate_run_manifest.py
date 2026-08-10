#!/usr/bin/env python3
"""Validate a benchmark run manifest: schema plus semantics the schema cannot express.

JSON Schema encodes the cross-field invariants (arm vs treatment state, COMPLETE vs
artifacts, INVALID vs reasons). Two things it cannot express are checked here:

* chronology: ``ended_at`` must not precede ``started_at``;
* ``duration_seconds`` must agree with the recorded timestamps.

Schema validation is skipped with a clear notice when ``jsonschema`` is absent, so
this runner is still useful in the project's pytest+pyyaml CI environment. The
semantic checks always run.

Usage:
  validate_run_manifest.py <run-manifest.json> [...]
Exit codes: 0 valid, 1 invalid manifest, 2 usage/IO error.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "SCHEMAS" / "run-manifest.schema.json"


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def semantic_errors(manifest: dict) -> list[str]:
    errors: list[str] = []
    started_raw = manifest.get("started_at")
    ended_raw = manifest.get("ended_at")

    started = ended = None
    for label, raw in (("started_at", started_raw), ("ended_at", ended_raw)):
        if not isinstance(raw, str):
            errors.append(f"{label} must be an ISO-8601 string")
            continue
        try:
            parsed = parse_timestamp(raw)
        except ValueError:
            errors.append(f"{label} is not a parseable ISO-8601 timestamp: {raw!r}")
            continue
        if label == "started_at":
            started = parsed
        else:
            ended = parsed

    if started and ended:
        if ended < started:
            errors.append(f"ended_at ({ended_raw}) precedes started_at ({started_raw})")
        measured = (ended - started).total_seconds()
        declared = manifest.get("duration_seconds")
        if isinstance(declared, (int, float)) and abs(declared - measured) > 2:
            errors.append(
                f"duration_seconds ({declared}) disagrees with timestamps ({measured:.0f}s)"
            )
    return errors


def schema_errors(manifest: dict) -> tuple[list[str], bool]:
    """Return (errors, schema_checked)."""
    try:
        import jsonschema
    except ImportError:
        return [], False
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )
    return [e.message for e in validator.iter_errors(manifest)], True


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    failed = False
    for arg in argv[1:]:
        path = Path(arg)
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: unreadable manifest {path}: {exc}", file=sys.stderr)
            return 2
        if not isinstance(manifest, dict):
            print(f"FAIL {path}: manifest must be a JSON object", file=sys.stderr)
            failed = True
            continue

        errors, schema_checked = schema_errors(manifest)
        errors += semantic_errors(manifest)

        if errors:
            failed = True
            print(f"FAIL {path}", file=sys.stderr)
            for message in errors:
                print(f"  - {message}", file=sys.stderr)
        else:
            suffix = "" if schema_checked else " (SCHEMA NOT CHECKED: jsonschema not installed)"
            print(f"PASS {path}{suffix}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
