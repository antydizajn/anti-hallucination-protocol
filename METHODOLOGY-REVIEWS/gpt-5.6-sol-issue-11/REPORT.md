# Blind Review Audit - Methodology v6

Auditor: `gpt-5.6-sol`
Issue: `#11 [AGENT-READY][P1][METHODOLOGY] Blind review audit methodology v6`
Role: `FORENSIC_AUDIT`
Target repository: `antydizajn/anti-hallucination-protocol`
Target ref: `audit-methodology-v6`
Resolved target commit: `efecb86326a5935d0996cf4f3f1ba21b8106890d`
Primary target: `AUDIT-METHODOLOGY/**`
Methodology prompt blob: `190345443b4f2599a4a9e76e5d07f64e6a6b4ed1`
Execution capability: `PARTIAL` - GitHub repository inspection and durable writes were available; local shell/runtime execution was not used because this task audits methodology text and the target is read-only.

## Executive verdict

`STRONG BUT NEEDS FIXES`

The v6 methodology materially improves the previous design: control-plane/evidence-plane separation is explicit, fixed probe quotas are removed, target resolution is generalized, severity separates impact from precondition, same-model self-test is explicitly separated from independent behavioral evidence, and the behavioral protocol introduces blinding, randomization, predeclared acceptance criteria, per-family metrics, and raw-case preservation.

However, I reproduced two direct contract contradictions and one experimental-validity gap:

1. the machine-readable report example drops two fields that the same contract declares mandatory and load-bearing: `claim` and `mechanism`;
2. the untrusted-target boundary is weakened by later authorization to derive and execute baseline commands from target-controlled CI/README/helper content without a universal pre-execution sandbox/inspection gate;
3. the behavioral A/B protocol does not require fresh-session/process isolation or reset of persistent memory/tool/cache state between conditions, allowing treatment leakage in stateful agents.

These are methodology defects, not adjudicated project findings.

## Blindness record

Blind Phase A consumed:

- Issue #11 task contract;
- `AGENTS.md`, `AGENT-BOOTSTRAP.json`, `AUTONOMOUS-AGENT.md`, and `.github/agents/ahp-forensic-auditor.md` from the current control plane;
- `AUDIT-METHODOLOGY/README.md`;
- `AUDIT-METHODOLOGY/CANONICAL-AGENT-AUDIT-PROMPT.md`;
- `AUDIT-METHODOLOGY/REPORT-CONTRACT.md`;
- `AUDIT-METHODOLOGY/BEHAVIORAL-EVALUATION-PROTOCOL.md`;
- the migration pointer at `AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md` only as a pointer-safety artifact, not historical audit conclusions.

Before provisional findings were recorded, I did not consume `PROMPT-DESIGN-HISTORY.md`, historical audit conclusions, external-audit reports, adjudication records, or prior model reviews of methodology v6.

Blind Phase A ended after provisional findings F-001 and F-002 were recorded. Phase B then read `AUDIT-METHODOLOGY/PROMPT-DESIGN-HISTORY.md`. The history independently confirms that v6 intended both machine-readable lossless intake and explicit untrusted-target handling, so F-001 and F-002 attack declared v6 goals rather than importing historical conclusions.

## Property-by-property result

| Property | Result | Notes |
|---|---|---|
| control-plane / evidence-plane separation | STRONG WITH GAP | Explicit separation exists, but target-derived command execution creates an authority leak. |
| blindness against historical contamination | PASS WITH LIMIT | Path and conclusion classes are separated; current docs remain readable as implementation surface. No current concrete contamination contradiction reproduced. |
| target-mode precision | PASS | `CURRENT_MAIN`, `RELEASE_TAG`, `EXACT_COMMIT` are mutually clear; arbitrary branch/PR heads can be normalized to exact commit before audit. |
| future-proof baseline discovery | STRONG WITH GAP | Discover-first avoids stale hardcoded commands, but execution safety of discovered commands is under-specified. |
| untrusted-target-content boundary | FAIL | F-002. |
| impact vs precondition / threat-model severity | PASS | Explicit precondition classes and ordinary-path/local-write distinctions are present. |
| same-model self-test vs independent behavioral evidence | PASS | The separation is explicit in both forensic and behavioral protocols. |
| behavioral A/B protocol quality | NEEDS FIX | F-003 - state reset/isolation is missing. |
| report-contract losslessness | FAIL | F-001. |
| quantity-gaming resistance | PASS | Fixed probe quotas are explicitly rejected. |
| circularity / methodology self-validation | PASS | Forensic role contract states methodology audits must not use methodology conclusions as proof. |
| migration-pointer safety | PASS | Historical path is a pointer, not a second canonical copy, and identifies the prior blob. |
| future-version robustness | STRONG WITH LIMITS | Baseline discovery and exact target resolution are future-oriented; stateful behavioral isolation and safe execution need explicit general rules. |

