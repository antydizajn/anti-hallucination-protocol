from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_evidence_record.py"

spec = importlib.util.spec_from_file_location("check_evidence_record", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def ev(
    *,
    entailment="ENTAILS",
    integrity="CLEAN_OBSERVED",
    lineage="INDEPENDENT_ORIGIN",
    verifier_failure_state="NONE_OBSERVED",
):
    return {
        "source": "primary-source",
        "source_class": "primary",
        "entailment": entailment,
        "integrity": integrity,
        "lineage": lineage,
        "verifier_failure_state": verifier_failure_state,
    }


def rec(state="SUPPORTED_WITH_SCOPE", risk="T2", evidence=None, scope="checked source"):
    return {
        "claim_id": "c1",
        "claim": "X",
        "claim_type": "other",
        "risk_tier": risk,
        "state": state,
        "scope": scope,
        "evidence": evidence or [ev()],
    }


def test_happy_path():
    assert mod.validate(rec()) == []


def test_supported_requires_scope():
    errors = mod.validate(rec(scope=""))
    assert any("explicit non-empty scope" in e for e in errors)


def test_supported_requires_entailing_evidence():
    errors = mod.validate(rec(evidence=[ev(entailment="UNCLEAR")]))
    assert any("at least one ENTAILS" in e for e in errors)


def test_supported_rejects_direct_contradiction():
    errors = mod.validate(rec(evidence=[ev(), ev(entailment="CONTRADICTS")]))
    assert any("cannot coexist with CONTRADICTS" in e for e in errors)


def test_contaminated_evidence_cannot_earn_supported():
    errors = mod.validate(rec(evidence=[ev(integrity="CONTAMINATED")]))
    assert any("CONTAMINATED" in e for e in errors)


def test_failed_verifier_cannot_earn_supported():
    errors = mod.validate(rec(evidence=[ev(verifier_failure_state="FAILED")]))
    assert any("verifier FAILED" in e for e in errors)


def test_conflict_requires_both_sides():
    errors = mod.validate(rec(state="CONFLICT", evidence=[ev()]))
    assert any("both supporting and contradicting" in e for e in errors)


def test_conflict_with_both_sides_passes():
    r = rec(state="CONFLICT", evidence=[ev(), ev(entailment="CONTRADICTS")])
    assert mod.validate(r) == []


def test_not_found_cannot_hide_entailing_evidence():
    errors = mod.validate(rec(state="NOT_FOUND_WITHIN_SCOPE", evidence=[ev()]))
    assert any("cannot coexist with ENTAILS" in e for e in errors)


def test_error_records_failed_verifier():
    errors = mod.validate(rec(state="ERROR", evidence=[ev(entailment="UNCLEAR")]))
    assert any("FAILED verifier" in e for e in errors)


def test_t3_shared_origin_is_not_independence():
    errors = mod.validate(
        rec(risk="T3", evidence=[ev(lineage="SHARED_ORIGIN"), ev(lineage="DERIVED_COPY")])
    )
    assert any("no supporting evidence marked as an independent origin" in e for e in errors)


def test_t3_unknown_lineage_cannot_be_promoted_to_independent():
    errors = mod.validate(rec(risk="T3", evidence=[ev(lineage="UNKNOWN")]))
    assert any("all supporting lineage is UNKNOWN" in e for e in errors)


def test_one_independent_origin_is_allowed_without_fake_source_count_rule():
    # The protocol may still require an explicit single-source limitation in prose,
    # but the deterministic checker does not invent a universal two-source rule.
    assert mod.validate(rec(risk="T3", evidence=[ev(lineage="INDEPENDENT_ORIGIN")])) == []
