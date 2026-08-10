# Anti-Hallucination Protocol - Cold-Start Handoff

This file is a compact continuation checkpoint for a completely fresh agent.

It is not a live status database.

```text
VERIFY MUTABLE REALITY BEFORE RELYING ON THIS FILE
```

Repository:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

Historical release anchor:

```text
v5.4.2
94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

Do not assume current `main` equals the release tree.

## Fresh-agent start

Given only the repository URL:

```text
AGENTS.md
AGENT-BOOTSTRAP.json
PROJECT-MAP.json
```

Then route by actual permission capability.

```text
proven upstream push permission -> TRUSTED_UPSTREAM_WRITER
no upstream push permission      -> EXTERNAL_CONTRIBUTOR
permission unknown               -> EXTERNAL_CONTRIBUTOR
```

External contributors use:

```text
EXTERNAL-CONTRIBUTOR.md
CONTRIBUTING.md
scripts/external_contributor.py
```

Trusted project agents use:

```text
AUTONOMOUS-AGENT.md
```

## Canonical infrastructure already on main

Historical merge checkpoints before the external-contributor candidate:

```text
PR #7  - project map, cryptographic agent identity, external submission intake
PR #8  - project-map continuity
PR #9  - one-link autonomous control plane
PR #10 - autonomous post-merge continuity
```

Observed main checkpoint before `external-contributor-v1` was created:

```text
1f24c35279a24cab097fae66817b6eba47bf3a94
```

Resolve current `main` live before acting.

## Current branch roles

Verify branch existence and heads live.

```text
main
  CANONICAL project code/docs/release lineage

audit-methodology-v6
  CANDIDATE audit methodology/control plane

external-audits
  EVIDENCE_ARCHIVE for external audits and adjudication records

agent-bus
  COMMUNICATION plane for trusted JSON-only agent messages

