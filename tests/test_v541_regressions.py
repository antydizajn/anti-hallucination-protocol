from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_claim.py"
EVIDENCE = ROOT / "scripts" / "check_evidence_record.py"

spec = importlib.util.spec_from_file_location("check_evidence_record_v541", EVIDENCE)
assert spec and spec.loader
evmod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = evmod
spec.loader.exec_module(evmod)


def run_verifier(*args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(VERIFY), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, json.loads(completed.stdout.strip())


def ev(**overrides):
    value = {
        "source": "primary-source",
        "source_class": "primary",
        "source_identity": "canonical-source",
        "evidence_span": "claim-matched span",
        "retrieved_at": "2026-01-01T12:00:00+00:00",
        "freshness": "CURRENT_ENOUGH",
        "integrity": "CLEAN_OBSERVED",
        "lineage": "INDEPENDENT_ORIGIN",
        "lineage_basis": "independent primary observation",
        "lineage_verification": "VERIFIED",
        "independence_group": "primary-observation",
        "entailment": "ENTAILS",
        "verifier": "explicit verifier",
        "verifier_failure_state": "NONE_OBSERVED",
    }
    value.update(overrides)
    return value


def rec(**overrides):
    value = {
        "claim_id": "c1",
        "claim": "X",
        "claim_type": "other",
        "risk_tier": "T2",
        "state": "SUPPORTED_WITH_SCOPE",
        "scope": "checked scope",
        "evidence": [ev()],
    }
    value.update(overrides)
    return value


def test_empty_literal_file_contains_is_error():
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
        handle.write("anything\n")
        handle.flush()
        code, payload = run_verifier("file-contains", handle.name, "")
    assert code == 2
    assert payload["status"] == "ERROR"


def test_empty_regex_file_contains_is_error():
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
        handle.write("anything\n")
        handle.flush()
        code, payload = run_verifier("file-contains", handle.name, "", "--regex")
    assert code == 2
    assert payload["status"] == "ERROR"


def test_empty_file_line_expected_is_error():
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
        handle.write("anything\n")
        handle.flush()
        code, payload = run_verifier("file-line", handle.name, "1", "")
    assert code == 2
    assert payload["status"] == "ERROR"


def test_command_match_cannot_cross_stdout_stderr_boundary():
    code, payload = run_verifier(
        "command-output",
        "--expected",
        "MAGIC",
        "--",
        sys.executable,
        "-c",
        "import sys; sys.stdout.write('MAG'); sys.stderr.write('IC')",
    )
    assert code == 1
    assert payload["status"] == "NOT_FOUND"


def test_not_found_within_scope_requires_scope():
    errors = evmod.validate(
        rec(state="NOT_FOUND_WITHIN_SCOPE", scope="   ", evidence=[ev(entailment="UNCLEAR")])
    )
    assert any("requires an explicit non-empty scope" in e for e in errors)


def test_t3_same_source_cannot_claim_distinct_independence_groups():
    errors = evmod.validate(
        rec(
            risk_tier="T3",
            evidence=[
                ev(source="same", source_identity="id-a", independence_group="g-a"),
                ev(source="same", source_identity="id-b", independence_group="g-b"),
            ],
        )
    )
    assert any("same source under different independence groups" in e for e in errors)


def test_t3_same_source_identity_cannot_claim_distinct_independence_groups():
    errors = evmod.validate(
        rec(
            risk_tier="T3",
            evidence=[
                ev(source="a", source_identity="same-id", independence_group="g-a"),
                ev(source="b", source_identity="same-id", independence_group="g-b"),
            ],
        )
    )
    assert any("same source_identity under different independence groups" in e for e in errors)


def test_whitespace_claim_id_is_rejected():
    errors = evmod.validate(rec(claim_id="   "))
    assert any("claim_id must be" in e for e in errors)


def test_whitespace_claim_is_rejected():
    errors = evmod.validate(rec(claim="   "))
    assert any("claim must be" in e for e in errors)


def test_whitespace_source_is_rejected():
    errors = evmod.validate(rec(evidence=[ev(source="   ")]))
    assert any("source must be" in e for e in errors)


def test_partial_requires_some_partial_or_supporting_evidence():
    errors = evmod.validate(rec(state="PARTIAL", evidence=[ev(entailment="IRRELEVANT")]))
    assert any("PARTIAL requires at least one ENTAILS or PARTIAL" in e for e in errors)


def test_schema_valued_additional_properties_fails_closed():
    schema = copy.deepcopy(evmod.load_schema())
    schema["properties"]["evidence"]["items"]["additionalProperties"] = {
        "type": "string",
        "pattern": "^x$",
    }
    errors = evmod.validate_schema_definition(schema)
    assert any("schema-valued additionalProperties is not implemented" in e for e in errors)
