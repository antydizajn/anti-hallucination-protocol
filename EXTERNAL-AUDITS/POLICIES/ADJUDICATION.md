# External Audit Adjudication Protocol

## Purpose

Convert reported findings into explicit project evidence states without conflating submission, reproduction, acceptance, and remediation.

## Three separate dimensions

### 1. Artifact state

```text
RAW_ARCHIVED
NORMALIZED_ONLY
HASH_RECORDED
INCOMPLETE
```

### 2. Evidence state

```text
REPORTED
REPRODUCER_AVAILABLE
REPRODUCED
CROSS_CONFIRMED
FILE_VERIFIED
INFERENCE
HEURISTIC
UNVERIFIED
REJECTED
SUPERSEDED
```

### 3. Disposition

```text
OPEN
ACCEPTED_FOR_REMEDIATION
ACCEPTED_AS_LIMIT
DUPLICATE
REJECTED_AS_NON_BUG
REJECTED_BAD_REPRODUCER
PATCHED
REGRESSION_ADDED
FULL_GATE_VERIFIED
RELEASED
DEFERRED
```

These dimensions must never be collapsed into one status.

## Evidence ranking

Use this default ordering for factual/project claims:

```text
REPRODUCED
> CROSS_CONFIRMED
> FILE_VERIFIED
> INFERENCE
> HEURISTIC
> UNVERIFIED
```

A report's severity is not evidence strength.

A P1 with no reproducer can remain `REPORTED`.
A P3 with a clean reproducer can be `REPRODUCED`.

## Required adjudication record

Each finding should have:

```text
finding_id
auditor_finding_id
reported_severity
project_severity
reported_mechanism
project_interpretation
reproducer_status
reproducer_pointer
correlation_notes
evidence_state
disposition
affected_surface
fix_commit
regression_test
verification_evidence
release_tag
residual_risk
```

Unknown fields stay `UNKNOWN`; do not guess.

## Reproduction standard

For deterministic bugs, prefer:

```text
reported finding
-> independent minimal reproducer
-> observed incorrect behavior
-> mechanism isolated
-> patch
-> original reproducer blocked
-> close variant blocked where material
-> negative/control case still valid
-> full test/integrity/provenance/liveness gate
```

Only then use `FULL_GATE_VERIFIED`.

## Rejecting a finding

A finding may be rejected when:

- the reproducer is invalid;
- the claimed expected behavior contradicts the declared contract;
- the report confuses a documented limitation with a deterministic bug;
- the finding targets an artifact outside the declared release boundary;
- the claimed failure cannot be reproduced and stronger evidence contradicts it.

Record the rejection reason. Never delete the raw report because a finding was rejected.

## Correlated audits

Do not treat report count as evidence count.

Record shared factors such as:

```text
same canonical prompt
same operator
same model family
same provider/runtime
same target snapshot
same source set
same historical audit exposure
same reproducer copied between reports
```

Cross-confirmation should mean materially independent observation or reproduction, not repeated agreement.

## Remediation boundary

External reports diagnose. Remediation is a separate project action.

Do not edit `main` merely because a report exists.

When a finding is accepted, open a distinct remediation path and preserve exact links back to:

```text
audit_id
finding_id
reproducer
patch commit
regression
release evidence
```
