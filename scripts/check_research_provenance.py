#!/usr/bin/env python3
"""Check offline research-provenance consistency for Anti-Hallucination Protocol.

Two contracts are checked:

1. the curated v4 arXiv manifest against SKILL.md and research-foundations.md;
2. the v5 research manifest against the numbered source list in v5-gap-map.md.

This checker is deliberately OFFLINE. PASS means the repository's declared
source identities are internally consistent. It does not prove live existence,
source correctness, or correctness of the protocol's interpretation.

Exit codes:
  0 = provenance files are internally consistent
  1 = one or more provenance invariants failed
  2 = checker invocation / I/O / JSON error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ARXIV_ID_RE = re.compile(r"^\d{4}\.\d{4,5}$")
SKILL_ENTRY_RE = re.compile(
    r"\[(?P<title>.+?) - arXiv:(?P<id>\d{4}\.\d{4,5})\]"
    r"\((?P<url>https://arxiv\.org/abs/\d{4}\.\d{4,5})\)"
)
V5_ENTRY_RE = re.compile(r"^\d+\.\s+(?P<display>.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Paper:
    id: str
    title: str
    url: str


def load_manifest(path: Path) -> list[Paper]:
    data = json.loads(path.read_text(encoding="utf-8"))
    raw = data.get("papers")
    if not isinstance(raw, list):
        raise ValueError("manifest.papers must be a list")
    papers: list[Paper] = []
    for i, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"manifest paper #{i} must be an object")
        try:
            papers.append(Paper(id=item["id"], title=item["title"], url=item["url"]))
        except KeyError as exc:
            raise ValueError(f"manifest paper #{i} missing key {exc.args[0]}") from exc
    return papers


def load_v5_manifest(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    raw = data.get("sources")
    if not isinstance(raw, list):
        raise ValueError("v5 manifest sources must be a list")
    displays: list[str] = []
    for i, item in enumerate(raw, start=1):
        if not isinstance(item, dict) or not isinstance(item.get("display"), str):
            raise ValueError(f"v5 manifest source #{i} must contain string field 'display'")
        display = item["display"].strip()
        if not display:
            raise ValueError(f"v5 manifest source #{i} has empty display")
        displays.append(display)
    return displays


def validate_manifest(papers: list[Paper], minimum: int = 30) -> list[str]:
    errors: list[str] = []
    if len(papers) < minimum:
        errors.append(f"manifest has {len(papers)} papers; minimum is {minimum}")

    ids: set[str] = set()
    titles: set[str] = set()
    urls: set[str] = set()
    for paper in papers:
        if not ARXIV_ID_RE.fullmatch(paper.id):
            errors.append(f"invalid arXiv id format: {paper.id!r}")
        expected_url = f"https://arxiv.org/abs/{paper.id}"
        if paper.url != expected_url:
            errors.append(
                f"non-canonical URL for {paper.id}: {paper.url!r}; expected {expected_url!r}"
            )
        if not paper.title.strip():
            errors.append(f"empty title for {paper.id}")
        if paper.id in ids:
            errors.append(f"duplicate arXiv id: {paper.id}")
        if paper.title in titles:
            errors.append(f"duplicate title: {paper.title}")
        if paper.url in urls:
            errors.append(f"duplicate URL: {paper.url}")
        ids.add(paper.id)
        titles.add(paper.title)
        urls.add(paper.url)
    return errors


def parse_skill_entries(text: str) -> list[Paper]:
    return [
        Paper(id=m.group("id"), title=m.group("title"), url=m.group("url"))
        for m in SKILL_ENTRY_RE.finditer(text)
    ]


def compare_skill_to_manifest(papers: list[Paper], skill_text: str) -> list[str]:
    errors: list[str] = []
    entries = parse_skill_entries(skill_text)

    by_id: dict[str, list[Paper]] = {}
    for entry in entries:
        by_id.setdefault(entry.id, []).append(entry)

    manifest_ids = {p.id for p in papers}
    for paper in papers:
        found = by_id.get(paper.id, [])
        if not found:
            errors.append(f"SKILL.md missing manifest paper {paper.id}: {paper.title}")
            continue
        if len(found) != 1:
            errors.append(f"SKILL.md cites {paper.id} {len(found)} times; expected exactly once")
            continue
        entry = found[0]
        if entry.title != paper.title:
            errors.append(
                f"title mismatch for {paper.id}: SKILL={entry.title!r}; manifest={paper.title!r}"
            )
        if entry.url != paper.url:
            errors.append(
                f"URL mismatch for {paper.id}: SKILL={entry.url!r}; manifest={paper.url!r}"
            )

    extras = sorted(set(by_id) - manifest_ids)
    for paper_id in extras:
        errors.append(f"SKILL.md research-provenance citation not present in manifest: {paper_id}")
    return errors


def compare_foundations_to_manifest(papers: list[Paper], foundations_text: str) -> list[str]:
    errors: list[str] = []
    for paper in papers:
        exact = f"[{paper.id}]({paper.url})"
        count = foundations_text.count(exact)
        if count != 1:
            errors.append(
                f"research-foundations.md reference count for {paper.id} is {count}; expected 1"
            )
    return errors


def parse_v5_gap_entries(text: str) -> list[str]:
    marker = "## New research sources used for v5"
    end_marker = "## What v5 must NOT claim"
    if marker not in text or end_marker not in text:
        return []
    section = text.split(marker, 1)[1].split(end_marker, 1)[0]
    return [m.group("display").strip() for m in V5_ENTRY_RE.finditer(section)]


def compare_v5_gap_to_manifest(displays: list[str], gap_text: str) -> list[str]:
    errors: list[str] = []
    if len(displays) != len(set(displays)):
        errors.append("v5 research manifest contains duplicate display entries")

    found = parse_v5_gap_entries(gap_text)
    if not found:
        return ["v5-gap-map.md has no parseable numbered v5 research source list"]

    if found != displays:
        max_len = max(len(found), len(displays))
        for i in range(max_len):
            expected = displays[i] if i < len(displays) else "<none>"
            actual = found[i] if i < len(found) else "<missing>"
            if expected != actual:
                errors.append(
                    f"v5 research source #{i + 1} mismatch: gap={actual!r}; manifest={expected!r}"
                )
    return errors


def run(
    manifest: Path,
    skill: Path,
    foundations: Path,
    v5_manifest: Path,
    v5_gap: Path,
    minimum: int = 30,
) -> list[str]:
    papers = load_manifest(manifest)
    errors = validate_manifest(papers, minimum=minimum)
    skill_text = skill.read_text(encoding="utf-8")
    foundations_text = foundations.read_text(encoding="utf-8")
    errors.extend(compare_skill_to_manifest(papers, skill_text))
    errors.extend(compare_foundations_to_manifest(papers, foundations_text))

    v5_displays = load_v5_manifest(v5_manifest)
    gap_text = v5_gap.read_text(encoding="utf-8")
    errors.extend(compare_v5_gap_to_manifest(v5_displays, gap_text))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--minimum", type=int, default=30)
    args = parser.parse_args()

    root = args.root
    try:
        errors = run(
            root / "references" / "arxiv-manifest.json",
            root / "SKILL.md",
            root / "references" / "research-foundations.md",
            root / "references" / "v5-research-manifest.json",
            root / "references" / "v5-gap-map.md",
            minimum=args.minimum,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: provenance checker could not run: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("RESEARCH PROVENANCE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RESEARCH PROVENANCE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
