# Benchmark Review Template

## Status

Gate 1 per-benchmark review form.

This template must be completed before assigning any candidate a primary, confirmatory, or transfer role.

---

# 1. Identity

```yaml
benchmark_id:
canonical_name:
version:
revision_sha:
maintainer:
release_date:
last_refresh:
primary_source:
official_repository:
official_dataset:
```

## Source verification

- [ ] Original paper/specification inspected
- [ ] Official repository inspected where available
- [ ] Official dataset documentation inspected where available
- [ ] Version/revision recorded
- [ ] License inspected

Evidence:

```text

```

Unknowns:

```text

```

---

# 2. Construct

## What does this benchmark actually measure?

Primary construct:

```text

```

Secondary constructs:

```text

```

What it does NOT establish:

```text

```

Failure mechanism targeted:

```text

```

Why this is relevant to AHP measurement rather than merely adjacent capability evaluation:

```text

```

### Construct-mismatch check

- [ ] Not using evaluator accuracy as direct prevention efficacy
- [ ] Not using generic reasoning as factuality by default
- [ ] Not collapsing context faithfulness into world truth
- [ ] Not collapsing citation existence into citation entailment
- [ ] Not collapsing tool invocation into verified tool use

---

# 3. Task semantics

```yaml
task_type:
domain:
language:
interaction_type: SINGLE_TURN | MULTI_TURN | AGENTIC | MIXED
tools_required:
retrieval_required:
long_context_required:
context_length_profile:
unit_of_scoring:
```

Dependencies between turns/tasks:

```text

```

If multi-turn or agentic, identify the real experimental dependence unit:

```text

```

---

# 4. Answerability and utility

Answerability classes present:

```text

```

Positive-evidence / should-answer cases present?

```text
YES | NO | UNKNOWN
```

Estimated positive-evidence fraction:

```text

```

Should-abstain / withhold / clarify cases present?

```text
YES | NO | UNKNOWN
```

False-premise cases present?

```text
YES | NO | UNKNOWN
```

Partial credit supported by source benchmark?

```text
YES | NO | UNKNOWN
```

## Degenerate-policy analysis

Expected behavior of:

```text
ALWAYS_ABSTAIN:
ALWAYS_ANSWER:
KEYWORD_HEURISTIC:
RANDOM_POLICY:
ALWAYS_TOOL:
NEVER_TOOL:
COPY_CONTEXT:
```

Could any trivial policy achieve a misleadingly high score?

```text

```

Required guardrail if yes:

```text

```

---

# 5. Grading

```yaml
grading_type: DETERMINISTIC | RULE_BASED | HUMAN | LLM_JUDGE | HYBRID | UNKNOWN
grader_identity:
grader_version:
grader_version_pin_possible:
grader_prompt_public:
grader_prompt_hash:
human_validation_available:
estimated_label_noise:
```

Source-label to AHP-outcome mapping:

```text
SOURCE LABEL -> AHP OUTCOME

```

Unmapped labels:

```text

```

Known grader failure modes:

```text

```

If LLM judge is used, document:

```text
model/version:
prompt:
sampling:
pair/order sensitivity:
verbosity/style sensitivity:
human agreement:
reliability statistic:
fallback adjudication:
```

Primary-grader admissibility:

```text
ELIGIBLE | SECONDARY_ONLY | NOT_VALIDATED | UNKNOWN
```

---

# 6. Runtime/error semantics

How are the following represented?

```text
MODEL_TIMEOUT:
MODEL_API_ERROR:
TOOL_ERROR:
HARNESS_ERROR:
ENVIRONMENT_ERROR:
RATE_LIMIT:
EMPTY_VALID_RESULT:
EMPTY_PROVIDER_OUTPUT:
EVALUATOR_ERROR:
```

Check:

- [ ] Runtime failure cannot become clean abstention
- [ ] Tool error cannot become evidence absence
- [ ] Evaluator error cannot become model failure
- [ ] Empty output semantics are explicit

---

# 7. Contamination

```yaml
public_or_private:
answer_key_public:
private_split_available:
heldout_available:
dynamic_split_available:
temporal_split_available:
contamination_class: C0 | C1 | C2 | C3 | CX
benchmark_memorization_risk:
intervention_leakage_risk:
grader_leakage_risk:
temporal_staleness_risk:
```

Known contamination evidence:

```text

```

Contamination unknowns:

```text

```

Exposure to intervention designers:

```text
NONE | METADATA_ONLY | ITEM_LEVEL | RESULTS_LEVEL | UNKNOWN
```

Did public leaderboard outcomes influence intervention design?

