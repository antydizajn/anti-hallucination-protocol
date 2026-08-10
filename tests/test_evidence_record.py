from __future__ import annotations

import copy
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
    lineage_verification="VERIFIED",
    lineage_basis="independent primary observation",
    independence_group="primary-observation",
    source="primary-source",
    source_class="primary",
    source_identity="canonical source identity",
    evidence_span="claim-matched span",
    retrieved_at="2026-01-01T12:00:00+00:00",
    freshness="CURRENT_ENOUGH",
    verifier="deterministic-or-explicit-verifier",
    verifier_failure_state="NONE_OBSERVED",
):
    return {
        "source": source,
        "source_class": source_class,
        "source_identity": source_identity,
        "evidence_span": evidence_span,
        "retrieved_at": retrieved_at,
        "freshness": freshness,
        "integrity": integrity,
        "lineage": lineage,
        "lineage_basis": lineage_basis,
        "lineage_verification": lineage_verification,
        "independence_group": independence_group,
        "entailment": entailment,
        "verifier": verifier,
        "verifier_failure_state": verifier_failure_state,
    }


def rec(
    state="SUPPORTED_WITH_SCOPE",
    risk="T2",
    claim_type="other",
    evidence=None,
    scope="checked source",
    observation_time=None,
):
    result = {
        "claim_id": "c1",
        "claim": "X",
        "claim_type": claim_type,
        "risk_tier": risk,
        "state": state,
        "scope": scope,
        "evidence": evidence or [ev()],
    }
    if observation_time is not None:
        result["observation_time"] = observation_time
    return result


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


def test_contradicted_requires_contradicting_evidence():
    errors = mod.validate(rec(state="CONTRADICTED", evidence=[ev(entailment="UNCLEAR")]))
    assert any("requires at least one CONTRADICTS" in e for e in errors)


def test_contradicted_with_decisive_contradiction_is_structurally_valid():
    assert mod.validate(rec(state="CONTRADICTED", evidence=[ev(entailment="CONTRADICTS")])) == []


def test_contradicted_cannot_hide_surviving_support():
    errors = mod.validate(
        rec(state="CONTRADICTED", evidence=[ev(), ev(entailment="CONTRADICTS")])
    )
    assert any("use CONFLICT when both sides remain" in e for e in errors)


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
    assert any("requires an INDEPENDENT_ORIGIN" in e for e in errors)


def test_t3_unknown_lineage_cannot_be_promoted_to_independent():
    errors = mod.validate(rec(risk="T3", evidence=[ev(lineage="UNKNOWN")]))
    assert any("requires an INDEPENDENT_ORIGIN" in e for e in errors)


def test_t3_self_declared_independence_without_basis_fails():
    errors = mod.validate(rec(risk="T3", evidence=[ev(lineage_basis=None)]))
    assert any("non-empty lineage_basis" in e for e in errors)


def test_t3_heuristic_independence_cannot_earn_strong_state():
    errors = mod.validate(rec(risk="T3", evidence=[ev(lineage_verification="HEURISTIC")]))
    assert any("VERIFIED lineage" in e for e in errors)


def test_t3_verified_independence_requires_group():
    errors = mod.validate(rec(risk="T3", evidence=[ev(independence_group=None)]))
    assert any("requires a non-empty independence_group" in e for e in errors)


def test_t3_duplicate_independence_groups_are_rejected():
    errors = mod.validate(
        rec(
            risk="T3",
            evidence=[
                ev(source="source-a", source_identity="identity-a", independence_group="shared-origin"),
                ev(source="source-b", source_identity="identity-b", independence_group="shared-origin"),
            ],
        )
    )
    assert any("cannot reuse the same independence_group" in e for e in errors)


def test_t3_distinct_declared_groups_pass_structural_contract():
    assert mod.validate(
        rec(
            risk="T3",
            evidence=[
                ev(source="source-a", source_identity="identity-a", independence_group="group-a"),
                ev(source="source-b", source_identity="identity-b", independence_group="group-b"),
            ],
        )
    ) == []


def test_t3_unknown_source_class_cannot_earn_strong_state():
    errors = mod.validate(rec(risk="T3", evidence=[ev(source_class="unknown")]))
    assert any("source_class=unknown" in e for e in errors)


def test_t3_suspect_integrity_cannot_earn_strong_state():
    errors = mod.validate(rec(risk="T3", evidence=[ev(integrity="SUSPECT")]))
    assert any("integrity=CLEAN_OBSERVED" in e for e in errors)


def test_t3_unknown_integrity_cannot_earn_strong_state():
    errors = mod.validate(rec(risk="T3", evidence=[ev(integrity="UNKNOWN")]))
    assert any("integrity=CLEAN_OBSERVED" in e for e in errors)


def test_t3_requires_source_identity():
    errors = mod.validate(rec(risk="T3", evidence=[ev(source_identity=None)]))
    assert any("requires source_identity" in e for e in errors)


def test_t3_requires_evidence_span():
    errors = mod.validate(rec(risk="T3", evidence=[ev(evidence_span=None)]))
    assert any("requires evidence_span" in e for e in errors)


def test_t3_requires_retrieved_at():
    errors = mod.validate(rec(risk="T3", evidence=[ev(retrieved_at=None)]))
    assert any("requires retrieved_at" in e for e in errors)


def test_t3_retrieved_at_must_be_rfc3339():
    errors = mod.validate(rec(risk="T3", evidence=[ev(retrieved_at=".")]))
    assert any("retrieved_at must be a strict RFC3339" in e for e in errors)


def test_t3_retrieved_at_rejects_python_iso_space_separator():
    errors = mod.validate(
        rec(risk="T3", evidence=[ev(retrieved_at="2026-01-01 12:00:00+00:00")])
    )
    assert any("retrieved_at must be a strict RFC3339" in e for e in errors)


