# TruthfulQA - Gate 1 Benchmark Review

## Status

```yaml
benchmark_id: truthfulqa
review_status: COMPLETE_WITH_OPEN_RISKS
primary_eligible: true
primary_scope:
  - FALSE_PREMISE
  - MISCONCEPTION_RESISTANCE
  - TRUTHFUL_GENERATION
historical_public_role: D0_MEASUREMENT_DEVELOPMENT
control_discovery_role: D1_CONTROL_DISCOVERY
sealed_d2_role: NOT_ELIGIBLE_BY_DEFAULT
transfer_role: WEAK_STATIC_TRANSFER
```

TruthfulQA is useful for AHP because it probes whether models reproduce common human misconceptions and false beliefs. It is not a generic knowledge benchmark and should not be treated as one.

---

# 1. Identity

```yaml
canonical_name: TruthfulQA
question_count: 817
category_count: 38
primary_source: https://arxiv.org/abs/2109.07958
official_repository: https://github.com/sylinrl/TruthfulQA
license: Apache-2.0
```

The official repository exposes the benchmark questions and reference answers publicly.

In January 2025 the repository introduced an improved binary multiple-choice version and also updated/dropped some questions, including removal of the `Indexical Error: Time` category because some answers had become outdated or conflicted with modern internet-enabled model usage.

Therefore benchmark version/revision must be frozen explicitly.

---

# 2. Construct

## Primary constructs

```text
TRUTHFULNESS UNDER COMMON MISCONCEPTIONS
FALSE-PREMISE / MISLEADING-PREMISE RESISTANCE
RESISTANCE TO HUMAN-IMITATION FALSEHOODS
```

The benchmark was designed around questions for which humans may give false answers due to misconceptions or false beliefs.

## Secondary constructs

```text
INFORMATIVENESS
QUALIFIED CORRECTION
```

## What TruthfulQA does NOT establish

```text
broad factual recall
knowledge coverage
calibration in general
temporal freshness
citation correctness
RAG grounding
tool honesty
agent completion honesty
long-context grounding
universal hallucination reduction
```

A model can have strong broad factual recall while still failing TruthfulQA, or vice versa.

---

# 3. Task semantics

TruthfulQA has two major task families:

```text
GENERATION
MULTIPLE CHOICE
```

Generation asks for a short free-form answer and evaluates both truthfulness and informativeness.

Multiple choice evaluates the ability to identify true statements. The official repository now recommends the newer binary multiple-choice formulation over the original MC1/MC2 variants.

These are not interchangeable measurement instruments.

AHP must preserve task identity and must not pool generation and multiple-choice scores into a single headline without preregistered justification.

---

# 4. Answerability and utility

The benchmark explicitly recognizes a refusal-gaming problem.

Its generation objective distinguishes:

```text
TRUTHFULNESS
INFORMATIVENESS
```

because a model that answers "I have no comment" to every question could obtain high truthfulness while being useless.

This is directly relevant to AHP.

## Degenerate-policy analysis

```text
ALWAYS_ABSTAIN:
  can game truthfulness if informativeness is ignored

ALWAYS_ANSWER:
  vulnerable to misconception-induced falsehoods

GENERIC_DISCLAIMER:
  may superficially reduce false statements while reducing utility
```

Therefore TruthfulQA must never be used in AHP with a truthfulness-only primary score lacking a hard answer/usefulness guardrail.

---

# 5. Grading

## Generation task

The historical repository offers:

```text
fine-tuned GPT judge for truthfulness
fine-tuned GPT info classifier
BLEURT
ROUGE
BLEU
```

The repository states that the fine-tuned GPT metrics predicted human judgments better than the similarity metrics, but also states that the fine-tuned models are not externally available and should be used as TruthfulQA-specific metrics rather than assumed to generalize.

This creates a modern reproducibility problem for AHP:

```text
HISTORICAL GPT-JUDGE
!=
AVAILABLE FROZEN 2026 PRIMARY GRADER
```

AHP decision:

```yaml
historical_generation_grader: NOT_DIRECTLY_REUSABLE
new_llm_judge: D0_VALIDATION_REQUIRED
human_blinded_protocol: PRIMARY_CANDIDATE
```

## Multiple choice

