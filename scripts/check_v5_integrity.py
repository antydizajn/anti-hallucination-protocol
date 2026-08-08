#!/usr/bin/env python3
"""Offline structural integrity checker for Anti-Hallucination Protocol v5.x.

This validates repository-local structure and the deliberately narrow
frontmatter profile used by this skill. It is NOT a general YAML validator and
must not be described as one. It rejects malformed constructs that could make
our simple metadata extraction disagree with Hermes, including unterminated
quoted/flow scalars in top-level values.

It does not validate research truth, semantic entailment, web availability, or
Hermes runtime behavior.

A PASS means only that the checked structural contract is internally
consistent.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION_RE = re.compile(r"^5\.\d+\.\d+$")
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
]

LOCAL_MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://)([^)#]+)(?:#[^)]+)?\)")
BACKTICK_REF_RE = re.compile(r"`((?:references|scripts|tests)/[^`]+)`")
TOP_LEVEL_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?:\s*(?P<value>.*))?$")
NESTED_RE = re.compile(r"^(?P<indent>\s+)(?:[A-Za-z_][A-Za-z0-9_-]*):(.*)$")
LIST_RE = re.compile(r"^\s+-\s+.+$")


def _scalar_shape_error(value: str) -> str | None:
    if not value:
        return None
    if value[0] in {'"', "'"} and (len(value) < 2 or value[-1] != value[0]):
        return "unterminated quoted scalar"
    if value.startswith("[") and not value.endswith("]"):
        return "unterminated flow sequence"
    if value.startswith("{") and not value.endswith("}"):
        return "unterminated flow mapping"
    if value.endswith("]") and not value.startswith("["):
        return "unexpected closing flow-sequence bracket"
    if value.endswith("}") and not value.startswith("{"):
        return "unexpected closing flow-mapping brace"
    return None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    """Parse only the frontmatter profile used by this repository.

    Body text is never searched for metadata. This intentionally does not claim
    compatibility with arbitrary YAML syntax.
    """

    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["SKILL.md must begin with YAML frontmatter delimiter '---'"]

    closing = text.find("\n---\n", 4)
    if closing < 0:
        return {}, text, ["SKILL.md YAML frontmatter has no closing '---' delimiter"]

    front = text[4:closing]
    body = text[closing + 5 :]
    values: dict[str, str] = {}
    current_top: str | None = None

    for lineno, raw in enumerate(front.splitlines(), start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        if raw[0].isspace():
            if current_top is None:
                errors.append(f"frontmatter line {lineno}: nested value has no parent key")
                continue
            if not (NESTED_RE.match(raw) or LIST_RE.match(raw)):
                errors.append(f"frontmatter line {lineno}: unsupported or malformed nested syntax")
            continue

        match = TOP_LEVEL_RE.match(raw)
        if not match:
            errors.append(f"frontmatter line {lineno}: malformed top-level mapping")
            current_top = None
            continue
        key = match.group("key")
        value = (match.group("value") or "").strip()
        if key in values:
            errors.append(f"frontmatter line {lineno}: duplicate top-level key {key!r}")
        shape_error = _scalar_shape_error(value)
        if shape_error:
            errors.append(f"frontmatter line {lineno}: {shape_error}")
        values[key] = value
        current_top = key

    return values, body, errors


def unquote_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


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
        name = unquote_scalar(frontmatter.get("name", ""))
        version = unquote_scalar(frontmatter.get("version", ""))
        if name != "anti-hallucination-protocol":
            errors.append(
                f"SKILL.md frontmatter name is {name!r}; expected 'anti-hallucination-protocol'"
            )
        if not VERSION_RE.fullmatch(version):
            errors.append(
                f"SKILL.md frontmatter version is {version!r}; expected semantic v5 version like '5.2.0'"
            )

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
