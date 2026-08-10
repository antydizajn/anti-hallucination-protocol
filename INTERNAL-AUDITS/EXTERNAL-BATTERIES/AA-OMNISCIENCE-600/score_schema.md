# AA-Omniscience-600 scoring contract

## Purpose

This scorer measures answer calibration on the public AA-Omniscience battery.

It is an external diagnostic, not proof of general hallucination prevention.

## Required outputs

Every run MUST emit:

- correct_count
- incorrect_count
- partial_count
- not_attempted_count
- attempt_rate
- incorrect_rate_among_attempts
- useful_coverage
- aggregate_score

## Required interpretation

Never report only aggregate_score.

A lower hallucination rate achieved by refusing everything is not an automatic improvement.

## Invalid conclusions

The benchmark alone cannot establish:

- tool-use reliability;
- evidence lineage correctness;
- current-state verification;
- universal hallucination reduction.

## Comparison

Valid comparison:

CONTROL vs LEGACY vs CURRENT under identical:

- model
- provider
- temperature/settings
- prompt
- question revision
- evaluator version

## Public data warning

AA-Omniscience-Public is not held-out evidence.

```
PUBLIC DATASET != HELD-OUT DATASET
```
