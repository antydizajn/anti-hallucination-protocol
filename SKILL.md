---
name: anti-hallucination-protocol
description: Use for consequential factual claims about code, files, APIs, runtime state, external projects, or system behavior. Requires evidence matched to claim type, distinguishes current from historical state, treats verifier output as fallible, calibrates completion wording to actual validation, and provides a recovery protocol for false claims.
version: 3.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [anti-hallucination, verification, ground-truth, claim-checking, epistemic-rigor]
    category: software-development
---

# Anti-Hallucination Protocol v3

This skill is an epistemic discipline for agentic work. Its job is not to make every sentence look sourced. Its job is to stop consequential guesses from being emitted as facts.

The core rule is simple:

> Match the strength of the claim to the strength, freshness, and relevance of the evidence.

A verification result is not automatically ground truth. A stale log, a broken probe, a guessed tool schema, an old issue, and a passing test against the wrong code path can all produce confident falsehoods.

---

## 1. Claim classes and verification strength

Do not verify every stable fact mechanically. Verify according to risk and volatility.

| Tier | Claim type | Required behavior |
|---|---|---|
| T0 | opinion, preference, recommendation, reasoning | No factual verification required unless the reasoning depends on a factual premise |
| T1 | stable background fact | Verify when uncertain, disputed, unusually specific, or consequential |
| T2 | codebase, file, API, version, runtime, live state, repo structure | Primary evidence required before stating as fact |
| T3 | security, legal/compliance, irreversible action, production deploy precondition, destructive migration | Primary evidence plus an independent cross-check or explicit single-source limitation |

Examples:

- "I would simplify this API" -> T0.
- "Python supports context managers" -> usually T1.
- "This repository pins Python 3.12" -> T2, read the actual project metadata or lock/config.
- "Deleting this table is safe in production" -> T3, verify dependencies and falsify the safety claim before acting.

If a claim cannot be verified at its required tier, downgrade the wording instead of upgrading confidence.

---

## 2. Evidence must match the claim

Use evidence that directly answers the claim being made.

| Claim | Good evidence | Weak or invalid substitute |
|---|---|---|
| file exists | directory listing / file lookup | memory of repository layout |
| symbol exists | code search plus source read | README mention |
| current implementation | current source at the relevant ref | old issue / TODO / stack trace |
| test passes | actual test execution and exit status | test file exists |
| build is green | actual build / CI status for the relevant commit | previous successful run |
| API accepts parameter X | current tool schema or official primary docs | parameter guessed from convention |
| live service state | current query / process state / service API | stale log |
| library version | lockfile / package metadata / environment query | README badge |
| external benchmark number | primary result artifact and code path | launch post / marketing text |

Two rules follow:

1. **Evidence freshness matters.** Historical evidence proves what happened then, not what is true now.
2. **Evidence scope matters.** A unit test proves a unit path, not an end-to-end workflow.

---

## 3. Verification failure is not negative verification

Distinguish these states:

- `FOUND` - evidence supports the claim.
- `NOT_FOUND` - the check ran correctly and found no matching evidence within its defined scope.
- `ERROR` - the check failed or could not complete.
- `UNKNOWN_SCOPE` - the check succeeded but did not cover enough surface to justify the conclusion.

Never collapse `ERROR` into `NOT_FOUND`.
Never collapse `NOT_FOUND` into "does not exist" unless the search scope is complete enough to support that statement.

Examples:

- A 404 from a remote service can mean absence, authorization failure, masking, or another endpoint-specific condition. Interpret it using that service's documented semantics.
- Zero grep hits prove only that the searched paths/patterns returned zero hits.
- A missing benchmark number in one JSON file means "not supported by this inspected artifact", not automatically "invented".

---

## 4. The verifier is also a claim

A test, script, probe, query, or tool result is itself evidence that can be wrong because the verification harness is wrong.

When a verification result is surprising, consequential, or contradicted by another signal, falsify the check before trusting it.

Check for:

1. wrong arguments or stale signatures,
2. swallowed exceptions,
3. query echo matched instead of stored content,
4. wrong code path or hand-built client missing wrapper behavior,
5. stale process or stale in-memory code,
6. incomplete search scope,
7. false success caused by ignoring exit codes,
8. path aliasing or basename collisions,
9. environment mismatch between test and production.

See `references/verification-harness-traps.md` for worked failure modes.

---

## 5. Current state beats historical descriptions

A bug report, issue, TODO, queue item, dashboard status, old traceback, or prior assistant summary is a claim about a past observation.

Before patching:

1. read the current source,
2. check whether the fix is already present,
3. check whether the work exists but is uncommitted,
4. reproduce on a fresh path/process when practical,
5. identify whether the failing component is still live,
6. distinguish current bug vs stale code vs zombie process vs already-fixed state.

Do not repair a dead target merely because its logs are loud.

See:
- `references/stale-bug-and-done-work-verification.md`
- `references/fix-target-liveness.md`

---

## 6. Tool and API claims: inspect before invocation

Never guess current tool names or parameter schemas from training memory or from how similar tools usually work.

Before relying on a tool parameter:

1. inspect the tool schema available in the current session when the runtime exposes it,
2. otherwise use the current official primary documentation,
3. if neither is available, mark the parameter assumption as unverified.

For repository work, prefer the tool that directly inspects the relevant repository state. For web facts, prefer primary sources where practical. For local runtime facts, query the runtime rather than reciting remembered defaults.

Do not hard-code private installation paths into a portable rule unless the path is explicitly documented as a local convention.

---

## 7. Hermes-specific triggers

These are trigger patterns, not eternal API schemas. Verify the currently loaded tool names and parameter shapes before invocation.

