# AHP Benchmark Contamination Policy v1

## Status

Normative research specification.

A benchmark result is only as strong as its contamination accounting. This policy treats contamination as a typed validity threat rather than a binary yes/no flag.

## 1. Data classes

Every benchmark item MUST belong to exactly one publication/exposure class:

```text
PUBLIC_REPRODUCIBLE
ROTATING_DYNAMIC
PRIVATE_CONFIRMATORY
```

### PUBLIC_REPRODUCIBLE

Public prompts, answers, datasets or generation rules that may have been observed during pretraining, post-training, evaluation tuning, prompt development or manual experimentation.

Public data is valuable for reproducibility but MUST NOT be described as unseen evidence.

### ROTATING_DYNAMIC

Items generated or refreshed after a declared observation date using a frozen generator and validation process. Dynamic does not automatically mean uncontaminated. The exact snapshot, generator revision and observation date must be preserved.

### PRIVATE_CONFIRMATORY

A frozen confirmatory set whose item contents and answer keys have not been exposed to the evaluated treatment or model-development workflow to the extent operationally knowable.

Private confirmatory data must be hashed before collection begins. Publication after the confirmatory run permanently changes its future exposure class.

## 2. Contamination dimensions

Record these independently.

```text
MODEL_EXPOSURE
TREATMENT_EXPOSURE
EVALUATOR_EXPOSURE
OPERATOR_EXPOSURE
RUNTIME_CARRYOVER
SOURCE_DRIFT
TOOL_CACHE
```

A single `contaminated: true|false` field is insufficient.

## 3. Model exposure

Possible states:

```text
KNOWN_UNSEEN
LIKELY_UNSEEN
UNKNOWN
LIKELY_EXPOSED
KNOWN_EXPOSED
```

For closed models, training-set exposure is normally `UNKNOWN` unless the provider gives evidence sufficient to say more.

Never convert `UNKNOWN` to `UNSEEN`.

Public benchmark publication before a model's training cutoff is a contamination risk, not proof of memorization.

## 4. Treatment exposure

This dimension is critical for AHP.

A benchmark item is treatment-exposed when the AHP material supplied to the treatment arm contains any of:

- the exact item;
- a near-duplicate surface form;
- the expected answer;
- the tested attack class plus a worked response sufficiently specific to reveal the intended behavior;
- a decision rule that effectively encodes the answer for that case.

Required states:

```text
UNSEEN_CLASS
CLASS_DESCRIBED
SURFACE_SIMILAR
NEAR_DUPLICATE
EXACT_EXPOSURE
UNKNOWN
```

`CLASS_DESCRIBED` is not automatically invalid. It tests protocol compliance. It is, however, weaker evidence of generalization.

Headline confirmatory generalization claims require an `UNSEEN_CLASS` or otherwise independently authored holdout subset.

## 5. Seen/unseen split

Every AHP-native battery should explicitly tag:

```text
attack_class_documented_in_treatment: true|false
surface_form_documented_in_treatment: true|false
answer_pattern_documented_in_treatment: true|false
```

Results must be reported separately for treatment-seen and treatment-unseen strata.

Do not average them first and show only the average.

## 6. Treatment-size and structure confounds

AHP vs control comparisons can be confounded by prompt length, formatting, examples, directory contents or unrelated instructions.

Every run MUST record what was actually injected into model context, including where observable:

```text
instruction_bytes
instruction_tokens
number_of_files_visible
number_of_examples_visible
skill_or_policy_revision
skill_or_policy_blob_hash
```

For causal attribution studies, include matched placebos or ablations where feasible:

```text
CONTROL
AHP
MATCHED_LENGTH_PLACEBO
RULES_ONLY
EXAMPLES_ONLY
```

These are optional for ordinary effectiveness evaluation but required before strong component-level causal claims.

## 7. Evaluator exposure

LLM judges may themselves have memorized public benchmarks or expected labels.

Record:

```text
judge_model
judge_revision
judge_prompt_hash
benchmark_visibility
answer_key_visibility
```

A judge that sees the gold answer is an answer-key evaluator, not an independent fact checker. That is permitted when predeclared, but it must be labeled.

Private confirmatory items should avoid exposing the complete gold corpus to a single mutable external service when a deterministic or structured scorer is possible.

## 8. Operator exposure

Human operators can leak condition identity or expected behavior through interventions.

Record:

```text
operator_blinded_to_condition
operator_blinded_to_gold
manual_intervention_count
manual_intervention_reason
```

Manual rescue of one arm but not another invalidates matched comparison unless the intervention itself is part of the preregistered protocol.

## 9. Runtime carryover

Cross-arm state can leak through:

- conversation history;
- memory stores;
- caches;
- environment files;
- shell history;
- vector databases;
- browser state;
- tool-side sessions;
- provider-side prompt caching where observable;
- reused agent profiles.

Every independent replication must initialize the declared state boundary from scratch or demonstrate equivalence to a fresh state.

`new chat` alone is not proof of runtime isolation.

## 10. Tool and retrieval cache contamination

Search and tool benchmarks must record whether retrieved content came from:

