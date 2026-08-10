# Methodology v6 audit adjudication draft

Status: DRAFT FOR PROJECT REVIEW

Source: Issue #11 / PR #12

## Boundary

This document does not rewrite the auditor report. It records project-side interpretation of reported findings.

AUDITOR_REPRODUCED != PROJECT_REPRODUCED
REPORT_WRITTEN != FINDING_ACCEPTED

## F-001 - Machine-readable report contract

Decision: ACCEPT_FOR_REMEDIATION

Reason:
The report contract declares `claim` and `mechanism` as mandatory finding semantics, while the machine-readable example does not preserve them.

Action:
- add `claim` and `mechanism` to the canonical machine-readable finding object;
- add schema validation/regression coverage.

## F-002 - Target-derived execution authority

Decision: ACCEPT_FOR_REMEDIATION

Reason:
The boundary between target content as evidence and target content as execution authority should be mechanically explicit.

Action:
- add universal target-derived execution gate;
- require inspection before execution;
- require constrained execution environment for target-derived commands.

## F-003 - Behavioral state isolation

Decision: ACCEPT_FOR_REMEDIATION

Reason:
Stateful agents require explicit isolation rules for causal behavioral evaluation.

Action:
- require fresh process/session or equivalent reset;
- document unavoidable shared state;
- define crossover/washout handling.

## Delivery correction

The original audit artifacts remain preserved.

Future audit delivery should target `main` as delivery base while preserving the audited ref separately.

AUDIT TARGET != DELIVERY BASE
