#!/usr/bin/env python3
"""Small deterministic verifier for anti-hallucination-protocol.

The script distinguishes positive evidence, negative evidence, and verifier
failure. It is not a semantic theorem prover: FOUND means only that the selected
narrow check succeeded within its stated scope.

Exit codes:
  0 = FOUND / verified within the selected mode's scope
  1 = NOT_FOUND / check ran successfully but evidence did not match
  2 = ERROR / invalid invocation, I/O failure, command failure, decoding failure,
      output-limit failure, or verifier error
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NoReturn

FOUND = 0
NOT_FOUND = 1
ERROR = 2
DEFAULT_MAX_OUTPUT_BYTES = 1_000_000


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


def _path_kind(path: Path) -> str:
    try:
        if path.is_symlink():
            return "symlink"
        if path.is_file():
            return "file"
        if path.is_dir():
            return "directory"
        if os.path.lexists(path):
            return "other"
        return "missing"
    except OSError:
        return "error"


def mode_file_exists(args: argparse.Namespace) -> int:
    path = Path(args.path)
    claim = f"path exists with required kind {args.kind}: {path}"
    try:
        exists = os.path.lexists(path)
        kind = _path_kind(path)
    except OSError as exc:
        emit(
            "ERROR",
            claim=claim,
            evidence={"path": str(path)},
            detail=f"filesystem check failed: {exc}",
        )
        return ERROR

    evidence = {"path": str(path), "observed_kind": kind, "required_kind": args.kind}
    if not exists:
        emit(
            "NOT_FOUND",
            claim=claim,
            evidence=evidence,
            detail="path does not exist at this exact path",
        )
        return NOT_FOUND

    if args.kind != "any" and kind != args.kind:
        emit(
            "NOT_FOUND",
            claim=claim,
            evidence=evidence,
            detail=f"path exists, but observed kind {kind!r} does not match required kind {args.kind!r}",
        )
        return NOT_FOUND

    emit(
        "FOUND",
        claim=claim,
        evidence=evidence,
        detail="path exists with the required kind",
    )
    return FOUND


def read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeError) as exc:
        return None, str(exc)


def mode_file_contains(args: argparse.Namespace) -> int:
    if not args.pattern.strip():
        fail("file-contains pattern must not be empty or whitespace-only")

    path = Path(args.path)
    if not path.is_file():
        kind = _path_kind(path)
        emit(
            "ERROR",
            claim=f"file contains pattern: {path}",
            evidence={"path": str(path), "observed_kind": kind},
            detail="file-contains requires a regular file",
        )
        return ERROR

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
    if not args.expected.strip():
        fail("file-line expected text must not be empty or whitespace-only")

    path = Path(args.path)
    if not path.is_file():
        emit(
            "ERROR",
            claim=f"line {args.line} contains expected text: {path}",
            evidence={"path": str(path), "observed_kind": _path_kind(path)},
            detail="file-line requires a regular file",
        )
        return ERROR

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


def _decode_utf8(data: bytes, stream_name: str) -> tuple[str | None, str | None]:
    try:
        return data.decode("utf-8", errors="strict"), None
    except UnicodeDecodeError as exc:
        return None, f"{stream_name} is not valid UTF-8: {exc}"


def mode_command_output(args: argparse.Namespace) -> int:
    command = list(args.command)
    if not command:
        fail("command-output requires a command after --")
    if not args.expected.strip():
        fail("--expected must not be empty or whitespace-only")

    try:
        # Spool process output to temporary files. This avoids retaining arbitrarily
        # large stdout/stderr in memory before the evidentiary size limit is checked.
        with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
            completed = subprocess.run(
                command,
                stdout=stdout_file,
                stderr=stderr_file,
                text=False,
                timeout=args.timeout,
                check=False,
            )
            stdout_size = stdout_file.tell()
            stderr_size = stderr_file.tell()
            total_bytes = stdout_size + stderr_size
            if total_bytes > args.max_output_bytes:
                emit(
                    "ERROR",
                    claim="command output contains expected text",
                    evidence={
                        "command": command,
                        "returncode": completed.returncode,
                        "stdout_bytes": stdout_size,
                        "stderr_bytes": stderr_size,
                        "captured_output_bytes": total_bytes,
                        "max_output_bytes": args.max_output_bytes,
                    },
                    detail="captured output exceeded verifier limit; output was not accepted as evidence",
                )
                return ERROR
            stdout_file.seek(0)
            stderr_file.seek(0)
            stdout_bytes = stdout_file.read()
            stderr_bytes = stderr_file.read()
    except subprocess.TimeoutExpired as exc:
        emit(
            "ERROR",
            claim="command output contains expected text",
            evidence={"command": command, "timeout_seconds": args.timeout},
            detail=f"command exceeded timeout: {exc}",
        )
        return ERROR
    except (OSError, subprocess.SubprocessError) as exc:
        emit(
            "ERROR",
            claim="command output contains expected text",
            evidence={"command": command},
            detail=f"command could not be executed: {exc}",
        )
        return ERROR

    stdout, stdout_err = _decode_utf8(stdout_bytes, "stdout")
    stderr, stderr_err = _decode_utf8(stderr_bytes, "stderr")
    decode_error = stdout_err or stderr_err
    if decode_error is not None:
        emit(
            "ERROR",
            claim="command output contains expected text",
            evidence={
                "command": command,
                "returncode": completed.returncode,
                "stdout_bytes": len(stdout_bytes),
                "stderr_bytes": len(stderr_bytes),
            },
            detail=decode_error,
        )
        return ERROR

    assert stdout is not None and stderr is not None
    evidence = {
        "command": command,
        "returncode": completed.returncode,
        "required_exit": args.require_exit,
        "expected": args.expected,
        "stdout": stdout,
        "stderr": stderr,
    }

    if completed.returncode != args.require_exit:
        emit(
            "ERROR",
            claim="command output contains expected text",
            evidence=evidence,
            detail=f"command exit code {completed.returncode} != required {args.require_exit}; output match is not accepted as verification",
        )
        return ERROR

    if args.expected in stdout or args.expected in stderr:
        emit(
            "FOUND",
            claim="command output contains expected text",
            evidence=evidence,
            detail="command exited with required code and stdout or stderr contained expected text",
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
    p_exists.add_argument("--kind", choices=["any", "file", "directory", "symlink"], default="any")
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
    p_cmd.add_argument("--max-output-bytes", type=int, default=DEFAULT_MAX_OUTPUT_BYTES)
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
    if getattr(args, "max_output_bytes", 1) < 1:
        fail("--max-output-bytes must be >= 1")

    command = getattr(args, "command", None)
    if command and command[0] == "--":
        args.command = command[1:]

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
