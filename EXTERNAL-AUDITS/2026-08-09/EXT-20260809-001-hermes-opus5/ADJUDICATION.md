# Adjudication Record

Audit ID: `EXT-20260809-001`

## Audit-level status

```text
artifact_state: HASH_RECORDED
adjudication_status: NOT_STARTED
canonical_project_impact: NONE_YET
```

No finding in this file is accepted merely because the submitted report labels it P1/P2/P3.

The raw submitted artifact is not yet committed byte-for-byte on this branch, so the archive must not claim `RAW_ARCHIVED`.

## Finding status

| finding | evidence state | disposition | project note |
|---|---|---|---|
| EXT-20260809-001-F01 | REPORTED | OPEN | Needs independent reproduction against an exact target snapshot. |
| EXT-20260809-001-F02 | REPORTED | OPEN | Needs reproduction plus precise liveness threat-model boundary. |
| EXT-20260809-001-F03 | REPORTED | OPEN | Needs reproduction and contract adjudication: regex correctness vs verification vacuity. |
| EXT-20260809-001-F04 | REPORTED | OPEN | Needs reproduction and integrity-scope adjudication. |
| EXT-20260809-001-F05 | REPORTED | OPEN | Needs reproduction; proposed fix must distinguish `memory` from legitimate user-supplied primary evidence. |
| EXT-20260809-001-F06 | REPORTED | OPEN | Needs semantic contract decision for `--kind any`. |
| EXT-20260809-001-F07 | REPORTED | OPEN | Needs reproduction and decision about how much semantic policy integrity can reasonably be deterministic. |
| EXT-20260809-001-F08 | REPORTED | OPEN | Needs reproduction; likely error-category handling issue if confirmed. |
| EXT-20260809-001-F09 | REPORTED | OPEN | Primarily runtime/observability roadmap unless a deterministic false claim is demonstrated. |
| EXT-20260809-001-F10 | REPORTED | OPEN | Host-local observation, not automatically a repository defect. |

## Required next step

Do not patch `main` from this document.

First perform an authorized reproduction pass and write the observed results here or in a linked reproduction record. State transitions must be evidence-driven.
