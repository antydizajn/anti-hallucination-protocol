#!/usr/bin/env python3
"""Semantic validator for Anti-Hallucination Protocol v5 evidence records.

This checker intentionally validates only a small set of invariants that can be
checked deterministically. It does not decide whether prose evidence truly
entails a claim.

Exit codes:
  0 = deterministic invariants passed
  1 = one or more invariants failed
  2 = invocation / I/O / JSON error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STRONG = "SUPPORTED_WITH_SCOPE"


def validate(record: dict) -> list[str]:
    errors: list[str] = []

    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return ["evidence must be a non-empty list"]

    state = record.get("state")
    risk = record.get("risk_tier")
    scope = record.get("scope")

    if state == STRONG and not isinstance(scope, str):
        errors.append("SUPPORTED_WITH_SCOPE requires an explicit non-empty scope")
    elif state == STRONG and not scope.strip():
        errors.append("SUPPORTED_WITH_SCOPE requires an explicit non-empty scope")

    entails = [e for e in evidence if e.get("entailment") == "ENTAILS"]
    contradictions = [e for e in evidence if e.get("entailment") == "CONTRADICTS"]
    contaminated = [e for e in evidence if e.get("integrity") == "CONTAMINATED"]
    failed_verifiers = [e for e in evidence if e.get("verifier_failure_state") == "FAILED"]
    unknown_scope_signals = [e for e in evidence if e.get("entailment") in {"UNCLEAR", "IRRELEVANT"}]

    if state == STRONG and not entails:
        errors.append("SUPPORTED_WITH_SCOPE requires at least one ENTAILS evidence item")
    if state == STRONG and contradictions:
        errors.append("SUPPORTED_WITH_SCOPE cannot coexist with CONTRADICTS evidence")
    if state == STRONG and contaminated:
        errors.append("SUPPORTED_WITH_SCOPE cannot rely on CONTAMINATED evidence")
    if state == STRONG and failed_verifiers:
        errors.append("SUPPORTED_WITH_SCOPE cannot rely on evidence whose verifier FAILED")

    if state == "CONTRADICTED" and not contradictions:
        errors.append("CONTRADICTED requires at least one CONTRADICTS evidence item")

    if state == "CONFLICT":
        if not entails or not contradictions:
            errors.append("CONFLICT requires both supporting and contradicting evidence")

    if state == "NOT_FOUND_WITHIN_SCOPE" and entails:
        errors.append("NOT_FOUND_WITHIN_SCOPE cannot coexist with ENTAILS evidence")

    if state == "ERROR" and not any(
        e.get("verifier_failure_state") == "FAILED" for e in evidence
    ):
        errors.append("ERROR state should record at least one FAILED verifier")

    if risk == "T3" and state == STRONG:
        lineages = {
            e.get("lineage")
            for e in entails
            if e.get("lineage") in {"INDEPENDENT_ORIGIN", "SHARED_ORIGIN", "DERIVED_COPY", "UNKNOWN"}
        }
        if lineages <= {"DERIVED_COPY", "SHARED_ORIGIN"}:
            errors.append(
                "T3 SUPPORTED_WITH_SCOPE has no supporting evidence marked as an independent origin"
            )
        if all(e.get("lineage") == "UNKNOWN" for e in entails):
            errors.append(
                "T3 SUPPORTED_WITH_SCOPE cannot claim independence when all supporting lineage is UNKNOWN"
            )

    # A strong verdict dominated by unclear/irrelevant evidence is suspicious even if one
    # item entails. Do not fail solely because weak extra evidence exists, but require the
    # strong evidence to outnumber zero - already guaranteed above. This comment documents
    # why we intentionally avoid a fake quantitative threshold here.
    _ = unknown_scope_signals

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()

    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not isinstance(record, dict):
        print("FAIL: evidence record must be a JSON object")
        return 1

    errors = validate(record)
    if errors:
        print("EVIDENCE RECORD: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("EVIDENCE RECORD: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
