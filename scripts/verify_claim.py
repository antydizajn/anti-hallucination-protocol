#!/usr/bin/env python3
"""Small deterministic verifier for anti-hallucination-protocol.

The script deliberately distinguishes positive evidence, negative evidence, and
verification failure. It is not a universal theorem prover and must not be used
to claim more than the selected mode can establish.

Exit codes:
  0 = FOUND / verified within the mode's scope
  1 = NOT_FOUND / check ran successfully but evidence did not match
  2 = ERROR / invalid invocation, I/O failure, command failure, or verifier error
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

FOUND = 0
NOT_FOUND = 1
ERROR = 2


def emit(status: str, *, claim: str, evidence: dict, detail: str) -> None:
    print(
        json.dumps(
            {
                "status": status,
                "claim": claim,
                "evidence": evidence,
                "detail": detail,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def fail(message: str) -> NoReturn:
    emit("ERROR", claim="verifier invocation", evidence={}, detail=message)
    raise SystemExit(ERROR)


def mode_file_exists(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        exists = path.exists()
    except OSError as exc:
        emit(
            "ERROR",
            claim=f"path exists: {path}",
            evidence={"path": str(path)},
            detail=f"filesystem check failed: {exc}",
        )
        return ERROR

    if exists:
        emit(
            "FOUND",
            claim=f"path exists: {path}",
            evidence={"path": str(path), "kind": "filesystem"},
            detail="path exists",
        )
        return FOUND

    emit(
        "NOT_FOUND",
        claim=f"path exists: {path}",
        evidence={"path": str(path), "kind": "filesystem"},
        detail="path does not exist at this exact path",
    )
    return NOT_FOUND


def read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeError) as exc:
        return None, str(exc)


def mode_file_contains(args: argparse.Namespace) -> int:
    path = Path(args.path)
    text, err = read_text(path)
    claim = f"file contains pattern: {path}"
    if err is not None:
        emit(
            "ERROR",
            claim=claim,
            evidence={"path": str(path)},
            detail=f"could not read UTF-8 text: {err}",
        )
        return ERROR

    assert text is not None
    try:
        matcher = re.compile(args.pattern) if args.regex else None
    except re.error as exc:
        emit(
            "ERROR",
            claim=claim,
            evidence={"path": str(path), "pattern": args.pattern, "regex": True},
            detail=f"invalid regular expression: {exc}",
        )
        return ERROR

    matches: list[dict[str, object]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        hit = bool(matcher.search(line)) if matcher else args.pattern in line
        if hit:
            matches.append({"line": lineno, "text": line})
            if len(matches) >= args.max_matches:
                break

    evidence = {
        "path": str(path),
        "pattern": args.pattern,
        "regex": bool(args.regex),
        "matches": matches,
    }
    if matches:
        emit("FOUND", claim=claim, evidence=evidence, detail="pattern matched file content")
        return FOUND

    emit(
        "NOT_FOUND",
        claim=claim,
        evidence=evidence,
        detail="pattern did not match this file; this does not prove absence elsewhere",
    )
    return NOT_FOUND


def mode_file_line(args: argparse.Namespace) -> int:
    if args.line < 1:
        fail("--line must be >= 1")

    path = Path(args.path)
    text, err = read_text(path)
    claim = f"line {args.line} contains expected text: {path}"
    if err is not None:
        emit(
            "ERROR",
            claim=claim,
            evidence={"path": str(path), "line": args.line},
            detail=f"could not read UTF-8 text: {err}",
        )
        return ERROR

    assert text is not None
    lines = text.splitlines()
    if args.line > len(lines):
        emit(
            "NOT_FOUND",
            claim=claim,
            evidence={"path": str(path), "line": args.line, "line_count": len(lines)},
            detail="requested line is outside the file",
        )
        return NOT_FOUND

    actual = lines[args.line - 1]
    evidence = {
        "path": str(path),
        "line": args.line,
        "actual": actual,
        "expected": args.expected,
    }
    if args.expected in actual:
        emit("FOUND", claim=claim, evidence=evidence, detail="expected text is present on exact line")
        return FOUND

    emit("NOT_FOUND", claim=claim, evidence=evidence, detail="expected text is absent from exact line")
    return NOT_FOUND


def mode_command_output(args: argparse.Namespace) -> int:
    command = list(args.command)
    if not command:
        fail("command-output requires a command after --")
    if args.expected == "":
        fail("--expected must not be empty")

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=args.timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        emit(
            "ERROR",
            claim="command output contains expected text",
            evidence={"command": command},
            detail=f"command could not be executed: {exc}",
        )
        return ERROR

    output = completed.stdout + completed.stderr
    evidence = {
        "command": command,
        "returncode": completed.returncode,
        "expected": args.expected,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }

    if completed.returncode != args.require_exit:
        emit(
            "ERROR",
            claim="command output contains expected text",
            evidence=evidence,
            detail=f"command exit code {completed.returncode} != required {args.require_exit}; output match is not accepted as verification",
        )
        return ERROR

    if args.expected in output:
        emit(
            "FOUND",
            claim="command output contains expected text",
            evidence=evidence,
            detail="command exited with required code and output contained expected text",
        )
        return FOUND

    emit(
        "NOT_FOUND",
        claim="command output contains expected text",
        evidence=evidence,
        detail="command exited with required code but expected text was absent",
    )
    return NOT_FOUND


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)

    p_exists = sub.add_parser("file-exists")
    p_exists.add_argument("path")
    p_exists.set_defaults(func=mode_file_exists)

    p_contains = sub.add_parser("file-contains")
    p_contains.add_argument("path")
    p_contains.add_argument("pattern")
    p_contains.add_argument("--regex", action="store_true")
    p_contains.add_argument("--max-matches", type=int, default=5)
    p_contains.set_defaults(func=mode_file_contains)

    p_line = sub.add_parser("file-line")
    p_line.add_argument("path")
    p_line.add_argument("line", type=int)
    p_line.add_argument("expected")
    p_line.set_defaults(func=mode_file_line)

    p_cmd = sub.add_parser("command-output")
    p_cmd.add_argument("--expected", required=True)
    p_cmd.add_argument("--require-exit", type=int, default=0)
    p_cmd.add_argument("--timeout", type=float, default=30.0)
    p_cmd.add_argument("command", nargs=argparse.REMAINDER)
    p_cmd.set_defaults(func=mode_command_output)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if getattr(args, "max_matches", 1) < 1:
        fail("--max-matches must be >= 1")
    if getattr(args, "timeout", 1.0) <= 0:
        fail("--timeout must be > 0")

    command = getattr(args, "command", None)
    if command and command[0] == "--":
        args.command = command[1:]

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
