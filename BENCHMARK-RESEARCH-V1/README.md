# AHP Benchmark Research v1

## Status

Research and specification phase.

This branch does not claim benchmark results.
It defines the research foundation for a future Anti-Hallucination Protocol evaluation system.

## Core principle

A single hallucination score is rejected.

AHP evaluation must separate failure families:

- parametric factuality
- knowledge boundary and abstention
- calibration
- temporal freshness
- grounding
- conflicting evidence
- long-form factuality
- citation entailment
- tool failures
- agentic failures
- prompt injection in evidence
- user pressure and sycophancy

## Design rule

`benchmark score != scientific evidence by itself`

Every result must preserve:

- benchmark identity
- revision/hash
- evaluator identity
- model/provider identity
- runtime conditions
- contamination status
- limitations

## Initial deliverables

Planned:

1. benchmark taxonomy
2. benchmark registry
3. scoring contract
4. contamination policy
5. AHP-native adversarial battery specification
6. experimental design
7. evaluator reliability policy

## Known rejected approaches

- one universal hallucination score
- treating HaluEval-style detection as prevention evidence
- treating public datasets as held-out proof
- rewarding abstention without usefulness metrics
- LLM judge as unquestionable oracle
- benchmark results without runtime boundary labels

## Relationship to existing INTERNAL-AUDITS

This work intentionally starts separately from previous benchmark material.
Existing designs are treated as input evidence, not as ground truth.

Known methodological risks include:

- abstention imbalance
- benchmark leakage
- missing operational metric definitions
- insufficient positive controls
- treatment confounds

These are design constraints for v1.
