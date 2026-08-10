#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required", file=sys.stderr)
    raise SystemExit(69)

EXPECTED_ROWS = 600
EXPECTED_SOURCE_REVISION = "4a8ffc87c4650054825fb767fe0da4a4fc97ff32"
EXPECTED_LEGACY_COMMIT = "b71cc9d06b58c8f12e06b77606a279f536a18959"
EXPECTED_CURRENT_COMMIT = "94bfd13f9c4818a949775bd73c1c0d91ce6a3116"
EXPECTED_LEGACY_BLOB = "2de9613a846771db159d041ab0e75bf92805b9a4"
EXPECTED_CURRENT_BLOB = "0860d4547a5e8e7ed27221724da0cdaaf33a1b41"
ARM_TO_CONDITION = {"A": "CONTROL", "B": "LEGACY", "C": "CURRENT"}
PRELOAD_MARKER = 'user launched this CLI session with the "anti-hallucination-protocol" skill preloaded'
RUNNER_SCHEMA = "aa-omniscience-hermes-run-v2"
RESPONSE_SCHEMA = "aa-omniscience-response-v2"
RUN_IDENTITY_SCHEMA = "aa-omniscience-run-identity-v2"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def stable_json_sha256(data: Any) -> str:
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def profile_home(profile: str) -> tuple[Path, Path]:
    proc = run(["hermes", "-p", profile, "config", "path"])
    cfg_path = Path(proc.stdout.strip()).expanduser().resolve()
    if not cfg_path.is_file():
        raise RuntimeError(f"profile config does not exist: {cfg_path}")
    return cfg_path.parent, cfg_path


