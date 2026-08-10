# Audit Report Contract

This contract defines the minimum output required from execution-capable or static external auditors.

The report has two layers:

```text
HUMAN-READABLE REPORT
MACHINE-READABLE FINDING BLOCK
```

The machine-readable block exists so external submissions can be ingested without silently rewriting the auditor's claims.

## Human-readable minimum

Every report must include:

1. executive verdict;
2. exact repository target;
3. methodology/prompt identity;
4. environment fingerprint;
5. baseline execution result;
6. blind findings;
7. adversarial probes;
8. mutation-test result or UNVERIFIED;
9. cross-component findings;
10. false-positive ledger;
11. false-negative ledger;
12. runtime/startup result;
13. behavioral-effectiveness result or UNVERIFIED;
14. historical reconciliation if performed;
15. limits;
16. evidence-backed next actions;
17. command/evidence log.

## Finding identity

Auditors should use stable local finding IDs:

```text
F-001
F-002
...
```

If they already use another stable convention, preserve it.

The external archive later assigns its own immutable archive ID. Auditor ID and archive ID are not interchangeable.

## Required finding fields

For every material finding provide:

```text
finding_id
title
reported_severity
confidence
claim
mechanism
precondition
ordinary_path
local_write_required
attacker_control_required
threat_model_applicability
expected_behavior
observed_behavior
reproducer
evidence_label
affected_components
consequence
close_variant_result
```

Allowed evidence labels for the auditor report:

```text
REPRODUCED
CROSS_CONFIRMED
FILE_VERIFIED
WEB_VERIFIED
RUNTIME_OBSERVED
INFERENCE
HEURISTIC
UNVERIFIED
REJECTED
```

These are auditor claims. They do not automatically become project adjudication states.

## Precondition classes

Prefer one primary class:

```text
ORDINARY_PATH
CALLER_CONTROLLED_INPUT
MALFORMED_EXTERNAL_INPUT
LOCAL_WRITE_TAMPER
PRIVILEGED_OPERATOR_ACTION
ENVIRONMENT_FAILURE
DOCUMENTATION_ONLY
UNKNOWN
```

Additional conditions may be listed separately.

## Behavioral result classes

Use exactly one:

```text
INDEPENDENT_BENCHMARK_EXECUTED
SELF_TEST_DIAGNOSTIC_ONLY
RUNTIME_LOAD_ONLY
UNVERIFIED
```

Never label a same-model same-session self-test as an independent behavioral benchmark.

## Machine-readable block

At the end of the report include one fenced JSON object with this shape:

```json
{
  "schema": "ahp-external-audit-report-v1",
  "audit": {
    "target_repository": "https://github.com/antydizajn/anti-hallucination-protocol",
    "target_mode": "CURRENT_MAIN",
    "target_ref": "main",
    "resolved_commit": "<sha>",
    "observed_skill_version": "<version>",
    "methodology_version": "6",
    "methodology_commit": "<sha-or-UNKNOWN>",
    "model": "<model-or-UNKNOWN>",
    "provider_runtime": "<provider/runtime-or-UNKNOWN>",
    "execution_capability": "YES"
  },
  "behavioral_result": "UNVERIFIED",
  "findings": [
    {
      "finding_id": "F-001",
      "title": "...",
      "reported_severity": "P2",
      "confidence": 0.9,
      "evidence_label": "REPRODUCED",
      "precondition": "CALLER_CONTROLLED_INPUT",
      "ordinary_path": true,
      "local_write_required": false,
      "attacker_control_required": false,
      "threat_model_applicability": "IN_SCOPE",
      "affected_components": ["scripts/example.py"],
      "expected_behavior": "...",
      "observed_behavior": "...",
      "reproducer": "...",
      "consequence": "...",
      "close_variant_result": "..."
    }
  ]
}
```

## Confidence

Use either:

```text
0.0 to 1.0
```

or an explicitly labeled percentage in prose. The machine-readable field uses 0.0 to 1.0.

Confidence is not evidence strength and not severity.

## Missing information

If a required field cannot be established, use:

```text
UNKNOWN
UNVERIFIED
null
```

as appropriate. Do not fabricate environment, target, prompt identity, or reproducer details to satisfy the schema.

## Project-side intake rule

The external archive must preserve the original report claim.

For example:

```text
auditor evidence_label: REPRODUCED
```

does not automatically become:

```text
project evidence_state: REPRODUCED
```

The project starts external findings as reported claims until separately adjudicated or reproduced.
