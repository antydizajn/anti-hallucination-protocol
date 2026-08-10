#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required", file=sys.stderr)
    raise SystemExit(69)

EXPECTED_ROWS = 600
ARM_TO_CONDITION = {"A": "CONTROL", "B": "LEGACY", "C": "CURRENT"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def configure_no_tools(profile: str) -> Path:
    proc = run(["hermes", "-p", profile, "config", "path"])
    cfg_path = Path(proc.stdout.strip()).expanduser().resolve()
    if not cfg_path.is_file():
        raise RuntimeError(f"profile config does not exist: {cfg_path}")
    data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError("profile config root must be a mapping")
    pts = data.setdefault("platform_toolsets", {})
    if not isinstance(pts, dict):
        raise RuntimeError("platform_toolsets must be a mapping")
    # Explicit platform selection prevents fallback to Hermes' default CLI toolset.
    # no_mcp is a Hermes-reserved sentinel that prevents default MCP injection.
    pts["cli"] = ["no_mcp"]
    context = data.setdefault("context", {})
    if not isinstance(context, dict):
        raise RuntimeError("context must be a mapping")
    context["engine"] = "compressor"
    cfg_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return cfg_path


def load_questions(path: Path) -> list[dict]:
    records: list[dict] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj.get("schema") != "aa-omniscience-question-v1":
            raise ValueError(f"line {line_no}: unexpected schema")
        if "answer" in obj:
            raise ValueError(f"line {line_no}: gold answer leakage detected")
        qid = int(obj["question_id"])
        if not str(obj.get("prompt", "")).strip():
            raise ValueError(f"line {line_no}: blank prompt")
        records.append(obj)
    if len(records) != EXPECTED_ROWS:
        raise ValueError(f"expected {EXPECTED_ROWS} questions, got {len(records)}")
    ids = [int(x["question_id"]) for x in records]
    if ids != list(range(1, 601)):
        raise ValueError("questions must be ordered exactly by question_id 1..600")
    return records


def main() -> int:
    p = argparse.ArgumentParser(description="Run one AA-Omniscience A/B/C arm through stateless Hermes -z calls")
    p.add_argument("rep_slug")
    p.add_argument("arm", choices=["A", "B", "C"])
    p.add_argument("provider")
    p.add_argument("model")
    p.add_argument("questions_jsonl", type=Path)
    p.add_argument("output_dir", type=Path)
    p.add_argument("--reasoning")
    p.add_argument("--limit", type=int, default=600, help="smoke testing only when below 600")
    args = p.parse_args()

    if not args.rep_slug or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for ch in args.rep_slug):
        print("ERROR: invalid rep slug", file=sys.stderr)
        return 64
    if not 1 <= args.limit <= EXPECTED_ROWS:
        print("ERROR: --limit must be 1..600", file=sys.stderr)
        return 64
    if not shutil_which("hermes"):
        print("ERROR: hermes not found in PATH", file=sys.stderr)
        return 69

    profile = f"ahpbench-{args.rep_slug}-{args.arm.lower()}"
    condition = ARM_TO_CONDITION[args.arm]
    out = args.output_dir.resolve()
    workdir = out / "workdir"
    usage_dir = out / "usage"
    out.mkdir(parents=True, exist_ok=True)
    workdir.mkdir(parents=True, exist_ok=True)
    usage_dir.mkdir(parents=True, exist_ok=True)

    for name in ("AGENTS.md", "HERMES.md", ".hermes.md", "CLAUDE.md", ".cursorrules"):
        if (workdir / name).exists():
            print(f"ERROR: contaminated workdir contains {name}", file=sys.stderr)
            return 2

    try:
        questions = load_questions(args.questions_jsonl.resolve())
        cfg_path = configure_no_tools(profile)
    except Exception as exc:
        print(f"ERROR: preflight failed: {exc}", file=sys.stderr)
        return 2

    responses_path = out / "responses.jsonl"
    existing: dict[int, dict] = {}
    if responses_path.exists():
        for line in responses_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                existing[int(obj["question_id"])] = obj

    started_at = utc_now()
    selected = questions[: args.limit]
    for idx, item in enumerate(selected, 1):
        qid = int(item["question_id"])
        if qid in existing and existing[qid].get("run_status") == "OK":
            continue
        usage_path = usage_dir / f"{qid:03d}.json"
        cmd = [
            "hermes", "-p", profile,
            "--in", str(workdir),
            "-z", str(item["prompt"]),
            "--provider", args.provider,
            "--model", args.model,
            "--usage-file", str(usage_path),
        ]
        if args.reasoning:
            cmd.extend(["--reasoning", args.reasoning])
        if args.arm in {"B", "C"}:
            cmd.extend(["-s", "anti-hallucination-protocol"])

        t0 = time.monotonic()
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration = time.monotonic() - t0
        response = proc.stdout.strip()
        status = "OK" if proc.returncode == 0 and response else "ERROR"
        record = {
            "schema": "aa-omniscience-response-v1",
            "question_id": qid,
            "domain": item["domain"],
            "topic": item["topic"],
            "response": response,
            "response_sha256": hashlib.sha256(response.encode("utf-8")).hexdigest(),
            "run_status": status,
            "hermes_exit_code": proc.returncode,
            "stderr": proc.stderr.strip() if proc.returncode != 0 else "",
            "duration_seconds": round(duration, 6),
            "usage_file": str(usage_path.relative_to(out)) if usage_path.exists() else None,
        }
        existing[qid] = record
        with responses_path.open("w", encoding="utf-8") as fh:
            for key in sorted(existing):
                fh.write(json.dumps(existing[key], ensure_ascii=False) + "\n")
        print(f"[{idx}/{len(selected)}] q{qid:03d} {status}", flush=True)

    completed = [existing.get(int(x["question_id"])) for x in selected]
    ok_count = sum(1 for x in completed if x and x.get("run_status") == "OK")
    error_count = len(selected) - ok_count
    meta = {
        "schema": "aa-omniscience-hermes-run-v1",
        "battery": "AA-OMNISCIENCE-600",
        "classification": ["EXTERNAL", "PUBLIC", "NOT_HELD_OUT"],
        "rep_slug": args.rep_slug,
        "arm": args.arm,
        "condition": condition,
        "profile": profile,
        "provider": args.provider,
        "model": args.model,
        "reasoning": args.reasoning,
        "questions_sha256": sha256_file(args.questions_jsonl.resolve()),
        "profile_config_sha256": sha256_file(cfg_path),
        "tools_policy": "NO_NATIVE_TOOLS_NO_DEFAULT_MCP",
        "platform_toolsets_cli": ["no_mcp"],
        "context_engine": "compressor",
        "ahp_preload_requested": args.arm in {"B", "C"},
        "started_at": started_at,
        "ended_at": utc_now(),
        "requested_question_count": len(selected),
        "ok_count": ok_count,
        "error_count": error_count,
        "complete_question_set": len(selected) == EXPECTED_ROWS and ok_count == EXPECTED_ROWS,
        "result_boundary": "RUNTIME_ERROR_IS_NOT_NOT_ATTEMPTED",
    }
    (out / "RUN-METADATA.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if error_count:
        print(f"AA ARM: INCOMPLETE - {error_count} runtime errors", file=sys.stderr)
        return 3
    if args.limit < EXPECTED_ROWS:
        print("AA ARM: SMOKE ONLY - not a complete benchmark run")
        return 0
    print("AA ARM: COMPLETE 600/600")
    return 0


def shutil_which(name: str) -> str | None:
    from shutil import which
    return which(name)


if __name__ == "__main__":
    raise SystemExit(main())
