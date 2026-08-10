# AA-Omniscience contamination boundary

## Classification

AA-Omniscience-Public is an external public diagnostic battery.

Classification:

```text
EXTERNAL
PUBLIC
NOT_HELD_OUT
```

This means the test material originates outside AHP, but the execution remains project-run unless an independent party reproduces it.

```text
EXTERNAL DATASET != INDEPENDENT REPLICATION
PUBLIC DATASET != HELD-OUT DATASET
```

## Allowed claims

Allowed after a valid completed and adjudicated run:

- "Model scored X on AA-Omniscience-Public at pinned revision Y under recorded runtime configuration Z."
- "Under matched run identities and evaluator version, condition A and condition B differed on this public battery."

Not allowed:

- "The model has never seen these questions."
- "This is uncontaminated held-out generalization evidence."
- "This proves real-world knowledge improvement."
- "This proves AHP prevents hallucination generally."

## Required comparison metrics

Do not report only one aggregate score.

Record:

- correct count;
- incorrect count;
- partial count;
- not-attempted count;
- attempt rate;
- incorrect rate among attempts;
- useful coverage;
- AHP diagnostic aggregate;
- evaluator identity/version/type.

The local diagnostic aggregate is not claimed to be the official upstream AA-Omniscience leaderboard metric.

## Abstention warning

A system can improve a wrong-answer metric by refusing nearly everything.

Therefore:

```text
LOWER WRONG ANSWERS != AUTOMATICALLY BETTER SYSTEM
```

Interpret incorrect answers together with usefulness and coverage.

## Runtime failure warning

Provider failures, Hermes failures, treatment-load failures, parser failures, and other infrastructure errors are not epistemic abstentions.

```text
ERROR != NOT_ATTEMPTED
```

They must be rerun or reported as runtime failures. They cannot be converted into a safer-looking benchmark outcome.

## Evidence boundary

Static validation can establish file/schema/contract integrity only.

```text
STATIC PASS != DATASET FETCH PASS
STATIC PASS != HERMES RUNTIME PASS
STATIC PASS != AHP EFFECTIVENESS
```
