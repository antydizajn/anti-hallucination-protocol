#!/usr/bin/env python3
"""Adversarial tests for scripts/verify_claim.py.

The priority is preventing false FOUND results. A verifier that fails closed
with ERROR is preferable to one that converts execution failure or malformed
output into positive evidence.
"""

from __future__ import annotations

import json
import os
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
            code, payload = run_verifier("file-exists", handle.name, "--kind", "file")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")
        self.assertEqual(payload["evidence"]["observed_kind"], "file")

    def test_missing_file_is_not_found_not_error(self) -> None:
        missing = str(Path(tempfile.gettempdir()) / "verify-claim-definitely-missing-7f41a")
        Path(missing).unlink(missing_ok=True)
        code, payload = run_verifier("file-exists", missing)
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "NOT_FOUND")

    def test_directory_does_not_satisfy_required_file_kind(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            code, payload = run_verifier("file-exists", directory, "--kind", "file")
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "NOT_FOUND")
        self.assertEqual(payload["evidence"]["observed_kind"], "directory")

    def test_directory_can_be_verified_as_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            code, payload = run_verifier("file-exists", directory, "--kind", "directory")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unsupported")
    def test_symlink_requires_explicit_symlink_kind_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target.txt"
            link = Path(directory) / "link.txt"
            target.write_text("x", encoding="utf-8")
            os.symlink(target, link)
            code, payload = run_verifier("file-exists", str(link), "--kind", "symlink")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")
        self.assertEqual(payload["evidence"]["observed_kind"], "symlink")

    def test_literal_match_does_not_treat_regex_metacharacters_as_regex(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
            handle.write("value=a.b\nvalue=axb\n")
            handle.flush()
            code, payload = run_verifier("file-contains", handle.name, "a.b")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "FOUND")
        self.assertEqual(payload["evidence"]["matches"][0]["text"], "value=a.b")

    def test_file_contains_rejects_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            code, payload = run_verifier("file-contains", directory, "anything")
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")

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

    def test_invalid_utf8_command_output_is_structured_error(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "anything",
            "--",
            sys.executable,
            "-c",
            "import os; os.write(1, b'\\xff')",
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")
        self.assertIn("not valid UTF-8", payload["detail"])

    def test_oversized_output_is_error_not_evidence(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "MAGIC_MATCH",
            "--max-output-bytes",
            "64",
            "--",
            sys.executable,
            "-c",
            "print('MAGIC_MATCH' + 'x' * 200)",
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")
        self.assertIn("exceeded verifier limit", payload["detail"])

    def test_nonpositive_output_limit_is_rejected(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "x",
            "--max-output-bytes",
            "0",
            "--",
            sys.executable,
            "-c",
            "print('x')",
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")

    def test_timeout_is_structured_error(self) -> None:
        code, payload = run_verifier(
            "command-output",
            "--expected",
            "never",
            "--timeout",
            "0.05",
            "--",
            sys.executable,
            "-c",
            "import time; time.sleep(0.5)",
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "ERROR")
        self.assertIn("timeout", payload["detail"])


if __name__ == "__main__":
    unittest.main()