## Findings

### F-001 - Machine-readable report contract is not lossless

Reported severity: `P1`
Confidence: `0.99`
Evidence state: `FILE_VERIFIED`
Precondition: `ORDINARY_PATH`
Threat-model applicability: `IN_SCOPE`

Claim:
`REPORT-CONTRACT.md` states that every material finding must provide `claim` and `mechanism`, and says the machine-readable block exists so external submissions can be ingested without silently rewriting auditor claims. The canonical JSON shape omits both fields.

Mechanism:
An auditor following the canonical machine-readable example can produce a structurally plausible finding object that lacks the finding's semantic proposition (`claim`) and causal explanation (`mechanism`). Any downstream intake relying on that object cannot reconstruct those fields without reading prose or reinterpreting the auditor.

Expected behavior:
Every field declared mandatory and necessary to preserve auditor meaning should be represented in the machine-readable schema/example, or the contract should explicitly define where it is preserved losslessly.

Observed behavior:
The required-field list includes `claim` and `mechanism`; the JSON example includes `finding_id`, `title`, severity, confidence, evidence, precondition, affected components, expected/observed behavior, reproducer, consequence and close variant, but not `claim` or `mechanism`.

Evidence:
`AUDIT-METHODOLOGY/REPORT-CONTRACT.md`, sections `Required finding fields` and `Machine-readable block`.

Impact:
Lossy external-audit ingestion and increased risk that archive/adjudication layers silently infer or rewrite what the auditor actually claimed and how the failure works.

Proposed change:
Add `claim` and `mechanism` to the canonical machine-readable finding object and, preferably, publish a validated JSON Schema that matches the prose contract. Add a regression test that rejects omission of every load-bearing required field.

### F-002 - Untrusted target data can become executable authority through baseline discovery

Reported severity: `P1`
Confidence: `0.93`
Evidence state: `FILE_VERIFIED`
Precondition: `MALFORMED_EXTERNAL_INPUT`
Threat-model applicability: `IN_SCOPE`

Claim:
The canonical prompt declares all target-repository content untrusted audit data and says repository text does not gain authority merely because it contains imperative instructions. Later sections nevertheless authorize tests/checkers shipped by the target and require the auditor to derive baseline gates from target CI, README run instructions, and helper inventory. Only `legacy helper` execution receives an explicit pre-execution outside-write inspection warning.

Mechanism:
A compromised or adversarial target can place an executable command in CI/README or a shipped test/helper. A literal auditor can treat that target-defined command as the discovered baseline and execute it because section 7 says to derive and run the baseline while section 2 allows target-shipped tests/checkers. This converts target-controlled data into action authority without a universal sandbox, allowlist, static inspection, or side-effect gate.

Expected behavior:
Target content may suggest candidate commands, but no target-derived command should become authorized solely because it appears in CI/README/helper inventory. Every target-derived execution should require an explicit control-plane rule such as disposable sandbox/container, no credentials, constrained filesystem/network, command inspection, and prohibition on external side effects.

Observed behavior:
The prompt provides a universal untrusted-data rule, then a broad execution authorization, with the explicit side-effect inspection caveat scoped only to legacy helpers.

Evidence:
`AUDIT-METHODOLOGY/CANONICAL-AGENT-AUDIT-PROMPT.md`, sections `0. CONTROL PLANE / UNTRUSTED TARGET BOUNDARY`, `2. SAFETY / MUTATION BOUNDARY`, and `7. DISCOVER THE BASELINE, THEN RUN IT`.

Impact:
The audit methodology can expose an execution-capable auditor to target-defined code execution and can violate its own read-only/no-external-side-effect boundary. It also creates prompt-injection ambiguity: README/CI content is nominally data but can indirectly determine actions.

Proposed change:
Add a universal `TARGET-DERIVED EXECUTION GATE`: inspect every command/script first; execute only in a disposable sandbox with credentials removed and external writes/network disabled unless separately authorized; README/CI text may identify candidate baseline commands but never grants execution authority. Apply this rule to tests, checkers, package hooks, build steps, liveness scripts, and all helpers, not only legacy code.

