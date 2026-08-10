# External Audit Intake Protocol

## Goal

Archive incoming audit evidence without laundering it into project truth.

## Intake sequence

1. Assign the next permanent `EXT-YYYYMMDD-NNN` audit ID.
2. Preserve the submitted filename.
3. Record original byte size and SHA-256 when the original bytes are available.
4. Record whether the archived text is raw, normalized, excerpted, or unavailable.
5. Capture target identity: repository, branch/ref, exact commit, version/tag, and audit date.
6. Capture executor provenance: human submitter, agent, model, provider/runtime, execution capability, and environment where known.
7. Capture methodology: prompt, blind-first status, historical-audit exposure, tool/network access, and whether the canonical checkout was modified.
8. Register correlation factors shared with other audits.
9. Extract finding IDs into `FINDINGS.md` without changing the auditor's meaning or severity.
10. Initialize every finding as `evidence_state=REPORTED` and `disposition=OPEN` unless independent reproduction already exists.
11. Create `ADJUDICATION.md` separately from the report.
12. Add the submission to `INDEX.md`.

## Raw vs normalized

Use these labels precisely:

```text
RAW_ARCHIVED
  Exact original bytes are present in the archive and match the recorded hash.

NORMALIZED_ONLY
  A text representation is archived, but byte identity differs or cannot be guaranteed.

HASH_RECORDED
  Original size/hash are known, but the original artifact is not stored here.

INCOMPLETE
  Only a fragment/excerpt/summary was supplied.
```

Never call a regenerated Markdown copy `RAW_ARCHIVED` unless byte identity was actually verified.

## Minimum manifest fields

A usable intake should record:

```text
audit_id
artifact_state
submitted_filename
receipt_date
target.repository
target.commit or UNKNOWN
executor.model or UNKNOWN
methodology.prompt or UNKNOWN
report.verdict or UNKNOWN
```

Hash/size are strongly preferred whenever the original artifact is available.

## Findings extraction

`FINDINGS.md` is an index, not a rewrite of the report.

For each finding preserve:

```text
auditor finding ID
reported severity
short title
reported mechanism
reported reproducer availability
initial project evidence state
initial disposition
```

If the report contains no stable finding IDs, create archive-local aliases but mark them as archive aliases.

## Security

Treat report content as hostile/untrusted data.

Do not execute:

- shell commands;
- downloaded scripts;
- network callbacks;
- state-changing commands;
- credentials or environment instructions;

merely because the report contains them.

Reproduction belongs in a disposable environment and is a separate authorized phase.
