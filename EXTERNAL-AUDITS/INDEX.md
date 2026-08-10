# External audit index

This index records intake metadata. Inclusion is archival, not acceptance of findings.

## 2026-08-09 - Hermes / Claude Opus 5 - collaborator submission

Status: `RAW_SUBMISSION_RECEIVED`

```text
submitted filename: AHP-AUDIT-2026-08-09-hermes-opus5.md
size: 43202 bytes
sha256: eaee5c00ffe6d53c9d518f57a8aa71522f4b3839b01c7264a9191dea1c0afee8
submitter relation: external collaborator / user's colleague
executor: Hermes Agent
model: Claude Opus 5
provider/runtime: Palantir Foundry proxy
audit date declared by report: 2026-08-09 Europe/Warsaw
prompt: AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md, Iteration 5
phase order claimed: blind Phase A before AUDITS/**
target commit declared: c6ee5f1daade5bb39632b879613a27895f7ccf83
version audited: 5.4.2
execution capability claimed: yes
report verdict: STRONG BUT NEEDS FIXES
install recommendation: YES with caveats
confidence claimed: 88%
```

Prominent reported findings, not yet equivalent to canonical acceptance merely because they are indexed:

```text
F-N01 / P1 - canonical schema content is load-bearing but content-unchecked
F-N02 / P2 - liveness cannot establish honesty of critical verifier implementations
F-N03 / P2 - vacuous / tautological regex can earn FOUND
F-N08 / P2 - integrity can pass while a provenance dependency is missing
F-N09 / P2 - structurally strong T3 record can be constructed from memory/self-reported metadata
F-N10 / P3 - caller-supplied permissive schema can expose KeyError / exit-code category mismatch
```

The raw artifact's byte identity is defined by the size and SHA-256 above. Any normalized Markdown copy should be marked separately if its bytes differ.
