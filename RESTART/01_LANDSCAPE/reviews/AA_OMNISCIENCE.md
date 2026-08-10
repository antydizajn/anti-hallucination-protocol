# AA-Omniscience-Public - Gate 1 Benchmark Review

## Status

```yaml
benchmark_id: aa_omniscience
review_status: COMPLETE_WITH_OPEN_RISKS
primary_eligible: true
primary_scope:
  - BROAD_FACTUAL_COVERAGE
  - OMNISCIENCE_STYLE_KNOWLEDGE_PROBING
  - SHORT_FACTUAL_ANSWERING
historical_public_role: D0_MEASUREMENT_DEVELOPMENT
control_discovery_role: D1_CONTROL_DISCOVERY
sealed_public_d2_role: NO
sealed_private_d2_role: POSSIBLE_IF_CUSTODY_VERIFIED
transfer_role: UNKNOWN
```

AA-Omniscience is potentially one of the highest-value AHP candidates because it targets broad factual coverage at scale. Its most important property is not the public subset, but the separation between public inspection data and a larger evaluation set.

The D2 status depends entirely on custody, access control, and whether the hidden portion remains genuinely inaccessible during treatment design.

---

# 1. Identity

```yaml
canonical_name: Artificial Analysis Omniscience
public_dataset: AA-Omniscience-Public
provider: Artificial Analysis
platform: Hugging Face
public_subset: 600 questions
full_evaluation_size_claim: 6000 questions
```

Source inspected:

```text
https://huggingface.co/datasets/ArtificialAnalysis/AA-Omniscience-Public
```

Important distinction:

```text
AA-Omniscience-Public
!=
full evaluation universe
```

The public dataset card describes a public subset intended for transparency while the larger benchmark is used for evaluation.

---

# 2. Construct

## Primary constructs

```text
BROAD FACTUAL KNOWLEDGE COVERAGE
QUESTION-DOMAIN COVERAGE
SHORT-FORM FACTUAL RESPONSE ACCURACY
```

## Secondary constructs

```text
knowledge boundary
unsupported factual claims
coverage of model knowledge
```

## What AA-Omniscience does NOT establish by itself

```text
citation correctness
source attribution
false-premise correction
RAG grounding
agent honesty
long-context reasoning
calibration
safe refusal policy
```

A model can score well on broad factual coverage and still hallucinate in grounded tasks.

---

# 3. Task semantics

AA-Omniscience is designed as a broad factual evaluation rather than a narrow misconception benchmark.

AHP interpretation:

```text
question asked
        ↓
model response
        ↓
correctness assessment
```

The benchmark is useful for estimating factual coverage but requires additional constructs to distinguish:

```text
unknown and honest
unknown and hallucinated
known and wrong
partially correct
```

The scoring contract must therefore be frozen before AHP experiments.

---

# 4. Answerability and utility

Broad factual benchmarks are vulnerable to a classic failure:

```text
maximize answer rate
        ↓
increase unsupported claims
```

AHP must not optimize only:

```text
accuracy among attempted answers
```

without measuring:

```text
coverage
attempt rate
incorrect claim rate
abstention quality
```

## Required stubs

```text
ALWAYS_ANSWER
ALWAYS_ABSTAIN
RANDOM
```

must be measured before treatment claims.

---

# 5. Grading

AA-Omniscience requires explicit grader review.

Unknowns requiring verification:

```text
reference-answer format
human adjudication process
automatic evaluator details
judge model/version
handling of partial correctness
handling of multiple valid answers
```

AHP decision:

```yaml
public_dataset: D0/D1 candidate
hidden_dataset: D2 candidate only after custody audit
external_judge: requires validation
```

No benchmark score should enter AHP evidence without a frozen scorer contract.

---

# 6. Contamination

## Public 600 subset

```yaml
public: true
answer_visibility: true
contamination_class: C2
D2: rejected
```

The public subset is useful for:

```text
adapter testing
measurement development
baseline debugging
```

but cannot be a sealed confirmation set.

## Hidden larger set

Potentially:

```yaml
D2_candidate: yes
```

Required evidence:

```text
who can access items
when treatment design freezes
whether model developers saw items
whether benchmark creators saw intervention results
custodian separation
version/hash
pre-registration
```

Without this evidence:

```text
hidden != sealed
```

---

# 7. Lineage

```yaml
lineage_group: artificialanalysis_omniscience
```

The benchmark should be counted as one lineage, not multiple independent datasets, even if public and private splits exist.

Public and hidden splits share construction assumptions.

---

# 8. Evidence-role decision

## D0

Strong candidate:

```text
baseline measurement
scorer development
coverage analysis
failure taxonomy discovery
```

## D1

Strong candidate:

```text
large-scale factual failure discovery
model comparison
error clustering
```

## D2

Decision:

```yaml
public_subset: NO
private_full_set: POSSIBLE
```

The private set requires a custody audit.

## T

Unknown.

A future refreshed Omniscience release could provide temporal transfer only if lineage and access conditions are documented.

---

# 9. Rejection-rule audit

```text
R1 construct mismatch: PASS for broad factuality only
R2 operational scoring boundary: OPEN
R3 degenerate-policy exploit: OPEN until abstention metrics added
R4 positive-evidence absence: PASS
R5 grader auditability: OPEN
R6 public material as sealed evidence: TRIGGERED
R7 lineage collapse: PASS if split relationship preserved
R8 overlap investigation: REQUIRED
R9 license/access: REQUIRED record
R10 answer leakage: HIGH on public subset
R11 capability mismatch: experiment dependent
R12 runtime failure collapse: adapter dependent
R13 prompt pseudoreplication: experiment dependent
R14 snapshot immutability: REQUIRED
R15 post-hoc exclusions: Gate 2 dependent
R16 denominator gaming: IMPORTANT
R17 measurement resolution: D0 REQUIRED
R18 hidden transformation: adapter review required
```

---

# 10. Final decision

```yaml
benchmark_id: aa_omniscience
review_status: COMPLETE_WITH_OPEN_RISKS
primary_eligible: true
best_roles:
  - D0_MEASUREMENT_DEVELOPMENT
  - D1_CONTROL_DISCOVERY
D2:
  public: rejected
  hidden: candidate_pending_custody_audit
critical_unknowns:
  - exact scorer protocol
  - hidden set governance
  - contamination boundary
  - item overlap/public-hidden relationship
```

## Bottom line

AA-Omniscience is potentially more valuable than many classic hallucination benchmarks because scale matters. But its scientific value comes from a properly governed hidden evaluation set, not the public 600 examples.

The public set is a development instrument. The hidden set could become confirmation evidence only after proving that it is actually sealed.
