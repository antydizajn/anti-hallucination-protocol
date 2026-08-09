# Anti-Hallucination Protocol - TODO / Roadmap

This file tracks work that remains after the deterministic v5.4.1 hardening release.

It is a roadmap, not evidence that a task is still open forever. Before acting on any item, inspect the current repository and determine whether later work already closed it.

## Stable release anchor

At the time this roadmap was created, the latest regression-verified public release was:

```text
v5.4.1
7f5454c9c8e58ca9bd0728d13210d6c5a6424bc1
```

Release evidence recorded in `AUDITS/v5.4.1-hardening-status.md`:

```text
Python 3.11 CI: PASS
Python 3.13 CI: PASS
Python 3.13: 124 collected / 124 passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
behavioral obedience: UNKNOWN
```

Do not treat the current `main` HEAD, current test count, current CI status, live research titles, or current Hermes behavior as immutable facts. Recompute them.

---

# NOW - documentation and evidence hygiene

## TODO-NOW-001 - bring `AUDITS/SUMMARY.md` through v5.4.1

Status: OPEN
Priority: HIGH
Class: audit synthesis / documentation

`AUDITS/SUMMARY.md` currently ends its main disposition at v5.4 and still describes running the v5.4 regression suite and fresh blind audit as future work. That is stale after the v5.4.1 hardening and final regression verification.

Required work:

- add a v5.4 Round 3 / v5.4.1 section;
- separate audit classes rather than averaging them;
- record which findings were actually reproduced versus source-inferred;
- record the independent reproduction of the two invalid YAML test assumptions;
- record the deterministic false-FOUND paths discovered around empty matchers;
- record same-source / same-source-identity independence hardening;
- record symlink escape, schema-form drift, whitespace-only values, `PARTIAL`, liveness, BOM and quoted duplicate-key hardening;
- record final release evidence from the actual GitHub Actions run;
- preserve the explicit limitation that behavioral obedience remains UNKNOWN;
- preserve rejected findings and do not silently upgrade heuristic claims.

Definition of done:

- synthesis accurately describes v5.4.1;
- every major disposition has an evidence class;
- no claim that v5.4.1 solved semantic truth, real-world source independence or behavioral obedience.

## TODO-NOW-002 - complete audit archive integrity

Status: OPEN
Priority: HIGH
Class: evidence archive

Known concrete debt:

`AUDITS/PPX-GLM5.2.md` is still an explicit placeholder for an original 91,118-byte report with SHA-256:

```text
4addb24f096248a7be5f7e0090df70daa957676a01478610b293bf23f0eccf20
```

Required work:

- replace the placeholder only if the original raw bytes are available;
- verify byte count and SHA-256 before calling the archive complete;
- inventory the newer Round 3 audit files and determine which are raw reports, summaries, copied chat output or methodology reviews;
- record hashes for raw external reports where source bytes are available;
- never claim a complete byte-identical audit archive until every claimed raw report is actually verified.

This is an archive-integrity task, not a runtime correctness blocker.

## TODO-NOW-003 - inventory Round 3 audit evidence

Status: OPEN
Priority: HIGH
Class: evidence provenance

Build an explicit Round 3 manifest covering the audits/reviews used for v5.4.1.

For each artifact record:

- filename;
- model;
- audit date;
- target commit/version if known;
- fresh clone / project files / static review / methodology review;
- execution capability;
- exact test inventory if executed;
- source-file hash where raw bytes exist;
- whether the report is complete or excerpted.

Do not reconstruct missing reports from memory and call them raw evidence.

## TODO-NOW-004 - verify repository protection and release mechanics

Status: OPEN
Priority: MEDIUM
Class: repository operations

Inspect, do not assume:

- whether `main` has branch protection or rulesets;
- whether the permanent Python 3.11/3.13 regression workflow is a required check;
- whether force-push is disabled for normal work;
- whether GitHub Release objects exist for the release tags or only Git tags exist.

If protection is absent, consider requiring the regression workflow before merges. Do not rewrite historical tags merely to improve presentation.

---

# NEXT - behavioral benchmark v0.1

## TODO-BEH-001 - design the first real AHP behavioral benchmark

Status: OPEN
Priority: HIGHEST PROJECT FRONTIER
Class: behavioral evaluation

This is the most important unresolved project question after v5.4.1.

Goal:

Measure whether loading AHP changes real agent behavior. Do not infer this from deterministic tests.

The benchmark should compare at minimum:

```text
CONTROL: same model / same task / AHP not loaded
TREATMENT: same model / same task / AHP explicitly loaded
```

Use fresh sessions and keep all other controllable conditions as similar as possible.

The benchmark must not require access to hidden chain-of-thought. Score observable outputs and tool traces.

Proposed artifact layout, not yet implemented:

```text
benchmarks/
  README.md
  cases/
  runners/
  schemas/
  results/
```

Do not create this structure until the benchmark contract is designed.

## TODO-BEH-002 - benchmark case families

Status: OPEN
Priority: HIGH

Include at least these case families:

1. **User pressure does not upgrade evidence state**
   - reach `INCONCLUSIVE`;
   - apply pressure such as "just say yes", "stop hedging", "I know it works";
   - no new evidence means no silent upgrade to `SUPPORTED_WITH_SCOPE`.

2. **Preferred-answer pressure / conflict preservation**
   - support plus material contradiction;
   - user clearly prefers one side;
   - preserve `CONFLICT` when both sides remain material.

3. **Tool failure**
   - failing verifier/search emits expected-looking text;
   - `ERROR` must remain `ERROR`.

4. **Current-state claims**
   - stale memory/docs conflict with a fresh runtime/API observation;
   - measure whether the model performs a fresh probe and scopes the answer.

5. **Correlated sources**
   - multiple URLs/agents share one origin;
   - source count must not be mistaken for independent support.

6. **Long context / evidence position**
   - decisive evidence early, middle and late;
   - measure omission, overclaim and false certainty.

7. **Prompt injection inside evidence**
   - retrieved content contains instructions;
   - measure whether evidence stays out of the instruction plane.

8. **Completion overclaim**
   - patch exists but deployment/user path is unobserved;
   - model must not say "fixed/deployed/working" without matching evidence.

9. **Compaction/restart / durable traces**
   - earlier action survives only in durable trace;
   - model must not confidently deny it solely because conversational memory is compacted.

10. **Startup loading versus obedience**
    - verify the skill was actually loaded at boot;
    - score behavior separately from load evidence.

## TODO-BEH-003 - define behavioral metrics before running models

Status: OPEN
Priority: HIGH

Predefine metrics before looking at results to reduce benchmark gaming.

Candidate metrics:

- false-support rate;
- false-absence rate;
- inappropriate-certainty rate;
- correct abstention/downgrade rate;
- conflict-preservation rate;
- fresh-probe rate for current-state questions;
- ERROR-collapse rate;
- source-correlation / false-independence rate;
- completion-overclaim rate;
- prompt-injection compliance rate;
- user-pressure epistemic-upgrade rate;
- explicit checked/not-checked reporting rate;
- startup-load success rate;
- loaded-but-noncompliant rate.

Report denominators and confidence intervals where sample sizes justify them. Do not convert a tiny qualitative sample into a universal percentage claim.

## TODO-BEH-004 - build a multi-model evaluation matrix

Status: OPEN
Priority: MEDIUM/HIGH

Use more than one model family when feasible.

Requirements:

- fresh sessions;
- same case definitions;
- explicit model/version/provider;
- AHP loaded state recorded;
- tool/runtime availability recorded;
- repetitions sufficient to expose nondeterminism;
- raw observable transcripts/traces preserved when privacy permits.

Do not average models into one score without also publishing per-model results.

## TODO-BEH-005 - define acceptance criteria

Status: OPEN
Priority: HIGH

Before calling AHP behaviorally effective, define what result would count as evidence for improvement and what would count as failure.

At minimum distinguish:

```text
NO EFFECT
IMPROVEMENT WITH REGRESSIONS
CONSISTENT IMPROVEMENT
MODEL-SPECIFIC EFFECT
INCONCLUSIVE
```

A benchmark must be able to falsify the project's hoped-for effect. If every result can be interpreted as success, the benchmark is invalid.

---

# NEXT - Hermes runtime and startup integration

## TODO-RUN-001 - verify `/start` integration in real clean sessions

Status: OPEN
Priority: HIGH

README now requires explicit startup loading for always-on use.

Verify in real fresh Hermes sessions:

- `/start` or equivalent boot procedure actually calls `skill_view(name="anti-hallucination-protocol")`;
- startup trace contains a successful AHP load;
- the loaded version matches the intended installed version;
- a restart/new session repeats the load;
- failure to load is visible rather than silently treated as active.

Remember:

```text
INSTALLED != LOADED
LOADED != OBEYED
```

## TODO-RUN-002 - verify `${HERMES_SKILL_DIR}` behavior in real Hermes

Status: OPEN
Priority: MEDIUM

Test the documented helper invocation in a real Hermes runtime with:

- skill template variables enabled;
- template variables disabled, if supported by the current Hermes version;
- current working directory unrelated to the skill directory;
- path containing spaces where feasible.

Separate official documentation claims from actually observed runtime behavior.

## TODO-RUN-003 - investigate a real runtime/output gate

Status: RESEARCH
Priority: MEDIUM

AHP currently remains a policy skill plus explicitly invoked deterministic helpers.

Research current Hermes extension/plugin/hook architecture before designing enforcement.

Possible goal:

- intercept or gate only load-bearing consequential claims/actions;
- avoid making harmless T0/T1 tasks ceremonial;
- preserve explicit failure modes;
- avoid silently turning a helper error into denial or absence.

Do not implement a runtime gate from guessed Hermes APIs.

## TODO-RUN-004 - consider a read-only startup diagnostic

Status: DESIGN
Priority: MEDIUM

Consider a helper that can report:

```text
INSTALLED
DISCOVERABLE
LOADED - only if observable from a durable runtime trace
VERSION MATCH / MISMATCH
STARTUP INTEGRATION UNKNOWN
```

It should be read-only by default. Do not automatically edit `/start`, config or user state.

---

# RESEARCH - provenance and external observation

## TODO-RES-001 - provenance graph / source-origin resolution

Status: RESEARCH
Priority: MEDIUM

Current structural independence metadata deliberately does not prove real-world independence.

Research a provenance layer capable of representing:

- syndication;
- common wire-service origin;
- mirrors;
- repository forks;
- copied benchmark/result lineage;
- dependency/source ancestry;
- direct versus derivative evidence.

A provenance graph should reduce obvious false independence without pretending that unknown lineage is proven independence.

## TODO-RES-002 - live world-state adapters

Status: RESEARCH
Priority: MEDIUM

For current-state claims, prefer auditable external observations over human visual confirmation when stronger probes exist.

Candidate adapters:

- HTTP/health checks;
- process/service probes;
- database queries;
- repository/API state;
- package/version queries;
- signed/authoritative API responses;
- domain-specific sensors.

Every adapter needs explicit scope, observation time and failure semantics.

## TODO-RES-003 - semantic entailment evaluation

Status: RESEARCH
Priority: MEDIUM

The structural checker does not prove that a source span semantically entails a claim.

Investigate semantic entailment methods without collapsing them into an oracle:

- NLI models;
- structured extraction;
- claim/source decomposition;
- multi-judge disagreement;
- human adjudication for benchmark ground truth;
- confidence calibration.

A semantic verifier's own result must remain a scoped claim subject to evaluation.

## TODO-RES-004 - judge-bias harness

Status: RESEARCH
Priority: MEDIUM

If LLM judges are used in the behavioral benchmark, explicitly measure:

- self-preference bias;
- verbosity/style preference;
- position bias;
- correlated judge failures;
- disagreement with deterministic ground truth where available.

Do not let one LLM judge silently become the benchmark oracle.

## TODO-RES-005 - risk-tier calibration

Status: RESEARCH
Priority: LOW/MEDIUM

Study whether models consistently classify T0-T3 consequences as intended.

Focus on ambiguous boundary cases rather than inventing universal numerical risk thresholds.

Human governance may define acceptable risk and authorization policy, but human judgment is not automatically factual ground truth.

---

# PLATFORM / PORTABILITY

## TODO-PLAT-001 - native Windows evidence

Status: OPEN
Priority: LOW/MEDIUM

Current docs explicitly avoid claiming native Windows Bash execution.

Future validation could separately test:

- Python checkers on native Windows;
- liveness under Git Bash;
- liveness under WSL;
- path separators;
- symlink capability/permissions;
- Unicode and spaces in paths.

Do not change the support claim until actual execution evidence exists.

## TODO-PLAT-002 - broaden Python CI only when justified

Status: OPTIONAL
Priority: LOW

Current permanent CI runs Python 3.11 and 3.13 on Ubuntu.

Consider additional versions/platforms only if they correspond to supported/real user environments. More matrix cells are not automatically more evidence.

---

# RELEASE / MAINTENANCE

## TODO-REL-001 - decide whether to add `CHANGELOG.md`

Status: OPTIONAL
Priority: LOW/MEDIUM

The reconstructed Git history and tags preserve real development history, but a concise human-facing changelog could make release differences easier to inspect.

If added:

- derive entries from verified commits/releases;
- distinguish policy changes from deterministic hardening;
- do not fabricate historical dates or release notes.

## TODO-REL-002 - verify release tags after future releases

Status: RECURRING

For every future release:

- exact version in `SKILL.md`;
- integrity checker exact release pin;
- full regression suite executed;
- provenance check executed;
- liveness executed;
- release candidate audited as appropriate;
- tag created only after evidence exists;
- record exact commit and CI run.

## TODO-REL-003 - keep handoff and TODO self-staleness resistant

Status: RECURRING

`PROJECT-HANDOFF.md` must preserve historical anchors but should not hardcode ephemeral claims such as "main is N commits ahead" as if they remain current.

When a new release is made:

- update the stable release anchor;
- update historical release evidence;
- move closed roadmap items to a changelog/synthesis rather than deleting their history blindly;
- keep current-state instructions phrased as live verification steps.

---

# DO NOT DO WITHOUT NEW EVIDENCE

These ideas were previously rejected, downgraded or identified as likely security theatre. Do not reintroduce them merely because a new model suggests them.

- Do not re-bloat `SKILL.md` into the v5.2 monolith.
- Do not add epistemic enums merely to sound more precise.
- Do not blacklist phrases such as `trust me` and pretend that proves provenance.
- Do not hard-require terminal access for the entire policy layer.
- Do not claim universal freshness windows without domain-specific evidence.
- Do not treat human review as an automatic truth oracle.
- Do not automatically mutate `/start`, Hermes config, memory or user state during installation/audit.
- Do not call source-count independent evidence without origin analysis.
- Do not call deterministic structural validation semantic truth.
- Do not call a documented architectural unknown a code defect unless a project claim contradicts the limitation.
- Do not create v5.5 merely because the version number is available.

---

# Definition of done for future fixes

A deterministic bug is not closed by prose alone.

Preferred closure sequence:

```text
1. minimal reproducer
2. evidence label
3. smallest mechanism-level patch
4. regression for original reproducer
5. close-variant/adversarial regression
6. full current test suite
7. integrity/provenance/liveness as relevant
8. documentation only after behavior matches it
9. independent audit/reproduction when severity justifies it
```

For behavioral work:

```text
1. predeclared case and metric
2. control/treatment design
3. observable trace/output
4. repeated runs
5. per-model result
6. failure analysis
7. limitations
8. no universal claim beyond measured scope
```

---

# Current project-level priority

Unless new reproduced evidence points elsewhere, the ordering should be:

```text
1. update audit synthesis / archive integrity
2. design behavioral benchmark contract
3. run AHP-loaded versus control Hermes evaluations
4. improve runtime/startup observability
5. research provenance/live-state/semantic layers
6. only then consider a new major protocol release
```

The next confidence increase should come from **measured behavior**, not from adding another page of instructions to the active skill.
