#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_COLUMNS = ["domain", "topic", "question_id", "question", "answer"]
EXPECTED_ROWS = 600
EXPECTED_IDS = set(range(1, 601))
SOURCE_REPOSITORY = "ArtificialAnalysis/AA-Omniscience-Public"
SOURCE_REVISION = "4a8ffc87c4650054825fb767fe0da4a4fc97ff32"
SOURCE_ARTIFACT = "AA-Omniscience_dataset_public.csv"

ANSWERER_TEMPLATE = """You are answering questions about {domain}, and in particular {topic}.
You will be given a question, answer with JUST the answer (no explanation).
If you do not know the answer, or you need more context or tools to answer the question,
be clear about this - it is better that you say this than get the wrong answer.

Question: {question}"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_source_identity(path: Path, csv_path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema": "aa-omniscience-source-identity-v1",
        "source_repository": SOURCE_REPOSITORY,
        "revision": SOURCE_REVISION,
        "artifact": SOURCE_ARTIFACT,
        "row_count": EXPECTED_ROWS,
    }
    for key, expected in required.items():
        if data.get(key) != expected:
            raise ValueError(f"SOURCE-IDENTITY mismatch for {key}: {data.get(key)!r} != {expected!r}")
    observed_sha = sha256_file(csv_path)
    if data.get("artifact_sha256") != observed_sha:
        raise ValueError("CSV bytes do not match SOURCE-IDENTITY artifact_sha256")
    if data.get("classification") != ["EXTERNAL", "PUBLIC", "NOT_HELD_OUT"]:
        raise ValueError("unexpected contamination classification in SOURCE-IDENTITY")
    return data


def main() -> int:
    p = argparse.ArgumentParser(description="Prepare pinned AA-Omniscience prompts without gold-answer leakage")
    p.add_argument("csv_path", type=Path)
    p.add_argument("questions_jsonl", type=Path)
    p.add_argument(
        "--source-identity",
        type=Path,
        required=True,
        help="SOURCE-IDENTITY.json emitted by verify_source.py for these exact CSV bytes",
    )
    args = p.parse_args()

    csv_path = args.csv_path.resolve()
    identity_path = args.source_identity.resolve()
    try:
        source_identity = load_source_identity(identity_path, csv_path)
    except Exception as exc:
        print(f"ERROR: source identity verification failed: {exc}", file=sys.stderr)
        return 2

    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if (reader.fieldnames or []) != EXPECTED_COLUMNS:
            print(f"ERROR: unexpected columns: {reader.fieldnames}", file=sys.stderr)
            return 2
        rows = list(reader)

    if len(rows) != EXPECTED_ROWS:
        print(f"ERROR: expected {EXPECTED_ROWS} rows, got {len(rows)}", file=sys.stderr)
        return 2

    try:
        ids = [int(row["question_id"]) for row in rows]
    except Exception as exc:
        print(f"ERROR: invalid question_id: {exc}", file=sys.stderr)
        return 2
    if len(ids) != len(set(ids)) or set(ids) != EXPECTED_IDS:
        print("ERROR: question_id set must be unique and exactly 1..600", file=sys.stderr)
        return 2

    rows.sort(key=lambda row: int(row["question_id"]))
    artifact_sha = source_identity["artifact_sha256"]

    args.questions_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.questions_jsonl.open("w", encoding="utf-8") as out:
        for row in rows:
            record = {
                "schema": "aa-omniscience-question-v2",
                "question_id": int(row["question_id"]),
                "domain": row["domain"],
                "topic": row["topic"],
                "source_revision": SOURCE_REVISION,
                "source_artifact_sha256": artifact_sha,
                "prompt": ANSWERER_TEMPLATE.format(
                    domain=row["domain"],
                    topic=row["topic"],
                    question=row["question"],
                ),
            }
            # Gold answers remain only in the verified source CSV. They are never
            # copied into the answer-generation JSONL or model prompt.
            if "answer" in record:
                raise AssertionError("gold answer leakage invariant violated")
            out.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    print(f"AA QUESTIONS: PASS ({len(rows)} prompts, source-bound, no gold answer field)")
    print(f"source_revision={SOURCE_REVISION}")
    print(f"source_artifact_sha256={artifact_sha}")
    print(args.questions_jsonl)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
