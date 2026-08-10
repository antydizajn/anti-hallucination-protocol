#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

REPO = "ArtificialAnalysis/AA-Omniscience-Public"
REVISION = "4a8ffc87c4650054825fb767fe0da4a4fc97ff32"
FILENAME = "AA-Omniscience_dataset_public.csv"
URL = f"https://huggingface.co/datasets/{REPO}/resolve/{REVISION}/{FILENAME}"
EXPECTED_COLUMNS = ["domain", "topic", "question_id", "question", "answer"]
EXPECTED_ROWS = 600
EXPECTED_DOMAINS = 6
EXPECTED_TOPICS = 41
EXPECTED_IDS = set(range(1, 601))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="Download and verify pinned AA-Omniscience-Public")
    p.add_argument("out_dir", type=Path)
    p.add_argument("--timeout", type=int, default=60)
    args = p.parse_args()

    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / FILENAME
    observation_path = out / "dataset-observation.json"

    try:
        with urllib.request.urlopen(URL, timeout=args.timeout) as resp:
            payload = resp.read()
    except Exception as exc:
        print(f"ERROR: download failed: {exc}", file=sys.stderr)
        return 2

    if not payload:
        print("ERROR: downloaded dataset is empty", file=sys.stderr)
        return 2

    csv_path.write_bytes(payload)

    try:
        text = payload.decode("utf-8-sig")
        reader = csv.DictReader(text.splitlines())
        columns = reader.fieldnames or []
        rows = list(reader)
    except Exception as exc:
        print(f"ERROR: CSV parse failed: {exc}", file=sys.stderr)
        return 3

    failures: list[str] = []
    if columns != EXPECTED_COLUMNS:
        failures.append(f"columns={columns!r}, expected={EXPECTED_COLUMNS!r}")
    if len(rows) != EXPECTED_ROWS:
        failures.append(f"row_count={len(rows)}, expected={EXPECTED_ROWS}")

    domains = {r.get("domain", "") for r in rows}
    topics = {r.get("topic", "") for r in rows}
    try:
        ids = {int(r["question_id"]) for r in rows}
    except Exception as exc:
        failures.append(f"question_id parse failed: {exc}")
        ids = set()

    if len(domains) != EXPECTED_DOMAINS:
        failures.append(f"domain_count={len(domains)}, expected={EXPECTED_DOMAINS}")
    if len(topics) != EXPECTED_TOPICS:
        failures.append(f"topic_count={len(topics)}, expected={EXPECTED_TOPICS}")
    if ids != EXPECTED_IDS:
        failures.append("question_id set is not exactly 1..600")

    empty_fields = []
    for idx, row in enumerate(rows, start=1):
        for key in EXPECTED_COLUMNS:
            if not str(row.get(key, "")).strip():
                empty_fields.append(f"row={idx} field={key}")
    if empty_fields:
        failures.append(f"empty required fields: {empty_fields[:10]}")

    schema_material = json.dumps(
        {"columns": columns, "expected_rows": EXPECTED_ROWS},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    observation = {
        "schema": "ahp-aa-omniscience-source-observation-v1",
        "source_repository": REPO,
        "revision": REVISION,
        "filename": FILENAME,
        "url": URL,
        "sha256": sha256_bytes(payload),
        "bytes": len(payload),
        "row_count": len(rows),
        "columns": columns,
        "schema_sha256": sha256_bytes(schema_material),
        "domain_count": len(domains),
        "topic_count": len(topics),
        "question_id_min": min(ids) if ids else None,
        "question_id_max": max(ids) if ids else None,
        "verification": "PASS" if not failures else "FAIL",
        "failures": failures,
        "contamination_class": "PUBLIC_NOT_HELD_OUT"
    }
    observation_path.write_text(json.dumps(observation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if failures:
        print("AA SOURCE VERIFY: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        print(f"Observation: {observation_path}", file=sys.stderr)
        return 1

    print("AA SOURCE VERIFY: PASS")
    print(f"CSV: {csv_path}")
    print(f"Observation: {observation_path}")
    print(f"SHA256: {observation['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
