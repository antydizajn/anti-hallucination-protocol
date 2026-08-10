# SimpleQA - Gate 1 Benchmark Review

## Status

```yaml
benchmark_id: simpleqa
review_status: COMPLETE_WITH_OPEN_RISKS
primary_eligible: true
primary_scope:
  - PARAMETRIC_FACTUALITY
  - KNOWLEDGE_BOUNDARY
  - SHORT_FORM_SELECTIVE_ACCURACY
historical_public_role: D0_MEASUREMENT_DEVELOPMENT
control_discovery_role: D1_CONTROL_DISCOVERY
sealed_d2_role: NOT_ELIGIBLE_BY_DEFAULT
transfer_role: SECONDARY_ONLY_UNLESS_NEW_INDEPENDENT_REFRESH_EXISTS
```

SimpleQA is a strong short-form factuality instrument, but it is public, adversarially collected against GPT-4-family outputs, approximately 3% residual benchmark error was estimated by the authors, and its standard grader is a prompted frontier-model classifier. It therefore requires explicit grader validation and cannot serve as a sealed confirmatory holdout by default.

---

# 1. Identity

```yaml
canonical_name: SimpleQA
maintainer: OpenAI
primary_source: https://cdn.openai.com/papers/simpleqa.pdf
official_repository: https://github.com/openai/simple-evals
source_dataset_endpoint: https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv
question_count: 4326
```

Source paper and official implementation inspected 2026-08-10.

---

# 2. Construct

## Primary constructs

```text
SHORT_FORM FACTUALITY
KNOWLEDGE BOUNDARY
SELECTIVE ANSWERING / NOT-ATTEMPTED BEHAVIOR
```

The paper explicitly frames SimpleQA as a targeted benchmark for whether models "know what they know" while answering short fact-seeking questions with a single indisputable answer.

## Secondary constructs

```text
stated-confidence calibration
response-frequency calibration
```

## What SimpleQA does NOT establish

```text
long-form factuality
citation entailment
citation completeness
RAG grounding
agent/tool honesty
false-premise correction
temporal freshness
multi-turn epistemic behavior
broad hallucination reduction
```

The paper itself explicitly notes that restricting the benchmark to short-form factuality leaves open whether improvements generalize to long-form factuality.

---

# 3. Task semantics

The benchmark contains 4,326 short fact-seeking questions.

Construction requirements included:

```text
single indisputable answer
reference answer should not change over time
reference answer supported by evidence
question difficult enough that at least one sampled frontier-model completion was incorrect
answerable by 2023-12-31
```

The source paper states that the dataset was adversarially collected against four OpenAI model responses, mostly GPT-4 variants, with GPT-3.5 introduced for part of the process.

This has two implications:

1. SimpleQA is intentionally difficult for a known model family.
2. Performance differences may partially reflect construction-time model targeting, so cross-model comparisons require care.

---

# 4. Data quality

Two independent human annotators had to agree on the answer.

The paper reports additional source diversity requirements and a third-annotator audit of 1,000 examples.

The authors estimate residual benchmark error at approximately:

```text
~3%
```

Common issues included:

```text
ambiguous questions
contradictory reputable sources
more than one actually correct answer
```

Therefore:

```text
SIMPLEQA GOLD != PERFECT GOLD
```

AHP must preserve an adjudication path for contested or broken items rather than forcing every disagreement into model error.

---

# 5. Answerability and utility

The benchmark grader labels:

```text
CORRECT
INCORRECT
NOT_ATTEMPTED
```

Definitions are useful for AHP because:

- hedged but factually wrong statements remain INCORRECT;
- a clean refusal or incomplete non-contradictory answer can be NOT_ATTEMPTED;
- a fully correct answer is CORRECT.

However the source paper itself discusses metric gaming and notes that a single-number metric has tradeoffs. It proposes overall-correct, correct-given-attempted and their harmonic mean, and discusses an alternative explicit negative penalty for incorrect answers.

Therefore the source benchmark does NOT settle AHP's final primary endpoint.

## Degenerate-policy analysis

```text
ALWAYS_ABSTAIN:
  overall correct approximately zero
  can avoid incorrect answers
  must fail any AHP primary endpoint designed to reward useful answering

ALWAYS_ANSWER:
  high attempt rate but many incorrect answers on difficult items

SELECTIVE_ANSWERING:
  central behavior tested
```

SimpleQA is a strong D0 instrument for endpoint metrology because it exposes the answer-vs-abstain tradeoff directly.

---

# 6. Grading

The official `simple-evals` implementation uses a prompted model grader that sees:

