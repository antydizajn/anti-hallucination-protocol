# Gate 1 Exit Criteria

## Status

Normative transition gate.

Gate 1 asks:

> Do we have a defensible measurement landscape and evidence pool assignment before designing or claiming intervention efficacy?

Gate 1 does NOT ask:

> Does AHP work?

No treatment efficacy conclusion is permitted from Gate 1.

---

# Required artifacts

Gate 1 cannot close without:

```text
benchmark registry
benchmark review records
lineage records
contamination ledger
grader risk register
pool assignment record
source provenance record
```

---

# Mandatory properties

## 1. Construct clarity

Every primary candidate must have:

```text
measured construct
non-measured adjacent constructs
scoring unit
answerability semantics
failure interpretation
```

No benchmark enters primary consideration through name similarity.

---

## 2. Evidence pool separation

Every benchmark must belong to exactly one current pool:

```text
D0_MEASUREMENT_DEVELOPMENT
D1_CONTROL_DISCOVERY
D2_CONFIRMATORY_CANDIDATE
T_TRANSFER_CANDIDATE
EXCLUDE
```

A benchmark may change pools only through a recorded review decision.

---

## 3. Lineage accounting

The project must know:

```text
how many benchmark names exist
how many data lineages exist
how many grader lineages exist
how many genuinely independent evidence families exist
```

The final count is not benchmark count.

---

## 4. Contamination accounting

Before any D2 promotion:

Required:

```text
item exposure assessment
designer exposure assessment
answer-key exposure assessment
leaderboard exposure assessment
model-training exposure assessment
intervention leakage assessment
```

Unknown contamination cannot silently become clean holdout status.

---

## 5. Grader readiness

Every primary metric requires:

```text
grader identity
grader revision
failure modes
validation plan
arm-bias risk assessment
```

A convenient grader is not automatically a valid measurement instrument.

---

## 6. Positive/negative balance assessment

Every abstention-sensitive candidate must document:

```text
should-answer cases
should-abstain cases
false-premise cases
underspecified cases
clarification-needed cases
```

A system improving only by refusing is not automatically improved.

---

## 7. Degenerate baseline assessment

Before primary admission where relevant:

Evaluate whether trivial strategies dominate:

```text
always abstain
always answer
always tool
never tool
copy context
surface heuristics
```

If yes, add guardrails or downgrade.

---

## 8. No hidden transformation

The adapter contract must show:

```text
source task
normalization
transformation
treatment injection
scoring
```

Semantic changes require explicit review.

---

# Gate 1 PASS conditions

All must be true:

```text
measurement inventory exists
benchmark roles are explicit
lineage is recorded
contamination is recorded
primary candidates pass review
unknowns are visible
no intervention efficacy claim is made
```

---

# Gate 1 FAIL conditions

Any of:

```text
benchmark count used as evidence count
public benchmark treated as sealed automatically
old AHP tests treated as efficacy proof
LLM judge treated as oracle
unknown contamination ignored
lineage not mapped
answerability not defined
scoring invented after seeing results
```

---

# Gate 1 output

The final artifact is:

```yaml
measurement_landscape_status:
primary_candidate_count:
secondary_candidate_count:
development_only_count:
excluded_count:
independent_lineage_count:
critical_unknowns:
open_risks:
next_gate_eligibility:
```

A PASS permits moving to:

```text
Gate 2 - preregistration and frozen causal contract
```

It does not permit:

```text
claiming efficacy
shipping treatment
announcing improvement
```

---

# Interpretation invariant

```text
GOOD LANDSCAPE != GOOD EXPERIMENT
GOOD EXPERIMENT != POSITIVE RESULT
POSITIVE RESULT != GENERALIZATION
GENERALIZATION != UNIVERSALITY
```
