# External audit, test and reproducer intake

This is the preferred machine-friendly route for sending new external evidence to the project.

A submission being accepted by the intake validator means only:

```text
STRUCTURALLY_VALID_SUBMISSION
```

It does not mean:

```text
finding true
finding reproduced by project
severity accepted
patch required
bug fixed
```

## Preferred route - pull request

Create a unique directory:

```text
SUBMISSIONS/INBOX/<submission-id>/
```

Minimum:

```text
manifest.json
REPORT.md
```

Additional attachments/reproducers are allowed as declared artifacts. Do not require the project to execute them during intake.

Suggested ID:

```text
SUB-YYYYMMDD-<short-source>-<random-or-sequence>
```

Example:

```text
SUB-20260810-opus5-a1b2
```

Then open a pull request to `main` containing only the submission unless a maintainer explicitly requests other changes.

The PR intake workflow validates the submission structure and hashes. It deliberately does not execute submitted scripts or binaries.

## Manifest

Example:

```json
{
  "schema": "ahp-external-submission-v1",
  "submission_id": "SUB-20260810-opus5-a1b2",
  "submission_type": "FORENSIC_AUDIT",
  "submitted_at": "2026-08-10T03:00:00+02:00",
  "submitter": {
    "type": "HUMAN",
    "name": "external collaborator"
  },
  "executor": {
    "type": "AGENT",
    "model": "Claude Opus 5",
    "provider_runtime": "UNKNOWN"
  },
  "target": {
    "repository": "https://github.com/antydizajn/anti-hallucination-protocol",
    "ref": "main",
    "commit": "UNKNOWN"
  },
  "methodology": {
    "name": "UNKNOWN",
    "version": "UNKNOWN",
    "commit": "UNKNOWN"
  },
  "execution_occurred": true,
  "artifacts": [
    {
      "path": "REPORT.md",
      "sha256": "<64 lowercase hex chars or UNKNOWN>"
    }
  ],
  "declared_findings": [
    {
      "id": "F-001",
      "severity": "P2",
      "title": "example"
    }
  ],
  "correlation_hints": [
    "shared canonical prompt with other agents"
  ]
}
```

## Allowed submission types

```text
FORENSIC_AUDIT
BEHAVIORAL_EVALUATION
REPRODUCER
TEST_CASE
RESEARCH_REVIEW
DOCUMENT_REVIEW
OTHER
```

## Hashes

If you know exact artifact bytes, provide lowercase SHA-256.

If you do not, use:

```text
UNKNOWN
```

Do not fabricate a digest merely to satisfy the manifest.

The validator recomputes every declared non-UNKNOWN hash.

## Reproducers and executable files

You may submit a reproducer as an artifact, but the intake workflow does not execute it.

This is deliberate:

```text
RECEIVED CODE != SAFE TO EXECUTE
```

Execution happens only in a separate, authorized reproduction phase in a disposable environment.

## Human-friendly route

If you do not want to prepare JSON, open the repository issue form:

```text
External audit / test submission
```

Maintainers may later normalize that report into a machine-readable submission. The normalized record must preserve that it was normalized and must not pretend to be byte-identical raw evidence unless verified.

## Project-side lifecycle

```text
RECEIVED
-> STRUCTURALLY_VALID_SUBMISSION
-> TRIAGED
-> independently REPRODUCED / REJECTED / UNVERIFIED
-> ACCEPTED_FOR_REMEDIATION where appropriate
-> PATCHED
-> REGRESSION_ADDED
-> FULL_GATE_VERIFIED
-> RELEASED
```

No stage is implied merely by the existence of the next one.
