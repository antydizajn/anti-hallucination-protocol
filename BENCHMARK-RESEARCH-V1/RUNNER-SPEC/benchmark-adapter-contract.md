# Benchmark Adapter Contract v1

## Status

Normative runner specification.

An adapter is the only permitted bridge between an external benchmark and the AHP runner.

The adapter MUST preserve the benchmark's construct. It may normalize representation, but it may not silently redefine what counts as success.

## 1. Core rule

```text
BENCHMARK SOURCE != ADAPTER != RUNNER != EVALUATOR
```

Each layer has separate identity, revision and failure modes.

## 2. Required adapter identity

Every adapter MUST declare:

```yaml
adapter_id: string
adapter_version: semver
benchmark_id: registry id
benchmark_revision: string
source_revision: string | null
adapter_source_hash: string
created_on: ISO-8601 date
```

The benchmark id MUST exist in `REGISTRY/benchmark-registry.yaml`.

If `runner_allowed` is false, confirmatory execution MUST fail closed.

## 3. Required construct mapping

Each adapter MUST explicitly state:

```yaml
construct:
  source_construct: string
  ahp_layer: string
  primary_endpoint: string
  guardrail_endpoints: [string]
  evaluation_unit: ITEM | TRACE | SESSION
  tool_mode: NONE | PROVIDED_CONTEXT | SEARCH | TOOL_ENVIRONMENT | MIXED
```

A benchmark cannot be selected merely because its title contains `hallucination`, `factuality`, `agent` or `truth`.

## 4. Dataset pinning

The adapter MUST pin the exact evaluated material where technically possible:

```yaml
dataset:
  source: string
  revision: string
  split: string
  content_hash: string | null
  snapshot_date: ISO-8601 date | null
  item_count_expected: integer | null
```

Mutable aliases such as `latest`, an unpinned branch, or an unversioned web endpoint are not sufficient for confirmatory runs unless the construct is explicitly live/dynamic.

Dynamic benchmarks MUST record the observation snapshot and date for each run.

## 5. Prompt preservation

The adapter MUST separate:

```text
SOURCE PROMPT
NORMALIZATION
TREATMENT INJECTION
MODEL RESPONSE
```

A benchmark adapter may normalize encoding, field names and transport format.

It MUST NOT silently:

- rewrite the semantic task;
- add hints about the answer;
- add AHP-specific attack labels to CONTROL;
- delete ambiguity that is part of the construct;
- add ambiguity not present in the source;
- change tool permissions differently across matched arms.

Any benchmark-specific prompt transformation requires a declared transformation id and rationale.

## 6. Gold boundary

Gold data MUST remain logically separate from model-visible input unless the benchmark construct explicitly provides reference material to the model.

Required fields:

```yaml
gold:
  visibility_to_model: NONE | PARTIAL | FULL | CONSTRUCT_DEFINED
  answer_type: EXACT | SET | RANGE | STRUCTURED | RUBRIC | REFERENCE_WORLD | NONE
  source: string | null
```

A judge seeing the answer key is permitted only when `EVALUATOR-POLICY.md` allows it and the visibility is recorded.

## 7. Tool contract

For tool-enabled benchmarks the adapter MUST declare:

```yaml
tools:
  required: true | false
  definitions_hash: string | null
  permission_profile: string
  retrieval_budget: object | null
  live_or_frozen: LIVE | FROZEN_SNAPSHOT | SIMULATED_REFERENCE_WORLD | NONE
```

Matched CONTROL and AHP arms MUST receive the same tool capability unless the research question explicitly studies a tool-capability intervention.

## 8. Input item contract

Canonical runner item:

```yaml
item_id: string
benchmark_id: string
source_item_id: string | null
prompt:
  messages: array
  raw_source: object | string | null
context:
  provided_evidence: array
  observation_time: ISO-8601 | null
gold:
  answer: object | null
  answerability: ANSWERABLE | UNANSWERABLE | CONDITIONAL | UNKNOWN
metadata:
  domain: string | null
  topic: string | null
  difficulty: string | null
  exposure_class: string
```

Benchmark-specific metadata may be added under `metadata.source_specific`.

## 9. Output normalization

The adapter may normalize provider output into:

```yaml
response:
  text: string | null
  structured_output: object | null
  citations: array
  declared_confidence: number | null
  tool_calls: array
```

Provider refusal, empty content, API error and timeout MUST remain distinct.

## 10. Abstention mapping

The adapter MUST NOT use source benchmark `NOT_ATTEMPTED` or similar labels as a direct synonym for `ABSTAIN_CLEAN` without validating the source semantics.

If source grading allows speculative candidates inside a not-attempted answer, the AHP adapter MUST preserve the distinction:

```text
ABSTAIN_CLEAN
ABSTAIN_SPECULATIVE
```

## 11. Partial credit

If the source benchmark supports partial answers, the adapter MUST define the exact mapping.

If it does not, do not invent universal 0.5 weighting.

`PARTIAL` is a categorical outcome unless a benchmark-specific, predeclared numeric score exists.

