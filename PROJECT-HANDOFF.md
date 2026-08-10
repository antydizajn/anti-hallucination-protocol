# Anti-Hallucination Protocol - Cold-Start Handoff

This file is a compact continuation checkpoint for a completely fresh agent.

It is not a live status database.

Rule zero:

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

Do not assume current `main` still equals that release tree.

## Fresh-agent start

If you received only the repository URL, read:

```text
AGENTS.md
AGENT-BOOTSTRAP.json
AUTONOMOUS-AGENT.md
README.md
PROJECT-MAP.json
```

Then follow the live-work discovery contract in `AUTONOMOUS-AGENT.md`.

If you received an explicit task, use `AGENTS.md` to locate the correct workflow and branch.

## Current canonical architecture

As of the reconstruction that produced this handoff, `main` contains:

```text
SKILL.md
README.md
AGENTS.md
PROJECT-MAP.json
PROJECT-HANDOFF.md
TODO.md
AGENT-IDENTITY/
SUBMISSIONS/
scripts/
tests/
AUDITS/
.github/workflows/
```

The project infrastructure merged through PR #7 and continuity fix PR #8.

The latest observed `main` commit before the autonomous-control-plane candidate was created was:

```text
a3e1b436b9b296cb056f3c658e9b52db510ba7a9
```

This SHA is historical context. Resolve current `main` live before acting.

## Branch roles

Verify branch existence and heads live. Intended roles are:

```text
main
  CANONICAL code/docs/release lineage

audit-methodology-v6
  CANDIDATE audit methodology/control plane

external-audits
  EVIDENCE_ARCHIVE for external audits and project adjudication records

agent-bus
  COMMUNICATION plane for JSON-only agent-to-agent messages

submission/*
  isolated reviewer/submission workspaces

ahp-usage-test
  EXPERIMENTAL historical behavioral/usage material

backup/pre-history-migration-2026-08-08
  BACKUP only

v5.4.2-user-pressure-invariant
  HISTORICAL feature/release branch
```

`PROJECT-MAP.json` is the machine-readable companion.

## New project infrastructure now on main

### Root navigation

`AGENTS.md` is the human/agent project map.

It answers:

```text
where is canonical code?
where are audits?
where do I submit evidence?
where do agents communicate?
where do I run tests?
which branches are historical?
```

### Agent identity

`AGENT-IDENTITY/` defines an optional Ed25519/OpenSSH signature layer.

Assurance ladder:

```text
DECLARED_IDENTITY_ONLY
KEY_BOUND_IDENTITY
DEDICATED_GITHUB_PRINCIPAL
DUAL_ATTESTED
```

Current critical limit:

```text
VALID SIGNATURE != TRUE CONTENT
VALID SIGNATURE != MODEL IDENTITY PROVEN
VALID SIGNATURE != HUMAN NON-INTERVENTION PROVEN
MULTIPLE SIGNED AGENTS != INDEPENDENT EVIDENCE
```

Real private keys are intentionally not stored in the repository.

A real agent reaches `KEY_BOUND_IDENTITY` only after an Ed25519 private key is generated and stored outside GitHub/repository content and its public key is reviewed into `AGENT-IDENTITY/registry.json`.

### External submissions

`SUBMISSIONS/` is the preferred machine-friendly intake path.

A submission has:

```text
SUBMISSIONS/INBOX/<submission-id>/manifest.json
plus declared artifacts
```

`check_external_submission.py` validates structure, confinement and declared hashes.

The submission intake Action is deliberately non-executing.

Never collapse:

```text
STRUCTURALLY_VALID_SUBMISSION != ACCEPTED_FINDING
RECEIVED != REPRODUCED
```

A GitHub Issue Form is also present as a human-friendly fallback.

## Autonomous control-plane candidate

The branch that introduced this handoff revision is:

```text
autonomous-control-plane-v1
```

Its intended additions are:

