# FreshQA - Gate 1 Benchmark Review

## Status

```yaml
benchmark_id: freshqa
review_status: COMPLETE_WITH_OPEN_RISKS
final_disposition: MULTI_ROLE_BY_SNAPSHOT
primary_eligible: true
eligible_pool:
  historical_public_snapshots: D0_MEASUREMENT_DEVELOPMENT
  frozen_control_discovery_snapshot: D1_CONTROL_DISCOVERY
  public_future_refresh: T_TRANSFER_CANDIDATE
  sealed_confirmatory: NOT_ELIGIBLE_BY_DEFAULT
```

FreshQA is useful for AHP, but only if snapshot identity and evidence role are explicit.

A FreshQA benchmark name without a date/version is not a valid experimental identity.

---

# 1. Identity

```yaml
benchmark_id: freshqa
canonical_name: FreshQA
version: dynamic_snapshots
maintainer: freshllms
primary_source: https://arxiv.org/abs/2310.03214
official_repository: https://github.com/freshllms/freshqa
license: Apache-2.0
license_verified: true
```

Official repository inspected 2026-08-10.

At inspection time the repository README publicly listed:

```text
FreshQA April 21, 2026
Next update: May 11, 2026
```

and stated that the dataset is updated weekly or upon request.

This creates an important provenance warning:

```text
README STATED UPDATE CADENCE
!=
PROOF THAT A NEWER SNAPSHOT EXISTS
```

The latest snapshot explicitly exposed by the inspected README is therefore recorded as:

```text
2026-04-21
```

without inferring an unlisted August 2026 snapshot.

Primary sources:

- paper: https://arxiv.org/abs/2310.03214
- official repo: https://github.com/freshllms/freshqa
- official license: https://github.com/freshllms/freshqa/blob/main/LICENSE

---

# 2. Construct

## Primary constructs

```text
TEMPORAL_FRESHNESS
FALSE_PREMISE
PARAMETRIC / CURRENT-WORLD FACTUALITY
```

## Secondary constructs

```text
KNOWLEDGE_BOUNDARY
MULTI_HOP_FACTUAL QA
HALLUCINATION UNDER STRICT CLAIM-LEVEL EVALUATION
RETRIEVAL-AUGMENTED FACTUALITY when paired with search methods
```

## What FreshQA does NOT establish by itself

FreshQA does not establish:

```text
general hallucination prevention
citation entailment
citation completeness
RAG attribution correctness
tool-failure handling
agent completion honesty
long-context evidence retention
general calibration
safe abstention across arbitrary domains
cross-domain protocol effectiveness
```

A win on FreshQA cannot be promoted into:

```text
AHP generally reduces hallucinations
```

without independent evidence on other constructs and lineages.

---

# 3. Task semantics

The paper defines FreshQA as 600 natural questions divided into four broad answer-change categories:

```text
NEVER_CHANGING
SLOW_CHANGING
FAST_CHANGING
FALSE_PREMISE
```

The original dataset structure reported in the paper:

```text
test:
  125 questions x 4 categories = 500

development:
  25 questions x 4 categories = 100
```

Questions also vary between:

```text
ONE_HOP
MULTI_HOP
```

FreshQA is dynamic: answers and even category labels may change over time.

Therefore every run must bind:

```text
snapshot_date
source_artifact_hash or immutable captured copy where terms permit
run_date
model snapshot
reference-answer snapshot
```

A result recorded only as:

```text
FreshQA accuracy = X
```

is incomplete.

---

# 4. Answerability and utility

FreshQA includes both:

```text
valid-premise questions requiring an answer
false-premise questions requiring rebuttal/correction
```

This is valuable for AHP because a useful system must distinguish:

```text
WARRANTED COMMITMENT
from
WARRANTED NON-COMMITMENT / PREMISE CORRECTION
```

However FreshQA is not primarily an abstention benchmark.

The original evaluation protocol credits a response when a confident/definitive correct answer is given or can clearly be inferred. For false-premise items, the false premise must be identified to receive credit.

This means a generic:

```text
I don't know
```

is not a valid universal winning strategy.

## Degenerate-policy expectations

```text
ALWAYS_ABSTAIN:
  should fail most valid-premise items

ALWAYS_ANSWER:
  should fail false-premise items and may hallucinate stale claims

KEYWORD_HEURISTIC:
  possible artifact risk, must be empirically checked on D0

RANDOM_POLICY:
  expected poor

ALWAYS_TOOL:
  not part of the source benchmark definition; tool behavior depends on adapter/runtime

NEVER_TOOL:
  meaningful baseline if tested models otherwise receive browsing capability
```

FreshQA therefore has useful positive/negative action balance, but AHP must preserve an explicit answer/task-completion guardrail rather than treating lower unsupported-answer rate alone as success.

---

# 5. Grading

The source paper uses two evaluation modes:

```text
RELAXED
  primary answer correctness

STRICT
  primary answer correctness
  + all factual claims must be accurate/up-to-date
  + any hallucination can invalidate the response
```

