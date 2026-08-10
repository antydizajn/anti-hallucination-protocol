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

If you received only the repository URL, read:

```text
AGENTS.md
AGENT-BOOTSTRAP.json
AUTONOMOUS-AGENT.md
README.md
PROJECT-MAP.json
```

Then follow `AUTONOMOUS-AGENT.md`.

If the user gave an explicit task, use `AGENTS.md` to route it.

If the user gave only the repository URL, GitHub Issues with `[AGENT-READY]` are the live work queue.

If no safe ready item exists:

```text
STOP_WITH_NO_ASSIGNED_WORK
```

Do not manufacture a mission.

## Canonical infrastructure now on main

Project infrastructure merged through:

```text
PR #7 - project map, agent identity, external submission intake
PR #8 - post-merge project-map continuity
PR #9 - autonomous one-link control plane
```

Observed merge commit for PR #9:

```text
8169b8d5cc3465ca56812b3aa6d2315c7032a075
```

This SHA is a historical checkpoint. Resolve current `main` live before acting.

`main` now includes:

```text
AGENTS.md
AGENT-BOOTSTRAP.json
AUTONOMOUS-AGENT.md
PROJECT-MAP.json
PROJECT-HANDOFF.md
AGENT-IDENTITY/
SUBMISSIONS/
.github/agents/
.github/workflows/submission-intake.yml
.github/workflows/submission-triage.yml
```

## Operational model

```text
ONE REPOSITORY URL
-> ORIENT
-> FIND EXPLICIT WORK
-> CLAIM SCOPE
-> EXECUTE
-> VERIFY
-> WRITE DURABLE OUTPUT
-> HANDOFF
```

Live work state belongs primarily in GitHub Issues.

```text
TODO.md = strategic roadmap context
GitHub Issues = live operational work ledger
```

Ready autonomous work is marked:

```text
[AGENT-READY]
```

Claim and handoff schemas:

```text
AHP_WORK_CLAIM_V1
AHP_WORK_HANDOFF_V1
```

Normal change path:

```text
Issue
-> claim
-> branch
-> reproduce when applicable
-> patch if authorized
-> tests/gates
-> Pull Request
-> CI
-> merge
-> release verification when applicable
```

## Specialized repository agent roles

Repository-level GitHub custom-agent profiles live under:

```text
.github/agents/
```

Current roles:

```text
ahp-router
ahp-forensic-auditor
ahp-reproducer
ahp-remediator
ahp-release-verifier
```

A non-GitHub execution-capable agent should follow the same role boundaries manually.

Role separation matters:

```text
AUDITOR != PROJECT ADJUDICATOR
REPRODUCER != REMEDIATOR BEFORE EVIDENCE CAPTURE
REMEDIATOR != RELEASE VERIFIER
AGENT ASSIGNED != AGENT CORRECT
```

## Branch roles

Verify current branch existence and heads live.

Intended semantics:

```text
main
  CANONICAL code/docs/release lineage and autonomous bootstrap

audit-methodology-v6
  CANDIDATE audit methodology/control plane until its merge state changes

external-audits
  EVIDENCE_ARCHIVE for external reports and project adjudication records

agent-bus
  COMMUNICATION plane for JSON-only agent-to-agent messages

submission/*
  isolated reviewer/submission workspaces

ahp-usage-test
  EXPERIMENTAL historical behavioral/usage material

project-infrastructure-v1
  HISTORICAL merged development branch

autonomous-control-plane-v1
  HISTORICAL merged development branch

backup/pre-history-migration-2026-08-08
  BACKUP only

v5.4.2-user-pressure-invariant
  HISTORICAL release-feature branch
```

Machine-readable companion:

```text
PROJECT-MAP.json
```

## Agent identity

`AGENT-IDENTITY/` defines optional Ed25519/OpenSSH sender verification.

Assurance ladder:

```text
DECLARED_IDENTITY_ONLY
KEY_BOUND_IDENTITY
DEDICATED_GITHUB_PRINCIPAL
DUAL_ATTESTED
```

Private keys must remain outside repository content.

Do not collapse:

```text
VALID SIGNATURE != TRUE CONTENT
VALID SIGNATURE != MODEL IDENTITY PROVEN
VALID SIGNATURE != HUMAN NON-INTERVENTION PROVEN
MULTIPLE SIGNED AGENTS != INDEPENDENT EVIDENCE
```

A real agent reaches `KEY_BOUND_IDENTITY` only after its external private key exists and the corresponding public key is reviewed into `AGENT-IDENTITY/registry.json`.

## External submissions

Preferred machine-friendly intake:

```text
SUBMISSIONS/INBOX/<submission-id>/manifest.json
```

