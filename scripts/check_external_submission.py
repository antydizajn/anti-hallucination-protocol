#!/usr/bin/env python3
"""Validate external AHP submissions without executing submitted content.

A successful result means STRUCTURALLY_VALID_SUBMISSION only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_TYPES = {
    "FORENSIC_AUDIT",
    "BEHAVIORAL_EVALUATION",
    "REPRODUCER",
    "TEST_CASE",
    "RESEARCH_REVIEW",
    "DOCUMENT_REVIEW",
    "OTHER",
}
ALLOWED_SEVERITIES = {"P0", "P1", "P2", "P3", "UNKNOWN"}
ID_RE = re.compile(r"^SUB-[A-Za-z0-9._-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
MAX_ARTIFACT_BYTES = 8 * 1024 * 1024
HASH_CHUNK_BYTES = 1024 * 1024


def sha256_streamed(target: Path) -> str:
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(HASH_CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def inside(root: Path, target: Path) -> bool:
    try:
        target.resolve(strict=True).relative_to(root.resolve(strict=True))
        return True
    except (OSError, ValueError):
        return False


def validate_manifest(subdir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = subdir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{subdir.name}: manifest.json unreadable/invalid: {exc}"]
    if not isinstance(manifest, dict):
        return [f"{subdir.name}: manifest must be an object"]
    required = {
        "schema", "submission_id", "submission_type", "submitted_at",
        "submitter", "executor", "target", "methodology",
        "execution_occurred", "artifacts", "declared_findings", "correlation_hints",
    }
    missing = sorted(required - set(manifest))
    for key in missing:
        errors.append(f"{subdir.name}: missing required field {key}")
    if manifest.get("schema") != "ahp-external-submission-v1":
        errors.append(f"{subdir.name}: unsupported schema")
    submission_id = manifest.get("submission_id")
    if not nonempty(submission_id) or not ID_RE.fullmatch(submission_id):
        errors.append(f"{subdir.name}: invalid submission_id")
    elif submission_id != subdir.name:
        errors.append(f"{subdir.name}: directory name must equal submission_id")
    if manifest.get("submission_type") not in ALLOWED_TYPES:
        errors.append(f"{subdir.name}: invalid submission_type")
    if not isinstance(manifest.get("execution_occurred"), bool):
        errors.append(f"{subdir.name}: execution_occurred must be boolean")
    for obj_name in ("submitter", "executor", "target", "methodology"):
        if not isinstance(manifest.get(obj_name), dict):
            errors.append(f"{subdir.name}: {obj_name} must be object")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{subdir.name}: artifacts must be non-empty list")
    else:
        seen_paths: set[str] = set()
        for idx, item in enumerate(artifacts, start=1):
            if not isinstance(item, dict):
                errors.append(f"{subdir.name}: artifact #{idx} must be object")
                continue
            rel = item.get("path")
            digest = item.get("sha256")
            if not nonempty(rel):
                errors.append(f"{subdir.name}: artifact #{idx} path missing")
                continue
            rel_path = Path(rel)
            if rel_path.is_absolute() or ".." in rel_path.parts:
                errors.append(f"{subdir.name}: artifact #{idx} path traversal/absolute path forbidden")
                continue
            rel_norm = rel_path.as_posix()
            if rel_norm in seen_paths:
                errors.append(f"{subdir.name}: duplicate artifact path {rel_norm}")
                continue
            seen_paths.add(rel_norm)
            target = subdir / rel_path
            if not target.exists():
                errors.append(f"{subdir.name}: declared artifact missing: {rel_norm}")
                continue
            if target.is_symlink() or not target.is_file():
                errors.append(f"{subdir.name}: artifact must be a regular non-symlink file: {rel_norm}")
                continue
            if not inside(subdir, target):
                errors.append(f"{subdir.name}: artifact escapes submission root: {rel_norm}")
                continue
            size = target.stat().st_size
            if size > MAX_ARTIFACT_BYTES:
                errors.append(
                    f"{subdir.name}: artifact exceeds {MAX_ARTIFACT_BYTES} bytes "
                    f"({size}): {rel_norm}"
                )
                continue
            if digest == "UNKNOWN":
                pass
            elif isinstance(digest, str) and SHA_RE.fullmatch(digest):
                actual = sha256_streamed(target)
                if actual != digest:
                    errors.append(f"{subdir.name}: SHA-256 mismatch for {rel_norm}")
            else:
                errors.append(f"{subdir.name}: invalid sha256 for {rel_norm}")
    findings = manifest.get("declared_findings")
    if not isinstance(findings, list):
        errors.append(f"{subdir.name}: declared_findings must be list")
    else:
        ids: set[str] = set()
        for idx, finding in enumerate(findings, start=1):
            if not isinstance(finding, dict):
                errors.append(f"{subdir.name}: finding #{idx} must be object")
                continue
            fid = finding.get("id")
            if not nonempty(fid):
                errors.append(f"{subdir.name}: finding #{idx} id missing")
            elif fid in ids:
                errors.append(f"{subdir.name}: duplicate finding id {fid}")
            else:
                ids.add(fid)
            if finding.get("severity", "UNKNOWN") not in ALLOWED_SEVERITIES:
                errors.append(f"{subdir.name}: finding #{idx} invalid severity")
            if not nonempty(finding.get("title")):
                errors.append(f"{subdir.name}: finding #{idx} title missing")
    if not isinstance(manifest.get("correlation_hints"), list):
        errors.append(f"{subdir.name}: correlation_hints must be list")
    return errors


def validate_root(root: Path) -> list[str]:
    if not root.exists():
        return []
    if not root.is_dir():
        return [f"submission root is not directory: {root}"]
    errors: list[str] = []
    ids: set[str] = set()
    for child in sorted(root.iterdir()):
        if child.name.startswith("."):
            continue
        if child.is_symlink() or not child.is_dir():
            errors.append(f"unexpected non-directory entry under inbox: {child.name}")
            continue
        if child.name in ids:
            errors.append(f"duplicate submission directory: {child.name}")
        ids.add(child.name)
        errors.extend(validate_manifest(child))
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path("SUBMISSIONS/INBOX"))
    args = p.parse_args()
    try:
        errors = validate_root(args.root)
    except OSError as exc:
        print(f"SUBMISSION INTAKE: ERROR - {exc}", file=sys.stderr)
        return 2
    if errors:
        print("SUBMISSION INTAKE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SUBMISSION INTAKE: STRUCTURALLY_VALID_SUBMISSION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
