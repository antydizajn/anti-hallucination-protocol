#!/usr/bin/env python3
"""Adversarial tests for scripts/verify_claim.py.

The priority is preventing false VERIFIED/FOUND results. A verifier that fails
closed with ERROR is preferable to one that converts an execution failure into
positive evidence.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_claim.py"


def run_verifier(*args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    payload = json.loads(completed.stdout.strip())
    return completed.returncode, payload


class VerifyClaimTests(unittest.TestCase):
    def test_existing_file_is_found(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
            handle.write("alpha\nbeta\n")
            handle.flush()
            code, payload = run_verifier("file-exists", handle.name)
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")

    def test_missing_file_is_not_found_not_error(self) -> None:
        missing = str(Path(tempfile.gettempdir()) / "verify-claim-definitely-missing-7f41a")
        Path(missing).unlink(missing_ok=True)
        code, payload = run_verifier("file-exists", missing)
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "NOT_FOUND")

    def test_literal_match_does_not_treat_regex_metacharacters_as_regex(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
            handle.write("value=a.b\nvalue=axb\n")
            handle.flush()
            code, payload = run_verifier("file-contains", handle.name, "a.b")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")
        self.assertEqual(payload["evidence"]["matches"][0]["text"], "value=a.b")

    def test_invalid_regex_is_error_not_not_found(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
            handle.write("alpha\n")
            handle.flush()
            code, payload = run_verifier("file-contains", handle.name, "(", "--regex")
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")

    def test_out_of_range_line_is_not_found(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
            handle.write("one\ntwo\n")
            handle.flush()
            code, payload = run_verifier("file-line", handle.name, "99", "two")
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "NOT_FOUND")

    def test_nonzero_command_exit_cannot_be_verified_by_matching_stderr(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "MAGIC_MATCH",
            "--",
            sys.executable,
            "-c",
            "import sys; print('MAGIC_MATCH', file=sys.stderr); raise SystemExit(7)",
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")
        self.assertEqual(payload["evidence"]["returncode"], 7)

    def test_expected_output_with_required_exit_is_found(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "MAGIC_MATCH",
            "--",
            sys.executable,
            "-c",
            "print('MAGIC_MATCH')",
        )
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")

    def test_empty_expected_is_rejected(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "",
            "--",
            sys.executable,
            "-c",
            "print('anything')",
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")

    def test_custom_required_exit_must_match_exactly(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "EXPECTED_FAILURE",
            "--require-exit",
            "3",
            "--",
            sys.executable,
            "-c",
            "import sys; print('EXPECTED_FAILURE'); raise SystemExit(3)",
        )
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")
        self.assertEqual(payload["evidence"]["returncode"], 3)


if __name__ == "__main__":
    unittest.main()
