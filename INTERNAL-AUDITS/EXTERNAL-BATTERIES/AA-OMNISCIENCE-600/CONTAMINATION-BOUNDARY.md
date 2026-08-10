# AA-Omniscience contamination boundary

## Classification

AA-Omniscience-Public is an external public diagnostic battery.

Classification:

```
EXTERNAL
PUBLIC
NOT HELD OUT
```

## Allowed claims

Allowed:

- "Model scored X on AA-Omniscience-Public at pinned revision Y."
- "Under identical prompts, condition A and condition B differed on this public battery."

Not allowed:

- "Model has never seen these questions."
- "This proves real-world knowledge improvement."
- "This proves AHP prevents hallucination generally."

## Required comparison metrics

Do not report only one aggregate score.

Record:

- correct count
- incorrect count
- partial count
- not attempted count
- attempt rate
- incorrect rate among attempts
- useful coverage
- aggregate benchmark score

## Abstention warning

A system can improve hallucination metrics by refusing everything.

Therefore:

```
LOWER WRONG ANSWERS != AUTOMATICALLY BETTER SYSTEM
```

Interpret with usefulness and coverage metrics.
