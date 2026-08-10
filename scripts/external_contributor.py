#!/usr/bin/env python3
"""Minimum-friction external contributor helper for AHP.

This helper is intentionally conservative:
- no upstream write access is required;
- unknown permission defaults to EXTERNAL_CONTRIBUTOR;
- generic intake never executes submitted reproducer code;
- a successful local validation means STRUCTURALLY_VALID_SUBMISSION only;
- completion requires a real upstream Pull Request URL.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

UPSTREAM = "antydizajn/anti-hallucination-protocol"
UPSTREAM_URL = f"https://github.com/{UPSTREAM}"
STATE_NAME = "ahp-external-contributor.json"
READY = "[AGENT-READY]"
PRIORITY = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
PR_URL_RE = re.compile(r"^https://github\.com/antydizajn/anti-hallucination-protocol/pull/\d+$")


class FlowError(RuntimeError):
    def __init__(self, state: str, message: str):
        super().__init__(message)
        self.state = state


def run(cmd: list[str], *, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise FlowError("TASK_BLOCKED", f"cannot execute {cmd[0]}: {exc}") from exc
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise FlowError("TASK_BLOCKED", f"command failed ({proc.returncode}): {' '.join(cmd)}\n{detail}")
    return proc


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise FlowError("TASK_BLOCKED", f"required tool not found: {name}")


def repo_root() -> Path:
    proc = run(["git", "rev-parse", "--show-toplevel"], check=False)
    if proc.returncode != 0:
        raise FlowError("TASK_BLOCKED", "run this helper inside a Git clone of the repository")
    return Path(proc.stdout.strip()).resolve()


def require_clean(root: Path) -> None:
    proc = run(["git", "status", "--porcelain"], cwd=root)
    if proc.stdout.strip():
        raise FlowError("TASK_BLOCKED", "worktree is not clean; start from a clean clone or commit/stash existing work")


def state_path(root: Path) -> Path:
    git_dir = run(["git", "rev-parse", "--git-dir"], cwd=root).stdout.strip()
    path = Path(git_dir)
    if not path.is_absolute():
        path = root / path
    return path.resolve() / STATE_NAME


def save_state(root: Path, data: dict[str, Any]) -> None:
    state_path(root).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FlowError("TASK_BLOCKED", "external contributor state missing/invalid; run `start` first") from exc
    if not isinstance(data, dict):
        raise FlowError("TASK_BLOCKED", "external contributor state is not an object")
    return data


def gh_authenticated() -> bool:
    return run(["gh", "auth", "status"], check=False).returncode == 0


def github_login() -> str:
    proc = run(["gh", "api", "user", "--jq", ".login"], check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        raise FlowError("NO_GITHUB_AUTH", "GitHub authentication required; run `gh auth login`")
    return proc.stdout.strip()


def upstream_push_permission() -> bool:
    proc = run(["gh", "api", f"repos/{UPSTREAM}", "--jq", ".permissions.push"], check=False)
    if proc.returncode != 0:
        return False
    return proc.stdout.strip().lower() == "true"


def ensure_remote(root: Path, name: str, url: str) -> None:
    existing = run(["git", "remote", "get-url", name], cwd=root, check=False)
    if existing.returncode == 0:
        if existing.stdout.strip() != url:
            run(["git", "remote", "set-url", name, url], cwd=root)
    else:
        run(["git", "remote", "add", name, url], cwd=root)


def ensure_fork(root: Path, login: str) -> None:
    check = run(["gh", "api", f"repos/{login}/anti-hallucination-protocol", "--jq", ".full_name"], check=False)
    if check.returncode != 0:
        created = run(["gh", "repo", "fork", UPSTREAM, "--clone=false", "--remote=false"], check=False)
        if created.returncode != 0:
            detail = (created.stderr or created.stdout).strip()
            raise FlowError("NO_FORK_CAPABILITY", f"could not create/reuse fork: {detail}")
    fork_url = f"https://github.com/{login}/anti-hallucination-protocol.git"
    ensure_remote(root, "fork", fork_url)


def list_ready_issues() -> list[dict[str, Any]]:
    proc = run([
        "gh", "issue", "list", "--repo", UPSTREAM, "--state", "open",
        "--search", f"{READY} in:title", "--limit", "100",
        "--json", "number,title,createdAt,url,body",
    ], check=False)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise FlowError("TASK_BLOCKED", f"cannot query live work ledger: {detail}")
    try:
        items = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise FlowError("TASK_BLOCKED", "GitHub returned invalid Issue JSON") from exc
    if not isinstance(items, list):
        raise FlowError("TASK_BLOCKED", "GitHub Issue result is not a list")
    return [x for x in items if isinstance(x, dict) and READY in str(x.get("title", ""))]


def issue_priority(title: str) -> int:
    for key, value in PRIORITY.items():
        if f"[{key}]" in title:
            return value
    return 99


def choose_issue(items: list[dict[str, Any]], number: int | None) -> dict[str, Any]:
    if number is not None:
        for item in items:
            if item.get("number") == number:
                return item
        proc = run(["gh", "issue", "view", str(number), "--repo", UPSTREAM, "--json", "number,title,createdAt,url,body,state"], check=False)
        if proc.returncode != 0:
            raise FlowError("NO_ASSIGNED_WORK", f"Issue #{number} not available")
        item = json.loads(proc.stdout)
        if item.get("state") != "OPEN" or READY not in str(item.get("title", "")):
            raise FlowError("NO_ASSIGNED_WORK", f"Issue #{number} is not an open {READY} work item")
        return item
    if not items:
        raise FlowError("NO_ASSIGNED_WORK", f"no open {READY} Issues")
    return sorted(items, key=lambda x: (issue_priority(str(x.get("title", ""))), str(x.get("createdAt", ""))))[0]


def target_ref_from_issue(body: str) -> str:
    patterns = [
        r"Target branch:\s*```(?:text)?\s*([^\n`]+)",
        r"target_ref\s*[:=]\s*`?([A-Za-z0-9._/-]+)`?",
    ]
    for pattern in patterns:
        match = re.search(pattern, body, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if re.fullmatch(r"[A-Za-z0-9._/-]+", value):
                return value
    return "main"


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value[:48] or "work"


def infer_submission_type(title: str) -> str | None:
    upper = title.upper()
    if "BEHAVIOR" in upper:
        return "BEHAVIORAL_EVALUATION"
    if "REPRODU" in upper:
        return "REPRODUCER"
    if "TEST" in upper:
        return "TEST_CASE"
    if "AUDIT" in upper or "METHODOLOGY" in upper:
        return "FORENSIC_AUDIT"
    return None


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def scaffold_submission(root: Path, login: str, issue: dict[str, Any], stype: str, target_ref: str, target_commit: str) -> str:
    day = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
    safe_login = re.sub(r"[^A-Za-z0-9._-]", "-", login)
    sid = f"SUB-{day}-{safe_login}-issue{issue['number']}"
    subdir = root / "SUBMISSIONS" / "INBOX" / sid
    subdir.mkdir(parents=True, exist_ok=True)
    report = subdir / "REPORT.md"
    if not report.exists():
        report.write_text(
            f"# External contribution for Issue #{issue['number']}\n\n"
            f"Target ref: `{target_ref}`\n\nTarget commit: `{target_commit}`\n\n"
            "Replace this scaffold with the durable report/result required by the Issue.\n",
            encoding="utf-8",
        )
    manifest = {
        "schema": "ahp-external-submission-v1",
        "submission_id": sid,
        "submission_type": stype,
        "submitted_at": utc_now(),
        "submitter": {"type": "AGENT", "name": login},
        "executor": {"type": "AGENT", "model": "UNKNOWN", "provider_runtime": "UNKNOWN"},
        "target": {"repository": UPSTREAM_URL, "ref": target_ref, "commit": target_commit},
        "methodology": {
            "name": "audit-methodology-v6" if target_ref == "audit-methodology-v6" else "UNKNOWN",
            "version": "UNKNOWN",
            "commit": target_commit if target_ref == "audit-methodology-v6" else "UNKNOWN",
        },
        "execution_occurred": False,
        "artifacts": [{"path": "REPORT.md", "sha256": "UNKNOWN"}],
        "declared_findings": [],
        "correlation_hints": [],
    }
    (subdir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sid


def attempt_claim(issue_number: int, login: str, target_ref: str, target_commit: str, branch: str) -> None:
    claim = {
        "schema": "AHP_WORK_CLAIM_V1",
        "issue": issue_number,
        "agent_id": f"external:{login}",
        "claimed_at": utc_now(),
        "target_ref": target_ref,
        "target_commit": target_commit,
        "planned_branch": branch,
        "identity_assurance": "DECLARED_IDENTITY_ONLY",
        "permission_mode": "EXTERNAL_CONTRIBUTOR",
    }
    body = "External contributor claim (best effort):\n\n```json\n" + json.dumps(claim, indent=2, sort_keys=True) + "\n```"
    proc = run(["gh", "issue", "comment", str(issue_number), "--repo", UPSTREAM, "--body", body], check=False)
    if proc.returncode != 0:
        print("WARNING: Issue claim comment unavailable; continuing in fork. Pull Request will be the durable handoff.", file=sys.stderr)


def start(args: argparse.Namespace) -> int:
    for tool in ("git", "gh"):
        require_tool(tool)
    root = repo_root()
    require_clean(root)
    ensure_remote(root, "upstream", f"https://github.com/{UPSTREAM}.git")
    if not gh_authenticated():
        raise FlowError("NO_GITHUB_AUTH", "authenticate with `gh auth login`; upstream Write is not required")
    login = github_login()
    has_push = upstream_push_permission()
    if has_push and not args.force_external:
        print("TRUSTED_UPSTREAM_WRITER")
        print("This helper is the zero-write external path. Use AUTONOMOUS-AGENT.md for the trusted upstream workflow, or rerun with --force-external.")
        return 0
    print("EXTERNAL_CONTRIBUTOR")
    ensure_fork(root, login)
    issue = choose_issue(list_ready_issues(), args.issue)
    body = str(issue.get("body", ""))
    target_ref = args.base or target_ref_from_issue(body)
    fetch = run(["git", "fetch", "upstream", target_ref], cwd=root, check=False)
    if fetch.returncode != 0:
        raise FlowError("TARGET_UNRESOLVED", f"cannot fetch target ref {target_ref}: {(fetch.stderr or fetch.stdout).strip()}")
    target_commit = run(["git", "rev-parse", "FETCH_HEAD"], cwd=root).stdout.strip()
    branch = f"external/{slug(login)}/issue-{issue['number']}-{slug(str(issue.get('title', 'work')))}"
    run(["git", "switch", "-c", branch, target_commit], cwd=root)
    stype = infer_submission_type(str(issue.get("title", "")))
    submission_id = scaffold_submission(root, login, issue, stype, target_ref, target_commit) if stype else None
    attempt_claim(int(issue["number"]), login, target_ref, target_commit, branch)
    data = {
        "schema": "ahp-external-contributor-state-v1",
        "mode": "EXTERNAL_CONTRIBUTOR",
        "upstream": UPSTREAM,
        "login": login,
        "issue": int(issue["number"]),
        "issue_title": str(issue.get("title", "")),
        "issue_url": str(issue.get("url", "")),
        "target_ref": target_ref,
        "target_commit": target_commit,
        "branch": branch,
        "submission_id": submission_id,
        "started_at": utc_now(),
    }
    save_state(root, data)
    print(f"ISSUE #{issue['number']}: {issue.get('title', '')}")
    print(f"TARGET {target_ref} @ {target_commit}")
    print(f"BRANCH {branch}")
    if submission_id:
        print(f"SUBMISSION SUBMISSIONS/INBOX/{submission_id}/")
    print(str(issue.get("url", "")))
    return 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_findings(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    items = data.get("findings", []) if isinstance(data, dict) else data
    if not isinstance(items, list):
        return []
    out: list[dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        fid = item.get("finding_id", item.get("id"))
        title = item.get("title")
        severity = item.get("severity", "UNKNOWN")
        if isinstance(fid, str) and fid.strip() and isinstance(title, str) and title.strip():
            sev = severity if isinstance(severity, str) and severity in {"P0", "P1", "P2", "P3", "UNKNOWN"} else "UNKNOWN"
            out.append({"id": fid.strip(), "severity": sev, "title": title.strip()})
    return out


def refresh_manifest(root: Path, state: dict[str, Any], execution_occurred: bool) -> None:
    sid = state.get("submission_id")
    if not sid:
        return
    subdir = root / "SUBMISSIONS" / "INBOX" / str(sid)
    manifest_path = subdir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FlowError("LOCAL_VALIDATION_FAILED", f"cannot read submission manifest: {exc}") from exc
    artifacts = []
    for path in sorted(subdir.rglob("*")):
        if path == manifest_path or not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(subdir).as_posix()
        artifacts.append({"path": rel, "sha256": sha256(path)})
    if not artifacts:
        raise FlowError("LOCAL_VALIDATION_FAILED", "submission contains no artifacts")
    manifest["submitted_at"] = utc_now()
    manifest["execution_occurred"] = bool(execution_occurred)
    manifest["artifacts"] = artifacts
    manifest["target"] = {
        "repository": UPSTREAM_URL,
        "ref": state["target_ref"],
        "commit": state["target_commit"],
    }
    manifest["declared_findings"] = extract_findings(subdir / "FINDINGS.json")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_submission(root: Path, state: dict[str, Any]) -> None:
    sid = state.get("submission_id")
    if not sid:
        return
    target = root / "SUBMISSIONS" / "INBOX" / str(sid)
    proc = run([sys.executable, "scripts/check_external_submission.py", "--root", str(target.parent)], cwd=root, check=False)
    if proc.returncode != 0:
        print(proc.stdout, end="")
        print(proc.stderr, end="", file=sys.stderr)
        raise FlowError("LOCAL_VALIDATION_FAILED", "external submission validation failed")
    print(proc.stdout.strip())


def existing_pr_url(state: dict[str, Any]) -> str | None:
    head = f"{state['login']}:{state['branch']}"
    proc = run([
        "gh", "pr", "list", "--repo", UPSTREAM, "--state", "open",
        "--head", head, "--json", "url", "--jq", ".[0].url",
    ], check=False)
    value = proc.stdout.strip() if proc.returncode == 0 else ""
    return value if PR_URL_RE.fullmatch(value) else None


def submit(args: argparse.Namespace) -> int:
    for tool in ("git", "gh"):
        require_tool(tool)
    root = repo_root()
    state = load_state(root)
    if state.get("mode") != "EXTERNAL_CONTRIBUTOR":
        raise FlowError("TASK_BLOCKED", "state is not EXTERNAL_CONTRIBUTOR")
    if not gh_authenticated():
        raise FlowError("NO_GITHUB_AUTH", "GitHub authentication required")
    current = run(["git", "branch", "--show-current"], cwd=root).stdout.strip()
    if current != state.get("branch"):
        raise FlowError("TASK_BLOCKED", f"current branch {current!r} does not match started work branch {state.get('branch')!r}")
    refresh_manifest(root, state, args.execution_occurred)
    validate_submission(root, state)
    run(["git", "add", "-A"], cwd=root)
    staged = run(["git", "diff", "--cached", "--quiet"], cwd=root, check=False)
    if staged.returncode == 0:
        raise FlowError("TASK_BLOCKED", "no contribution changes to submit")
    if staged.returncode not in (0, 1):
        raise FlowError("TASK_BLOCKED", "could not inspect staged changes")
    message = args.message or f"external: contribute for issue #{state['issue']}"
    run(["git", "commit", "-m", message], cwd=root)
    push = run(["git", "push", "-u", "fork", f"HEAD:refs/heads/{state['branch']}"], cwd=root, check=False)
    if push.returncode != 0:
        raise FlowError("PUSH_FAILED", (push.stderr or push.stdout).strip())
    existing = existing_pr_url(state)
    if existing:
        print(existing)
        return 0
    title = args.title or f"[EXTERNAL][#{state['issue']}] {state['issue_title']}"
    body = (
        f"External contribution for #{state['issue']}.\n\n"
        f"Target captured at start: `{state['target_ref']}` @ `{state['target_commit']}`.\n\n"
        "Evidence boundaries:\n\n"
        "```text\n"
        "PR OPEN != CHANGE ACCEPTED\n"
        "STRUCTURALLY_VALID_SUBMISSION != FINDING TRUE\n"
        "AUDITOR REPRODUCED != PROJECT REPRODUCED\n"
        "```\n"
    )
    proc = run([
        "gh", "pr", "create", "--repo", UPSTREAM,
        "--head", f"{state['login']}:{state['branch']}",
        "--base", state["target_ref"],
        "--title", title, "--body", body,
    ], check=False)
    if proc.returncode != 0:
        raise FlowError("PR_CREATION_FAILED", (proc.stderr or proc.stdout).strip())
    candidates = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    url = next((line for line in reversed(candidates) if PR_URL_RE.fullmatch(line)), "")
    if not url:
        url = existing_pr_url(state) or ""
    if not PR_URL_RE.fullmatch(url):
        raise FlowError("PR_CREATION_FAILED", "GitHub command completed but no verifiable upstream PR URL was returned")
    print(url)
    return 0


def doctor(_: argparse.Namespace) -> int:
    for tool in ("git", "gh"):
        require_tool(tool)
    root = repo_root()
    print(f"repo_root={root}")
    print(f"github_auth={'YES' if gh_authenticated() else 'NO'}")
    if gh_authenticated():
        print(f"github_login={github_login()}")
        print(f"upstream_push={'YES' if upstream_push_permission() else 'NO'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AHP zero-write external contributor helper")
    sub = parser.add_subparsers(dest="command", required=True)
    p_start = sub.add_parser("start", help="discover work, fork if needed, and create the local work branch")
    p_start.add_argument("--issue", type=int)
    p_start.add_argument("--base", help="override target base/ref only when the task contract requires it")
    p_start.add_argument("--force-external", action="store_true", help="use fork/PR mode even if upstream push permission exists")
    p_start.set_defaults(func=start)
    p_submit = sub.add_parser("submit", help="validate, push to fork, and open upstream Pull Request")
    p_submit.add_argument("--execution-occurred", action="store_true")
    p_submit.add_argument("--message")
    p_submit.add_argument("--title")
    p_submit.set_defaults(func=submit)
    p_doctor = sub.add_parser("doctor", help="show local/auth/permission capability state")
    p_doctor.set_defaults(func=doctor)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.func(args))
    except FlowError as exc:
        print(exc.state)
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
