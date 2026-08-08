#!/usr/bin/env python3
"""Check internal integrity of v4's verified arXiv provenance.

This is deliberately an OFFLINE integrity checker. It proves that the canonical
manifest, SKILL.md and research-foundations.md agree. It does not claim that a
network resource still exists at runtime; arXiv identity/existence was checked
when the manifest was curated.

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


def run(manifest: Path, skill: Path, foundations: Path, minimum: int = 30) -> list[str]:
    papers = load_manifest(manifest)
    errors = validate_manifest(papers, minimum=minimum)
    skill_text = skill.read_text(encoding="utf-8")
    foundations_text = foundations.read_text(encoding="utf-8")
    errors.extend(compare_skill_to_manifest(papers, skill_text))
    errors.extend(compare_foundations_to_manifest(papers, foundations_text))
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
