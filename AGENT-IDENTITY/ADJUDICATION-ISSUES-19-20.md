# Agent identity issue adjudication draft

## Issue #19 - SIGNED != FRESH

Decision: ACCEPT_AS_LIMIT

The verifier proves key-bound identity at signing time. It does not provide replay protection, uniqueness, ordering, or freshness guarantees.

Action:
- document `VALID SIGNATURE != FRESH MESSAGE`;
- keep replay policy in consumer/transport layer unless a specific verifier contract requires otherwise.

## Issue #20 - Envelope fields outside signed object

Decision: ACCEPT_FOR_REMEDIATION

The design choice of detached signature metadata is valid, but the envelope boundary should be machine-enforced.

Action:
- reject unknown top-level fields;
- document that only `signed` is authenticated;
- avoid future trust decisions based on unsigned envelope metadata.

Boundary:

VALID SIGNATURE != ALL ENVELOPE DATA AUTHENTICATED