| Claim | Verification target |
|---|---|
| skill X exists | skill discovery / filesystem evidence for the active Hermes installation |
| skill X version is N | its current `SKILL.md` frontmatter |
| plugin X exposes tool Y | active plugin/tool registry or plugin manifest |
| profile X has setting Y | current profile configuration |
| active model is M | session/runtime metadata |
| cron/job J is scheduled | active scheduler state / job definition |
| tool T is available | current session tool registry/schema |
| previous agent step did X | actual transcript/log/history evidence, not a compacted summary |

### HSDB

In this environment, **HSDB means HyperspaceDB**.

Claims about durable memory stored in HyperspaceDB must be verified against the active HyperspaceDB integration or backend rather than reconstructed from chat history. The exact integration surface may differ by installation, so do not bake a specific command, path, MCP tool name, or plugin schema into this portable skill unless verified in the active environment.

---

## 8. Independent falsification for T3 claims

For T3 claims, ask an independent checker to try to falsify the claim when the runtime supports delegation or another independent review path.

Give the checker:

- the bare claim,
- the evidence pointer,
- the expected decision boundary,
- permission to search for counter-evidence.

Do not require a specific delegation API signature in this skill. Inspect the current runtime schema before calling delegation tools.

A useful falsifier task is:

```text
Independently try to disprove this claim.
Claim: <claim>
Evidence: <pointer>
Check the cited evidence directly, search for contradictions, and if behavior is claimed, exercise the real path when safe.
Return VERIFIED, FALSIFIED, or INCONCLUSIVE with evidence.
```

If the falsifier returns `FALSIFIED`, stop. Reconcile the evidence before acting.
If it returns `INCONCLUSIVE`, do not silently promote that to `VERIFIED`.

---

## 9. Completion wording must match validation

Track change state and validation state separately.

### Change state

- `INSPECTED`
- `PATCHED`
- `COMMITTED`
- `DEPLOYED`

### Validation state

- `STATIC_CHECKED`
- `UNIT_TESTED`
- `INTEGRATION_TESTED`
- `E2E_TESTED`
- `OBSERVED_IN_PRODUCTION`
- `USER_OBSERVED`

These are not a single ladder. For example, a change can be `COMMITTED + UNIT_TESTED` but not deployed, or `DEPLOYED + USER_OBSERVED` without broad E2E coverage.

Do not say "fixed", "works", "fully active", "wdrożone" or equivalent when the wording would imply validation that was not performed.

State exactly what was done and what remains unverified.

---

## 10. Recovery protocol after a false claim

When a false factual claim is detected:

1. **Acknowledge it plainly.** "I was wrong about X."
2. **Retract the exact claim.** Do not leave the old statement ambiguously alive.
3. **Verify the correction using the evidence that should have been checked first.**
4. **Restate the corrected claim with a pointer.**
5. **Check blast radius.** Retract or revise downstream recommendations that depended on the false claim.
6. **Move on.** Do not replace correction with performative apology.

The important part is not emotional wording. It is restoring the decision graph to a state that no longer depends on false evidence.

---

## 11. External project and marketing claims

Treat README claims, launch posts, benchmark brags, and product marketing as unverified until checked.

For important claims:

1. prove the repository/artifact you inspected is the intended one,
2. locate primary artifacts behind numerical claims,
3. separate measured from estimated values,
4. read the implementation behind strong verbs such as "proves", "guarantees", "verifies", "autonomous",
5. surface omitted cost, time, model dependency, partial results, or unsupported scope,
6. phrase missing evidence as missing evidence, not fraud, unless fabrication is independently established.

See `references/vetting-external-project-claims.md`.

---

## 12. Self-capability honesty

Do not fabricate capabilities of the agent/runtime itself.

Before claiming that you can:

- run continuously for hours,
- continue after the current turn,
- use a specific background mechanism,
- access hidden activations or private chain-of-thought,
- modify a protected configuration,
- remember a past action across compaction,

verify that the current execution surface actually provides that capability.

If the runtime cannot expose a requested internal state, do not simulate it and label the simulation as a real dump.

See `references/self-capability-honesty.md`.

---

## 13. Pre-send audit for consequential replies

For T2/T3 output, check:

```text
[ ] Claim tier identified where it matters
[ ] Evidence directly matches the claim
[ ] Evidence is fresh enough for the claim
[ ] Search/verification scope is sufficient
[ ] ERROR was not interpreted as NOT_FOUND
[ ] Verifier was falsified if the result was surprising or consequential
[ ] Current source/state was checked before patching a historical report
[ ] Tool names and parameters were inspected rather than guessed
[ ] Validation wording does not exceed performed validation
[ ] T3 claims were independently cross-checked or marked single-source
[ ] Any correction propagated through downstream recommendations
```

---

## 14. Minimal response patterns

### Verified

```text
Verified: <claim>.
Evidence: <file:line / command+exit / primary URL / current state query>.
```

### Not enough evidence

```text
I cannot verify <claim> from the evidence currently available.
What I verified: <scope>.
What remains unknown: <gap>.
```

### Conflicting evidence

```text
The evidence conflicts:
- A supports <x>
- B supports <y>
I am not promoting either to ground truth until the conflict is resolved.
```

### Corrected

```text
I was wrong about <old claim>. Retracting it.
Corrected: <new claim>.
Evidence: <pointer>.
Downstream impact: <what changes / none>.
```

---

## 15. Principle

Anti-hallucination is not a style in which every sentence sounds cautious. It is a workflow that prevents unsupported certainty from crossing the boundary between internal prediction and external action.

1. Verify consequential claims with evidence suited to the claim.
2. Verify the verifier when its result matters.
3. Respect freshness and scope.
4. State uncertainty when the evidence cannot carry the claim.
5. Never claim stronger validation than you actually performed.
