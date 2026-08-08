#!/usr/bin/env python3
"""Offline structural integrity checker for Anti-Hallucination Protocol v5.

This verifies repository-local invariants only. It does not validate research
claims, web availability, semantic entailment, or Hermes runtime compatibility.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_PATHS = [
    "references/research-foundations.md",
    "references/v5-gap-map.md",
    "references/evidence-state-model.md",
    "references/untrusted-evidence-boundary.md",
    "references/evidence-record.schema.json",
    "scripts/verify_claim.py",
    "scripts/check_research_provenance.py",
    "scripts/check_evidence_record.py",
    "tests/test_verify_claim.py",
    "tests/test_research_provenance.py",
    "tests/test_evidence_record.py",
    "tests/adversarial_cases.md",
]

REQUIRED_STATES = [
    "SUPPORTED_WITH_SCOPE",
    "PARTIAL",
    "CONTRADICTED",
    "CONFLICT",
    "NOT_FOUND_WITHIN_SCOPE",
    "INCONCLUSIVE",
    "ERROR",
    "UNKNOWN_SCOPE",
]

LOCAL_MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://)([^)#]+)(?:#[^)]+)?\)")
BACKTICK_REF_RE = re.compile(r"`((?:references|scripts|tests)/[^`]+)`")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["SKILL.md missing"]

    text = skill.read_text(encoding="utf-8")
    if "version: 5.0.0" not in text:
        errors.append("SKILL.md does not declare version 5.0.0")

    for rel in REQUIRED_PATHS:
        if not (root / rel).is_file():
            errors.append(f"required file missing: {rel}")

    for state in REQUIRED_STATES:
        if state not in text:
            errors.append(f"required evidence state missing from SKILL.md: {state}")

    # Every major v5 reference must be reachable from the operational core.
    for rel in [
        "references/research-foundations.md",
        "references/v5-gap-map.md",
        "references/evidence-state-model.md",
        "references/untrusted-evidence-boundary.md",
    ]:
        if rel not in text:
            errors.append(f"SKILL.md does not reference {rel}")

    # Check explicit local markdown links and backtick path references that look like files.
    candidates = set(LOCAL_MD_LINK_RE.findall(text))
    candidates.update(BACKTICK_REF_RE.findall(text))
    for rel in sorted(candidates):
        # Ignore illustrative placeholders and paths that are clearly commands rather than files.
        if any(ch in rel for ch in "<>*"):
            continue
        target = root / rel
        if not target.exists():
            errors.append(f"SKILL.md references missing local path: {rel}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    try:
        errors = validate(args.root)
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("V5 INTEGRITY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("V5 INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
