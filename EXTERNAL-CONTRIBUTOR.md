# External contributor - zero upstream write access

Use this path if you are a completely fresh human or AI agent who can read this public repository but cannot push to `antydizajn/anti-hallucination-protocol`.

You do **not** need collaborator access.

```text
PUBLIC REPO
-> READ
-> DISCOVER [AGENT-READY] WORK
-> FORK
-> WORK IN YOUR FORK
-> VALIDATE
-> PULL REQUEST
```

## Fast path

Prerequisites:

```text
git
Python 3.11+
GitHub CLI `gh`
a GitHub account authenticated in `gh`
```

If you have only the repository URL, clone it and run:

```bash
gh repo clone antydizajn/anti-hallucination-protocol
cd anti-hallucination-protocol
python3 scripts/external_contributor.py start
```

`start` will:

1. verify the repository and tools;
2. resolve current upstream state;
3. query your actual GitHub permission;
4. default to `EXTERNAL_CONTRIBUTOR` when write permission cannot be proven;
5. discover open `[AGENT-READY]` Issues;
6. select the highest-priority oldest suitable task unless `--issue N` is supplied;
7. create/reuse your fork when upstream write is absent;
8. configure an `upstream` remote and a `fork` remote without requiring upstream write;
9. create a local work branch from the task target;
10. scaffold `SUBMISSIONS/INBOX/<submission-id>/` for audit/test/reproducer tasks;
11. attempt a best-effort Issue claim comment when your GitHub account may comment.

If there is no ready work, it stops with:

```text
NO_ASSIGNED_WORK
```

It does not invent a mission.

## Do the task

Read the selected Issue completely. The Issue is the work contract.

For an audit/test/reproducer submission, put durable results in the scaffolded directory. Typical files are:

```text
SUBMISSIONS/INBOX/<submission-id>/
├── manifest.json
├── REPORT.md
├── FINDINGS.json       # when applicable
├── COMPLETION.json     # when applicable
└── attachments/        # optional
```

For a code/documentation fix, edit the task-relevant files normally on your fork branch.

Do not write to the internal `agent-bus`. External contributors enter through Issues / forks / Pull Requests / `SUBMISSIONS/`.

## Submit with one command

After your work is complete:

```bash
python3 scripts/external_contributor.py submit
```

For submission workspaces, `submit` automatically:

- updates observable manifest fields;
- records the exact target commit captured at `start`;
- calculates SHA-256 for submitted artifacts;
- runs `scripts/check_external_submission.py` locally;
- refuses malformed submissions before opening a PR.

Then it:

- commits the current work;
- pushes only to your `fork` remote when you do not have upstream write;
- opens a Pull Request against the correct upstream base;
- verifies that GitHub returned a real PR URL;
- prints that URL.

You may pass `--execution-occurred` if you actually executed the audit/test/reproducer rather than only writing or reviewing documents.

## Permission modes

The helper distinguishes:

```text
TRUSTED_UPSTREAM_WRITER
EXTERNAL_CONTRIBUTOR
```

A claimed identity is not proof of permission. The helper queries GitHub where possible.

If permission cannot be established, it fails safely into `EXTERNAL_CONTRIBUTOR` mode.

External mode never needs upstream `Write`.

## Claim semantics

The helper attempts an `AHP_WORK_CLAIM_V1` Issue comment. Public repositories commonly permit authenticated users to comment even when they cannot push.

If commenting is unavailable, this is not a reason to request `Write`. The helper continues in the contributor's fork and the resulting Pull Request becomes the durable project-visible handoff. Duplicate work remains possible when no claim channel is available, so inspect existing Issue comments and PRs before doing expensive work.

## Security boundary

Generic intake never executes submitted reproducer code.

Do not ask maintainers for secrets or upstream credentials.

Fork Pull Requests run through workflows using the unprivileged `pull_request` boundary. Do not convert external-submission validation to `pull_request_target` merely to obtain write credentials.

Never collapse:

```text
PUBLIC REPO != WRITE ACCESS
FORK != UPSTREAM MODIFICATION
CLAIM COMMENT != TASK CORRECTNESS
PR OPEN != CHANGE ACCEPTED
STRUCTURALLY_VALID_SUBMISSION != FINDING TRUE
AUDITOR REPRODUCED != PROJECT REPRODUCED
CI PASS != BEHAVIORAL EFFECTIVENESS
PATCHED != RELEASED
```

## Explicit failure states

The helper reports specific failures instead of false completion:

```text
NO_GITHUB_AUTH
NO_FORK_CAPABILITY
NO_ASSIGNED_WORK
TARGET_UNRESOLVED
LOCAL_VALIDATION_FAILED
PUSH_FAILED
PR_CREATION_FAILED
TASK_BLOCKED
```

A prepared command or local commit is not a submitted contribution. For successful external delivery, require a real Pull Request URL.
