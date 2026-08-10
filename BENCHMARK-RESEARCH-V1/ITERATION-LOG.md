# Benchmark Research Iteration Log

## Iteration 0

### Initial idea

Use AA-Omniscience as central hallucination benchmark.

### Evaluation

Rejected.

Reason:

AA is valuable but measures one narrow axis:

parametric factual knowledge + abstention.

It does not measure:

- grounding
- evidence conflict
- tool reliability
- temporal state
- citation entailment
- agentic failures

Score: 4/10

---

## Iteration 1

### Idea

Combine many existing hallucination benchmarks into one score.

### Evaluation

Rejected.

Problem:

Different benchmarks measure different constructs.

Combining them hides failure modes.

Score: 6/10

---

## Iteration 2

### Idea

Layered benchmark architecture.

Each benchmark family maps to a failure mechanism.

### Evaluation

Accepted direction.

Score: 8.5/10

Remaining issues:

- noisy real-world labels
- evaluator reliability
- contamination
- runtime variance

---

## Iteration 3

### Final direction

Three-dimensional evaluation:

1. Real-world benchmarks
2. Controlled reference-world benchmarks
3. AHP-specific adversarial transition tests

Accepted.

Score: 9.5/10

Missing only empirical validation.

---

# Permanent rules

Never:

- claim benchmark score equals truth
- treat public benchmark as unseen evidence
- reward refusal without coverage metrics
- use one LLM judge as oracle
- mix detector benchmarks with prevention benchmarks

Always:

- preserve raw evidence
- record benchmark identity
- separate runtime failure from epistemic failure
- report limitations
