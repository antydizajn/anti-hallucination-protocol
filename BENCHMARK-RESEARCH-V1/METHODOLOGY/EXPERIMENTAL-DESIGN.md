# AHP Experimental Design v1

## Status

Normative research specification for future pilots and confirmatory studies. This document does not claim any AHP effect.

## 1. Research question

Primary question:

> Does loading AHP improve how a model matches claim and action strength to the actual state of available evidence without collapsing into unnecessary refusal, ceremony or tool use?

This question is intentionally stronger than `does AHP reduce wrong answers?` because a degenerate always-abstain policy can reduce wrong answers while becoming less useful.

## 2. No universal A/B/C experiment

Different benchmark families require different matched conditions.

A global three-arm experiment imposed on every benchmark is rejected because it creates irrelevant arms and can confound protocol version with prompt length, tools and runtime state.

## 3. Core treatment conditions

### Effectiveness pair

```text
CONTROL
AHP_CURRENT
```

These are the default matched conditions for the primary effectiveness question.

### Optional causal diagnostics

```text
MATCHED_LENGTH_PLACEBO
RULES_ONLY
EXAMPLES_ONLY
AHP_LEGACY
```

These answer separate questions and must not be silently mixed into the primary endpoint.

`AHP_LEGACY` is historical comparison, not a necessary control.

## 4. Closed-book design

Use for:

- AA-Omniscience;
- SimpleQA Verified;
- FACTS Parametric;
- selected abstention tasks where tools would violate the construct.

Conditions:

```text
CONTROL, NO_TOOLS
AHP_CURRENT, NO_TOOLS
```

Held constant:

- model exact revision;
- provider route;
- sampling parameters;
- system/runtime scaffolding except treatment;
- maximum output budget;
- prompt surface;
- tool availability: none.

Expected possible AHP effect:

- lower unsupported guessing;
- improved selective behavior;
- cleaner abstention.

Not an expected AHP effect:

- magical increase in parametric factual memory.

Mandatory guardrail:

- correct coverage / unnecessary abstention.

## 5. Search and grounding design

Use for:

- FreshQA search condition;
- SealQA;
- FACTS Search;
- FACTS Grounding;
- FaithEval;
- RGB;
- RAGuard-like misleading evidence tests.

Conditions:

```text
CONTROL + SAME_TOOLS
AHP_CURRENT + SAME_TOOLS
```

Tool definitions, search backend, retrieval budget and permissions must be identical.

Measure separately:

```text
ACQUISITION
SELECTION
EVIDENCE_BINDING
CONFLICT_HANDLING
FINAL_CLAIM_STRENGTH
```

A final wrong answer does not reveal which stage failed.

## 6. Tool-reliability design

Use deterministic or reference-world tools where possible.

Factorial stimuli:

```text
TOOL_REQUIRED
TOOL_NOT_REQUIRED
```

crossed with:

```text
CLEAN_RESULT
EXECUTION_ERROR
EMPTY_VALID_RESULT
STALE_RESULT
MALFORMED_RESULT
CONFLICTING_RESULTS
```

crossed with:

```text
CONTROL
AHP_CURRENT
```

Critical distinctions:

```text
TOOL_ERROR != EMPTY_VALID_RESULT
TOOL_CALLED != RESULT_USED
RESULT_USED != RESULT_REPORTED_FAITHFULLY
```

## 7. Adversarial evidence design

Factor:

```text
CLEAN
NOISY
CONFLICTING
MISLEADING
PROMPT_INJECTED
```

Cross with:

```text
CONTROL
AHP_CURRENT
```

Where a security benchmark includes destructive or external actions, execute only in sandboxed/simulated environments appropriate to that benchmark.

## 8. AHP-native transition design

This is the mechanistic core.

Each base case defines an initial evidence state `E0`. The model produces response/state `R0`. Then only one variable changes.

Stimulus families:

```text
NO_NEW_EVIDENCE
USER_PRESSURE
REPEATED_ASSERTION
WEAK_NEW_EVIDENCE
MATERIAL_COUNTEREVIDENCE
DECISIVE_NEW_EVIDENCE
FRESHER_DIRECT_OBSERVATION
TOOL_ERROR
```

Expected transition examples:

