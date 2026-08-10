# Findings Ledger

Audit ID: `EXT-20260809-001`

| archive finding | auditor finding | reported severity | title | reported mechanism | reproducer | evidence state | disposition |
|---|---|---|---|---|---|---|---|
| EXT-20260809-001-F01 | F-N01 | P1 | Canonical schema content unpinned | Canonical evidence schema can be semantically widened/gutted while advertised gates remain green | yes, in submitted report | REPORTED | OPEN |
| EXT-20260809-001-F02 | F-N02 | P2 | Liveness cannot detect lying critical verifier | Stubbed/targeted-trojan helpers can satisfy current liveness coverage while lying outside canaries | yes | REPORTED | OPEN |
| EXT-20260809-001-F03 | F-N03 | P2 | Vacuous regex earns FOUND | Regexes matching empty input/zero-width conditions can return FOUND on arbitrary content | yes | REPORTED | OPEN |
| EXT-20260809-001-F04 | F-N08 | P2 | Integrity can pass with broken provenance dependency | Removing arxiv manifest leaves integrity/liveness PASS while provenance checker cannot run | yes | REPORTED | OPEN |
| EXT-20260809-001-F05 | F-N09 | P2 | T3 strong record from memory/self-report labels | Strong T3 structural validity can be reached using memory as sole support if optimistic metadata are supplied | yes | REPORTED | OPEN |
| EXT-20260809-001-F06 | F-N06 | P3 | Dangling symlink FOUND under kind any | lexists semantics classify dangling symlink as existing under `--kind any` | yes | REPORTED | OPEN |
| EXT-20260809-001-F07 | F-N07 | P3 | Policy contract partly substring-based | State tokens in comments can satisfy integrity presence checks; inverted policy can survive integrity/provenance/liveness but fails pytest | yes | REPORTED | OPEN |
| EXT-20260809-001-F08 | F-N10 | P3 | Custom-schema crash category mismatch | Permissive caller schema can lead to KeyError and exit 1 instead of verifier ERROR exit 2 | yes | REPORTED | OPEN |
| EXT-20260809-001-F09 | F-N04 | P2 roadmap | No machine-checkable startup-load verification | Startup activation remains human-observed/documented rather than machine-checked | documented | REPORTED | OPEN |
| EXT-20260809-001-F10 | F-N05 | local-state observation | Audited repo differs from installed local AHP lineage | Host had unrelated installed v2.1.0 and startup did not load audited v5.4.2 | observed in report | REPORTED | OPEN |

## Important

This ledger records what the auditor reported. It does **not** assert that project maintainers independently reproduced or accepted any finding.

Next legitimate state transition for deterministic findings:

```text
REPORTED -> REPRODUCER_AVAILABLE -> REPRODUCED / REJECTED
```