## 12. Numeric tolerance

All tolerances MUST be explicit and deterministic where possible:

```yaml
numeric_tolerance:
  mode: EXACT | ABSOLUTE | RELATIVE | SOURCE_DEFINED | NONE
  value: number | null
```

A judge MUST NOT decide tolerance ad hoc from prose examples.

## 13. Citation mapping

Citation benchmarks MUST preserve at least:

```text
CLAIM
CITATION IDENTITY
CITATION TARGET
EVIDENCE SPAN, if available
```

Citation existence alone cannot map to support.

## 14. Reference-world mapping

Reference-world adapters MUST expose evaluator-accessible world state while preventing unauthorized leakage into the model input.

Required:

```yaml
reference_world:
  world_revision: string
  initial_state_hash: string
  state_transition_log: string | null
  evaluator_predicate_revision: string
```

## 15. Multi-turn mapping

Multi-turn benchmarks MUST preserve session boundaries and turn dependencies.

Canonical fields:

```yaml
sequence:
  sequence_id: string
  turn_index: integer
  depends_on: [item_id]
  terminal_turn: true | false
```

Dependent turns are not independent experimental replications.

## 16. Contamination mapping

Every adapter MUST populate the fields required by `CONTAMINATION-POLICY.md`.

At minimum:

```yaml
exposure:
  data_class: string
  model_exposure: string
  treatment_exposure: string
  attack_class_documented_in_treatment: true | false | unknown
  surface_form_documented_in_treatment: true | false | unknown
```

Unknown stays unknown.

## 17. Evaluator mapping

Each adapter MUST declare exactly how source labels map to AHP scoring outcomes.

Required artifact:

```text
SOURCE LABEL -> AHP OUTCOME mapping table
```

Any unmapped source label MUST fail scoring rather than default to incorrect, abstain or pass.

## 18. Runtime failures

Adapter exceptions MUST map to runtime/evaluator channels, not task outcomes.

Examples:

```text
failed dataset parse -> HARNESS_ERROR
missing source artifact -> ENVIRONMENT_ERROR
judge timeout -> EVALUATOR_ERROR
model timeout -> MODEL_TIMEOUT
required tool timeout -> TOOL_ERROR
```

## 19. Adapter self-tests

Every runnable adapter MUST ship tests for at least:

```text
known correct answer
known incorrect answer
clean abstention, if applicable
speculative abstention, if applicable
runtime error preservation
unknown source label rejection
item count or split sanity
hash/revision pinning
CONTROL/AHP prompt equality before treatment injection
```

Tool-enabled adapters also require:

```text
tool error preservation
empty-valid-result distinction
trace capture
permission parity across arms
```

## 20. Degenerate policy probe

Before promotion to confirmatory-ready, the adapter MUST be tested against relevant degenerate baselines defined in `SCORING-CONTRACT.md`.

The result is an adapter validation artifact, not a model benchmark result.

## 21. Adapter review states

```text
DRAFT
SOURCE_MAPPED
SCORER_MAPPED
SELF_TESTED
PILOT_READY
CONFIRMATORY_READY
SUSPENDED
```

Promotion to `CONFIRMATORY_READY` requires:

```text
registry PRIMARY_VERIFIED
runner_allowed true
source revision pinned
construct reviewed
scorer reviewed
contamination fields mapped
self-tests pass
pilot does not reveal a structural scorer defect
```

## 22. No hidden semantics

The runner MUST NOT contain benchmark-specific scoring logic outside the adapter except shared primitives explicitly versioned in the scoring library.

If benchmark `X` requires a special rule, that rule belongs in adapter `X` or a declared shared primitive referenced by adapter `X`.

## 23. Adapter manifest example

```yaml
adapter_id: simpleqa-verified-v1
adapter_version: 1.0.0
benchmark_id: simpleqa-verified
benchmark_revision: "paper/dataset pinned revision"
source_revision: "source identifier"
adapter_source_hash: "sha256:..."
construct:
  source_construct: reconciled_short_form_factuality
  ahp_layer: PARAMETRIC_KNOWLEDGE
  primary_endpoint: incorrect_attempt_rate
  guardrail_endpoints: [correct_coverage, unnecessary_abstention_rate]
  evaluation_unit: ITEM
  tool_mode: NONE
dataset:
  source: "official source"
  revision: "pinned"
  split: test
  content_hash: "sha256:..."
  snapshot_date: null
  item_count_expected: 1000
```

## 24. Non-collapse invariants

```text
ADAPTER_RUNS != ADAPTER_IS_VALID
SOURCE_LABEL != AHP_LABEL_UNLESS_MAPPED
NOT_ATTEMPTED != CLEAN_ABSTENTION_BY_DEFAULT
DATASET_URL != DATASET_REVISION
PROMPT_NORMALIZATION != SEMANTIC_REWRITE
PROVIDER_EMPTY_OUTPUT != ABSTENTION
TOOL_ERROR != EMPTY_VALID_RESULT
ITEM_COUNT != INDEPENDENT_REPLICATION_COUNT
```
