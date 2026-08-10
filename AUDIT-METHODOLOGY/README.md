# Audit Methodology

This directory is the canonical control plane for independent audits of Anti-Hallucination Protocol.

It is intentionally separate from audit evidence and historical reports.

```text
AUDIT-METHODOLOGY/** = how audits are performed
AUDITS/**             = canonical project audit history / synthesis / release evidence
EXTERNAL-AUDITS/**    = external submissions and their adjudication on the external-audits branch
```

Core separation:

```text
AUDIT INSTRUCTIONS != AUDIT EVIDENCE
AUDITOR REPORT      != VERIFIED FINDING
REPORTED            != REPRODUCED
PATCHED             != REGRESSION VERIFIED
```

## Canonical files

- `CANONICAL-AGENT-AUDIT-PROMPT.md` - current blind-first forensic audit prompt. This is the copy-paste artifact for independent agents.
- `REPORT-CONTRACT.md` - required human-readable and machine-readable output contract.
- `BEHAVIORAL-EVALUATION-PROTOCOL.md` - separate protocol for measuring model behavior and AHP effect. A forensic repo audit is not automatically a behavioral benchmark.
- `PROMPT-DESIGN-HISTORY.md` - design lineage and rationale. Do not give this file to an auditor before its blind phase.

## Blindness boundary

During Phase A, the auditor may inspect the live implementation, tests, CI, README, SKILL, references, and executable helpers necessary to understand and attack the current target.

The auditor must not consume prior conclusions from:

```text
AUDITS/**
EXTERNAL-AUDITS/**
prior agent reports
adjudication ledgers
remediation summaries that disclose prior findings
review threads containing prior audit conclusions
PROMPT-DESIGN-HISTORY.md
```

The canonical prompt itself is not prior evidence. That is why it lives outside `AUDITS/**`.

## Target modes

The methodology is release-agnostic. Every audit must explicitly choose one target mode:

```text
CURRENT_MAIN
RELEASE_TAG
EXACT_COMMIT
```

The auditor records the resolved commit and the version observed in `SKILL.md`. It must not silently reinterpret current `main` as a historical release.

## Canonicality

The canonical public source for methodology is `main` after the methodology change is merged.

For a comparative multi-model round, pin the exact methodology commit or blob identity and give every auditor the same canonical prompt bytes. A URL to a mutable branch name alone is not sufficient provenance for a strict comparison.

## Evidence maxim

> **One reproducer outranks five opinions.**

Agent count is not independence. Shared prompt, operator, model family, provider/runtime, source set, target snapshot, or reproducer lineage can create correlated failure domains.
