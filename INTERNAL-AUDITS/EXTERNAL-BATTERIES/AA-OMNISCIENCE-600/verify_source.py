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


def schema_sha256(columns: list[str]) -> str:
    payload = json.dumps(columns, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def download(dest: Path) -> None:
    req = urllib.request.Request(URL, headers={"User-Agent": "ahp-aa-omniscience-verifier/1"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def main() -> int:
    p = argparse.ArgumentParser(description="Download and verify the pinned AA-Omniscience public CSV")
    p.add_argument("output_dir", type=Path)
    p.add_argument("--no-download", action="store_true", help="verify an already present CSV only")
    args = p.parse_args()

    out = args.output_dir.resolve()
    csv_path = out / FILENAME
    identity_path = out / "SOURCE-IDENTITY.json"

    try:
        if not args.no_download:
            download(csv_path)
        if not csv_path.is_file():
            raise ValueError(f"missing CSV: {csv_path}")

        raw = csv_path.read_bytes()
        artifact_sha = sha256_bytes(raw)

        with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            columns = reader.fieldnames or []
            rows = list(reader)

        if columns != EXPECTED_COLUMNS:
            raise ValueError(f"unexpected columns: {columns!r}")
        if len(rows) != EXPECTED_ROWS:
            raise ValueError(f"expected {EXPECTED_ROWS} rows, got {len(rows)}")

        ids: list[int] = []
        for row in rows:
            try:
                qid = int(row["question_id"])
            except Exception as exc:
                raise ValueError(f"invalid question_id: {row.get('question_id')!r}") from exc
            ids.append(qid)
            if not row["domain"].strip() or not row["topic"].strip() or not row["question"].strip() or not row["answer"].strip():
                raise ValueError(f"blank required field at question_id={qid}")

        if len(ids) != len(set(ids)):
            raise ValueError("duplicate question_id detected")
        if set(ids) != EXPECTED_IDS:
            missing = sorted(EXPECTED_IDS - set(ids))[:10]
            extra = sorted(set(ids) - EXPECTED_IDS)[:10]
            raise ValueError(f"question_id set must be exactly 1..600; missing={missing}, extra={extra}")

        domains = sorted({r["domain"] for r in rows})
        topics = sorted({r["topic"] for r in rows})
        if len(domains) != EXPECTED_DOMAINS:
            raise ValueError(f"expected {EXPECTED_DOMAINS} domains, got {len(domains)}")
        if len(topics) != EXPECTED_TOPICS:
            raise ValueError(f"expected {EXPECTED_TOPICS} topics, got {len(topics)}")

        identity = {
            "schema": "aa-omniscience-source-identity-v1",
            "source_repository": REPO,
            "revision": REVISION,
            "artifact": FILENAME,
            "source_url": URL,
            "artifact_sha256": artifact_sha,
            "columns": columns,
            "schema_sha256": schema_sha256(columns),
            "row_count": len(rows),
            "domain_count": len(domains),
            "topic_count": len(topics),
            "question_id_min": min(ids),
            "question_id_max": max(ids),
            "question_ids_unique": True,
            "classification": ["EXTERNAL", "PUBLIC", "NOT_HELD_OUT"],
        }
        identity_path.write_text(json.dumps(identity, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("AA SOURCE: PASS")
        print(f"revision={REVISION}")
        print(f"artifact_sha256={artifact_sha}")
        print(f"rows={len(rows)} domains={len(domains)} topics={len(topics)}")
        print(identity_path)
        return 0
    except Exception as exc:
        print(f"AA SOURCE: FAIL - {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