The validator checks structure, path confinement, declared artifacts and hashes.

The intake workflow is deliberately non-executing.

After a submission has entered canonical `main`, deterministic submission triage creates one `[AGENT-READY]` Issue per `submission_id` unless the marker already exists.

Never collapse:

```text
STRUCTURALLY_VALID_SUBMISSION != ACCEPTED_FINDING
RECEIVED != REPRODUCED
AUDITOR REPRODUCED != PROJECT REPRODUCED
```

A GitHub Issue Form exists as human-friendly fallback.

## External audit evidence

Dedicated external archive:

```text
branch: external-audits
path: EXTERNAL-AUDITS/
```

Archive state, project evidence state and project disposition are separate dimensions.

Archived does not mean true, reproduced, accepted or fixed.

## Audit methodology v6

Candidate branch:

```text
audit-methodology-v6
```

Control-plane namespace:

```text
AUDIT-METHODOLOGY/
```

It is designed to separate audit instructions from historical evidence.

Before provisional blind findings, do not consume prior conclusions from:

```text
AUDITS/**
external-audits
prior model reports
adjudication ledgers
prior summaries of methodology findings
```

Do not call methodology v6 canonical until its actual merge state is verified.

## Agent bus

Communication branch:

```text
agent-bus
```

Agent conversational traffic is JSON-only under `AGENT-BUS/`.

Communication artifacts are not audit evidence or project adjudication by themselves.

The original bus messages used declared identities. Do not retroactively call unsigned historical messages cryptographically authenticated.

New messages can use `AGENT-IDENTITY/` once real key provisioning exists.

## Release and CI evidence

Historical v5.4.2 release verification recorded:

```text
Python 3.11 CI: PASS
Python 3.13 CI: PASS
Python 3.13: 126/126 tests passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
user-pressure invariant: present and regression-locked
behavioral obedience: UNKNOWN
```

These are release-event facts, not current-main facts.

PR #7 infrastructure candidate later passed a Python 3.13 run with 134/134 tests.

PR #9 autonomous-control-plane candidate later passed:

```text
Python 3.11 regression job: PASS
Python 3.13 regression job: PASS
Python 3.13: 142/142 tests passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
```

Those results apply to the tested PR tree. They still do not prove behavioral effectiveness.

## Core epistemic invariants

```text
claim strength <= evidence strength

STRUCTURALLY_VALID != TRUE
CHECKER PASS != SEMANTIC TRUTH
ISSUE OPEN != FINDING TRUE
AGENT ASSIGNED != AGENT CORRECT
SIGNED != TRUE
RECEIVED != VERIFIED
AUDITOR REPRODUCED != PROJECT REPRODUCED
REPRODUCED != FIXED
PATCHED != RELEASED
GREEN UNIT TESTS != MODEL OBEDIENCE
CI PASS != BEHAVIORAL EFFECTIVENESS
INSTALLED != LOADED
LOADED != OBEYED
USER PRESSURE + NO NEW EVIDENCE != STRONGER EVIDENCE STATE
```

Project maxim:

```text
One reproducer outranks five opinions.
```

## AHP architecture boundary

AHP remains:

```text
compact active policy in SKILL.md
+
progressive-disclosure references
+
narrow deterministic helpers
+
regression/adversarial tests
+
research/provenance mappings
+
audit evidence trail
```

It is not:

```text
a truth oracle
a semantic theorem prover
a sandbox
a proof that Markdown instructions were obeyed
a proof of source independence
a proof of behavioral effectiveness
```

Do not bloat `SKILL.md` with repository orchestration details that belong in the control-plane files.

## Current scientific frontier

The largest unresolved practical question remains behavioral effectiveness in real Hermes sessions.

Unit tests and successful startup/loading do not establish performance under:

```text
long context
tool failures
contradictory evidence
user pressure
correlated sources
current-state questions
prompt injection inside evidence
completion pressure
model/provider changes
session compaction/restart
```

A proper benchmark needs controlled baseline vs AHP evaluation and must separate self-test diagnostics from independent behavioral evidence.

## Cold-start live verification

Before consequential work, obtain current equivalents of:

```text
current main HEAD
current branch list
latest release tags
open [AGENT-READY] Issues
open Pull Requests
current relevant CI runs
current SKILL.md version
current diff from latest release tag
```

Do not repeat historical test counts as current results without observing them.

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

## Final rule

A fresh agent can now begin from one repository URL.

But autonomy is permission to follow a durable work contract, not permission to invent one.

Use:

```text
EXPLICIT USER TASK
or
EXPLICIT [AGENT-READY] ISSUE
```

Otherwise:

```text
STOP_WITH_NO_ASSIGNED_WORK
```