```text
question
gold target
predicted answer
```

and outputs:

```text
CORRECT
INCORRECT
NOT_ATTEMPTED
```

The paper reports a manual check of 300 graded examples with two disagreements, but explicitly says no formal grader-performance study was conducted.

AHP decision:

```yaml
source_grader: D0_VALIDATION_REQUIRED
unvalidated_llm_grader_as_confirmatory_primary: REJECT
```

Required D0 validation:

```text
freeze grader model/version
freeze exact prompt
freeze parser
freeze retries/failure mapping
blind arm identity
human-calibration subset
confusion matrix by source class
position/style bias probes where applicable
```

Critical implementation finding:

The official code defaults a grader parse failure to `NOT_ATTEMPTED`.

For AHP this behavior is NOT acceptable as a generic measurement rule because:

```text
GRADER_PARSE_FAILURE != MODEL_NOT_ATTEMPTED
```

Our adapter must preserve evaluator failure as its own error channel.

---

# 7. Contamination

```yaml
public_or_private: PUBLIC
answer_key_public: true
contamination_class: C2
benchmark_memorization_risk: HIGH
intervention_leakage_risk: HIGH_IF_ITEM_LEVEL_INSPECTED
```

The entire test set is publicly downloadable.

Therefore public SimpleQA cannot be D2 for an intervention whose developers have access to the benchmark or whose design was influenced by SimpleQA item/result patterns.

---

# 8. Lineage

```yaml
lineage_group: openai_simpleqa
construction:
  - human-authored questions
  - independent human answer verification
  - adversarial difficulty screen using mostly GPT-4-family outputs
  - prompted-model quality-control classifiers
```

The use of GPT-4-family outputs during item selection is part of benchmark lineage and should be recorded when interpreting model-family-specific effects.

SimpleQA must not be counted as independent of a derived benchmark if that benchmark copies or transforms its questions.

---

# 9. Evidence-role decision

## D0

Strong candidate for:

```text
adapter validation
grader validation
endpoint metrology
always-answer / always-abstain stubs
selective-answer utility testing
label-noise/adjudication procedures
```

## D1

Strong candidate for CONTROL discovery on:

```text
short-form factual errors
not-attempted behavior
model knowledge boundary
```

## D2

```text
NOT ELIGIBLE BY DEFAULT
```

because it is a fully public static benchmark.

## T

Useful as secondary external comparability, but a static public benchmark is weak temporal-transfer evidence.

---

# 10. Rejection-rule audit

```text
R1  construct mismatch: PASS within short-form factuality scope
R2  no operational scoring boundary: PASS
R3  degenerate-policy exploit: D0 REQUIRED
R4  positive-evidence absence: PASS
R5  grader not auditable: OPEN RISK; official prompt available but judge must be revalidated
R6  exposed material as sealed evidence: TRIGGERED for D2
R7  lineage collapse: PASS if lineage recorded
R8  overlap not investigated: OPEN until panel-wide overlap audit
R9  license/access unresolved: OPEN - repository/data terms must be recorded explicitly in registry
R10 answer-key leakage: HIGH for public data
R11 capability mismatch: experiment-design dependent
R12 runtime failure collapse: official grader parse fallback must be replaced
R13 prompt pseudoreplication: experiment-design dependent
R14 mutable benchmark without snapshot: low risk if exact CSV hash pinned
R15 post-hoc exclusions: Gate 2 dependent
R16 denominator gaming: IMPORTANT - attempted-only metrics require hard utility controls
R17 insufficient measurement resolution: D0 required
R18 hidden benchmark transformation: adapter review required
```

---

# 11. Final decision

```yaml
benchmark_id: simpleqa
review_status: COMPLETE_WITH_OPEN_RISKS
primary_eligible: true
primary_scope:
  - PARAMETRIC_FACTUALITY
  - KNOWLEDGE_BOUNDARY
  - SHORT_FORM_SELECTIVE_ACCURACY
best_roles:
  - D0_MEASUREMENT_DEVELOPMENT
  - D1_CONTROL_DISCOVERY
sealed_d2_role: NOT_ELIGIBLE_BY_DEFAULT
critical_risks:
  - public contamination
  - approximately 3 percent residual label error
  - prompted LLM grader requiring revalidation
  - attempted-only metric gaming
  - benchmark construction targeted against GPT-4-family outputs
```

## Bottom line

SimpleQA belongs in the AHP measurement panel as a strong short-form selective-factuality ruler.

It must not become the whole definition of hallucination, and its public test set must not be presented as sealed confirmation.
