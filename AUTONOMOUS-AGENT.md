# Autonomous agent entrypoint

This file is for a completely fresh execution-capable agent that has been given only:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

Do not ask the user to reconstruct project history before reading the repository.

## First 90 seconds

1. Confirm the active repository is `antydizajn/anti-hallucination-protocol`.
2. Resolve the current `main` HEAD. Do not assume a cached SHA is current.
3. Read:

```text
AGENTS.md
AGENT-BOOTSTRAP.json
README.md
PROJECT-MAP.json
PROJECT-HANDOFF.md
```

4. Determine capability mode from actual GitHub permissions where possible.

```text
proven upstream push permission -> TRUSTED_UPSTREAM_WRITER
no upstream push permission      -> EXTERNAL_CONTRIBUTOR
permission unknown               -> EXTERNAL_CONTRIBUTOR
```

5. If you are `EXTERNAL_CONTRIBUTOR`, continue in `EXTERNAL-CONTRIBUTOR.md`. Do not stop merely because you cannot create upstream branches.
6. If you are a trusted upstream writer, use the internal workflow below.

## DISCOVER_WORK

GitHub Issues are the live operational work ledger.

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

Within equal priority, prefer the oldest unclaimed item unless the Issue declares dependencies.

`TODO.md` is roadmap context, not proof that a task remains open.

## Internal trusted claim protocol

Before material work:

1. read the full Issue and comments;
2. verify the target/ref/commit;
3. look for a recent `AHP_WORK_CLAIM_V1` comment;
4. avoid a duplicate live claim less than two hours old;
5. create a new JSON claim comment.

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

Use `KEY_BOUND_IDENTITY` only after a real signature verifies against a non-revoked registered key.

For an external contributor, lack of branch write access is normal. Use `EXTERNAL-CONTRIBUTOR.md` instead of reporting `NO_WRITE_CAPABILITY`.

## Internal work branch

Default trusted branch:

```text
agent/<agent-id>/issue-<number>-<short-slug>
```

Do not write ordinary work directly to `main`.

External contributors use branches in their own forks. External agents do not need `agent-bus` write access.

## Role routing

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

Repository custom-agent profiles live under `.github/agents/` when supported. Other agents should follow the same role boundaries manually.

## Mandatory evidence boundaries

```text
PUBLIC REPO != WRITE ACCESS
FORK != UPSTREAM MODIFICATION
PR OPEN != CHANGE ACCEPTED
ISSUE OPEN != FINDING TRUE
AGENT ASSIGNED != AGENT CORRECT
SIGNED != TRUE
RECEIVED != VERIFIED
STRUCTURALLY_VALID_SUBMISSION != ACCEPTED_FINDING
AUDITOR REPRODUCED != PROJECT REPRODUCED
REPRODUCED != FIXED
PATCHED != RELEASED
GREEN TESTS != MODEL OBEDIENCE
CI PASS != BEHAVIORAL EFFECTIVENESS
```

## Completion

For trusted change-producing tasks:

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

External contributors use:

```text
issue
-> best-effort claim
-> fork
-> contributor branch
-> evidence/work
-> local validation
-> upstream Pull Request
```

A material task is not complete merely because a response or command was prepared.

## Stop conditions

Use explicit states rather than false completion:

```text
STOP_WITH_NO_ASSIGNED_WORK
NO_GITHUB_AUTH
NO_FORK_CAPABILITY
TARGET_UNRESOLVED
DEPENDENCY_BLOCKED
LOCAL_VALIDATION_FAILED
PUSH_FAILED
PR_CREATION_FAILED
INSUFFICIENT_EVIDENCE_FOR_REQUESTED_STATE
```

Autonomy means following a durable work contract without constant human relaying. It does not mean manufacturing tasks or upgrading evidence states.
