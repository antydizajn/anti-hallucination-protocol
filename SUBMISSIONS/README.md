# External audit, test and reproducer intake

This is the preferred machine-friendly route for sending new external evidence to AHP.

Successful intake means only:

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

## Fastest path for an external agent with no write access

Do not ask for collaborator `Write`.

```bash
gh repo clone antydizajn/anti-hallucination-protocol
cd anti-hallucination-protocol
python3 scripts/external_contributor.py start
# perform the selected [AGENT-READY] task
python3 scripts/external_contributor.py submit
```

See `EXTERNAL-CONTRIBUTOR.md` for the complete zero-write flow.

The helper can:

- detect that upstream push is unavailable;
- create/reuse the contributor's fork;
- discover `[AGENT-READY]` work;
- resolve the exact inspection target;
- keep audit target and PR delivery base separate;
- scaffold the submission directory;
- calculate artifact SHA-256 values;
- run this repository's intake validator locally;
- push only to the contributor's fork;
- create an upstream Pull Request and verify the returned PR URL.

For audit/test/reproducer tasks, the canonical directory is:

```text
SUBMISSIONS/INBOX/<submission-id>/
```

Typical contents:

```text
manifest.json
REPORT.md
FINDINGS.json       # when applicable
COMPLETION.json     # when applicable
attachments/        # optional
```

## Manual route

If not using the helper, create a unique directory under `SUBMISSIONS/INBOX/` and open a Pull Request to `main` containing the submission.

Suggested ID:

```text
SUB-YYYYMMDD-<short-source>-<random-or-sequence>
```

The manifest schema is `ahp-external-submission-v1` and records:

- `submission_id`;
- `submission_type`;
- `submitted_at`;
- submitter metadata;
- executor metadata;
- exact target repository/ref/commit where known;
- methodology identity where applicable;
- whether execution actually occurred;
- declared artifacts and SHA-256 values;
- declared findings;
- correlation hints.

Use `UNKNOWN` for facts you cannot establish. Do not invent a model identity, provider, digest, independence claim or execution state merely to satisfy a schema.

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

## Local validation

Run:

```bash
python3 scripts/check_external_submission.py --root SUBMISSIONS/INBOX
```

or let `scripts/external_contributor.py submit` run it automatically.

A passing result means only structural validity.

## Artifact size limit

Each declared artifact must be at most 8 MiB (`MAX_ARTIFACT_BYTES` in
`scripts/check_external_submission.py`). Larger artifacts are rejected instead of
being read into memory during hashing.

If your evidence genuinely exceeds that, split it or reference an external archive
in the report and keep the in-repo artifact to the material excerpt.

## Reproducers and executable files

You may submit reproducer code as an artifact, but generic intake does not execute it.

```text
RECEIVED CODE != SAFE TO EXECUTE
```

Execution belongs to a separately authorized reproduction phase in a disposable environment.

## Fork Pull Request security

External submissions use normal `pull_request` CI with minimal/read-only permissions where possible.

Do not change the external intake path to privileged `pull_request_target` merely to access secrets or write credentials.

Fork PRs must not receive maintainer secrets merely because they contain a valid manifest.

## Human-friendly route

If preparing JSON is undesirable, use the repository Issue Form `External audit / test submission`.

Maintainers may later normalize that material into a machine-readable submission. Normalization is not byte-identical archival evidence unless exact source bytes were preserved and verified.

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
