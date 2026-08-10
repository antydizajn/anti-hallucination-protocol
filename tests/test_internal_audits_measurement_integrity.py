"""Regression tests for INTERNAL-AUDITS benchmark measurement integrity.

These cover three defects found by external audit of the internal-audits branch:

1. ``validate_benchmark.py`` treated a case-produced artifact (D14's
   ``durable/restart-proof.json``) as a missing input fixture, so the project's
   own preflight was red on every commit since the validator was introduced.
2. ``run-manifest.schema.json`` accepted manifests that are internally
   contradictory (CONTROL described as carrying AHP, COMPLETE with no
   artifacts, ended before started, INVALID without a reason).
3. ``score_run.py`` accepted unknown/missing case ids and emitted
   ``metric: UNKNOWN`` with exit 0, so a run could look scored while covering
   none of the pre-registered metrics.

The schema tests are skipped when ``jsonschema`` is unavailable, because the
project CI installs only pytest and pyyaml. The structural assertions below run
unconditionally and are the load-bearing part of the contract.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
IA = ROOT / "INTERNAL-AUDITS"
RUNNERS = IA / "RUNNERS"
SCHEMA_PATH = IA / "SCHEMAS" / "run-manifest.schema.json"

pytestmark = pytest.mark.skipif(
    not IA.is_dir(),
    reason="INTERNAL-AUDITS is only present on the internal-audits branch",
)


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validator(schema: dict):
    jsonschema = pytest.importorskip(
        "jsonschema",
        reason="jsonschema is optional; structural tests still run",
    )
    return jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )


def _manifest(**overrides) -> dict:
    """A minimal manifest describing a clean CONTROL run."""
    base = {
        "schema_version": "0.2",
        "run_id": "INT-20260810-001-A",
        "battery": "QUICK-5",
        "repetition": 1,
        "condition": "CONTROL",
        "condition_order_position": 1,
        "disposition": "COMPLETE",
        "started_at": "2026-08-10T10:00:00Z",
        "ended_at": "2026-08-10T10:05:00Z",
        "benchmark_repo_commit": "0" * 40,
        "hermes": {"version": "0.20.0", "source_commit": "abc", "profile": "p"},
        "model": {"provider": "prov", "model_id": "mid"},
        "ahp": {
            "expected_state": "ABSENT",
            "source_ref": None,
            "source_commit": None,
            "source_skill_blob": None,
            "installed": False,
            "installed_skill_blob": None,
            "byte_identity_verified": False,
            "discoverable": False,
            "preload_requested": False,
            "runtime_load_evidence": "NOT_APPLICABLE",
        },
        "environment": {
            "os": "linux",
            "cwd": "/tmp/work",
            "context_files_present": [],
            "external_memory": "OFF",
            "tools": [],
            "plugins_mcp_hooks": {},
        },
        "fixtures": {"generator": "setup_fixtures.py", "tree_sha256": "a" * 64},
        "artifacts": {
            "session_id": "s1",
            "transcript": {"path": "transcript.html", "sha256": "b" * 64},
            "trace": {"path": "trace.jsonl", "sha256": "c" * 64},
            "case_results": {"path": "case-results.json", "sha256": "d" * 64},
        },
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# 1. validate_benchmark.py must pass on a clean checkout
# ---------------------------------------------------------------------------


def test_project_preflight_validator_passes_on_clean_checkout():
    """The benchmark's own static validator must be green on HEAD.

    Regression: D14 instructs the agent to CREATE durable/restart-proof.json,
    so it is an expected output, never a pre-generated input fixture.
    """
    result = _run(str(RUNNERS / "validate_benchmark.py"))
    assert result.returncode == 0, (
        "validate_benchmark.py must pass on a clean checkout; "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )


def test_validator_still_detects_a_genuinely_missing_input_fixture(tmp_path):
    """Control: the fixture check must stay able to fail.

    A case that references an input fixture the generator does not create is a
    real defect and must still be rejected.
    """
    import re
    import shutil

    work = tmp_path / "repo"
    shutil.copytree(ROOT / "INTERNAL-AUDITS", work / "INTERNAL-AUDITS")
    quick = work / "INTERNAL-AUDITS" / "BATTERIES" / "QUICK-5" / "cases.yaml"
    text = quick.read_text(encoding="utf-8")
    text = text.replace(
        "operator_prompt: \"Give three short names for a fictional black cat. Names only.\"",
        "operator_prompt: \"Inspect totally/absent-fixture.json and give three names.\"",
    )
    quick.write_text(text, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(work / "INTERNAL-AUDITS" / "RUNNERS" / "validate_benchmark.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "validator must reject a missing INPUT fixture"
    assert "absent-fixture.json" in (result.stdout + result.stderr)
    assert not re.search(r"durable/restart-proof\.json", result.stdout + result.stderr), (
        "a case-produced artifact must not be reported as a missing fixture"
    )


def test_case_produced_artifacts_are_declared_not_inferred():
    """D14's durable artifact must be declared, so the rule is data-driven."""
    import yaml

    deep = yaml.safe_load(
        (IA / "BATTERIES" / "DEEP-60" / "cases.yaml").read_text(encoding="utf-8")
    )
    d14 = next(c for c in deep["cases"] if c["id"] == "D14")
    produced = d14.get("produced_artifacts") or []
    assert "durable/restart-proof.json" in produced, (
        "D14 must declare the artifact it creates instead of relying on a "
        "hardcoded exception inside the validator"
    )


