# Canonical Audit Prompt Design History

This file preserves the design lineage of the canonical audit methodology.

It is NOT the prompt to give auditors during blind Phase A.

The exact previous canonical artifact remains available in Git history at the prior path:

```text
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md
```

Previous canonical blob identity before the v6 methodology split:

```text
blob sha: 6e0b0d6fc75c5e3d9142745e6be1399dd1bc6df2
canonical generation: Iteration 5
```

## Iteration 1

Primary changes:
- strict repository boundary;
- evidence labels;
- false-positive focus;
- read-only audit;
- explicit reproducer requirements.

Main design principle introduced:

> One reproducer outranks five opinions.

## Iteration 2

Added:
- fresh clone;
- blind-first Phase A;
- environment fingerprint;
- exact commit identity;
- baseline execution;
- historical reconciliation only after independent hypotheses/probes.

This prevented prior audits from becoming the hypothesis generator for every subsequent model.

## Iteration 3

Added systematic adversarial families:
- narrow verifier false positives/negatives;
- evidence-record state attacks;
- schema/checker drift;
- frontmatter/release integrity;
- liveness;
- research provenance;
- cross-component contradictions.

It also introduced explicit minimum probe counts. Those counts were useful while bootstrapping coverage, but v6 removes quota-driven methodology in favor of materially distinct failure classes.

## Iteration 4

Added:
- runtime/load distinction;
- operator/user pressure cases;
- current-state checks;
- correlated-source cases;
- long-context cases;
- explicit rejection of `human = truth oracle`.

This iteration correctly separated external observation, provenance, evaluator independence, and human governance.

## Iteration 5

Became the first canonical copy-paste comparative prompt.

It added:
- full blind-first forensic sequence;
- test-the-tests requirement;
- false-positive and false-negative ledgers;
- severity framework;
- required final report structure;
- hard stop before remediation.

Known design debt discovered after use:

1. The canonical prompt itself lived under `AUDITS/**` while instructing blind auditors not to read `AUDITS/**`.
2. It mixed prompt-design history with the production copy-paste prompt.
3. It retained `v5.4.1+` and fixed-v5.4.1 wording after the project advanced.
4. It hardcoded baseline commands before telling the auditor to discover the current snapshot.
5. It did not explicitly treat `EXTERNAL-AUDITS/**` as prior evidence contamination.
6. Severity did not sufficiently separate impact from exploit/precondition/threat-model applicability.
7. Runtime diagnostics and independent behavioral-effectiveness testing were too close together.
8. The final report was human-readable but not optimized for deterministic external-audit intake.
9. Fixed probe quotas could encourage quantity gaming.
10. The target repository as untrusted data was not explicit enough in the audit control plane.

## Methodology v6

The v6 split addresses those issues by creating:

```text
AUDIT-METHODOLOGY/
├── README.md
├── CANONICAL-AGENT-AUDIT-PROMPT.md
├── REPORT-CONTRACT.md
├── BEHAVIORAL-EVALUATION-PROTOCOL.md
└── PROMPT-DESIGN-HISTORY.md
```

Major v6 changes:
- control plane moved outside `AUDITS/**`;
- historical design rationale separated from canonical prompt bytes;
- target modes generalized to CURRENT_MAIN / RELEASE_TAG / EXACT_COMMIT;
- blind boundary expanded to external audit/adjudication evidence;
- baseline changed to discover-first;
- probe quotas replaced by failure-class coverage;
- vacuous regex, schema weakening, lying verifier, dangling symlink, and weak-source T3 classes explicitly represented as examples of mechanisms worth probing;
- impact and precondition/threat model separated;
- behavioral effectiveness moved to a dedicated protocol;
- report contract gains machine-readable findings;
- repository content explicitly treated as untrusted audit data;
- comparative rounds should pin exact methodology identity, not only a mutable URL.

## Preservation rule

Do not copy future audit findings into the canonical prompt merely because they are recent.

Promote a finding class into methodology only when it represents a durable attack family or recurring verifier weakness rather than one release-specific bug.

This prevents the canonical prompt from becoming a giant replay list that primes every auditor toward historical findings and destroys the novel-hunt value of the blind phase.
