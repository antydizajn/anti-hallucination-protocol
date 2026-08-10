#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required for static validation", file=sys.stderr)
    raise SystemExit(69)

ROOT = Path(__file__).resolve().parents[2]
IA = ROOT / "INTERNAL-AUDITS"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid YAML {path.relative_to(ROOT)}: {exc}")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def fixture_paths_from_generator(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    # The fixture generator intentionally stores paths as literal dict keys.
    return set(re.findall(r'^\s*"([A-Za-z0-9._/-]+)"\s*:', text, flags=re.M))


def main() -> int:
    required = [
        IA / "BENCHMARK-DESIGN.md",
        IA / "BATTERIES/QUICK-5/cases.yaml",
        IA / "BATTERIES/DEEP-60/cases.yaml",
        IA / "BATTERIES/DEEP-60/timed-core.yaml",
        IA / "SCHEMAS/run-manifest.schema.json",
        IA / "RUNNERS/bootstrap_profiles.sh",
        IA / "RUNNERS/install_frozen_ahp.sh",
        IA / "RUNNERS/setup_fixtures.py",
        IA / "RUNNERS/start_condition.sh",
        IA / "RUNNERS/collect_run.sh",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    quick = load_yaml(IA / "BATTERIES/QUICK-5/cases.yaml")
    deep = load_yaml(IA / "BATTERIES/DEEP-60/cases.yaml")
    core = load_yaml(IA / "BATTERIES/DEEP-60/timed-core.yaml")
    load_json(IA / "SCHEMAS/run-manifest.schema.json")

    qcases = quick.get("cases") or []
    dcases = deep.get("cases") or []
    if len(qcases) != 5:
        fail(f"QUICK-5 must contain exactly 5 cases, got {len(qcases)}")
    if len(dcases) != 60:
        fail(f"DEEP-60 pool must contain exactly 60 cases, got {len(dcases)}")

    qids = [c.get("id") for c in qcases]
    dids = [c.get("id") for c in dcases]
    if len(set(qids)) != len(qids):
        fail("duplicate QUICK-5 case id")
    if len(set(dids)) != len(dids):
        fail("duplicate DEEP-60 case id")
    if qids != [f"Q{i:02d}" for i in range(1, 6)]:
        fail(f"unexpected QUICK-5 ids: {qids}")
    if dids != [f"D{i:02d}" for i in range(1, 61)]:
        fail("DEEP-60 ids must be exactly D01..D60 in order")

    execution = core.get("execution_order") or []
    if not 12 <= len(execution) <= 15:
        fail(f"timed core must contain 12-15 probes, got {len(execution)}")
    core_ids = [x.get("case_id") for x in execution]
    unknown = [x for x in core_ids if x not in set(dids)]
    if unknown:
        fail(f"timed core references unknown pool cases: {unknown}")
    if len(core_ids) != len(set(core_ids)):
        fail("timed core contains duplicate case ids")
    if core_ids[-1] != "D14":
        fail("D14 durable restart probe must be last in timed core")
    seq = [x.get("sequence") for x in execution]
    if seq != list(range(1, len(execution) + 1)):
        fail(f"timed-core sequence is not contiguous: {seq}")

    fixtures = fixture_paths_from_generator(IA / "RUNNERS/setup_fixtures.py")
    known_fixture_refs = set()
    for corpus in (quick, deep):
        for case in corpus.get("cases") or []:
            text = " ".join(str(case.get(k, "")) for k in ("setup", "operator_prompt", "operator_prompts", "pass_rule"))
            for m in re.findall(r'(?<![A-Za-z0-9_-])([A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)+)', text):
                if not m.startswith(("http/", "https/")):
                    known_fixture_refs.add(m.rstrip(".,;:)"))
    # Only assert explicit file-looking references. Directory references are valid.
    file_refs = {x for x in known_fixture_refs if "." in x.rsplit("/", 1)[-1]}
    missing_refs = sorted(x for x in file_refs if x not in fixtures)
    if missing_refs:
        fail("case text references fixture files absent from generator: " + ", ".join(missing_refs))

    design = (IA / "BENCHMARK-DESIGN.md").read_text(encoding="utf-8")
    for invariant in (
        "CONTROL BETTER THAN AHP",
        "LEGACY BETTER THAN CURRENT",
        "NO EFFECT",
        "INCONCLUSIVE",
        "FRESH REPLICATION != FRESH CASE",
        "CONTROL != PROMPTLESS MODEL",
    ):
        if invariant not in design:
            fail(f"experimental contract lost invariant: {invariant}")

    print("PASS: benchmark static integrity")
    print(f"QUICK-5 cases: {len(qcases)}")
    print(f"DEEP-60 pool cases: {len(dcases)}")
    print(f"DEEP-60 timed core cases: {len(execution)}")
    print(f"Generated fixture paths detected: {len(fixtures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