```text
INCONCLUSIVE + USER_PRESSURE -> remain INCONCLUSIVE
INCONCLUSIVE + REPEATED_ASSERTION -> remain INCONCLUSIVE
INCONCLUSIVE + DECISIVE_NEW_EVIDENCE -> justified upgrade
SUPPORTED + MATERIAL_COUNTEREVIDENCE -> justified downgrade/conflict
UNKNOWN + TOOL_ERROR -> ERROR/UNKNOWN, not certainty
STALE_SUPPORT + FRESHER_DIRECT_OBSERVATION -> bind fresher evidence
```

The evaluation target is evidence responsiveness, not stubbornness.

## 9. Paired positive twins

For every family dominated by downgrade/abstention cases, create positive twins where evidence is sufficient and a scoped affirmative answer is required.

Example pair:

```text
A: deployment command printed, not executed -> must not claim deployed
B: deployment executed and externally observed healthy -> should claim deployed with scope
```

A generic refusal must fail B.

Target for AHP-native confirmatory subsets:

- approximately balanced consequential downgrade and justified-upgrade opportunities where construct permits;
- enough benign controls to estimate ceremony cost.

## 10. Negative controls

Include harmless tasks where verification is unnecessary.

Examples:

- creative wording;
- preference transformation;
- formatting;
- deterministic local calculation already fully specified;
- low-risk summarization of supplied text.

Measure unnecessary verification/tool use/refusal.

AHP must be able to lose on these metrics.

## 11. Degenerate baselines

Before calling a battery discriminative, test where technically meaningful:

```text
ALWAYS_ABSTAIN
ALWAYS_ANSWER
ALWAYS_USE_TOOL
NEVER_USE_TOOL
COPY_CONTEXT
```

A battery is not confirmatory-ready if a trivial policy dominates its intended primary endpoint without an obvious guardrail failure.

## 12. Replication unit

Definitions follow `SCORING-CONTRACT.md`.

For AHP treatment effects:

```text
PRIMARY INDEPENDENT UNIT = independently initialized PAIRED_BLOCK
```

A paired block contains matched CONTROL and AHP_CURRENT executions under a shared frozen benchmark/runtime configuration.

Prompts nested in the same session are repeated observations, not independent replications.

## 13. Freshness and state reset

Each independent paired block must begin from a declared fresh-state boundary.

At minimum verify where applicable:

```text
new agent/profile/process
empty conversation state
memory disabled or reset
neutral working directory
no cross-arm fixture mutation
no cross-arm browser/tool session
identical tool permissions
identical environment variables except treatment-specific identifiers
```

If provider-side state cannot be controlled, record it as an external limitation.

## 14. Arm order

CONTROL must not always run first.

For two-arm effectiveness studies, counterbalance across replications:

```text
AB
BA
```

For three conditions, use a balanced Latin-square or all six permutations when feasible:

```text
ABC
BCA
CAB
ACB
CBA
BAC
```

Condition order assignment is frozen before outcomes are inspected.

## 15. Item order

Independent items may be randomized using a stored seed.

Dependent multi-turn sequences must preserve declared prerequisites.

Represent dependencies explicitly as a DAG rather than relying on undocumented hard-coded order.

If a long-session construct requires fixed position, record position as part of the construct and analyze it as such.

## 16. Long-session design

Hallucination can emerge from state accumulation.

Evaluate at least conceptually distinct checkpoints:

```text
FRESH
AFTER_20_TURNS
AFTER_50_TURNS
POST_COMPACTION
POST_RESTART_WITH_DURABLE_STATE
```

Do not reset after every case when the research question is long-session drift.

Do not treat checkpoint cases within one session as independent replications.

## 17. Randomization record

Every run manifest must contain:

```yaml
allocation:
  replication_id: string
  arm_order: [CONTROL, AHP_CURRENT]
  arm_order_seed: integer | null
  item_order_seed: integer | null
  sequence_variant: string | null
```

Reproduction requires the allocation, not only the final transcript.

## 18. Blinding

Where feasible:

- evaluator should be blind to condition identity;
- human adjudicator should be blind to model identity and treatment;
- model obviously cannot be blind to treatment instructions.

Do not put `AHP should answer X` metadata into judge-visible traces.

## 19. Evaluator hierarchy

Use the least subjective sufficient evaluator:

```text
1 deterministic rule
2 normalized exact/structured match
3 executable/reference-world state check
4 claim decomposition + evidence verification
5 validated specialist model
6 multiple independent judges
7 human adjudication
```

LLM judge convenience is not a reason to skip deterministic scoring.

## 20. Judge disagreement

For rubric cases, preserve judge outputs independently.

Do not majority-vote away systematic disagreement without recording it.

Required outputs:

```text
agreement rate
pairwise agreement
adjudicated count
evaluator error count
```

Evaluator reliability must itself be validated on a human-labeled or deterministic corpus before confirmatory deployment.

## 21. Pilot stage

Purpose:

- verify isolation;
- discover ambiguous items;
- estimate variance;
- test degenerate baselines;
- test scorer reliability;
- detect ceiling/floor effects;
- estimate runtime/cost.

Pilot data can modify the design but then becomes development-exposed.

Pilot data does not count toward the frozen private confirmatory result unless that inclusion rule was fixed before pilot inspection, which is generally discouraged.

## 22. Confirmatory preregistration

Freeze before collection:

```text
hypothesis
benchmark revision
private holdout hash
conditions
primary endpoint per layer
guardrails
smallest effect of practical interest where defensible
replication unit
sample/replication plan
arm-order schedule
item-order rules
exclusion rules
invalidation rules
evaluator versions/prompts
analysis script hash
multiple-comparison correction
```

## 23. Statistical analysis

Prefer paired analyses because CONTROL and AHP_CURRENT share the same item/configuration block.

Report:

- raw counts;
- paired effect estimates;
- uncertainty intervals;
- per-replication distributions;
- guardrail changes.

For confirmatory secondary endpoint families, predeclare a correction such as Holm or Benjamini-Hochberg depending on the inferential goal.

Do not select the correction after seeing which one makes a result significant.

## 24. Heterogeneity

Do not hide model-specific effects behind one mean.

Stratify at minimum by:

```text
MODEL
BENCHMARK_LAYER
TOOL_MODE
EXPOSURE_CLASS
SEEN_VS_UNSEEN_ATTACK_CLASS
```

AHP may help one model family and harm another. That is a valid result.

## 25. Provider and model drift

Cloud model aliases can move.

Record exact provider-reported revision when available plus observation date.

If the provider silently changes the model during collection, split the experiment into separate runtime epochs or invalidate the affected comparison.

## 26. Treatment integrity

For every AHP arm verify both identity and actual loading.

Required distinctions:

```text
INSTALLED
DISCOVERABLE
INJECTED_IN_CONTEXT
BEHAVIORALLY_ACTIVE
```

A file existing on disk is not proof that the model saw it.

The run manifest should preserve treatment blob/hash and injected token count where observable.

## 27. Control integrity

CONTROL must not gain AHP through:

- local skills;
- memory;
- copied system prompts;
- context files;
- benchmark instructions that teach the answer;
- prior conversation carryover.

Verify the control boundary, do not assume it.

## 28. Public vs private evidence

Final reporting should have separate sections:

```text
PUBLIC REPRODUCIBLE RESULTS
ROTATING/DYNAMIC RESULTS
PRIVATE CONFIRMATORY RESULTS
```

Do not blend these into one unlabeled pooled score.

## 29. Valid conclusions

The experimental framework must allow all of these outcomes:

```text
AHP HELPS ON THIS LAYER
NO DETECTABLE EFFECT
AHP HARMS ON THIS LAYER
MIXED TRADEOFF
EVALUATION INCONCLUSIVE
RUNTIME INVALID
```

A benchmark architecture that cannot return `AHP HARMS` is not a scientific evaluation.

## 30. Forbidden inference shortcuts

```text
LOWER HALLUCINATION RATE -> AHP BETTER, without checking coverage
MORE ABSTENTION -> BETTER CALIBRATION
PUBLIC BENCHMARK -> UNSEEN TEST
ONE LONG SESSION -> MANY INDEPENDENT REPLICATIONS
AHP FILE PRESENT -> AHP LOADED
TOOL CALL SUCCEEDED -> ANSWER GROUNDED
JUDGE SAID PASS -> GROUND TRUTH
THREE MODELS IMPROVED -> UNIVERSAL EFFECT
NO SIGNIFICANCE -> PROOF OF NO EFFECT
```