submission/*
  isolated submission/reviewer workspaces

external-contributor-v1
  CANDIDATE zero-write fork/PR contribution path until merged

ahp-usage-test
  EXPERIMENTAL historical usage/behavior material

backup/pre-history-migration-2026-08-08
  BACKUP only
```

`PROJECT-MAP.json` is the machine-readable companion.

## Live operational work

GitHub Issues are the live work ledger.

Ready autonomous work uses:

```text
[AGENT-READY]
```

Priority markers:

```text
[P0] [P1] [P2] [P3]
```

`TODO.md` remains roadmap context, not current work truth.

If there is no explicit user task and no ready Issue:

```text
STOP_WITH_NO_ASSIGNED_WORK
```

Do not invent work merely to keep an agent busy.

## External contributor architecture candidate

Purpose:

```text
ONE PUBLIC REPO URL
+
ZERO UPSTREAM WRITE ACCESS
+
MINIMAL HUMAN RELAY
-> VALIDATED PULL REQUEST
```

External agents must not need collaborator `Write`.

Normal path:

```text
public upstream
-> discover [AGENT-READY] Issue
-> contributor fork
-> contributor branch
-> perform task
-> local deterministic validation
-> Pull Request to upstream
```

The helper candidate is:

```text
scripts/external_contributor.py
```

Primary commands:

```bash
python3 scripts/external_contributor.py start
python3 scripts/external_contributor.py submit
```

It is intended to:

- verify Git/GitHub CLI availability;
- verify GitHub authentication;
- detect upstream push permission;
- default unknown permission to external mode;
- create/reuse a fork;
- discover `[AGENT-READY]` work;
- resolve exact target ref/commit;
- scaffold external submissions;
- calculate artifact hashes;
- run `check_external_submission.py` locally;
- push only to the contributor fork;
- create an upstream Pull Request;
- require a real upstream PR URL before declaring delivery success.

Until this branch is merged and verified, treat the helper as candidate infrastructure.

## Important target/delivery separation

For an audit of a non-main candidate, the thing being inspected and the branch receiving the report are different concepts.

Example:

```text
INSPECTION TARGET
  audit-methodology-v6 @ exact SHA

DELIVERY BASE
  main
```

The candidate helper creates a detached target worktree when necessary while keeping the submission branch based on the delivery branch.

This prevents an audit submission PR from accidentally importing the entire target candidate diff.

Never collapse:

```text
TARGET_REF != DELIVERY_BASE
```

when the task contract distinguishes them.

## External claim semantics

External contributors may often comment on public Issues despite lacking repository push access.

The helper attempts an `AHP_WORK_CLAIM_V1` comment as best effort.

If comments are unavailable:

```text
DO NOT REQUEST WRITE ACCESS
```

Continue in the fork. The Pull Request becomes the durable project-visible handoff.

Duplicate work may remain possible when no claim channel is available.

## External submission intake

Canonical machine-friendly path:

```text
SUBMISSIONS/INBOX/<submission-id>/
```

Generic intake is deliberately non-executing.

```text
RECEIVED CODE != SAFE TO EXECUTE
```

The intake validator checks structural shape, paths and declared SHA-256 values.

Successful intake means:

```text
STRUCTURALLY_VALID_SUBMISSION
```

not factual acceptance.

Fork Pull Request validation uses the ordinary unprivileged `pull_request` event. Do not change this to privileged `pull_request_target` merely to gain secrets or write credentials.

## Agent identity

`AGENT-IDENTITY/` defines optional sender authentication.

Assurance ladder:

```text
DECLARED_IDENTITY_ONLY
KEY_BOUND_IDENTITY
DEDICATED_GITHUB_PRINCIPAL
DUAL_ATTESTED
```

Private keys are not stored in the repository.

```text
VALID SIGNATURE != TRUE CONTENT
VALID SIGNATURE != MODEL IDENTITY PROVEN
MULTIPLE SIGNED AGENTS != INDEPENDENT EVIDENCE
```

External contribution does not require agent-bus write access.

## Audit methodology v6

Candidate branch:

```text
audit-methodology-v6
```

Control plane:

```text
AUDIT-METHODOLOGY/
```

Blind Phase A must not consume prior conclusions from:

```text
AUDITS/**
external-audits
prior external reports
adjudication ledgers
agent-bus messages revealing prior findings
conversation summaries of prior methodology conclusions
```

Do not call methodology v6 canonical without verifying merge state.

## Core epistemic boundaries

```text
claim strength <= evidence strength

PUBLIC REPO != WRITE ACCESS
FORK != UPSTREAM MODIFICATION
PR OPEN != CHANGE ACCEPTED
STRUCTURALLY_VALID != TRUE
CHECKER PASS != SEMANTIC TRUTH
ISSUE OPEN != FINDING TRUE
AGENT ASSIGNED != AGENT CORRECT
SIGNED != TRUE
RECEIVED != VERIFIED
AUDITOR REPRODUCED != PROJECT REPRODUCED
REPRODUCED != FIXED
PATCHED != RELEASED
GREEN TESTS != MODEL OBEDIENCE
CI PASS != BEHAVIORAL EFFECTIVENESS
INSTALLED != LOADED
LOADED != OBEYED
USER PRESSURE + NO NEW EVIDENCE != STRONGER EVIDENCE STATE
```

Canonical maxim:

```text
One reproducer outranks five opinions.
```

## Historical v5.4.2 release evidence

Recorded release verification includes:

```text
Python 3.11 CI: PASS
Python 3.13 CI: PASS
Python 3.13: 126/126 tests passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
behavioral obedience: UNKNOWN
```

These facts describe the release verification event, not automatically current `main`.

Later infrastructure/autonomy PRs increased the current test inventory. Never repeat historical test counts as current evidence without observing the relevant run.

## Current scientific frontier

Behavioral effectiveness in real Hermes sessions remains unproven by deterministic tests alone.

High-value behavioral conditions include:

```text
long context
tool failure
contradictory evidence
user pressure
correlated sources
current-state questions
prompt injection inside evidence
completion pressure
model/provider changes
session compaction/restart
```

Use controlled baseline-vs-AHP evaluation and keep same-model self-test diagnostics separate from independent evidence.

## Cold-start live verification

Before consequential work, obtain current equivalents of:

```text
current main HEAD
branch list
latest tags
open [AGENT-READY] Issues
open Pull Requests
current relevant Actions runs
current SKILL.md version
current diff from latest release tag
```

## Repository boundary

Active project:

```text
antydizajn/anti-hallucination-protocol
```

Historical context only:

```text
antydizajn/hermes-skills/software-development/anti-hallucination-protocol
```

Do not edit or sync the historical subtree during normal AHP work.