def test_t3_future_retrieved_at_is_rejected():
    errors = mod.validate(rec(risk="T3", evidence=[ev(retrieved_at="2999-01-01T00:00:00Z")]))
    assert any("retrieved_at cannot be materially in the future" in e for e in errors)


def test_t3_requires_verifier_provenance():
    errors = mod.validate(rec(risk="T3", evidence=[ev(verifier=None)]))
    assert any("requires verifier provenance" in e for e in errors)


def test_t3_requires_clean_verifier_state_for_supporting_evidence():
    errors = mod.validate(rec(risk="T3", evidence=[ev(verifier_failure_state="UNKNOWN")]))
    assert any("requires verifier_failure_state=NONE_OBSERVED" in e for e in errors)


def test_t3_current_state_requires_observation_time():
    errors = mod.validate(rec(risk="T3", claim_type="current_state"))
    assert any("requires observation_time" in e for e in errors)


def test_t3_current_state_observation_time_must_be_rfc3339():
    errors = mod.validate(
        rec(risk="T3", claim_type="current_state", observation_time="not-a-time")
    )
    assert any("observation_time must be a strict RFC3339" in e for e in errors)


def test_t3_current_state_future_observation_time_is_rejected():
    errors = mod.validate(
        rec(risk="T3", claim_type="current_state", observation_time="2999-01-01T00:00:00Z")
    )
    assert any("observation_time cannot be materially in the future" in e for e in errors)


def test_t3_current_state_requires_current_enough_evidence():
    errors = mod.validate(
        rec(
            risk="T3",
            claim_type="current_state",
            observation_time="2026-01-01T12:00:00+00:00",
            evidence=[ev(freshness="UNKNOWN")],
        )
    )
    assert any("freshness=CURRENT_ENOUGH" in e for e in errors)


def test_t3_current_state_full_auditable_record_passes_contract():
    r = rec(
        risk="T3",
        claim_type="current_state",
        observation_time="2026-01-01T12:00:00+00:00",
        evidence=[ev()],
    )
    assert mod.validate(r) == []


def test_terra_opaque_current_state_false_pass_is_closed():
    bad = rec(
        risk="T3",
        claim_type="current_state",
        evidence=[
            ev(
                source="opaque-string",
                source_class="unknown",
                source_identity=None,
                evidence_span=None,
                retrieved_at=None,
                freshness="UNKNOWN",
                lineage="INDEPENDENT_ORIGIN",
                lineage_basis=None,
                lineage_verification="UNKNOWN",
                independence_group=None,
                verifier=None,
                verifier_failure_state="UNKNOWN",
            )
        ],
    )
    errors = mod.validate(bad)
    assert errors
    assert any("observation_time" in e for e in errors)
    assert any("source_class=unknown" in e for e in errors)
    assert any("lineage_basis" in e for e in errors)


def test_incomplete_t3_record_cannot_pass_schema_gate():
    bad = {
        "state": "SUPPORTED_WITH_SCOPE",
        "risk_tier": "T3",
        "scope": "unattributed scope",
        "evidence": [{"entailment": "ENTAILS", "lineage": "INDEPENDENT_ORIGIN"}],
    }
    errors = mod.validate(bad)
    assert errors
    assert any("missing required field" in e for e in errors)


def test_unknown_state_is_rejected():
    bad = rec()
    bad["state"] = "TOTALLY_UNKNOWN_STATE"
    assert any("allowed enum" in e for e in mod.validate(bad))


def test_unknown_risk_tier_is_rejected():
    bad = rec()
    bad["risk_tier"] = "T9000"
    assert any("allowed enum" in e for e in mod.validate(bad))


def test_unknown_entailment_is_rejected():
    bad = rec(evidence=[ev()])
    bad["evidence"][0]["entailment"] = "TRUST_ME_BRO"
    assert any("allowed enum" in e for e in mod.validate(bad))


def test_unknown_integrity_is_rejected():
    bad = rec(evidence=[ev()])
    bad["evidence"][0]["integrity"] = "TOTALLY_FINE_PROBABLY"
    assert any("allowed enum" in e for e in mod.validate(bad))


def test_unknown_lineage_is_rejected():
    bad = rec(evidence=[ev()])
    bad["evidence"][0]["lineage"] = "FIVE_AGENTS_AGREE"
    assert any("allowed enum" in e for e in mod.validate(bad))


def test_unknown_lineage_verification_is_rejected():
    bad = rec(evidence=[ev()])
    bad["evidence"][0]["lineage_verification"] = "FIVE_AGENTS_AGREE"
    assert any("allowed enum" in e for e in mod.validate(bad))


def test_non_object_evidence_item_is_rejected_without_crash():
    bad = rec(evidence=["not-an-evidence-object"])
    errors = mod.validate(bad)
    assert errors
    assert any("expected type object" in e for e in errors)


def test_additional_properties_are_rejected():
    bad = rec()
    bad["evidence"][0]["confidence_the_model_felt"] = 0.999
    assert any("additional property" in e for e in mod.validate(bad))


def test_unimplemented_schema_keyword_fails_closed():
    schema = copy.deepcopy(mod.load_schema())
    schema["properties"]["claim"]["pattern"] = "^X$"
    errors = mod.validate_schema_definition(schema)
    assert any("unsupported schema keyword 'pattern'" in e for e in errors)


def test_validate_refuses_schema_it_cannot_fully_interpret():
    schema = copy.deepcopy(mod.load_schema())
    schema["properties"]["claim"]["maxLength"] = 10
    errors = mod.validate(rec(), schema=schema)
    assert any("unsupported schema keyword 'maxLength'" in e for e in errors)
