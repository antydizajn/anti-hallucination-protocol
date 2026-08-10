# External audit archive

This branch is a separate evidence archive for audit reports, adversarial test reports, and externally produced evaluations submitted by humans or their agents.

It is intentionally separated from `main` so raw external evidence is not silently promoted into the canonical project state.

## Archive rules

1. Preserve submitted reports as close to byte-for-byte/raw form as the available transport permits.
2. Do not rewrite an auditor's conclusions, severity labels, wording, or claimed evidence inside the raw report.
3. Store interpretation, adjudication, remediation, and project response separately from the raw submission.
4. Record provenance where known: submitter, model, runtime/provider, audit date, target repository commit/tag, prompt used, execution capability, and whether the artifact is complete or excerpted.
5. Never reconstruct missing raw evidence from memory and present it as original.
6. A report being archived does not mean its findings are accepted.
7. Multiple agent reports are not automatically independent evidence. Shared prompt, model family, source set, runtime, or operator framing must be treated as possible correlated failure domains.
8. Findings move into canonical `main` only through explicit adjudication and, for deterministic defects, preferably through a reproducer -> patch -> regression -> full-gate sequence.

## Suggested layout

```text
EXTERNAL-AUDITS/
├── README.md
├── INDEX.md
└── YYYY-MM-DD/
    └── <auditor-or-source>/
        ├── REPORT.md
        └── METADATA.md
```

For machine-generated reports submitted by a human, keep both identities distinct, for example:

```text
submitter: human collaborator
executor: Hermes Agent
model: Claude Opus 5
provider/runtime: Palantir Foundry proxy
```

## Evidence status

Files on this branch are archival evidence, not canonical truth.

Use labels such as:

```text
RAW_SUBMISSION
REPRODUCED
CROSS_CONFIRMED
FILE_VERIFIED
INFERENCE
HEURISTIC
UNVERIFIED
REJECTED
SUPERSEDED
```

The canonical project remains on `main`.