The new binary setting can provide a simpler objective scoring surface, but it measures recognition/selection rather than free-form truthful generation.

Therefore a binary MC result cannot silently substitute for the generation construct.

---

# 6. Runtime/error semantics

TruthfulQA itself does not define AHP runtime semantics.

The adapter must keep separate:

```text
MODEL_TIMEOUT
MODEL_API_ERROR
EVALUATOR_ERROR
EMPTY_OUTPUT
CLEAN_ABSTENTION
```

An evaluator failure or empty transport response cannot become a truthful refusal.

---

# 7. Contamination

```yaml
public_or_private: PUBLIC
answer_key_public: true
contamination_class: C2
benchmark_memorization_risk: HIGH
intervention_leakage_risk: HIGH_IF_ITEM_LEVEL_INSPECTED
```

TruthfulQA is an old, widely used public benchmark with public reference answers.

It is therefore not eligible as a sealed D2 holdout by default.

A treatment designed after inspecting TruthfulQA failures may still be evaluated on TruthfulQA for development or comparability, but not presented as independent confirmation.

---

# 8. Lineage and versioning

```yaml
lineage_group: truthfulqa
construction: human-crafted misconception-inducing questions
shared_public_items: yes
major_revision_note: January 2025 binary MC update and item cleanup
```

The repository also notes a related smaller TruthfulQA task in BIG-bench and explicitly warns that neither task should appear in training data when testing on the other.

This means BIG-bench TruthfulQA and the original TruthfulQA must not automatically be counted as independent benchmark lineages.

---

# 9. Evidence-role decision

## D0

Strong for:

```text
false-premise scoring
misconception-resistance measurement
truthfulness-vs-informativeness endpoint metrology
refusal-gaming stubs
human/judge calibration
```

## D1

Useful for CONTROL discovery of:

```text
misconception-triggered falsehoods
failure to challenge misleading premises
overconfident false answers
```

## D2

```text
NOT ELIGIBLE BY DEFAULT
```

because the benchmark and reference answers are public and widely exposed.

## T

Static public TruthfulQA is weak as genuinely fresh transfer evidence. It is better treated as an external comparability family than as proof of temporal or sealed generalization.

---

# 10. Rejection-rule audit

```text
R1  construct mismatch: PASS within misconception/truthfulness scope
R2  no operational scoring boundary: PASS only after generation-vs-MC contract frozen
R3  degenerate-policy exploit: IMPORTANT - truthfulness alone is abstention-gameable
R4  positive-evidence absence: PASS only when informativeness/usefulness preserved
R5  grader not auditable: TRIGGERED for direct reuse of historical unavailable GPT judges
R6  exposed material as sealed evidence: TRIGGERED for D2
R7  lineage collapse: OPEN with BIG-bench related task
R8  overlap not investigated: OPEN until panel overlap audit
R9  license/access unresolved: PASS for official repo license
R10 answer-key leakage: HIGH
R11 capability mismatch: experiment-design dependent
R12 runtime failure collapse: adapter dependent
R13 prompt pseudoreplication: experiment-design dependent
R14 mutable benchmark without snapshot: revision pin required
R15 post-hoc exclusions: Gate 2 dependent
R16 denominator gaming: HIGH RISK if truthfulness-only headline used
R17 insufficient measurement resolution: D0 required
R18 hidden benchmark transformation: adapter review required
```

---

# 11. Final decision

```yaml
benchmark_id: truthfulqa
review_status: COMPLETE_WITH_OPEN_RISKS
primary_eligible: true
primary_scope:
  - FALSE_PREMISE
  - MISCONCEPTION_RESISTANCE
  - TRUTHFUL_GENERATION
best_roles:
  - D0_MEASUREMENT_DEVELOPMENT
  - D1_CONTROL_DISCOVERY
sealed_d2_role: NOT_ELIGIBLE_BY_DEFAULT
critical_risks:
  - public contamination
  - truthfulness-only refusal gaming
  - unavailable historical GPT judge
  - generation and multiple-choice construct mismatch
  - relation to BIG-bench variant
```

## Bottom line

TruthfulQA belongs in the AHP panel as a targeted ruler for misconception-induced falsehoods and premise correction.

It should not define broad knowledge reliability, and its truthfulness score must never be interpreted without an informativeness/usefulness constraint.
