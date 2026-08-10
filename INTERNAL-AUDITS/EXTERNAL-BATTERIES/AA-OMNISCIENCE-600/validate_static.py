#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = {
    "SOURCE.md",
    "CONTAMINATION-BOUNDARY.md",
    "MANIFEST.md",
    "prepare_questions.py",
    "verify_source.py",
    "run_aa_arm.py",
    "score_schema.md",
    "score_aa.py",
    "HERMES-RUNBOOK.md",
}
PYTHON_FILES = {"prepare_questions.py", "verify_source.py", "run_aa_arm.py", "score_aa.py", "validate_static.py"}


def fail(message: str) -> None:
    raise SystemExit(f"AA STATIC: FAIL - {message}")


def require_text(path: Path, *needles: str) -> str:
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path.name} missing required contract text: {needle!r}")
    return text


def main() -> int:
    missing = sorted(name for name in REQUIRED if not (ROOT / name).is_file())
    if missing:
        fail(f"missing required files: {missing}")

    for name in sorted(PYTHON_FILES):
        path = ROOT / name
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"Python syntax error in {name}: {exc}")

    verifier = require_text(
        ROOT / "verify_source.py",
        "4a8ffc87c4650054825fb767fe0da4a4fc97ff32",
        'FILENAME = "AA-Omniscience_dataset_public.csv"',
        '"artifact_sha256"',
        '"schema_sha256"',
        '["EXTERNAL", "PUBLIC", "NOT_HELD_OUT"]',
    )
    if "EXPECTED_ROWS = 600" not in verifier:
        fail("verify_source.py does not pin the 600-row public artifact contract")

    prepare = require_text(
        ROOT / "prepare_questions.py",
        "--source-identity",
        '"aa-omniscience-question-v2"',
        '"source_artifact_sha256"',
        '"source_revision"',
    )
    # The source reader necessarily sees row["answer"], but generated record
    # construction must never assign an answer field.
    if '"answer": row[' in prepare or "'answer': row[" in prepare:
        fail("prepare_questions.py appears to copy gold answers into generation records")

    runner = require_text(
        ROOT / "run_aa_arm.py",
        '"hermes", "-p", profile',
        '"chat"',
        '"-q", str(item["prompt"])',
        '"-s", "anti-hallucination-protocol"',
        "PRELOAD_MARKER",
        "RUN-IDENTITY.json",
        "run_identity_sha256",
        "prompt-size",
        'tools.get("count") != 0',
        "tool_call_count",
        "RUNTIME_ERROR_IS_NOT_NOT_ATTEMPTED",
    )
    if '"-z"' in runner or "' -z '" in runner:
        fail("run_aa_arm.py must not use Hermes -z until skill/cwd/reasoning propagation is re-proven")

    scorer = require_text(
        ROOT / "score_aa.py",
        'run_status != "OK"',
        "RUNTIME ERROR != NOT_ATTEMPTED",
        "ahp_diagnostic_aggregate_score",
        "evaluator",
        "MODEL_JUDGE",
    )
    if '"aggregate_score"' in scorer:
        fail("ambiguous aggregate_score field reintroduced; keep local diagnostic explicitly named")

    require_text(
        ROOT / "CONTAMINATION-BOUNDARY.md",
        "PUBLIC DATASET != HELD-OUT DATASET",
        "EXTERNAL DATASET != INDEPENDENT REPLICATION",
        "ERROR != NOT_ATTEMPTED",
        "STATIC PASS != HERMES RUNTIME PASS",
    )
    require_text(
        ROOT / "HERMES-RUNBOOK.md",
        "03fa32c92dd445eb64c7f67434dd91b32c40701d",
        "does not use Hermes `-z`",
        "RUNTIME_UNVERIFIED",
    )
    require_text(
        ROOT / "MANIFEST.md",
        "b71cc9d06b58c8f12e06b77606a279f536a18959",
        "94bfd13f9c4818a949775bd73c1c0d91ce6a3116",
        "PRELOAD REQUESTED != PRELOAD OBSERVED",
    )

    print("AA STATIC: PASS")
    print("Boundary: static contract integrity only; no dataset/model runtime executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
