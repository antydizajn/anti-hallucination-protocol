# AHP RESTART

## Status

`MEASUREMENT PROGRAM ONLY`

No intervention efficacy claim is currently supported.
No treatment implementation is admitted.

This directory supersedes the earlier `BENCHMARK-RESEARCH-V1` work as the normative research-program structure. Earlier benchmark research remains usable only as development evidence unless re-admitted under the rules here.

## Why this restart exists

The project previously risked two distinct forms of self-confirmation:

1. `SOLUTION BEFORE MEASUREMENT`
2. adaptive reuse of evaluation evidence after treatment decisions become outcome-dependent.

The restart therefore separates measurement development, failure discovery and treatment confirmation.

## Evidence worlds

```text
D0 = MEASUREMENT DEVELOPMENT
D1 = CONTROL DISCOVERY
D2 = SEALED PROMOTION
T  = EXTERNAL / TEMPORAL TRANSFER
```

### D0

May be inspected freely.

Used for:

- benchmark discovery;
- adapter debugging;
- grader validation;
- scorer debugging;
- schema debugging;
- runner debugging;
- stub baselines;
- variance estimation;
- session-isolation testing.

Never used as final independent efficacy evidence for an intervention influenced by it.

### D1

CONTROL-only discovery evidence.

May drive:

- failure clustering;
- hypothesis generation;
- intervention targeting.

Once it influences intervention design, it is permanently non-confirmatory for that intervention lineage.

### D2

Single-use sealed promotion evidence.

Treatment developers must not see item-level D2 content, reference answers, attack instances, grader outputs or CONTROL failures on D2 before treatment freeze.

After results are exposed:

```text
D2 = BURNED
```

A failed intervention may not be edited and rerun against the same D2.

### T

Independent transfer evidence from materially different lineages, maintainers, temporal refreshes or generation pipelines where feasible.

A D2 win without transfer support is not generalization evidence.

## Five gates

```text
GATE 1 - LANDSCAPE + LINEAGE + POOL ASSIGNMENT
GATE 2 - PREREGISTRATION + FROZEN CAUSAL CONTRACT
GATE 3 - CONTROL-ONLY MEASUREMENT PILOT ON D0
GATE 4 - CONTROL FAILURE DISCOVERY ON D1 + HYPOTHESIS FREEZE
GATE 5 - ONE-SHOT SEALED TREATMENT TEST ON D2 + TRANSFER
```

Development gate failure may return for repair.

Confirmatory failure has different semantics:

```text
D2 FAILURE
-> BURNS D2
-> CONSUMES CONFIRMATORY ATTEMPT
-> DOES NOT RESTORE HOLDOUT STATUS
```

## No solution code before admission

Until Gates 1-4 pass and a treatment hypothesis is frozen, intervention code is scientifically inadmissible.

Allowed work before intervention admission:

```text
research
measurement
benchmarks
adapters
scoring
grading
data provenance
analysis
manifests
audit
```

Forbidden as active research output before admission:

```text
new AHP behavioral rules
new treatment prompt
new policy tree
new evidence hierarchy intended as treatment
new intervention architecture
```

## Current state

```text
Gate 1: OPEN - NOT PASSED
Gate 2: NOT FROZEN
Gate 3: NOT STARTED
Gate 4: NOT STARTED
Gate 5: NOT ADMITTED
```

The existing benchmark registry contains useful D0 discovery work but does not yet satisfy the Gate 1 lineage, contamination, grader-risk, license, overlap and pool-assignment requirements.

## Primary methodological invariants

```text
PUBLIC != SEALED
HELD_OUT_ITEM != HELD_OUT_FROM_RESEARCH_PROCESS
NEW_ATTACK_NAME != INDEPENDENT_LINEAGE
MULTIPLE_LLM_JUDGES != INDEPENDENT_REPLICATION
PROMPT_ROW != EXPERIMENTAL_UNIT
RUNTIME_FAILURE != ABSTENTION
HASH_CONSISTENCY != HISTORICAL_ATTESTATION
BETTER_THAN_CONTROL != PROMOTED
NULL_CONFIRMATORY_RESULT != TRY_AGAIN_ON_SAME_HOLDOUT
```

## Experimental unit

The inferential unit is an independent fresh agent session or a matched block of independent fresh sessions.

Treatment condition must not change inside a persistent context-bearing session.

## Promotion principle

A future treatment must be capable of returning any of:

```text
TREATMENT_WINS
CONTROL_WINS
NO_EFFECT
MIXED
HARM
INCONCLUSIVE
```

Any architecture that cannot return these outcomes is not a scientific evaluation system.
