#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Aggregate AA-Omniscience adjudicated results")
    p.add_argument("results", type=Path, help="JSON with records containing outcome")
    p.add_argument("output", type=Path)
    args = p.parse_args()

    data = json.loads(args.results.read_text(encoding="utf-8"))
    rows = data.get("results")
    if not isinstance(rows, list) or len(rows) != 600:
        raise SystemExit("ERROR: expected exactly 600 adjudicated result records")

    counts = {
        "correct_count": 0,
        "incorrect_count": 0,
        "partial_count": 0,
        "not_attempted_count": 0,
    }

    for row in rows:
        outcome = row.get("outcome")
        if outcome == "CORRECT":
            counts["correct_count"] += 1
        elif outcome == "INCORRECT":
            counts["incorrect_count"] += 1
        elif outcome == "PARTIAL":
            counts["partial_count"] += 1
        elif outcome == "NOT_ATTEMPTED":
            counts["not_attempted_count"] += 1
        else:
            raise SystemExit(f"ERROR: unknown outcome {outcome!r}")

    attempted = counts["correct_count"] + counts["incorrect_count"] + counts["partial_count"]
    useful = counts["correct_count"] + counts["partial_count"]
    total = len(rows)

    result = {
        "schema": "aa-omniscience-score-v1",
        **counts,
        "attempt_rate": attempted / total,
        "incorrect_rate_among_attempts": counts["incorrect_count"] / attempted if attempted else None,
        "useful_coverage": useful / total,
        "aggregate_score": (counts["correct_count"] - counts["incorrect_count"]) / total,
        "warning": "PUBLIC_DATASET_NOT_HELD_OUT",
    }

    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
