# Gate 1 Benchmark Rejection Rules

## Status

Normative Gate 1 exclusion policy.

A benchmark can be scientifically useful and still be rejected from the primary candidate pool.

Rejection means:

```text
NOT ELIGIBLE FOR THE CLAIM ROLE REQUESTED
```

not:

```text
BAD BENCHMARK IN GENERAL
```

## 1. Automatic primary rejection

A candidate is rejected from `PRIMARY_ELIGIBLE` if any of the following is true.

### R1 - construct mismatch

The benchmark's actual construct does not measure the target axis it is being proposed for.

Examples:

- hallucination detector accuracy proposed as direct prevention evidence;
- generic reasoning benchmark proposed as factuality evidence;
- citation-existence metric proposed as citation-entailment evidence;
- context-faithfulness benchmark proposed as world-truth benchmark.

Disposition:

```text
SECONDARY_ONLY or REJECT
```

### R2 - no operational scoring boundary

Reject if the project cannot define before treatment results:

- eligible items;
- answerability class;
- success/failure mapping;
- partial-credit rule;
- abstention mapping;
- runtime-failure mapping.

Unknown or unresolved labels must not be silently coerced.

### R3 - degenerate-policy exploit

Reject or repair if a trivial policy can score as a strong system on the intended endpoint without failing a hard guardrail.

Mandatory probes where relevant:

```text
ALWAYS_ABSTAIN
ALWAYS_ANSWER
KEYWORD_OR_SURFACE_HEURISTIC
RANDOM_POLICY
ALWAYS_TOOL
NEVER_TOOL
COPY_CONTEXT
```

If a shallow policy wins through lexical artifacts, benchmark prevalence, or scoring asymmetry, primary admission is blocked.

### R4 - positive-evidence absence

A benchmark dominated by should-abstain cases cannot serve as the sole primary instrument for an abstention-sensitive AHP claim if it lacks cases where proceeding/answering is clearly warranted.

Reason:

```text
LOWER ERROR RATE MAY BE PURE REFUSAL INFLATION
```

### R5 - grader not auditable

Reject from primary if grading materially depends on a component whose identity or behavior cannot be adequately fixed or validated.

Examples:

- moving unversioned LLM judge as sole grader;
- inaccessible judge prompt;
- unresolved label mapping;
- grader-human agreement below the preregistered threshold;
- systematic arm-style bias;
- material run-to-run instability that exceeds the measurement contract.

### R6 - public/exposed material proposed as sealed promotion evidence

Any item-level material already inspected by intervention designers cannot be `D2_CONFIRMATORY_CANDIDATE` for that intervention lineage.

Public static benchmark items known to the design team default to development or secondary comparability roles.

Exact-string novelty is insufficient if the benchmark recipe, answerability cues, attack ontology, grader behavior or lineage already informed the treatment.

### R7 - lineage collapse

A set of benchmark names does not become multiple independent lines of evidence when they share a load-bearing source lineage.

Primary diversity cannot be satisfied by relabeling:

- the same upstream dataset;
- the same transformed questions;
- the same synthetic generator;
- the same answer key;
- the same benchmark-construction recipe;
- the same evaluator;
- the same attack ontology.

Shared lineage must be recorded and counted accordingly.

### R8 - overlap not investigated

No candidate enters primary status while `overlap_status = NOT_CHECKED` when raw data access permits overlap analysis.

At minimum check where possible:

```text
normalized exact duplicate
normalized n-gram similarity
near-duplicate candidate signal
source URL overlap
answer overlap
upstream-dataset overlap
generation-pipeline overlap
```

Semantic similarity is a signal, not proof of leakage.

### R9 - license or access unresolved

Primary admission requires the intended use to be legally and operationally possible.

Reject or defer if:

- license is unknown;
- intended redistribution is prohibited but required by the design;
- private evaluation cannot actually be executed;
- benchmark terms conflict with intended automation;
- required source artifacts are unavailable.

### R10 - answer-key leakage into treatment

Reject a confirmatory assignment when treatment material directly or functionally describes the tested attack class, answer pattern or expected response at a level that makes efficacy versus answer-key leakage inseparable.

Seen-class and unseen-class results may be retained as development diagnostics, but not pooled into an unlabeled confirmatory headline.

### R11 - treatment/control capability mismatch

A benchmark comparison is not primary-eligible when CONTROL and TREATMENT differ in capabilities unrelated to the hypothesized mechanism.

