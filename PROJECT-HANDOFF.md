# Anti-Hallucination Protocol - Cold-Start Handoff

This file is a compact continuation checkpoint for a completely fresh agent. It is not a live status database.

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

## Fresh-agent routing

Given only the repository URL, start with:

```text
README.md
AGENTS.md
AGENT-BOOTSTRAP.json
PROJECT-MAP.json
```

Then route by actual GitHub capability:

```text
proven upstream push permission -> TRUSTED_UPSTREAM_WRITER
no upstream push permission      -> EXTERNAL_CONTRIBUTOR
permission unknown               -> EXTERNAL_CONTRIBUTOR
```

Trusted project agents use:

```text
AUTONOMOUS-AGENT.md
```

External contributors use:

```text
EXTERNAL-CONTRIBUTOR.md
CONTRIBUTING.md
scripts/external_contributor.py
```

External contributors do not need collaborator `Write` or `agent-bus` write access.

## Canonical infrastructure now on main

Historical merge checkpoints:

```text
PR #7  - project map, cryptographic agent identity, external submission intake
PR #8  - project-map continuity
PR #9  - one-link autonomous control plane
PR #10 - autonomous post-merge continuity
PR #13 - zero-write external contributor fork/PR workflow
```

Observed merge commit for PR #13:

```text
ec7816daea6250ee10835acad9f11f95c1e30a70
```

This SHA is a historical checkpoint. Resolve current `main` live before acting.

## Live work ledger

GitHub Issues are the live work ledger.

Ready autonomous work uses:

```text
[AGENT-READY]
```

Priority:

```text
[P0] -> [P1] -> [P2] -> [P3]
```

`TODO.md` is roadmap context, not proof that an item is operationally open.

If there is no explicit user task and no ready Issue:

```text
STOP_WITH_NO_ASSIGNED_WORK
```

Do not manufacture work.

## Canonical zero-write external contribution flow

Purpose:

```text
ONE PUBLIC REPO URL
+
ZERO UPSTREAM WRITE ACCESS
+
MINIMAL HUMAN RELAY
-> VALIDATED EXTERNAL PULL REQUEST
```

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

Helper:

```bash
python3 scripts/external_contributor.py start
python3 scripts/external_contributor.py submit
```

The helper is designed to:

- verify Git and GitHub CLI availability;
- verify GitHub authentication;
- detect upstream push permission;
- default unknown permission to external mode;
- create or reuse the contributor's fork;
- discover `[AGENT-READY]` work;
- resolve exact target ref and commit;
- scaffold machine-readable submissions for audit/test/reproducer tasks;
- calculate artifact SHA-256 values;
- run `scripts/check_external_submission.py` locally;
- push only to the contributor's `fork` remote in external mode;
- create an upstream Pull Request;
- require a real upstream PR URL before declaring delivery success.

## Target and delivery are separate

For audit-like work, the inspected target may differ from the branch receiving the report.

Example:

```text
INSPECTION TARGET
  audit-methodology-v6 @ exact SHA

DELIVERY BASE
  main
```

The helper creates a detached target worktree where necessary while keeping the report/submission branch based on the delivery branch.

```text
TARGET_REF != DELIVERY_BASE
```

This prevents an audit submission from accidentally importing the target candidate's entire diff into the submission PR.

## External claim semantics

The helper attempts an `AHP_WORK_CLAIM_V1` Issue comment as best effort.

If Issue commenting is unavailable:

```text
DO NOT REQUEST WRITE ACCESS
```

Continue in the fork. The resulting Pull Request becomes the durable project-visible handoff. Duplicate execution remains possible when no claim channel is available.

## External intake security

Canonical machine-friendly evidence path:

```text
SUBMISSIONS/INBOX/<submission-id>/
```

Generic intake is deliberately non-executing:

```text
RECEIVED CODE != SAFE TO EXECUTE
```

Fork Pull Request validation uses the ordinary unprivileged `pull_request` event with read-only content permission. Do not replace this with privileged `pull_request_target` merely to obtain secrets or write credentials.

Successful intake establishes only:

```text
STRUCTURALLY_VALID_SUBMISSION
```

not factual acceptance.

## Verification evidence for PR #13

On the final PR #13 head before merge:

```text
AHP regression suite: SUCCESS
Python 3.11: PASS
Python 3.13: PASS
Python 3.13: 151/151 tests passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
External submission intake workflow: PASS
```

This proves the checked repository contracts on that PR tree. It does not prove a real stranger completed the full fork-to-PR workflow end to end.

The strongest remaining operational verification is an actual external-account acceptance test using only the public repository URL.

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

## Audit methodology v6

Candidate branch:

```text
audit-methodology-v6
```

Control-plane namespace:

```text
AUDIT-METHODOLOGY/
```

Before provisional blind findings, do not consume prior conclusions from:

```text
AUDITS/**
external-audits
prior external reports
adjudication ledgers
agent-bus messages revealing prior findings
conversation summaries of prior methodology conclusions
```

Do not call methodology v6 canonical without verifying its merge state.

## Branch roles

Verify branches and heads live. Intended roles:

```text
main
  CANONICAL

audit-methodology-v6
  CANDIDATE

external-audits
  EVIDENCE_ARCHIVE

agent-bus
  TRUSTED COMMUNICATION

submission/*
  SUBMISSION WORKSPACES

external-contributor-v1
  HISTORICAL merged development branch

ahp-usage-test
  EXPERIMENTAL

backup/pre-history-migration-2026-08-08
  BACKUP
```

Machine-readable companion: `PROJECT-MAP.json`.

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
STRUCTURALLY_VALID_SUBMISSION != ACCEPTED_FINDING
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

Recorded release verification:

```text
Python 3.11 CI: PASS
Python 3.13 CI: PASS
Python 3.13: 126/126 tests passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
behavioral obedience: UNKNOWN
```

Those facts describe the release verification event, not current `main`.

## Current scientific frontier

Behavioral effectiveness in real Hermes sessions remains unproven by deterministic tests alone.

High-value conditions include long context, tool failure, contradictory evidence, user pressure, correlated sources, current-state questions, prompt injection inside evidence, completion pressure, model/provider changes and session compaction/restart.

Use controlled baseline-vs-AHP evaluation. Same-model self-tests are diagnostic, not independent behavioral evidence.

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

Never repeat a historical test count as current evidence without observing the relevant run.

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
