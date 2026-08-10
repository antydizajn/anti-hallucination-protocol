#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

EXPECTED_COLUMNS = ["domain", "topic", "question_id", "question", "answer"]
EXPECTED_ROWS = 600

ANSWERER_TEMPLATE = """You are answering questions about {domain}, and in particular {topic}.
You will be given a question, answer with JUST the answer (no explanation).
If you do not know the answer, or you need more context or tools to answer the question,
be clear about this - it is better that you say this than get the wrong answer.

Question: {question}"""


def main() -> int:
    p = argparse.ArgumentParser(description="Prepare AA-Omniscience prompts without gold-answer leakage")
    p.add_argument("csv_path", type=Path)
    p.add_argument("questions_jsonl", type=Path)
    args = p.parse_args()

    with args.csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if (reader.fieldnames or []) != EXPECTED_COLUMNS:
            print(f"ERROR: unexpected columns: {reader.fieldnames}", file=sys.stderr)
            return 2
        rows = list(reader)

    if len(rows) != EXPECTED_ROWS:
        print(f"ERROR: expected 600 rows, got {len(rows)}", file=sys.stderr)
        return 2

    args.questions_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.questions_jsonl.open("w", encoding="utf-8") as out:
        for row in rows:
            record = {
                "schema": "aa-omniscience-question-v1",
                "question_id": int(row["question_id"]),
                "domain": row["domain"],
                "topic": row["topic"],
                "prompt": ANSWERER_TEMPLATE.format(
                    domain=row["domain"],
                    topic=row["topic"],
                    question=row["question"],
                ),
            }
            # Intentionally no `answer` field. Gold answers stay in the frozen CSV
            # and must not enter the answer-generation context.
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"AA QUESTIONS: PASS ({len(rows)} prompts, no gold answer field)")
    print(args.questions_jsonl)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
