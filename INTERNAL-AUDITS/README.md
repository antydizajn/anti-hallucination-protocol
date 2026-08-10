# Internal Behavioral Audit Evidence

`INTERNAL-AUDITS/` is the project-originated behavioral evaluation workspace for Anti-Hallucination Protocol (AHP).

It is deliberately separate from both:

```text
main             = canonical implementation/release state
external-audits  = evidence originating outside the canonical project process
internal-audits  = project-originated controlled experiments and benchmark runs
```

## Core boundary

```text
INTERNAL EVIDENCE != EXTERNAL INDEPENDENT CONFIRMATION
PROJECT_ORIGINATED = YES
EXTERNAL_INDEPENDENCE_CLAIM = NONE
```

A strong internal experiment can establish a reproducible project-side behavioral effect. It does not become external independent evidence merely because another model, profile, run, or evaluator participated.

## Benchmark v0.1

The first benchmark asks:

> Does loading AHP measurably change observable Hermes Agent behavior, and does frozen v5.4.2 improve behavior relative both to no AHP and to historical v2.0.0?

Three experimental conditions:

```text
A CONTROL  = Hermes Agent, AHP not loaded
B LEGACY   = same controlled runtime, AHP v2.0.0 explicitly preloaded
C CURRENT  = same controlled runtime, AHP v5.4.2 explicitly preloaded
```

Frozen AHP targets:

```text
v2.0.0 = repository tag/ref v2.0.0
v5.4.2 = release anchor 94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

Do not replace frozen targets with mutable `main` during an experiment.

## Non-collapse rules

```text
INSTALLED != LOADED
LOADED != OBEYED
OBEYED ONCE != BEHAVIORALLY EFFECTIVE
ONE RUN != REPRODUCIBLE EFFECT
THREE CONDITIONS != THREE INDEPENDENT SOURCES
MODEL SELF-SCORE != GROUND TRUTH
HUMAN SCORE != AUTOMATIC TRUTH
CHECKER PASS != SEMANTIC TRUTH
```

The benchmark scores observable outputs, tool traces and durable runtime evidence. Hidden chain-of-thought is neither required nor scored.

## Layout

```text
INTERNAL-AUDITS/
├── README.md
├── INDEX.md
├── BENCHMARK-DESIGN.md
├── PILOT-PLAN.md
├── POLICIES/
├── BATTERIES/
│   ├── QUICK-5/
│   └── DEEP-60/
├── SCHEMAS/
├── TEMPLATES/
├── INSTRUCTIONS/
├── RUNNERS/
└── RUNS/                 # create only when real evidence exists
```

## Hermes isolation boundary

Current Hermes CLI exposes `--ignore-rules`, but current CLI documentation states that this also skips preloaded skills. Therefore v0.1 does **not** compare CONTROL using `--ignore-rules` against treatments without it.

Instead all conditions use fresh profile state, a neutral working directory, the same model/provider/tools/default identity, and no external memory provider. B and C differ from A only by the installed/preloaded AHP artifact.

A Hermes profile isolates Hermes config, sessions, local memory, skills and state under profile-specific `HERMES_HOME`, but it is not a filesystem sandbox. The human runbook records that limitation.

## Historical hypothesis material

`ahp-usage-test/AHP_usage_test/` is hypothesis-generating evidence, not benchmark ground truth. High-value historical failure families include:

```text
fresh evidence loses to stale memory
recursive meta-collapse
INSTALLED/LOADED -> "working" overclaim
user pressure without new evidence
current-state scope confusion
```

Historical PASS labels are not imported as expected outcomes.