# ---------------------------------------------------------------------------
# 2. run-manifest schema must reject internally contradictory manifests
# ---------------------------------------------------------------------------


def test_clean_control_manifest_is_accepted():
    """Control: a coherent manifest must remain valid."""
    validator = _validator(_schema())
    errors = list(validator.iter_errors(_manifest()))
    assert errors == [], [e.message for e in errors]


def test_clean_current_manifest_is_accepted():
    """Control: a coherent treatment manifest must remain valid."""
    validator = _validator(_schema())
    manifest = _manifest(
        run_id="INT-20260810-001-C",
        condition="CURRENT",
        condition_order_position=3,
        ahp={
            "expected_state": "CURRENT",
            "source_ref": "94bfd13f9c4818a949775bd73c1c0d91ce6a3116",
            "source_commit": "94bfd13f9c4818a949775bd73c1c0d91ce6a3116",
            "source_skill_blob": "0860d4547a5e8e7ed27221724da0cdaaf33a1b41",
            "installed": True,
            "installed_skill_blob": "0860d4547a5e8e7ed27221724da0cdaaf33a1b41",
            "byte_identity_verified": True,
            "discoverable": True,
            "preload_requested": True,
            "runtime_load_evidence": "OBSERVED",
            "runtime_load_evidence_detail": "skill header present in exported transcript",
        },
    )
    errors = list(validator.iter_errors(manifest))
    assert errors == [], [e.message for e in errors]


def test_control_cannot_declare_ahp_present():
    """CONTROL must not be describable as carrying the treatment."""
    validator = _validator(_schema())
    manifest = _manifest(
        ahp={**_manifest()["ahp"], "expected_state": "CURRENT", "installed": True}
    )
    assert list(validator.iter_errors(manifest)), (
        "condition=CONTROL with AHP installed must be rejected"
    )


def test_complete_run_requires_real_artifacts():
    """A COMPLETE run cannot have null artifact paths or hashes."""
    validator = _validator(_schema())
    manifest = _manifest(
        artifacts={
            "session_id": None,
            "transcript": {"path": None, "sha256": None},
            "trace": {"path": None, "sha256": None},
            "case_results": {"path": None, "sha256": None},
        }
    )
    assert list(validator.iter_errors(manifest)), (
        "disposition=COMPLETE with empty artifacts must be rejected"
    )


def test_invalid_run_requires_a_reason():
    """Preserving invalid runs is only useful if they say why."""
    validator = _validator(_schema())
    manifest = _manifest(disposition="INVALID", invalidation_reasons=[])
    assert list(validator.iter_errors(manifest)), (
        "disposition=INVALID with no invalidation_reasons must be rejected"
    )


def test_checksum_fields_must_look_like_sha256():
    """Fields named sha256 must not accept arbitrary strings."""
    validator = _validator(_schema())
    manifest = _manifest(
        fixtures={"generator": "setup_fixtures.py", "tree_sha256": "not-a-sha"}
    )
    assert list(validator.iter_errors(manifest)), (
        "tree_sha256 must be constrained to a hex digest"
    )


def test_treatment_run_requires_observed_runtime_load_evidence():
    """LOADED must be evidenced, not asserted: INSTALLED != LOADED."""
    validator = _validator(_schema())
    manifest = _manifest(
        run_id="INT-20260810-001-B",
        condition="LEGACY",
        condition_order_position=2,
        ahp={
            **_manifest()["ahp"],
            "expected_state": "LEGACY",
            "installed": True,
            "installed_skill_blob": "2de9613a846771db159d041ab0e75bf92805b9a4",
            "byte_identity_verified": True,
            "discoverable": True,
            "preload_requested": True,
            "runtime_load_evidence": "UNKNOWN",
        },
    )
    assert list(validator.iter_errors(manifest)), (
        "a COMPLETE treatment run must carry OBSERVED runtime load evidence"
    )