def configure_no_tools(cfg_path: Path) -> None:
    data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError("profile config root must be a mapping")
    pts = data.setdefault("platform_toolsets", {})
    if not isinstance(pts, dict):
        raise RuntimeError("platform_toolsets must be a mapping")
    # Explicit CLI selection prevents fallback to Hermes' default composite.
    # no_mcp is the Hermes sentinel used to suppress default MCP inclusion.
    pts["cli"] = ["no_mcp"]
    context = data.setdefault("context", {})
    if not isinstance(context, dict):
        raise RuntimeError("context must be a mapping")
    context["engine"] = "compressor"
    cfg_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def inspect_tool_surface(profile: str) -> dict:
    proc = run(["hermes", "-p", profile, "prompt-size", "--platform", "cli", "--json"], check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"prompt-size failed: {proc.stderr.strip() or proc.stdout.strip()}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"prompt-size did not emit strict JSON: {proc.stdout[:500]!r}") from exc
    tools = data.get("tools") or {}
    if tools.get("count") != 0:
        raise RuntimeError(f"no-tools preflight failed: effective agent exposes {tools.get('count')!r} tools")
    return data


def parse_identity_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise RuntimeError(f"missing frozen-treatment identity record: {path}")
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def verify_treatment(profile: str, arm: str, profile_dir: Path, bench_home: Path, rep_slug: str) -> dict:
    identity_path = bench_home / "work" / rep_slug / "integrity" / "ahp-identity.txt"
    identity = parse_identity_file(identity_path)
    skill_path = profile_dir / "skills" / "anti-hallucination-protocol" / "SKILL.md"
    skills_proc = run(["hermes", "-p", profile, "skills", "list", "--source", "local", "--enabled-only"], check=False)
    skills_text = f"{skills_proc.stdout}\n{skills_proc.stderr}"
    discoverable = "anti-hallucination-protocol" in skills_text.lower()

    if arm == "A":
        if skill_path.exists() or discoverable or identity.get("control_ahp_discoverable") != "NO":
            raise RuntimeError("CONTROL purity failed: AHP is present/discoverable or identity record is inconsistent")
        return {
            "expected_preload": False,
            "ahp_commit": None,
            "ahp_skill_git_blob": None,
            "skill_path": None,
            "discoverable": False,
            "identity_record_sha256": sha256_file(identity_path),
        }

    expected_commit = EXPECTED_LEGACY_COMMIT if arm == "B" else EXPECTED_CURRENT_COMMIT
    expected_blob = EXPECTED_LEGACY_BLOB if arm == "B" else EXPECTED_CURRENT_BLOB
    commit_key = "legacy_commit" if arm == "B" else "current_commit"
    installed_blob_key = "legacy_installed_skill_blob" if arm == "B" else "current_installed_skill_blob"
    if not skill_path.is_file():
        raise RuntimeError(f"treatment SKILL.md missing: {skill_path}")
    observed_blob = git_blob_sha1(skill_path)
    if observed_blob != expected_blob:
        raise RuntimeError(f"treatment SKILL.md blob mismatch: {observed_blob} != {expected_blob}")
    if identity.get(commit_key) != expected_commit or identity.get(installed_blob_key) != expected_blob:
        raise RuntimeError("frozen-treatment identity record does not match preregistered treatment")
    if not discoverable:
        raise RuntimeError("treatment skill is installed but not discoverable/enabled")
    return {
        "expected_preload": True,
        "ahp_commit": expected_commit,
        "ahp_skill_git_blob": expected_blob,
        "ahp_skill_sha256": sha256_file(skill_path),
        "skill_path": str(skill_path),
        "discoverable": True,
        "identity_record_sha256": sha256_file(identity_path),
    }


def load_questions(path: Path) -> tuple[list[dict], str]:
    records: list[dict] = []
    artifact_hashes: set[str] = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj.get("schema") != "aa-omniscience-question-v2":
            raise ValueError(f"line {line_no}: expected aa-omniscience-question-v2")
        if "answer" in obj:
            raise ValueError(f"line {line_no}: gold answer leakage detected")
        if obj.get("source_revision") != EXPECTED_SOURCE_REVISION:
            raise ValueError(f"line {line_no}: unexpected source revision")
        artifact_sha = str(obj.get("source_artifact_sha256") or "").strip()
        if len(artifact_sha) != 64:
            raise ValueError(f"line {line_no}: missing/invalid source artifact SHA256")
        artifact_hashes.add(artifact_sha)
        qid = int(obj["question_id"])
        if not str(obj.get("prompt", "")).strip():
            raise ValueError(f"line {line_no}: blank prompt")
        records.append(obj)
    if len(records) != EXPECTED_ROWS:
        raise ValueError(f"expected {EXPECTED_ROWS} questions, got {len(records)}")
    ids = [int(x["question_id"]) for x in records]
    if ids != list(range(1, 601)):
        raise ValueError("questions must be ordered exactly by question_id 1..600")
    if len(artifact_hashes) != 1:
        raise ValueError("questions JSONL mixes source artifact identities")
    return records, next(iter(artifact_hashes))


def sqlite_session_ids(db_path: Path) -> set[str]:
    if not db_path.is_file():
        return set()
    with sqlite3.connect(db_path) as db:
        try:
            return {str(row[0]) for row in db.execute("SELECT id FROM sessions")}
        except sqlite3.DatabaseError as exc:
            raise RuntimeError(f"cannot read Hermes state DB {db_path}: {exc}") from exc


def read_new_session(db_path: Path, before_ids: set[str]) -> dict:
    if not db_path.is_file():
        raise RuntimeError("Hermes did not create profile state.db")
    with sqlite3.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        rows = list(db.execute("SELECT * FROM sessions ORDER BY started_at DESC"))
        new_rows = [row for row in rows if str(row["id"]) not in before_ids]
        if len(new_rows) != 1:
            raise RuntimeError(f"expected exactly one new Hermes session, observed {len(new_rows)}")
        session = dict(new_rows[0])
        sid = str(session["id"])
        messages = list(db.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY id", (sid,)))
        assistant_rows = [dict(row) for row in messages if row["role"] == "assistant" and str(row["content"] or "").strip()]
        if not assistant_rows:
            raise RuntimeError(f"session {sid} has no persisted assistant answer")
        answer = str(assistant_rows[-1]["content"]).strip()
        return {"session": session, "answer": answer, "messages": [dict(row) for row in messages]}


def capture_hermes_identity() -> dict:
    executable = shutil.which("hermes")
    if not executable:
        raise RuntimeError("hermes not found in PATH")
    proc = run(["hermes", "--version"], check=False)
    version_output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0 or not version_output:
        raise RuntimeError("unable to capture Hermes runtime identity")
    exe_path = Path(executable).resolve()
    return {
        "executable": str(exe_path),
        "executable_sha256": sha256_file(exe_path) if exe_path.is_file() else None,
        "version_output": version_output,
    }


def ensure_clean_workdir(workdir: Path) -> None:
    forbidden = ("AGENTS.md", "HERMES.md", ".hermes.md", "CLAUDE.md", ".cursorrules", "SOUL.md")
    for name in forbidden:
        if (workdir / name).exists():
            raise RuntimeError(f"contaminated workdir contains {name}")
    entries = [p.name for p in workdir.iterdir()]
    if entries:
        raise RuntimeError(f"AA workdir must be empty before execution; found: {entries[:10]}")


def atomic_write_json(path: Path, data: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_existing_responses(path: Path, run_identity_sha: str) -> dict[int, dict]:
    existing: dict[int, dict] = {}
    if not path.exists():
        return existing
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj.get("schema") != RESPONSE_SCHEMA:
            raise RuntimeError(f"responses.jsonl line {line_no}: incompatible schema")
        if obj.get("run_identity_sha256") != run_identity_sha:
            raise RuntimeError(f"responses.jsonl line {line_no}: run identity mismatch")
        qid = int(obj["question_id"])
        if qid in existing:
            raise RuntimeError(f"responses.jsonl contains duplicate question_id {qid}")
        existing[qid] = obj
    return existing


def write_responses(path: Path, records: dict[int, dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for key in sorted(records):
            fh.write(json.dumps(records[key], ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def main() -> int:
    p = argparse.ArgumentParser(description="Run one AA-Omniscience arm through fresh Hermes chat sessions")
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
    if not shutil.which("hermes"):
        print("ERROR: hermes not found in PATH", file=sys.stderr)
        return 69

    profile = f"ahpbench-{args.rep_slug}-{args.arm.lower()}"
    condition = ARM_TO_CONDITION[args.arm]
    out = args.output_dir.resolve()
    workdir = out / "workdir"
    out.mkdir(parents=True, exist_ok=True)
    workdir.mkdir(parents=True, exist_ok=True)

    try:
        # A previously executed workdir is not reused as model context. Resume
        # state lives in responses.jsonl/state.db, never in the model CWD.
        if any(workdir.iterdir()):
            shutil.rmtree(workdir)
            workdir.mkdir(parents=True)
        ensure_clean_workdir(workdir)
        questions_path = args.questions_jsonl.resolve()
        questions, source_artifact_sha = load_questions(questions_path)
        profile_dir, cfg_path = profile_home(profile)
        configure_no_tools(cfg_path)
        bench_home = Path(os.environ.get("AHP_BENCH_HOME", str(Path.home() / "ahp-benchmark-v01"))).expanduser().resolve()
        treatment = verify_treatment(profile, args.arm, profile_dir, bench_home, args.rep_slug)
        tool_surface = inspect_tool_surface(profile)
        hermes_identity = capture_hermes_identity()
    except Exception as exc:
        print(f"ERROR: preflight failed: {exc}", file=sys.stderr)
        return 2

    tool_surface_path = out / "TOOL-SURFACE-PREFLIGHT.json"
    atomic_write_json(tool_surface_path, tool_surface)

    run_identity = {
        "schema": RUN_IDENTITY_SCHEMA,
        "battery": "AA-OMNISCIENCE-600",
        "classification": ["EXTERNAL", "PUBLIC", "NOT_HELD_OUT"],
        "rep_slug": args.rep_slug,
        "arm": args.arm,
        "condition": condition,
        "profile": profile,
        "provider": args.provider,
        "model": args.model,
        "reasoning": args.reasoning,
        "execution_surface": "hermes-chat-query-quiet-v1",
        "question_order": "question_id_ascending_1_to_600",
        "questions_sha256": sha256_file(questions_path),
        "source_revision": EXPECTED_SOURCE_REVISION,
        "source_artifact_sha256": source_artifact_sha,
        "profile_config_sha256": sha256_file(cfg_path),
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "hermes": hermes_identity,
        "treatment": treatment,
        "tool_surface_preflight_sha256": sha256_file(tool_surface_path),
        "effective_tool_count_preflight": (tool_surface.get("tools") or {}).get("count"),
    }
    run_identity_sha = stable_json_sha256(run_identity)
    run_identity["run_identity_sha256"] = run_identity_sha
    run_identity_path = out / "RUN-IDENTITY.json"
    if run_identity_path.exists():
        prior = json.loads(run_identity_path.read_text(encoding="utf-8"))
        if prior != run_identity:
            print("ERROR: existing RUN-IDENTITY.json differs; refusing contaminated resume", file=sys.stderr)
            return 2
    else:
        atomic_write_json(run_identity_path, run_identity)

    responses_path = out / "responses.jsonl"
    try:
        existing = load_existing_responses(responses_path, run_identity_sha)
    except Exception as exc:
        print(f"ERROR: resume preflight failed: {exc}", file=sys.stderr)
        return 2

    db_path = profile_dir / "state.db"
    started_at = utc_now()
    selected = questions[: args.limit]
    hard_error = False

    for idx, item in enumerate(selected, 1):
        qid = int(item["question_id"])
        if qid in existing and existing[qid].get("run_status") == "OK":
            print(f"[{idx}/{len(selected)}] q{qid:03d} RESUME_OK", flush=True)
            continue

        before_ids = sqlite_session_ids(db_path)
        cmd = [
            "hermes", "-p", profile,
            "--in", str(workdir),
            "chat",
            "--provider", args.provider,
            "--model", args.model,
            "-Q",
            "-q", str(item["prompt"]),
        ]
        if args.reasoning:
            cmd.extend(["--reasoning", args.reasoning])
        if args.arm in {"B", "C"}:
            cmd.extend(["-s", "anti-hallucination-protocol"])

        t0 = time.monotonic()
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration = time.monotonic() - t0

        session_id = None
        response = ""
        session_meta: dict[str, Any] = {}
        preload_observed: bool | None = None
        error_reason = ""
        try:
            if proc.returncode != 0:
                raise RuntimeError(f"Hermes exit code {proc.returncode}")
            persisted = read_new_session(db_path, before_ids)
            session_meta = persisted["session"]
            session_id = str(session_meta["id"])
            response = persisted["answer"]
            system_prompt = str(session_meta.get("system_prompt") or "")
            preload_observed = PRELOAD_MARKER.lower() in system_prompt.lower()
            if preload_observed != bool(treatment["expected_preload"]):
                raise RuntimeError(
                    f"treatment load mismatch: expected_preload={treatment['expected_preload']} observed={preload_observed}"
                )
            if int(session_meta.get("tool_call_count") or 0) != 0:
                raise RuntimeError("no-tools invariant violated: session recorded tool calls")
            if not response:
                raise RuntimeError("empty persisted assistant response")
            status = "OK"
        except Exception as exc:
            status = "ERROR"
            error_reason = str(exc)
            hard_error = True

        usage = {
            key: session_meta.get(key)
            for key in (
                "input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens",
                "reasoning_tokens", "api_call_count", "billing_provider", "billing_base_url",
                "billing_mode", "estimated_cost_usd", "actual_cost_usd", "cost_status",
                "cost_source", "pricing_version", "tool_call_count",
            )
            if key in session_meta
        }
        record = {
            "schema": RESPONSE_SCHEMA,
            "run_identity_sha256": run_identity_sha,
            "question_id": qid,
            "domain": item["domain"],
            "topic": item["topic"],
            "response": response,
            "response_sha256": sha256_bytes(response.encode("utf-8")),
            "run_status": status,
            "error_reason": error_reason or None,
            "hermes_exit_code": proc.returncode,
            "stderr": proc.stderr.strip() if proc.returncode != 0 else "",
            "duration_seconds": round(duration, 6),
            "session_id": session_id,
            "ahp_preload_expected": bool(treatment["expected_preload"]),
            "ahp_preload_observed": preload_observed,
            "usage": usage,
        }
        existing[qid] = record
        write_responses(responses_path, existing)
        print(f"[{idx}/{len(selected)}] q{qid:03d} {status}", flush=True)
        if hard_error:
            # Fail closed on treatment/infrastructure errors. Do not continue a
            # run whose subsequent rows would no longer be scientifically clean.
            break

    completed = [existing.get(int(x["question_id"])) for x in selected]
    ok_count = sum(1 for x in completed if x and x.get("run_status") == "OK")
    error_count = len(selected) - ok_count
    meta = {
        "schema": RUNNER_SCHEMA,
        "battery": "AA-OMNISCIENCE-600",
        "classification": ["EXTERNAL", "PUBLIC", "NOT_HELD_OUT"],
        "run_identity_sha256": run_identity_sha,
        "rep_slug": args.rep_slug,
        "arm": args.arm,
        "condition": condition,
        "profile": profile,
        "provider": args.provider,
        "model": args.model,
        "reasoning": args.reasoning,
        "source_revision": EXPECTED_SOURCE_REVISION,
        "source_artifact_sha256": source_artifact_sha,
        "questions_sha256": run_identity["questions_sha256"],
        "tools_policy": "EFFECTIVE_AGENT_TOOL_COUNT_ZERO_PREFLIGHT_AND_ZERO_SESSION_TOOL_CALLS",
        "effective_tool_count_preflight": run_identity["effective_tool_count_preflight"],
        "ahp_preload_expected": bool(treatment["expected_preload"]),
        "treatment_load_evidence": "SESSION_SYSTEM_PROMPT_PRELOAD_MARKER",
        "started_at": started_at,
        "ended_at": utc_now(),
        "requested_question_count": len(selected),
        "ok_count": ok_count,
        "error_count": error_count,
        "complete_question_set": len(selected) == EXPECTED_ROWS and ok_count == EXPECTED_ROWS,
        "result_boundary": "RUNTIME_ERROR_IS_NOT_NOT_ATTEMPTED",
        "runtime_note": "Behavioral effectiveness is not established by runner completion alone.",
    }
    atomic_write_json(out / "RUN-METADATA.json", meta)

    if error_count:
        print(f"AA ARM: INCOMPLETE - {error_count} missing/error rows", file=sys.stderr)
        return 3
    if args.limit < EXPECTED_ROWS:
        print("AA ARM: SMOKE ONLY - not a complete benchmark run")
        return 0
    print("AA ARM: COMPLETE 600/600 EXECUTION ONLY - semantic grading still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