Examples:

- different tool availability;
- different retrieval budget;
- different model revision;
- different context window policy;
- different system scaffolding beyond treatment;
- different session isolation.

If prompt/context footprint itself is a plausible cause, a matched placebo or other causal diagnostic is required before mechanism attribution.

### R12 - runtime failure collapse

Reject scoring implementations that map:

```text
MODEL_TIMEOUT -> ABSTAIN
TOOL_ERROR -> NOT_FOUND
HARNESS_ERROR -> INCORRECT
EMPTY_PROVIDER_OUTPUT -> CLEAN_REFUSAL
EVALUATOR_ERROR -> MODEL_FAILURE
```

Runtime and evaluator channels remain separate.

### R13 - prompt-level pseudoreplication

Reject inferential plans that use prompt rows nested inside persistent sessions as independent randomized units.

Primary causal inference requires independent fresh sessions or matched blocks of independent sessions.

### R14 - mutable dynamic benchmark without snapshot contract

Dynamic/live instruments require observation time, revision/snapshot identity, and reproducible capture where the benchmark allows it.

A mutable `latest` endpoint with no frozen run record cannot support a reconstructable confirmatory result.

### R15 - unbounded post-hoc exclusions

Reject any proposed primary use if exclusions may be invented after arm outcomes are visible.

Exclusion and invalidation rules belong in Gate 2.

### R16 - metric gaming through denominator control

Reject endpoints where the evaluated model can improve its score simply by shrinking the denominator through selective refusal or selective output omission unless that behavior is explicitly penalized by the metric contract.

Examples:

```text
accuracy among attempted only
citation precision with no citation-coverage floor
hallucination among answered only
```

### R17 - benchmark too noisy for the declared SESOI

A benchmark or grader that cannot resolve the smallest effect of scientific interest within the preregistered resource ceiling cannot be a primary confirmatory instrument for that effect.

Disposition:

```text
MEASUREMENT_INADEQUATE or SECONDARY_ONLY
```

Do not increase the meaningful-effect threshold after learning that the ruler is too noisy.

### R18 - hidden benchmark transformation

Reject if the adapter materially rewrites the source task without an explicit transformation contract.

Normalization is allowed.
Semantic task substitution is not.

## 2. D2-specific rejection

A candidate is rejected from `D2_CONFIRMATORY_CANDIDATE` if any of these are true:

```text
intervention designers saw item-level content
CONTROL results from this material influenced treatment design
public leaderboard outcomes materially influenced treatment selection
same sealed shard was already opened
same generation recipe was adaptively tuned after prior treatment outcomes
custodian cannot prevent pre-freeze access
answer key is available to treatment-generation process
holdout hash/commitment cannot be fixed before treatment freeze
```

Once D2 results are revealed:

```text
D2 -> BURNED
```

No descendant treatment may call the same evidence fresh confirmation.

## 3. Transfer-specific rejection

A proposed transfer benchmark is not materially independent merely because:

- it has a different name;
- it is hosted elsewhere;
- it has paraphrased prompts;
- it uses another LLM judge;
- it samples the same upstream corpus through a different wrapper.

Transfer requires a credible lineage difference relevant to the claim.

## 4. Valid dispositions

Every reviewed candidate receives exactly one current disposition:

```text
PRIMARY_ELIGIBLE
SECONDARY_ONLY
DEVELOPMENT_ONLY
D2_CONFIRMATORY_CANDIDATE
T_TRANSFER_CANDIDATE
REJECT
PENDING_EVIDENCE
```

`PENDING_EVIDENCE` is preferable to inventing facts.

## 5. Rejection record

Every rejection or downgrade must record:

```yaml
benchmark_id:
decision:
requested_role:
rule_ids: []
evidence: []
unknowns: []
reviewer:
review_date:
reconsideration_condition:
```

A rejected candidate may be reconsidered only if the reason changes materially, for example a stable grader is released or a private held-out split becomes available.

It may not be reconsidered simply because current candidates produce inconvenient results.

## 6. Non-negotiable interpretation rule

```text
BENCHMARK USEFULNESS != PRIMARY ELIGIBILITY
PRIMARY ELIGIBILITY != D2 ELIGIBILITY
D2 ELIGIBILITY != GENERALIZATION
GENERALIZATION != UNIVERSALITY
```
