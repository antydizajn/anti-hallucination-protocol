# AA-Omniscience-600 scoring contract

## Boundary

This scorer aggregates semantic adjudications. It does not judge answer correctness itself.

Therefore:

```text
AGGREGATION != SEMANTIC GRADING
MODEL_JUDGE_SCORE != GROUND TRUTH
RUNTIME ERROR != NOT_ATTEMPTED
```

AA-Omniscience-Public is an external PUBLIC diagnostic, not held-out evidence.

## Required adjudication input

The input JSON must contain:

```json
{
  "evaluator": {
    "name": "...",
    "version": "...",
    "type": "HUMAN | MODEL_JUDGE | MIXED"
  },
  "results": [
    {
      "question_id": 1,
      "run_status": "OK",
      "outcome": "CORRECT"
    }
  ]
}
```

Requirements:

- exactly 600 result rows;
- unique `question_id` set exactly 1..600;
- every row has `run_status: OK`;
- evaluator name, version, and type are recorded;
- outcome is one of `CORRECT`, `INCORRECT`, `PARTIAL`, `NOT_ATTEMPTED`.

Any infrastructure/provider/Hermes/treatment error makes the scoring input invalid until that question is rerun successfully.

## Required outputs

Every valid score file emits:

- `correct_count`
- `incorrect_count`
- `partial_count`
- `not_attempted_count`
- `attempt_rate`
- `incorrect_rate_among_attempts`
- `useful_coverage`
- `ahp_diagnostic_aggregate_score`
- evaluator identity
- interpretation boundaries

Do not report only one aggregate number.

A system can lower its wrong-answer rate by refusing everything, so:

```text
LOWER WRONG ANSWERS != AUTOMATICALLY BETTER SYSTEM
```

Interpret incorrect answers together with attempt rate and useful coverage.

## Diagnostic aggregate

The local AHP diagnostic summary is:

```text
(correct_count - incorrect_count) / 600
```

It is deliberately named `ahp_diagnostic_aggregate_score`.

This harness does **not** claim that formula is the official upstream AA-Omniscience leaderboard metric. If an upstream-compatible metric is later added, record its source/version and emit it under a separate field rather than silently redefining this diagnostic.

## A/B/C comparison

Only compare CONTROL vs LEGACY vs CURRENT when the run identities establish identical:

- model;
- provider;
- reasoning/sampling configuration;
- question JSONL bytes;
- pinned dataset identity;
- question order;
- Hermes execution family;
- no-tools policy;
- evaluator identity/version.

The comparison must allow CONTROL to win, LEGACY to beat CURRENT, no effect, or an inconclusive result.

## Invalid conclusions

This battery alone cannot establish:

- tool-use reliability;
- evidence-lineage correctness;
- current-state verification;
- universal hallucination reduction;
- uncontaminated generalization.

```text
PUBLIC DATASET != HELD-OUT DATASET
EXTERNAL DATASET != INDEPENDENT REPLICATION
```