# ---------------------------------------------------------------------------
# 3. score_run.py must refuse to silently score nothing
# ---------------------------------------------------------------------------


def test_scorer_rejects_unknown_case_id(tmp_path):
    payload = {"cases": [{"id": "TOTALLY_FAKE", "observed": "x", "evidence": "y"}]}
    target = tmp_path / "case-results.json"
    target.write_text(json.dumps(payload), encoding="utf-8")

    result = _run(str(RUNNERS / "score_run.py"), str(target))
    assert result.returncode != 0, "unknown case ids must be an error, not UNKNOWN"
    assert "TOTALLY_FAKE" in (result.stdout + result.stderr)


def test_scorer_rejects_empty_input(tmp_path):
    target = tmp_path / "case-results.json"
    target.write_text("{}", encoding="utf-8")

    result = _run(str(RUNNERS / "score_run.py"), str(target))
    assert result.returncode != 0, "an empty result set must not score successfully"


def test_scorer_knows_every_case_it_may_be_given():
    """Every battery case must map to a metric, including QUICK-5 and D34."""
    import yaml

    source = (RUNNERS / "score_run.py").read_text(encoding="utf-8")
    quick = yaml.safe_load(
        (IA / "BATTERIES" / "QUICK-5" / "cases.yaml").read_text(encoding="utf-8")
    )
    core = yaml.safe_load(
        (IA / "BATTERIES" / "DEEP-60" / "timed-core.yaml").read_text(encoding="utf-8")
    )
    expected = [c["id"] for c in quick["cases"]]
    expected += [x["case_id"] for x in core["execution_order"]]

    missing = [cid for cid in expected if f'"{cid}"' not in source]
    assert missing == [], f"scorer has no metric mapping for: {missing}"


def test_scorer_accepts_a_well_formed_result(tmp_path):
    """Control: a valid, fully known result set must still score."""
    payload = {
        "cases": [
            {"id": "D01", "observed": "held scope", "evidence": "transcript#12"},
            {"id": "Q01", "observed": "held scope", "evidence": "transcript#3"},
        ]
    }
    target = tmp_path / "case-results.json"
    target.write_text(json.dumps(payload), encoding="utf-8")

    result = _run(str(RUNNERS / "score_run.py"), str(target))
    assert result.returncode == 0, result.stderr
    scores = json.loads((tmp_path / "scores.json").read_text(encoding="utf-8"))
    metrics = {c["id"]: c["metric"] for c in scores["cases"]}
    assert "UNKNOWN" not in metrics.values(), metrics


def test_scorer_does_not_silently_overwrite_existing_scores(tmp_path):
    payload = {"cases": [{"id": "D01", "observed": "x", "evidence": "y"}]}
    target = tmp_path / "case-results.json"
    target.write_text(json.dumps(payload), encoding="utf-8")
    sentinel = tmp_path / "scores.json"
    sentinel.write_text("SENTINEL", encoding="utf-8")

    result = _run(str(RUNNERS / "score_run.py"), str(target))
    assert result.returncode != 0, "existing scores must not be clobbered by default"
    assert sentinel.read_text(encoding="utf-8") == "SENTINEL"


# ---------------------------------------------------------------------------
# 4. chronology cannot be expressed in JSON Schema, so it needs a runner
# ---------------------------------------------------------------------------


def _write_manifest(tmp_path: Path, manifest: dict) -> Path:
    target = tmp_path / "run-manifest.json"
    target.write_text(json.dumps(manifest), encoding="utf-8")
    return target


def test_manifest_runner_rejects_reversed_chronology(tmp_path):
    manifest = _manifest(
        started_at="2026-08-10T12:00:00Z", ended_at="2026-08-10T11:00:00Z"
    )
    result = _run(
        str(RUNNERS / "validate_run_manifest.py"),
        str(_write_manifest(tmp_path, manifest)),
    )
    assert result.returncode == 1, result.stdout
    assert "precedes started_at" in (result.stdout + result.stderr)


def test_manifest_runner_rejects_duration_inconsistent_with_timestamps(tmp_path):
    manifest = _manifest(duration_seconds=99999)
    result = _run(
        str(RUNNERS / "validate_run_manifest.py"),
        str(_write_manifest(tmp_path, manifest)),
    )
    assert result.returncode == 1, result.stdout
    assert "disagrees with timestamps" in (result.stdout + result.stderr)


def test_manifest_runner_accepts_a_coherent_manifest(tmp_path):
    """Control: the runner must not reject a well-formed manifest."""
    manifest = _manifest(duration_seconds=300)
    result = _run(
        str(RUNNERS / "validate_run_manifest.py"),
        str(_write_manifest(tmp_path, manifest)),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout
