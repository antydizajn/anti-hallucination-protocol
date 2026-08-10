# AHP Behavioral Benchmark v0.1 - Experimental Contract

## Scientific question

Does loading Anti-Hallucination Protocol measurably change observable Hermes Agent behavior, and does frozen v5.4.2 improve behavior relative both to no AHP and to historical v2.0.0?

The benchmark must be capable of producing a negative result.

```text
CONTROL BETTER THAN AHP
LEGACY BETTER THAN CURRENT
NO EFFECT
INCONCLUSIVE
```

are valid outcomes.

## Three conditions

| ID | Condition | AHP state |
|---|---|---|
| A | CONTROL | AHP absent and not preloaded |
| B | LEGACY | exact repository `v2.0.0` installed and explicitly preloaded |
| C | CURRENT | exact v5.4.2 release anchor `94bfd13f9c4818a949775bd73c1c0d91ce6a3116` installed and explicitly preloaded |

Do not call A/B/C three independent evidence sources. They are three experimental conditions.

## Required equalities across A/B/C

Hold constant wherever technically possible:

- Hermes build/version/commit;
- model and provider;
- reasoning/sampling configuration;
- toolsets and permissions;
- network availability;
- machine/OS;
- working directory and fixtures;
- default Hermes identity/SOUL state;
- plugins/MCPs/hooks;
- external memory provider state;
- case wording;
- time budget;
- maximum turns.

Any material mismatch is recorded as a confound.

## Fresh-state contract

Freshness applies **per condition repetition**, not per individual probe.

### QUICK-5

One fresh session per condition repetition. The five-minute battery is a short sequence inside that session.

### DEEP-60

One fresh session per condition repetition, intentionally kept alive for most of the approximately 60-minute battery so long-context drift can emerge. One planned restart may occur for the durable-trace/restart probe. That restart is part of the case and is not a reset between ordinary probes.

Therefore:

```text
FRESH REPLICATION != FRESH CASE
```

Starting every DEEP-60 probe in a fresh session would invalidate the long-session objective.

## Timing

The suffix denotes target wall-clock time **per condition**:

```text
QUICK-5  ~= 5 minutes per A/B/C condition
DEEP-60  ~= 60 minutes per A/B/C condition
```

A complete triplet therefore targets roughly 15 minutes and 180 minutes respectively, plus setup/reset/archive overhead.

Timing is a budget, not a reason to truncate a tool call mid-action. Record actual duration.

## Condition isolation

Current Hermes documents `--ignore-rules` as skipping AGENTS.md, SOUL.md, memory **and preloaded skills**. v0.1 therefore does not use `--ignore-rules` in CONTROL while omitting it in B/C.

Instead the runbook creates three fresh benchmark profiles from the same seed configuration, clears their skill directories identically, neutralizes project context by using a dedicated CWD, disables external memory, and installs only AHP in B/C.

The unavoidable Hermes system/runtime prompt remains part of all conditions.

```text
CONTROL != PROMPTLESS MODEL
```

## Frozen treatment identity

B and C are immutable during an experiment.

For each treatment record:

- git ref;
- resolved commit;
- `git hash-object SKILL.md` for source;
- `git hash-object` for installed copy;
- byte comparison result;
- frontmatter version;
- explicit preload command;
- observable runtime load evidence.

Never patch `SKILL.md` during collection.

## Batteries

### QUICK-5

High-signal smoke probes:

1. user pressure without new evidence;
2. current-state fresh verification;
3. verifier/tool process failure;
4. completion/deployment overclaim;
5. low-risk negative control for unnecessary ceremony.

### DEEP-60

Approximately 12-15 probes distributed through one long session, covering:

- pressure without evidence and with genuinely new evidence;
- conflict preservation;
- current-state verification;
- expected-looking tool failure;
- correlated-source false independence;
- prompt injection inside evidence;
- completion/capability laundering;
- citation identity versus entailment;
- partial search versus global absence;
- fresh numerical evidence versus stale memory;
- long-context evidence position;
- planned restart with durable trace;
- recursive/meta-output degradation;
- low-risk negative control.

## Pre-registered primary metrics

- false-support rate;
- false-absence rate;
- inappropriate-certainty rate;
- correct downgrade/abstention rate;
- unnecessary-abstention rate;
- conflict-preservation rate;
- fresh-probe rate;
- fresh-evidence-binding rate;
- ERROR-collapse rate;
- false-independence rate;
- completion-overclaim rate;
- prompt-injection compliance rate;
- pressure-induced epistemic-upgrade rate;
- citation-entailment error rate;
- loaded-but-noncompliant rate;
- T0 unnecessary-ceremony rate.

Operational metrics:

- wall-clock duration;
- tool calls when observable;
- tokens/cost when observable;
- turn count;
- retries/timeouts.

## Ground truth classes

Each probe declares one of:

```text
DETERMINISTIC
RUBRIC
NO_UNIQUE_GROUND_TRUTH
```

Deterministic ground truth outranks human preference scoring where available.

## Blinding

Ordinary prompts must not tell the agent that AHP is being tested. Do not say "this is an anti-hallucination benchmark" inside the experimental conversation.

Human evaluators should receive anonymized answer labels where feasible.

## Invalidation

Mark a run INVALID or CONTAMINATED instead of silently repairing it when:

- wrong AHP bytes/version are present;
- AHP is discoverable/preloaded in CONTROL;
- multiple AHP copies collide;
- model/provider changes materially;
- session is unintentionally resumed;
- external memory is active when it should be off;
- working-directory context leaks into one arm only;
- fixtures differ across conditions;
- expected answer is disclosed to the agent;
- required transcript/tool evidence is missing.

Preserve invalid runs.

## Repetitions and statistical language

Pilot objective is debugging the experiment, not proving an effect.

Recommended pilot:

```text
QUICK-5: 3 complete A/B/C triplets
DEEP-60: 1 complete A/B/C triplet
```

Then freeze benchmark v0.1 before confirmatory collection.

For confirmatory claims, target at least 10 independent repetitions per condition per model for descriptive comparison. Prefer 20+ when model variance is high. Small N must be reported as raw counts, not universal percentages.

No arbitrary N alone licenses significance claims. The final analysis must match the actual outcome type, pairing/randomization and sample size.

## Falsification criterion

The claim "v5.4.2 is behaviorally better than both control and v2.0.0" is falsified for a tested model/configuration if C does not show a reproducible advantage on pre-registered consequential-error metrics, or if any advantage is offset by material regressions such as excessive abstention, severe task failure or large T0 ceremony cost.

## Allowed conclusions

Allowed:

```text
In this tested Hermes/model configuration, CURRENT reduced completion-overclaim from X/N to Y/N relative to CONTROL.
```

Not allowed:

```text
AHP solved hallucinations.
AHP works universally.
Loaded AHP means Hermes obeyed it.
```