```text
YES | NO | UNKNOWN
```

Could this benchmark still qualify for D2?

```text
YES | NO | UNKNOWN
```

Why:

```text

```

---

# 8. Lineage and overlap

Lineage group:

```text

```

Upstream datasets:

```text

```

Derived from:

```text

```

Generation pipeline:

```text

```

Shared grader with:

```text

```

Shared reference corpus with:

```text

```

Known item overlap with:

```text

```

Overlap checks completed:

- [ ] exact hash
- [ ] normalized exact hash
- [ ] n-gram / MinHash signal
- [ ] semantic-neighbor signal
- [ ] source URL overlap
- [ ] answer overlap
- [ ] benchmark ancestry

Current overlap status:

```text
NOT_CHECKED | NO_KNOWN_OVERLAP | EXACT_OVERLAP | NEAR_DUPLICATE_SIGNAL | SHARED_LINEAGE | UNKNOWN
```

Independence claim:

```text
MATERIALLY_INDEPENDENT | PARTIALLY_INDEPENDENT | NOT_INDEPENDENT | UNKNOWN
```

Basis and limitations:

```text

```

---

# 9. Access, license, and feasibility

```yaml
license:
license_verified:
redistribution_allowed:
commercial_use:
runtime_requirements:
estimated_tokens:
estimated_tool_calls:
estimated_cost:
estimated_runtime:
```

Operational blockers:

```text

```

---

# 10. Candidate evidence role

Candidate pool:

```text
D0_MEASUREMENT_DEVELOPMENT
D1_CONTROL_DISCOVERY
D2_CONFIRMATORY_CANDIDATE
T_TRANSFER_CANDIDATE
EXCLUDE
```

Requested disposition:

```text
PRIMARY_ELIGIBLE
SECONDARY_ONLY
DEVELOPMENT_ONLY
D2_CONFIRMATORY_CANDIDATE
T_TRANSFER_CANDIDATE
REJECT
PENDING_EVIDENCE
```

## Why this role is justified

```text

```

## Why a stronger role is not justified

```text

```

---

# 11. Rejection-rule audit

Evaluate every rule from `rejection-rules.md`.

```text
R1  construct mismatch: PASS | TRIGGERED | UNKNOWN
R2  no operational scoring boundary: PASS | TRIGGERED | UNKNOWN
R3  degenerate-policy exploit: PASS | TRIGGERED | UNKNOWN
R4  positive-evidence absence: PASS | TRIGGERED | UNKNOWN
R5  grader not auditable: PASS | TRIGGERED | UNKNOWN
R6  exposed material as sealed evidence: PASS | TRIGGERED | UNKNOWN
R7  lineage collapse: PASS | TRIGGERED | UNKNOWN
R8  overlap not investigated: PASS | TRIGGERED | UNKNOWN
R9  license/access unresolved: PASS | TRIGGERED | UNKNOWN
R10 answer-key leakage: PASS | TRIGGERED | UNKNOWN
R11 capability mismatch: PASS | TRIGGERED | UNKNOWN
R12 runtime failure collapse: PASS | TRIGGERED | UNKNOWN
R13 prompt pseudoreplication: PASS | TRIGGERED | UNKNOWN
R14 mutable benchmark without snapshot: PASS | TRIGGERED | UNKNOWN
R15 post-hoc exclusions: PASS | TRIGGERED | UNKNOWN
R16 denominator gaming: PASS | TRIGGERED | UNKNOWN
R17 insufficient measurement resolution: PASS | TRIGGERED | UNKNOWN
R18 hidden benchmark transformation: PASS | TRIGGERED | UNKNOWN
```

Any unresolved load-bearing `UNKNOWN` blocks primary promotion until resolved or explicitly moved to a non-primary role.

---

# 12. Missing-measurement analysis

What important behavior does this benchmark fail to cover?

```text

```

What complementary benchmark family is required?

```text

```

Does this benchmark create a blind spot if overweighted?

```text

```

---

# 13. Final Gate 1 review decision

```yaml
benchmark_id:
review_status: COMPLETE | INCOMPLETE
final_disposition:
primary_eligible: true | false
eligible_pool:
lineage_group:
contamination_class:
grader_primary_eligible: true | false | unknown
critical_unknowns: []
rejection_rules_triggered: []
reviewer:
review_date:
```

Decision rationale:

```text

```

## Evidence discipline

```text
UNKNOWN != NO_RISK
PUBLIC != SEALED
NEW_NAME != NEW_LINEAGE
GOOD_PAPER != VALID_PRIMARY_ROLE
HIGH_SCORE != SCIENTIFIC_VALIDITY
```
