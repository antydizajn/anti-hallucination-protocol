#!/usr/bin/env python3
"""Deterministic validator for Anti-Hallucination Protocol evidence records.

The validator has three layers:

1. reject schema keywords the checker does not implement;
2. validate the record against references/evidence-record.schema.json;
3. validate deterministic cross-field invariants.

It does not decide whether prose evidence truly entails a claim, whether a
source identity is factually correct, or whether two sources are truly
independent. A successful result means only that the record satisfies the
declared machine-readable contract and implemented deterministic invariants.

Exit codes:
  0 = STRUCTURALLY_VALID: schema + deterministic invariants passed
  1 = one or more record validation rules failed
  2 = invocation / I/O / JSON / unsupported-schema error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

STRONG = "SUPPORTED_WITH_SCOPE"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "references" / "evidence-record.schema.json"
MAX_CLOCK_SKEW = timedelta(minutes=5)
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)

# This checker deliberately implements a small JSON Schema subset. Failing on
# an unknown keyword is safer than silently ignoring a future assertion.
SUPPORTED_SCHEMA_KEYS = {
    "$schema",
    "$id",
    "title",
    "description",
    "type",
    "enum",
    "required",
    "properties",
    "additionalProperties",
    "items",
    "minItems",
    "minLength",
}


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "null":
        return value is None
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return False


def validate_schema_definition(schema: Any, path: str = "$schema") -> list[str]:
    """Reject schema constructs this deterministic checker would ignore."""

    if not isinstance(schema, dict):
        return [f"{path}: schema node must be an object"]

    errors: list[str] = []
    for key in schema:
        if key not in SUPPORTED_SCHEMA_KEYS:
            errors.append(f"{path}: unsupported schema keyword {key!r}")

    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict):
            errors.append(f"{path}.properties: must be an object")
        else:
            for key, child in properties.items():
                if not isinstance(key, str):
                    errors.append(f"{path}.properties: property names must be strings")
                    continue
                errors.extend(validate_schema_definition(child, f"{path}.properties.{key}"))

    items = schema.get("items")
    if items is not None:
        errors.extend(validate_schema_definition(items, f"{path}.items"))

    return errors


def validate_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON-Schema subset used by evidence-record.schema.json."""

    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type is not None:
        allowed = expected_type if isinstance(expected_type, list) else [expected_type]
        if not isinstance(allowed, list) or not all(isinstance(t, str) for t in allowed):
            return [f"{path}: schema has invalid type declaration"]
        if not any(_matches_type(instance, t) for t in allowed):
            return [f"{path}: expected type {'|'.join(allowed)}"]

    enum = schema.get("enum")
    if enum is not None and instance not in enum:
        errors.append(f"{path}: value {instance!r} is not in allowed enum {enum!r}")

    if isinstance(instance, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(instance) < min_length:
            errors.append(f"{path}: string length must be >= {min_length}")

    if isinstance(instance, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            errors.append(f"{path}: array must contain at least {min_items} item(s)")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                errors.extend(validate_schema(item, item_schema, f"{path}[{index}]"))

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            return [f"{path}: schema properties must be an object"]
        required = schema.get("required", [])
        if not isinstance(required, list) or not all(isinstance(k, str) for k in required):
            return [f"{path}: schema required must be a string list"]
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required field {key!r}")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in properties:
                    errors.append(f"{path}: additional property {key!r} is not allowed")
        for key, value in instance.items():
            child_schema = properties.get(key)
            if isinstance(child_schema, dict):
                errors.extend(validate_schema(value, child_schema, f"{path}.{key}"))
    return errors


def load_schema(path: Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("evidence schema must be a JSON object")
    definition_errors = validate_schema_definition(data)
    if definition_errors:
        raise ValueError("; ".join(definition_errors))
    return data


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_rfc3339(value: Any) -> datetime | None:
    if not _nonempty(value):
        return None
    text = value.strip()
    if not RFC3339_RE.fullmatch(text):
        return None
    normalized = text
    if normalized.endswith(("Z", "z")):
        normalized = normalized[:-1] + "+00:00"
    if "t" in normalized:
        normalized = normalized.replace("t", "T", 1)
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _validate_timestamp(value: Any, label: str, *, reject_future: bool = False) -> list[str]:
    parsed = _parse_rfc3339(value)
    if parsed is None:
        return [f"{label} must be a strict RFC3339 timestamp with timezone"]
    if reject_future and parsed > datetime.now(timezone.utc) + MAX_CLOCK_SKEW:
        return [f"{label} cannot be materially in the future"]
    return []


def validate(record: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    schema = schema if schema is not None else load_schema()
    definition_errors = validate_schema_definition(schema)
    if definition_errors:
        return definition_errors

    schema_errors = validate_schema(record, schema)
    if schema_errors:
        return schema_errors

    errors: list[str] = []
    evidence = record["evidence"]
    state = record["state"]
    risk = record["risk_tier"]
    claim_type = record["claim_type"]
    scope = record.get("scope")

    entails = [e for e in evidence if e["entailment"] == "ENTAILS"]
    contradictions = [e for e in evidence if e["entailment"] == "CONTRADICTS"]
    contaminated = [e for e in evidence if e["integrity"] == "CONTAMINATED"]
    failed_verifiers = [e for e in evidence if e["verifier_failure_state"] == "FAILED"]

    if state == STRONG and not _nonempty(scope):
        errors.append("SUPPORTED_WITH_SCOPE requires an explicit non-empty scope")
    if state == STRONG and not entails:
        errors.append("SUPPORTED_WITH_SCOPE requires at least one ENTAILS evidence item")
    if state == STRONG and contradictions:
        errors.append("SUPPORTED_WITH_SCOPE cannot coexist with CONTRADICTS evidence")
    if state == STRONG and contaminated:
        errors.append("SUPPORTED_WITH_SCOPE cannot retain CONTAMINATED evidence as support")
    if state == STRONG and failed_verifiers:
        errors.append("SUPPORTED_WITH_SCOPE cannot rely on evidence whose verifier FAILED")

    if state == "CONTRADICTED" and not contradictions:
        errors.append("CONTRADICTED requires at least one CONTRADICTS evidence item")
    if state == "CONTRADICTED" and entails:
        errors.append("CONTRADICTED cannot coexist with surviving ENTAILS evidence; use CONFLICT when both sides remain")
    if state == "CONFLICT" and (not entails or not contradictions):
        errors.append("CONFLICT requires both supporting and contradicting evidence")
    if state == "NOT_FOUND_WITHIN_SCOPE" and entails:
        errors.append("NOT_FOUND_WITHIN_SCOPE cannot coexist with ENTAILS evidence")
    if state == "ERROR" and not failed_verifiers:
        errors.append("ERROR state should record at least one FAILED verifier")

    if risk == "T3" and state == STRONG and entails:
        verified_independent = [
            e
            for e in entails
            if e["lineage"] == "INDEPENDENT_ORIGIN"
            and e["lineage_verification"] == "VERIFIED"
            and _nonempty(e.get("lineage_basis"))
        ]
        if not verified_independent:
            errors.append(
                "T3 SUPPORTED_WITH_SCOPE requires an INDEPENDENT_ORIGIN with VERIFIED lineage and non-empty lineage_basis"
            )

        groups: list[str] = []
        for item in verified_independent:
            group = item.get("independence_group")
            if not _nonempty(group):
                errors.append(
                    "T3 verified independent supporting evidence requires a non-empty independence_group"
                )
            else:
                groups.append(group.strip())
        if len(groups) != len(set(groups)):
            errors.append(
                "T3 verified independent supporting evidence cannot reuse the same independence_group"
            )

        if any(e["source_class"] == "unknown" for e in entails):
            errors.append("T3 SUPPORTED_WITH_SCOPE cannot rely on source_class=unknown")

        for index, item in enumerate(entails):
            if item["integrity"] != "CLEAN_OBSERVED":
                errors.append(
                    f"T3 supporting evidence #{index + 1} requires integrity=CLEAN_OBSERVED"
                )
            if not _nonempty(item.get("source_identity")):
                errors.append(f"T3 supporting evidence #{index + 1} requires source_identity")
            if not _nonempty(item.get("evidence_span")):
                errors.append(f"T3 supporting evidence #{index + 1} requires evidence_span")
            if not _nonempty(item.get("retrieved_at")):
                errors.append(f"T3 supporting evidence #{index + 1} requires retrieved_at")
            else:
                errors.extend(
                    _validate_timestamp(
                        item.get("retrieved_at"),
                        f"T3 supporting evidence #{index + 1} retrieved_at",
                        reject_future=True,
                    )
                )
            if item["verifier_failure_state"] != "NONE_OBSERVED":
                errors.append(
                    f"T3 supporting evidence #{index + 1} requires verifier_failure_state=NONE_OBSERVED"
                )
            if not _nonempty(item.get("verifier")):
                errors.append(f"T3 supporting evidence #{index + 1} requires verifier provenance")

    if risk == "T3" and state == STRONG and claim_type == "current_state":
        if not _nonempty(record.get("observation_time")):
            errors.append("T3 current_state SUPPORTED_WITH_SCOPE requires observation_time")
        else:
            errors.extend(
                _validate_timestamp(
                    record.get("observation_time"),
                    "T3 current_state observation_time",
                    reject_future=True,
                )
            )
        for index, item in enumerate(entails):
            if item["freshness"] != "CURRENT_ENOUGH":
                errors.append(
                    f"T3 current_state supporting evidence #{index + 1} requires freshness=CURRENT_ENOUGH"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
        schema = load_schema(args.schema)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not isinstance(record, dict):
        print("EVIDENCE RECORD: FAIL")
        print("- $: expected type object")
        return 1

    errors = validate(record, schema=schema)
    if errors:
        print("EVIDENCE RECORD: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("EVIDENCE RECORD: STRUCTURALLY_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
