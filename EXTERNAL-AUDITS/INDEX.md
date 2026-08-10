# External Audit Registry

This registry indexes external evidence. Inclusion means archived/intake-recorded, not accepted.

## Status vocabulary

```text
INTAKE
ADJUDICATION
REPRODUCTION
REMEDIATION
CLOSED
```

Evidence state and disposition live in each audit's own files and must not be inferred from this index.

## Audits

| audit ID | date | executor/model | target | artifact | verdict | workflow state | path |
|---|---|---|---|---|---|---|---|
| EXT-20260809-001 | 2026-08-09 | Hermes Agent / Claude Opus 5 | c6ee5f1daade5bb39632b879613a27895f7ccf83 / v5.4.2 | HASH_RECORDED | STRONG BUT NEEDS FIXES | INTAKE | `2026-08-09/EXT-20260809-001-hermes-opus5/` |

## EXT-20260809-001 artifact identity

```text
submitted filename: AHP-AUDIT-2026-08-09-hermes-opus5.md
size: 43202 bytes
sha256: eaee5c00ffe6d53c9d518f57a8aa71522f4b3839b01c7264a9191dea1c0afee8
artifact state: HASH_RECORDED
raw bytes committed: NO
```

Do not describe this artifact as `RAW_ARCHIVED` until exact original bytes are committed and reverified against the hash.

See:

```text
EXTERNAL-AUDITS/2026-08-09/EXT-20260809-001-hermes-opus5/MANIFEST.json
EXTERNAL-AUDITS/2026-08-09/EXT-20260809-001-hermes-opus5/FINDINGS.md
EXTERNAL-AUDITS/2026-08-09/EXT-20260809-001-hermes-opus5/ADJUDICATION.md
```

## Rule

Never convert:

```text
number of reports -> number of independent confirmations
```

Use `REGISTERS/CORRELATION.md` before making any cross-audit consensus claim.
