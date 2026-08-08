#!/usr/bin/env python3
"""Repository-local integrity checker for Anti-Hallucination Protocol v5.4.

Frontmatter acceptance is intentionally based on a real YAML parse, not a
home-grown approximation. This prevents the integrity checker from certifying
frontmatter that Hermes/PyYAML would reject or interpret differently.

This release checker pins the exact public release version. It validates only a
narrow repository contract. It does not validate research truth, semantic
entailment, web availability, or Hermes runtime behavior.

A PASS means only that the checked repository structure and metadata contract
are internally consistent for v5.4.0.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - environment failure, not a data case
    yaml = None

EXPECTED_VERSION = "5.4.0"
REQUIRED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "version",
    "author",
    "license",
    "platforms",
    "metadata",
}
REQUIRED_PATHS = [
    "README.md",
    "references/research-foundations.md",
    "references/v5-gap-map.md",
    "references/v5-research-manifest.json",
    "references/evidence-state-model.md",
    "references/untrusted-evidence-boundary.md",
    "references/evidence-record.schema.json",
    "references/verification-harness-traps.md",
    "references/stale-bug-and-done-work-verification.md",
    "references/fix-target-liveness.md",
    "references/self-capability-honesty.md",
    "references/multi-judge-ensemble.md",
    "references/vetting-external-project-claims.md",
    "references/adversarial-cases.md",
    "scripts/verify_claim.py",
    "scripts/check_research_provenance.py",
    "scripts/check_evidence_record.py",
    "scripts/liveness_check.sh",
    "tests/test_verify_claim.py",
    "tests/test_research_provenance.py",
    "tests/test_evidence_record.py",
    "tests/test_v5_integrity.py",
    "tests/test_liveness.py",
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
ACTIVE_REFERENCES = [
    "references/research-foundations.md",
    "references/v5-gap-map.md",
    "references/v5-research-manifest.json",
    "references/evidence-state-model.md",
    "references/untrusted-evidence-boundary.md",
    "references/verification-harness-traps.md",
    "references/stale-bug-and-done-work-verification.md",
    "references/fix-target-liveness.md",
    "references/self-capability-honesty.md",
    "references/multi-judge-ensemble.md",
    "references/vetting-external-project-claims.md",
    "references/adversarial-cases.md",
]

LOCAL_MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://)([^)#]+)(?:#[^)]+)?\)")
BACKTICK_REF_RE = re.compile(r"`((?:references|scripts|tests)/[^`]+)`")
TOP_LEVEL_KEY_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):", re.MULTILINE)


def split_frontmatter(text: str) -> tuple[str, str, list[str]]:
    if not text.startswith("---\n"):
        return "", text, ["SKILL.md must begin with YAML frontmatter delimiter '---'"]
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return "", text, ["SKILL.md YAML frontmatter has no closing '---' delimiter"]
    return text[4:closing], text[closing + 5 :], []


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, list[str]]:
    """Parse frontmatter with PyYAML and reject ambiguous top-level duplicates."""

    front, body, errors = split_frontmatter(text)
    if errors:
        return {}, body, errors
    if yaml is None:
        return {}, body, ["PyYAML is required for Hermes-compatible frontmatter validation"]

    try:
        data = yaml.safe_load(front)
    except yaml.YAMLError as exc:
        return {}, body, [f"SKILL.md frontmatter is not valid YAML: {exc}"]

    if not isinstance(data, dict):
        return {}, body, ["SKILL.md frontmatter must parse to a mapping/object"]

    seen: set[str] = set()
    for match in TOP_LEVEL_KEY_RE.finditer(front):
        key = match.group("key")
        if key in seen:
            errors.append(f"SKILL.md frontmatter has duplicate top-level key: {key}")
        seen.add(key)

    return data, body, errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["SKILL.md missing"]

    try:
        text = skill.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"SKILL.md could not be read as UTF-8: {exc}"]

    frontmatter, body, frontmatter_errors = parse_frontmatter(text)
    errors.extend(frontmatter_errors)

    missing_keys = sorted(REQUIRED_FRONTMATTER_KEYS - set(frontmatter))
    for key in missing_keys:
        errors.append(f"SKILL.md frontmatter missing required key: {key}")

    if frontmatter:
        name = frontmatter.get("name")
        version = frontmatter.get("version")
        if name != "anti-hallucination-protocol":
            errors.append(
                f"SKILL.md frontmatter name is {name!r}; expected 'anti-hallucination-protocol'"
            )
        if version != EXPECTED_VERSION:
            errors.append(
                f"SKILL.md frontmatter version is {version!r}; expected exact release version {EXPECTED_VERSION!r}"
            )

        platforms = frontmatter.get("platforms")
        if not isinstance(platforms, list) or not platforms or not all(
            isinstance(item, str) and item.strip() for item in platforms
        ):
            errors.append("SKILL.md frontmatter platforms must be a non-empty string list")

        metadata = frontmatter.get("metadata")
        if not isinstance(metadata, dict) or not isinstance(metadata.get("hermes"), dict):
            errors.append("SKILL.md frontmatter metadata.hermes must be a mapping")

    for rel in REQUIRED_PATHS:
        if not (root / rel).is_file():
            errors.append(f"required file missing: {rel}")

    for state in REQUIRED_STATES:
        if state not in body:
            errors.append(f"required evidence state missing from SKILL.md body: {state}")

    for rel in ACTIVE_REFERENCES:
        if rel not in body:
            errors.append(f"SKILL.md does not reference {rel}")

    candidates = set(LOCAL_MD_LINK_RE.findall(body))
    candidates.update(BACKTICK_REF_RE.findall(body))
    for rel in sorted(candidates):
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
