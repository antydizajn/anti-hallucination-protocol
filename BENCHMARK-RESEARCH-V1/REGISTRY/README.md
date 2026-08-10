# AHP Benchmark Registry v1

## Purpose

This registry is a research inventory, not a bag of benchmarks to run blindly.

The central rule is:

```text
DISCOVERED != VERIFIED != SUITABLE != SELECTED != CONFIRMATORY
```

A benchmark can be famous, relevant and still be the wrong instrument for a specific AHP claim.

## Authority levels

Every entry has one of four roles:

```text
CORE
SUPPORTING
DIAGNOSTIC
CANDIDATE
```

### CORE

Directly measures a construct that is load-bearing for AHP evaluation and has been reviewed against a primary source.

CORE does not mean contamination-free. Public CORE benchmarks remain public-exposed evidence.

### SUPPORTING

Useful external construct coverage, but not sufficient as a primary AHP effectiveness endpoint by itself.

Examples include general QA, long-context and agent task-success benchmarks that can provide guardrails or paired slices.

### DIAGNOSTIC

Primarily evaluates detectors, judges, attribution systems or internal subcomponents rather than the prevention effect of loading AHP.

Diagnostic instruments are useful for validating the evaluation stack.

### CANDIDATE

Potentially relevant instrument that has not completed primary-source review for this branch.

A CANDIDATE entry MUST NOT be wired into a confirmatory runner.

## Verification states

```text
PRIMARY_VERIFIED
SECONDARY_VERIFIED
CANDIDATE_PENDING_PRIMARY_REVIEW
REJECTED_FOR_PRIMARY_USE
RETIRED
```

Only `PRIMARY_VERIFIED` entries may be selected as confirmatory external instruments without an additional review step.

## Registry fields

Minimum fields:

```yaml
id: stable_machine_id
name: human readable name
family: benchmark family
role: CORE | SUPPORTING | DIAGNOSTIC | CANDIDATE
verification: verification state
primary_source: URL or null
exposure_class: PUBLIC_REPRODUCIBLE | ROTATING_DYNAMIC | PRIVATE_CONFIRMATORY | MIXED | UNKNOWN
construct: concise statement of what the instrument measures
ahp_use: intended AHP role
primary_risk: most important validity limitation
```

Optional fields may later include:

```yaml
paper_revision:
dataset_revision:
license:
public_size:
private_size:
grader_type:
tool_mode:
languages:
domains:
source_checked_on:
notes:
```

## Eligibility gate

An external benchmark becomes runnable only after all of these are resolved:

```text
PRIMARY SOURCE VERIFIED
DATASET REVISION PINNED
LICENSE/ACCESS REVIEWED
TASK CONSTRUCT MAPPED
SCORER SEMANTICS MAPPED
CONTAMINATION CLASS RECORDED
EXPECTED TOOL MODE FIXED
KNOWN LIMITATIONS WRITTEN
```

## Primary-source requirement

Survey papers, leaderboard pages, blog summaries and third-party benchmark lists are discovery aids.

They do not satisfy primary verification when an original paper, official dataset card or official project repository exists.

## No numeric prestige ranking

This registry intentionally does not assign a universal `quality_score`.

A controlled synthetic benchmark and a noisy real-world benchmark can both be excellent while optimizing different validity properties.

Selection is based on construct fit, not prestige.

## Real-world plus reference-world rule

A serious AHP evaluation should include both:

```text
REAL-WORLD EVIDENCE
REFERENCE-WORLD EVIDENCE
```

Real-world instruments provide ecological validity.

Reference-world instruments provide deterministic or tightly controlled truth conditions.

Neither substitutes for the other.

## Core selection target

The first implementation should remain small enough to audit end-to-end.

A plausible initial external core is approximately 10-15 instruments spanning:

- parametric factuality;
- abstention/calibration;
- temporal/search;
- grounding/conflict;
- long-form factuality;
- citation;
- tool/agent reliability;
- prompt injection;
- reference-world state.

The broader 100+ landscape exists to prevent tunnel vision, not to justify running 100 benchmarks at once.