```text
AUTONOMOUS-AGENT.md
AGENT-BOOTSTRAP.json
.github/agents/ahp-router.md
.github/agents/ahp-forensic-auditor.md
.github/agents/ahp-reproducer.md
.github/agents/ahp-remediator.md
.github/agents/ahp-release-verifier.md
.github/workflows/submission-triage.yml
```

Until merged, these are candidate infrastructure, not canonical `main`.

Purpose:

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

GitHub Issues become the live operational work ledger for `[AGENT-READY]` items.

A fresh agent receiving only the repo URL must not invent work. If no safe `[AGENT-READY]` item exists:

```text
STOP_WITH_NO_ASSIGNED_WORK
```

## Audit methodology v6

A separate candidate branch exists:

```text
audit-methodology-v6
```

Its intended control-plane namespace is:

```text
AUDIT-METHODOLOGY/
```

It separates audit instructions from historical audit evidence.

Important blind-audit boundary:

before provisional findings, a fresh auditor should not consume prior conclusions from:

```text
AUDITS/**
external-audits
prior model reports
adjudication ledgers
prior summaries of methodology findings
```

Do not call methodology v6 canonical until its actual merge state is verified.

## Agent bus

A dedicated communication branch exists:

```text
agent-bus
```

Its protocol uses JSON-only immutable agent-to-agent messages.

Communication artifact:

```text
AGENT-BUS message JSON
```

is not the same as:

```text
audit evidence
project adjudication
code change
```

The bus initially used `DECLARED_IDENTITY_ONLY`. New signed messages can later use the `AGENT-IDENTITY/` protocol once real external private-key provisioning exists.

Do not retroactively describe unsigned historical messages as cryptographically authenticated.

## v5.4.2 historical release evidence

Recorded release verification includes:

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

These are facts about the release verification event, not automatically facts about current `main`.

The infrastructure PR #7 later produced a successful current-branch regression run in which Python 3.13 collected 134 tests and all 134 passed, including new infrastructure tests. That evidence concerned the infrastructure PR tree, not the v5.4.2 release tag.

## Epistemic invariants to preserve

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

Canonical project maxim:

```text
One reproducer outranks five opinions.
```

## Core release/runtime architecture

AHP remains:

```text
compact active policy in SKILL.md
+
progressive-disclosure references
+
narrow deterministic scripts
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
a proof of real-world source independence
a proof of behavioral effectiveness
```

Do not casually re-bloat `SKILL.md` with audit/archive/infrastructure detail.

## Current scientific frontier

The largest unresolved practical question remains behavioral effectiveness in real Hermes sessions.

Deterministic tests prove checked contracts, not that a model obeys AHP under:

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

A proper behavioral benchmark should compare baseline vs AHP under controlled conditions and keep self-test diagnostics separate from independent evaluation.

## Open operational work

`TODO.md` still contains strategic/open historical roadmap items, including audit archive integrity, Round 3 evidence inventory, repository protection/release mechanics and behavioral benchmark work.

However:

```text
TODO.md = ROADMAP CONTEXT
GitHub Issues = LIVE OPERATIONAL WORK LEDGER
```

Verify whether an Issue already exists before creating duplicate work.

## Cold-start verification checklist

Before consequential work, obtain current equivalents of:

```text
current main HEAD
current branch list
latest tags
current open Issues
current open PRs
current CI workflows and relevant runs
current SKILL.md version
current diff from latest release tag
```

If implementation correctness matters, run or inspect the actual current test suite and deterministic gates.

Never repeat a historical test count as a current result without observing it.

## Repository boundary

Active project:

```text
antydizajn/anti-hallucination-protocol
```

Historical context only:

```text
antydizajn/hermes-skills/software-development/anti-hallucination-protocol
```

Do not edit or sync the old subtree as part of normal AHP work.

## Final cold-start rule

A fresh agent should be able to begin from one URL.

But autonomy does not mean authority to create its own mission.

Use:

```text
EXPLICIT USER TASK
or
EXPLICIT [AGENT-READY] ISSUE
```

Otherwise stop and report that no assigned work is available.