The paper reports human evaluation as the main study procedure.

For a 100-answer inter-rater subset, it reports agreement of:

```text
99% Relaxed
96% Strict
```

The paper also introduces FreshEval, a few-shot LLM-based automatic evaluator, reporting average agreement with human evaluation of approximately:

```text
96.5% Relaxed
96% Strict
```

The official repository explicitly states that human evaluators are considered more reliable for factuality, while FreshEval is offered as an easier automatic alternative.

## AHP grader decision

```yaml
source_human_protocol: PRIMARY_CANDIDATE
fresheval: D0_VALIDATION_REQUIRED
fresheval_as_unvalidated_primary: REJECT
```

FreshEval may not become the AHP primary grader solely because the authors reported high historical agreement.

AHP D0 must revalidate the exact frozen judge implementation against blinded human labels or another accepted gold/reference process.

Required FreshEval lock if used:

```text
judge model
exact version/snapshot
prompt/few-shot examples
Strict vs Relaxed mode
temperature/sampling
parser
retry policy
failure policy
arm blinding
human calibration subset
```

The repository currently recommends a historical GPT-4 preview model for FreshEval. That recommendation is not a suitable 2026 version pin for a new confirmatory study.

Therefore:

```text
FRESHEVAL IMPLEMENTATION FROM SOURCE
!=
FROZEN 2026 CONFIRMATORY GRADER
```

---

# 6. Runtime/error semantics

FreshQA itself is a QA dataset and evaluation protocol. Runtime/tool-error semantics are therefore introduced by the AHP adapter/runner, not by FreshQA.

AHP must preserve:

```text
MODEL_TIMEOUT != WRONG_ANSWER
MODEL_TIMEOUT != ABSTENTION
SEARCH_FAILURE != KNOWLEDGE_ABSENCE
TOOL_ERROR != FALSE_PREMISE_CORRECTION
EVALUATOR_ERROR != MODEL_FAILURE
```

If browsing/retrieval is enabled in a future experimental factor, failures of the retrieval environment require separate logging.

---

# 7. Contamination

## Current public snapshots

Classification:

```yaml
public_or_private: PUBLIC
answer_key_public: true
contamination_class: C2
benchmark_memorization_risk: HIGH
intervention_leakage_risk: HIGH_IF_ITEM_LEVEL_INSPECTED
temporal_staleness_risk: HIGH_WITHOUT_SNAPSHOT_BINDING
```

Reason:

FreshQA has been public since 2023, with many public historical snapshots and public reference answers.

Public static snapshots cannot be treated as sealed D2 merely because the treatment prompt does not contain their exact questions.

## Future refreshes

A future refresh can provide meaningful temporal novelty.

But:

```text
FUTURE AT DESIGN TIME
!=
AUTOMATICALLY SEALED CONFIRMATORY
```

Once publicly released, it may be exposed to model providers, retrieval systems, evaluators, developers, or treatment authors.

Therefore the default role of a future public FreshQA refresh is:

```text
T_TRANSFER_CANDIDATE
```

not automatically D2.

A genuinely D2-eligible FreshQA-derived shard would require a separate custody arrangement in which treatment designers cannot inspect item instances/reference answers before treatment freeze and where authorship/generation rules are independently controlled.

That is NOT established by the public FreshQA repository today.

---

# 8. Lineage and overlap

```yaml
lineage_group: freshllms_freshqa
source_authorship: human_authored
collection_sources:
  - NLP researchers including authors/colleagues
  - online freelancers
quality_control:
  - manual review
  - duplicate/invalid-question removal
  - answer verification
  - supporting evidence URLs
```

The paper reports that annotators were asked to provide supporting reputable URLs and that authors manually reviewed and cleaned items.

FreshQA snapshots over time are NOT independent benchmark lineages.

They are temporal descendants of the same benchmark lineage.

Therefore:

```text
FreshQA 2024
FreshQA 2025
FreshQA 2026
```

must not be counted as three independent benchmark families.

They can provide temporal replication, but their shared construction process must remain explicit.

Known related benchmark:

```text
SealQA builds on FreshQA
```

This relation must be reviewed before FreshQA and SealQA are counted as independent evidence families.

Current independence claim:

```yaml
status: PARTIALLY_INDEPENDENT_ACROSS_TIME_ONLY
scope: temporal_refresh
limitations:
  - shared benchmark design
  - shared maintainership
  - shared category ontology
  - potentially overlapping persistent questions across snapshots
```

Item-level overlap between snapshots must be measured rather than assumed absent.

---

# 9. Access, license and feasibility

```yaml
license: Apache-2.0
license_verified: true
repository_public: true
data_delivery: public Google Sheets snapshots linked by official repo
runtime_requirements: low for dataset-only evaluation; higher if retrieval/search is introduced
```

Operational issue:

The dataset is delivered as mutable/public spreadsheet snapshots rather than a single immutable packaged artifact.