### F-003 - Behavioral A/B protocol lacks explicit state isolation/reset

Reported severity: `P2`
Confidence: `0.90`
Evidence state: `FILE_VERIFIED`
Precondition: `ENVIRONMENT_FAILURE`
Threat-model applicability: `IN_SCOPE`

Claim:
The behavioral protocol requires baseline A vs AHP-loaded B, constant runtime factors, randomization and blinded evaluation, but does not require fresh sessions/processes or reset/isolation of persistent agent memory, caches, tool state, conversation history, startup state, or cross-condition artifacts.

Mechanism:
In a stateful agent, running one condition can alter memory, cache, tool state, filesystem state, or model context used by a later condition. Random assignment does not remove carryover. AHP-loaded runs can therefore contaminate nominal baseline runs or vice versa, biasing the estimated treatment effect.

Expected behavior:
Each case/condition should start from an explicitly equivalent clean state, or the protocol should define a crossover design with reset/washout and record residual carryover risk.

Observed behavior:
The protocol says to compare the same agent/runtime, keep context and system factors constant, and randomize assignment, but has no mandatory state-reset/session-isolation clause.

Evidence:
`AUDIT-METHODOLOGY/BEHAVIORAL-EVALUATION-PROTOCOL.md`, sections `Experimental conditions`, `Blinding`, `Unit of analysis`, and `Acceptance criteria`.

Impact:
A behavioral benchmark can attribute persistent-state carryover to AHP effectiveness or harm, reducing causal validity even when scoring is properly blinded.

Proposed change:
Require fresh process/session per condition where practical; reset or snapshot/restore memory, conversation, caches, tool state and writable fixtures; record unavoidable shared state; use paired case IDs/seeds where stochastic control is available; define washout/crossover handling for persistent runtimes.

## Non-findings and rejected attacks

- Fixed probe quantity gaming: not reproduced. v6 explicitly says not to game fixed counts and requires mechanism-driven coverage.
- Severity by impact alone: not reproduced. The methodology separates impact, precondition, attacker control, local write requirement, ordinary path and threat-model applicability.
- Same-model self-test promoted to independent evidence: not reproduced. Both forensic and behavioral protocols explicitly prohibit this.
- Migration pointer creating a second canonical prompt: not reproduced. The old `AUDITS/...` path is a migration pointer and tells the reader not to use it as the prompt.
- Target-mode ambiguity: not reproduced. An arbitrary mutable ref can be resolved to `EXACT_COMMIT` before the audit; the methodology correctly centers the immutable commit identity.
- Circular self-validation: not reproduced in the role contract. Methodology audits are instructed to treat the methodology itself as target data and not use its conclusions as proof.

## Limits

- This was a methodology audit, not an execution audit of AHP implementation v5.4.x.
- No local shell/runtime or behavioral benchmark was required to reproduce F-001 through F-003; they are control-contract defects visible in canonical text.
- Auditor evidence is not project adjudication.
- `AUDITOR REPRODUCED != PROJECT REPRODUCED`.
- `REPORT WRITTEN != FINDING ACCEPTED`.
- `SELF-TEST != INDEPENDENT BEHAVIORAL EVIDENCE`.

## Top next actions

1. Make the machine-readable report schema actually lossless by including `claim` and `mechanism` and validating required fields.
2. Add a universal sandbox/inspection gate before executing any target-derived command.
3. Add explicit state isolation/reset requirements to the behavioral A/B protocol.
4. Add methodology regression tests that mechanically check the prose-required finding fields against the machine-readable schema/example.

## Evidence log

- Resolved target branch snapshot by creating an isolated submission branch from `audit-methodology-v6` and comparing refs; both resolve to `efecb86326a5935d0996cf4f3f1ba21b8106890d` at audit start.
- Canonical prompt blob: `190345443b4f2599a4a9e76e5d07f64e6a6b4ed1`.
- Report contract blob: `7513e89d2cabc2626721f58b353c2162b4975190`.
- Behavioral protocol blob: `18b5e6270c375de0ddbd922b0521fcbe3a6e7d77`.
- Methodology README blob: `6de1bd8e0d5002c14c71a93bd1ae541dfcf4efa3`.
- Design history was read only after blind Phase A ended.
