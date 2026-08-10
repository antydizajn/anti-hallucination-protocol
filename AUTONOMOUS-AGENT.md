# Autonomous agent entrypoint

This file is for a completely fresh execution-capable agent that has been given only:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

Do not ask the user to reconstruct project history before reading the repository.

## First 90 seconds

1. Confirm the active repository is `antydizajn/anti-hallucination-protocol`.
2. Resolve the current `main` HEAD. Do not assume a cached SHA is current.
3. Read, in order:

```text
AGENTS.md
AGENT-BOOTSTRAP.json
README.md
PROJECT-MAP.json
PROJECT-HANDOFF.md
```

4. If the user gave an explicit task, follow that task after locating the correct workflow in `AGENTS.md`.
5. If the user gave only the repository URL, enter `DISCOVER_WORK` mode below.

## DISCOVER_WORK

GitHub Issues are the live work ledger.

Search open Issues whose title contains:

```text
[AGENT-READY]
```

Priority order:

```text
[P0]
[P1]
[P2]
[P3]
```

Within equal priority, prefer the oldest unclaimed work item unless the issue explicitly defines a different dependency order.

Do not treat `TODO.md` as proof that an item is still open. Issues are the operational queue; `TODO.md` remains strategic/historical roadmap context.

### Safe claim protocol

Before doing material work:

1. read the full Issue and comments;
2. verify the task still applies to current `main` or the explicitly named target;
3. look for a recent `AHP_WORK_CLAIM_V1` comment;
4. if another live claim exists and is less than 2 hours old, do not duplicate the work;
5. otherwise add a new comment containing a fenced JSON claim:

```json
{
  "schema": "AHP_WORK_CLAIM_V1",
  "issue": 123,
  "agent_id": "<declared-agent-id>",
  "claimed_at": "<RFC3339 timestamp>",
  "target_ref": "main",
  "target_commit": "<resolved SHA>",
  "planned_branch": "agent/<agent-id>/issue-123-<slug>",
  "identity_assurance": "DECLARED_IDENTITY_ONLY"
}
```

If a valid signed identity is actually provisioned under `AGENT-IDENTITY/`, the claim may use `KEY_BOUND_IDENTITY` only after signature verification succeeds. Never upgrade assurance because the agent says it owns a key.

If you cannot write an Issue comment or branch, do not claim the task. Report `NO_WRITE_CAPABILITY`.

## Work branch

For code, documentation, methodology or deterministic-test changes, work on a dedicated branch from the exact intended base.

Default:

```text
agent/<agent-id>/issue-<number>-<short-slug>
```

Do not write directly to `main`.

External-audit evidence, agent-bus traffic and dedicated submission workspaces have their own branch/path contracts. Follow `AGENTS.md` rather than forcing them through a normal code branch.

## Role routing

Classify the work before acting:

```text
FORENSIC_AUDIT      -> fresh auditor methodology; preserve blind phase
REPRODUCTION        -> reproduce before remediation
REMEDIATION         -> patch an already adjudicated target
RELEASE_VERIFY      -> verify candidate; do not redesign it
ARCHIVE_PROVENANCE  -> evidence inventory/hashes/provenance only
BEHAVIORAL_EVAL     -> behavioral evaluation protocol; do not infer effect from unit tests
REPOSITORY_OPS      -> branch/CI/protection/release mechanics
DOCUMENTATION       -> docs only unless evidence requires code changes
```

Repository-level GitHub Copilot custom agent profiles live under `.github/agents/` when available. A non-Copilot agent should still follow the same role boundaries.

## Mandatory evidence boundaries

Never collapse:

```text
ISSUE OPEN != FINDING TRUE
AGENT ASSIGNED != AGENT CORRECT
SIGNED != TRUE
RECEIVED != VERIFIED
STRUCTURALLY_VALID_SUBMISSION != ACCEPTED_FINDING
AUDITOR_REPRODUCED != PROJECT_REPRODUCED
REPRODUCED != FIXED
PATCHED != RELEASED
GREEN TESTS != MODEL OBEDIENCE
CI PASS != BEHAVIORAL EFFECTIVENESS
```

## Completion

A material task is not complete merely because a response was drafted.

For change-producing tasks, prefer:

```text
issue
-> claim
-> branch
-> evidence/reproducer
-> patch if authorized
-> tests/gates
-> pull request
-> durable handoff
```

After opening a PR, add a final Issue comment containing:

```json
{
  "schema": "AHP_WORK_HANDOFF_V1",
  "issue": 123,
  "agent_id": "<agent-id>",
  "status": "PR_OPEN",
  "target_commit": "<base SHA>",
  "work_branch": "<branch>",
  "pull_request": 456,
  "evidence": ["<paths / run ids / reproducer refs>"],
  "remaining_unknowns": []
}
```

If no PR is appropriate, use `status` such as `REPORT_WRITTEN`, `REPRODUCED`, `BLOCKED`, or `NO_CHANGE_RECOMMENDED` and point to durable evidence.

## Stop conditions

Stop rather than invent work when any of these applies:

```text
STOP_WITH_NO_ASSIGNED_WORK
NO_WRITE_CAPABILITY
TARGET_UNRESOLVED
DEPENDENCY_BLOCKED
INSUFFICIENT_EVIDENCE_FOR_REQUESTED_STATE
```

Autonomy means following a durable work contract without constant human relaying. It does not mean manufacturing tasks or upgrading evidence states.