AHP must capture and hash the exact evaluated snapshot where redistribution/terms permit, or record an immutable source export and checksum in the run manifest.

---

# 10. Evidence-role decision

## Historical public FreshQA snapshots

```yaml
pool: D0_MEASUREMENT_DEVELOPMENT
allowed:
  - adapter development
  - scorer development
  - grader validation
  - false-premise measurement tests
  - temporal/freshness construct validation
  - stub tests
forbidden:
  - independent D2 confirmation for a treatment influenced by FreshQA
```

## Fresh frozen public snapshot used for CONTROL discovery

Possible role:

```yaml
pool: D1_CONTROL_DISCOVERY
```

provided snapshot identity, run date, model snapshots and adapter are frozen.

If D1 FreshQA failures influence treatment design, that snapshot becomes permanently non-confirmatory for that treatment lineage.

## Future public refresh after treatment freeze

Preferred default role:

```yaml
pool: T_TRANSFER_CANDIDATE
strength: STRONG_FOR_TEMPORAL_TRANSFER
```

This is one of FreshQA's most valuable AHP roles.

## D2

```yaml
pool: D2_CONFIRMATORY_CANDIDATE
status: NOT_ELIGIBLE_BY_DEFAULT
```

Reason:

The public benchmark lineage and recipe are already visible, and public refreshes do not satisfy sealed custody merely by being temporally new.

A separately protected FreshQA-derived evaluation might become D2 eligible only under an independently audited holdout process.

---

# 11. Rejection-rule audit

```text
R1  construct mismatch: PASS within temporal-factuality/false-premise scope
R2  no operational scoring boundary: PASS, but AHP mapping must be frozen
R3  degenerate-policy exploit: PASS PROVISIONALLY; D0 stubs required
R4  positive-evidence absence: PASS
R5  grader not auditable: PASS for human protocol; FreshEval requires D0 revalidation
R6  exposed material as sealed evidence: TRIGGERED for public snapshots
R7  lineage collapse: PASS only if snapshots counted as one lineage
R8  overlap not investigated: TRIGGERED until snapshot-overlap analysis exists
R9  license/access unresolved: PASS for repository license; exact data-export terms still record provenance
R10 answer-key leakage: HIGH RISK for public snapshots
R11 capability mismatch: ADAPTER/DESIGN DEPENDENT
R12 runtime failure collapse: ADAPTER/DESIGN DEPENDENT
R13 prompt pseudoreplication: EXPERIMENT-DESIGN DEPENDENT
R14 mutable benchmark without snapshot: TRIGGERED unless exact snapshot frozen
R15 post-hoc exclusions: GATE 2 DEPENDENT
R16 denominator gaming: GATE 2 scorer mapping required
R17 insufficient measurement resolution: D0 REQUIRED
R18 hidden benchmark transformation: ADAPTER REVIEW REQUIRED
```

---

# 12. Missing-measurement analysis

FreshQA is especially strong for:

```text
temporal factuality
false-premise correction
strict factuality of short QA responses
```

It is weak or absent for:

```text
tool execution truthfulness
citation entailment
citation completeness
retrieval-source attribution
long-context grounding
agent workflow completion claims
explicit uncertainty calibration
multi-turn epistemic state transitions
```

Therefore FreshQA requires complementary benchmark lineages.

It cannot dominate the AHP panel merely because it is operationally convenient.

---

# 13. Final Gate 1 decision

```yaml
benchmark_id: freshqa
review_status: COMPLETE_WITH_OPEN_RISKS
primary_eligible: true
primary_scope:
  - TEMPORAL_FRESHNESS
  - FALSE_PREMISE
  - STRICT_FACTUALITY
historical_public_role: D0_MEASUREMENT_DEVELOPMENT
control_discovery_role: D1_CONTROL_DISCOVERY
future_public_refresh_role: T_TRANSFER_CANDIDATE
sealed_d2_role: NOT_ELIGIBLE_BY_DEFAULT
lineage_group: freshllms_freshqa
contamination_class_historical_public: C2
grader_primary_eligible:
  human_protocol: true
  fresheval: false_until_revalidated
critical_unknowns:
  - exact snapshot overlap rates across refreshes
  - current 2026 FreshEval judge replacement and calibration
  - D0 variance and SESOI resolution under AHP runtime
  - exact role of browsing/retrieval in future CONTROL panel
rejection_rules_triggered:
  - R6 for public snapshots as D2
  - R8 until overlap audit
  - R14 unless snapshot identity frozen
```

## Bottom line

FreshQA should be in the AHP measurement program.

Its best roles are:

```text
D0 measurement development
D1 temporal/false-premise CONTROL discovery
T temporal transfer using a genuinely later refresh
```

It should NOT be used as a convenient public D2 holdout.

The strongest AHP use of FreshQA is not:

```text
we scored well on FreshQA
```

but:

```text
a frozen CONTROL failure pattern discovered on one temporal state
is tested for generalization on a later temporal refresh without
pretending the shared FreshQA lineage is independent benchmark evidence
```
