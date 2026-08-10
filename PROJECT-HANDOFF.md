# Anti-Hallucination Protocol - Cold-Start Handoff

Compact continuation checkpoint for a fresh agent. Verify mutable GitHub state before relying on it.

Repository:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

Historical release anchor:

```text
v5.4.2
94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

Observed `main` checkpoint before this continuity update:

```text
5c52d7a8bdbc4bea254b9efa1634a9748b0cd27e
```

Resolve current `main` live before acting.

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

Trusted project agents use `AUTONOMOUS-AGENT.md`.

External contributors use:

```text
EXTERNAL-CONTRIBUTOR.md
CONTRIBUTING.md
scripts/external_contributor.py
```

External contributors do not need collaborator `Write` or `agent-bus` write access.

## Canonical infrastructure on main

Historical merge checkpoints:

```text
PR #7  - project map, agent identity, external submission intake
PR #8  - project-map continuity
PR #9  - one-link autonomous control plane
PR #10 - autonomous post-merge continuity
PR #13 - zero-write external contributor fork/PR workflow
PR #14 - zero-write post-merge continuity
```

Historical development branch lineage marker:

```text
external-contributor-v1
HISTORICAL merged development branch
```

Observed merge commits:

```text
PR #13 -> ec7816daea6250ee10835acad9f11f95c1e30a70
PR #14 -> 5c52d7a8bdbc4bea254b9efa1634a9748b0cd27e
```

## Immediate operational queue

GitHub Issues are the live work ledger. `[AGENT-READY]` means autonomous work is available.

As of the checkpoint recorded here:

```text
#11 [COMPLETED][P1][METHODOLOGY]
  Blind review audit methodology v6
  CLOSED as completed
  audit handoff lives in PR #12

#15 [ADJUDICATION][P1][METHODOLOGY]
  Review F-001 through F-003 from methodology v6 audit
  OPEN
  deliberately NOT [AGENT-READY]
  project-side adjudication follows after the external E2E acceptance run

#16 [AGENT-READY][P0][E2E]
  Zero-write external contributor acceptance test
  OPEN
  this is intentionally the highest-priority discoverable task for the next fresh external agent
```

Do not recreate #11. Do not let #15 pre-empt #16 by adding `[AGENT-READY]` before the E2E test finishes.

## What the next external test must prove

The remaining operational gap is a real stranger-account end-to-end run:

```text
ONLY PUBLIC REPO URL
+
NO UPSTREAM WRITE ACCESS
-> bootstrap discovery
-> discover Issue #16 without being told its number
-> detect EXTERNAL_CONTRIBUTOR
-> create/reuse own fork
-> create own branch
-> scaffold TEST_CASE submission
-> run local intake validation
-> push only to fork
-> create real Pull Request to upstream main
```

The human testing it should give the fresh agent only:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

Do not provide Issue #16, branch names, helper commands or submission paths manually. The test is invalid if the GitHub identity actually has upstream push permission. Do not use `--force-external` for the acceptance run.

Success is observed only when a real PR from the external fork appears upstream.

```text
COMMAND ATTEMPTED != COMMAND SUCCEEDED
FORK EXISTS != PUSH SUCCEEDED
PUSH SUCCEEDED != PR CREATED
PR CREATED != PR ACCEPTED
```

## Canonical zero-write flow

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

The helper is designed to verify Git/GitHub CLI/auth, detect upstream push permission, default unknown permission to external mode, create or reuse the contributor fork, resolve exact target state, scaffold submissions, calculate SHA-256 values, validate locally, push only to the `fork` remote, and require a real upstream PR URL before reporting delivery success.

## External intake security

Canonical machine-friendly evidence path:

```text
SUBMISSIONS/INBOX/<submission-id>/
```

Generic intake is deliberately non-executing:

```text
RECEIVED CODE != SAFE TO EXECUTE
```

Fork PR validation uses ordinary unprivileged `pull_request` with read-only content permission. Do not switch generic intake to privileged `pull_request_target` merely to obtain secrets or write credentials.

Successful intake establishes only:

```text
STRUCTURALLY_VALID_SUBMISSION
```

not factual acceptance.

## Verification evidence for zero-write infrastructure

Final PR #13 head before merge:

```text
AHP regression suite: SUCCESS
Python 3.11: PASS
Python 3.13: PASS
Python 3.13: 151/151 tests passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
External submission intake: PASS
```

PR #14 post-merge continuity regression also passed on Python 3.11 and 3.13.

These prove checked repository contracts, not the real external-account fork-to-PR path. Issue #16 exists specifically to close that evidence gap.

## Audit methodology v6

Candidate branch:

```text
audit-methodology-v6
```

Completed blind audit target:

```text
efecb86326a5935d0996cf4f3f1ba21b8106890d
```

Audit PR #12 is open and reports verdict `STRONG BUT NEEDS FIXES` with:

```text
F-001 P1 - machine-readable report contract loses mandatory claim/mechanism
F-002 P1 - target-derived executable baseline lacks universal pre-execution safety gate
F-003 P2 - behavioral A/B lacks explicit fresh-state/session isolation
```

Issue #15 is the project-side adjudication container. Auditor findings are not accepted findings until adjudicated.

```text
AUDITOR REPRODUCED != PROJECT REPRODUCED
REPORT WRITTEN != FINDING ACCEPTED
MULTIPLE GPT-5.6 SOL REVIEWS != INDEPENDENT FAILURE DOMAIN
```

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
GREEN UNIT TESTS != MODEL OBEDIENCE
CI PASS != BEHAVIORAL EFFECTIVENESS
INSTALLED != LOADED
LOADED != OBEYED
USER PRESSURE + NO NEW EVIDENCE != STRONGER EVIDENCE STATE
```

Canonical maxim:

```text
One reproducer outranks five opinions.
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
