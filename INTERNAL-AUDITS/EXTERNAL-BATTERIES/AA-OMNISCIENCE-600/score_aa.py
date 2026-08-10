#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_IDS = set(range(1, 601))
ALLOWED_OUTCOMES = {"CORRECT", "INCORRECT", "PARTIAL", "NOT_ATTEMPTED"}
ALLOWED_EVALUATOR_TYPES = {"HUMAN", "MODEL_JUDGE", "MIXED"}


def main() -> int:
    p = argparse.ArgumentParser(description="Aggregate independently adjudicated AA-Omniscience results")
    p.add_argument("results", type=Path, help="JSON containing evaluator metadata and 600 adjudicated records")
    p.add_argument("output", type=Path)
    args = p.parse_args()

    data = json.loads(args.results.read_text(encoding="utf-8"))
    evaluator = data.get("evaluator")
    if not isinstance(evaluator, dict):
        raise SystemExit("ERROR: evaluator metadata is required")
    for key in ("name", "version", "type"):
        if not str(evaluator.get(key) or "").strip():
            raise SystemExit(f"ERROR: evaluator.{key} is required")
    if evaluator["type"] not in ALLOWED_EVALUATOR_TYPES:
        raise SystemExit(f"ERROR: evaluator.type must be one of {sorted(ALLOWED_EVALUATOR_TYPES)}")

    rows = data.get("results")
    if not isinstance(rows, list) or len(rows) != 600:
        raise SystemExit("ERROR: expected exactly 600 adjudicated result records")

    ids: list[int] = []
    counts = {
        "correct_count": 0,
        "incorrect_count": 0,
        "partial_count": 0,
        "not_attempted_count": 0,
    }

    for row in rows:
        try:
            qid = int(row["question_id"])
        except Exception as exc:
            raise SystemExit(f"ERROR: invalid/missing question_id: {row.get('question_id')!r}") from exc
        ids.append(qid)

        # Infrastructure/treatment failures are never epistemic abstention.
        # Such rows must be rerun before semantic scoring is considered valid.
        run_status = row.get("run_status")
        if run_status != "OK":
            raise SystemExit(
                f"ERROR: question_id={qid} has run_status={run_status!r}; "
                "RUNTIME ERROR != NOT_ATTEMPTED and cannot enter semantic scoring"
            )

        outcome = row.get("outcome")
        if outcome not in ALLOWED_OUTCOMES:
            raise SystemExit(f"ERROR: question_id={qid} has unknown outcome {outcome!r}")
        if outcome == "CORRECT":
            counts["correct_count"] += 1
        elif outcome == "INCORRECT":
            counts["incorrect_count"] += 1
        elif outcome == "PARTIAL":
            counts["partial_count"] += 1
        else:
            counts["not_attempted_count"] += 1

    if len(ids) != len(set(ids)) or set(ids) != EXPECTED_IDS:
        raise SystemExit("ERROR: question_id set must be unique and exactly 1..600")

    attempted = counts["correct_count"] + counts["incorrect_count"] + counts["partial_count"]
    useful = counts["correct_count"] + counts["partial_count"]
    total = len(rows)

    result = {
        "schema": "aa-omniscience-score-v2",
        "evaluator": evaluator,
        **counts,
        "attempt_rate": attempted / total,
        "incorrect_rate_among_attempts": counts["incorrect_count"] / attempted if attempted else None,
        "useful_coverage": useful / total,
        # This is an AHP diagnostic summary, not asserted to be the upstream
        # AA-Omniscience leaderboard metric. Report component metrics alongside it.
        "ahp_diagnostic_aggregate_score": (counts["correct_count"] - counts["incorrect_count"]) / total,
        "warning": "PUBLIC_DATASET_NOT_HELD_OUT",
        "boundaries": [
            "RUNTIME_ERROR_IS_NOT_NOT_ATTEMPTED",
            "MODEL_JUDGE_SCORE_IS_NOT_GROUND_TRUTH" if evaluator["type"] in {"MODEL_JUDGE", "MIXED"} else "HUMAN_ADJUDICATION_RECORDED",
            "DIAGNOSTIC_AGGREGATE_IS_NOT_CLAIMED_AS_UPSTREAM_OFFICIAL_SCORE",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