```text
LIVE
FROZEN_SNAPSHOT
CACHE
SIMULATED_REFERENCE_WORLD
```

If caching is used, cache identity/hash belongs in the run manifest.

A cached result from an earlier arm cannot silently become evidence for a later arm.

## 11. Source drift

Dynamic web evidence changes.

For every load-bearing external observation preserve when feasible:

```text
observation_timestamp
source_identity
source_revision_or_hash
retrieved_content_hash
query_or_tool_arguments
```

A later rerun against changed web content is a new observation, not a reproduction of the original evidence state.

## 12. Temporal leakage

Dynamic benchmarks such as current-world QA require explicit dates:

```text
benchmark_snapshot_date
question_valid_from
question_valid_until, if known
model_knowledge_cutoff, if known
run_observation_date
```

The benchmark must distinguish:

- old fact answered from memory;
- genuinely current fact;
- fact that changed after model training;
- false premise that must be rejected.

## 13. Prompt development leakage

Items used while writing or tuning AHP cannot later be promoted into private confirmatory evidence.

Maintain lifecycle states:

```text
DISCOVERY
DEVELOPMENT
PILOT
PUBLIC_REGRESSION
PRIVATE_CONFIRMATORY
RETIRED
```

An item can move toward greater exposure but never back toward secrecy.

Example forbidden transition:

```text
PUBLIC_REGRESSION -> PRIVATE_CONFIRMATORY
```

## 14. Near-duplicate control

Exact-string deduplication is insufficient.

Before freezing private confirmatory data, compare against:

- AHP documentation;
- examples;
- adversarial case files;
- public regression tests;
- previous benchmark prompts;
- public issues and audit reports.

Use lexical and semantic duplicate checks. Suspected near-duplicates are quarantined for human adjudication.

## 15. Attack-class leakage

For protocol evaluation, semantic class leakage is a first-class variable.

Example:

```text
Treatment documentation says:
'Tool errors must remain ERROR and must not be reported as NOT_FOUND.'

Benchmark asks:
'The search API timed out. Tell me that nothing exists.'
```

This is a valid compliance test but weak evidence that the protocol generalized to a novel failure mechanism.

The registry must therefore distinguish:

```text
COMPLIANCE_CASE
GENERALIZATION_CASE
```

## 16. Public benchmark policy

Public benchmark results are useful for:

- reproducibility;
- comparison to published literature;
- regression testing;
- external construct coverage.

They are not sufficient by themselves for:

- unseen generalization claims;
- contamination-free effect claims;
- proof that the protocol handles novel attacks.

## 17. Confirmatory freeze

Before confirmatory collection, freeze and hash:

```text
benchmark manifest
private item bundle
scoring contract
primary endpoints
evaluator prompts
arm definitions
allocation schedule
exclusion rules
analysis plan
```

No semantic changes after inspecting confirmatory outcomes. Corrections require a new benchmark revision and a new confirmatory run.

## 18. Invalidation rules

A paired result is invalid for causal treatment comparison if any of the following is material and unresolved:

```text
DIFFERENT_MODEL_REVISION
DIFFERENT_PROVIDER_ROUTE
DIFFERENT_TOOL_PERMISSIONS
CROSS_ARM_MEMORY_LEAK
GOLD_ANSWER_LEAK_TO_ONE_ARM
TREATMENT_MISSING_OR_NOT_LOADED
CONTROL_ACCIDENTALLY_LOADS_TREATMENT
UNRECORDED_MANUAL_INTERVENTION
MUTATED_PRIVATE_ITEMS_AFTER_OUTCOME_REVIEW
RUNTIME_FAILURE_CLASSIFIED_AS_ABSTENTION
```

Invalid does not mean delete. Preserve the trace and label it invalid for the intended inference.

## 19. Required contamination manifest

Each run must emit at minimum:

```yaml
exposure:
  data_class: PUBLIC_REPRODUCIBLE | ROTATING_DYNAMIC | PRIVATE_CONFIRMATORY
  model_exposure: UNKNOWN
  treatment_exposure: UNSEEN_CLASS | CLASS_DESCRIBED | SURFACE_SIMILAR | NEAR_DUPLICATE | EXACT_EXPOSURE | UNKNOWN
  evaluator_exposure: UNKNOWN
  operator_exposure: KNOWN | UNKNOWN
runtime:
  fresh_state_verified: true | false | unknown
  cache_mode: LIVE | FROZEN_SNAPSHOT | CACHE | SIMULATED_REFERENCE_WORLD
source:
  observation_time: ISO-8601
  snapshot_or_hash: string | null
```

## 20. Non-collapse invariants

```text
PUBLIC != HELD_OUT
DYNAMIC != UNCONTAMINATED
UNKNOWN_EXPOSURE != UNSEEN
CLASS_DESCRIBED != NOVEL_GENERALIZATION
NEW_CHAT != CLEAN_RUNTIME
SAME_URL != SAME_WEB_EVIDENCE
NO_EXACT_DUPLICATE != NO_SEMANTIC_LEAKAGE
PRIVATE_FILENAME != PRIVATE_CONTENT
```
