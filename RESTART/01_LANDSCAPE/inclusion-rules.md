# Gate 1 - Benchmark Inclusion Rules

## Purpose

This document defines admission criteria for benchmark candidates during measurement landscape construction.

A benchmark is not included because it is popular.

A benchmark is not included because it produces a convenient result.

A benchmark is included only when its measurement properties can be inspected.

## Rule 1 - Construct first

Every candidate must answer:

```text
What latent construct does this measure?
```

Examples:

```text
unsupported commitment
failure to abstain when evidence is insufficient
fabrication of citations
RAG evidence mismatch
false premise handling
```

A generic "hallucination score" without construct definition is not sufficient.

## Rule 2 - Measurement boundaries

Every candidate must document:

```text
measures:

and:

does not measure:
```

Example:

A citation benchmark may measure citation entailment.

It does not automatically measure general factual reliability.

## Rule 3 - Positive and negative behavior

Hallucination research must not reward only refusal.

Candidate instruments should record:

```text
answerable cases
unanswerable cases
partial-answer cases
uncertain cases
```

A benchmark vulnerable to always-abstain exploitation cannot be the sole primary endpoint.

## Rule 4 - Grading transparency

Required:

- scoring method;
- grader identity;
- version pinning possibility;
- known grader limitations;
- human validation where available.

LLM judges require additional review.

Multiple LLM judges do not automatically equal independent evidence.

## Rule 5 - Lineage before diversity count

Ten benchmarks from one source family are not ten independent measurements.

Record:

```text
upstream datasets
shared generation pipeline
shared grader
shared authorship
shared items
```

## Rule 6 - Contamination classification

Every candidate receives:

```text
C0
C1
C2
C3
CX
```

Classification is not a claim of certainty.

It is a documented contamination-risk state.

## Rule 7 - Confirmatory eligibility

A benchmark cannot enter D2 candidate status if:

- intervention designers inspected item-level content;
- attack classes were extracted from it;
- results influenced treatment design;
- answer keys influenced prompt construction.

## Rule 8 - Dynamic and temporal evaluation

Static public benchmarks are useful for:

- development;
- comparison;
- calibration;
- historical analysis.

They require stronger justification for confirmatory generalization claims.

## Rule 9 - Cost and reproducibility

Record:

- compute cost;
- API cost;
- runtime;
- required tools;
- external dependencies;
- reproducibility constraints.

## Rule 10 - Explicit rejection is data

Rejected candidates must remain recorded.

Reasons include:

```text
unclear construct
unreliable labels
contamination risk
no positive evidence cases
refusal exploitation
unverifiable grader
license failure
shared lineage duplication
```

A benchmark landscape without rejection history is incomplete.
