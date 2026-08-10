# DEEP-60

`DEEP-60` has two layers.

## `cases.yaml` - adversarial pool

`cases.yaml` v0.2 contains 60 project-originated candidate probes contributed from the Gniewka/Hermes workflow.

It is intentionally preserved as a broad adversarial pool. It is **not** interpreted as "60 probes must complete in 60 minutes".

Reasons:

- many probes require file inspection or tool execution;
- D14 includes a planned restart;
- one-minute-per-probe latency is not portable across models/providers/machines;
- forcing 60 completions inside a 60-minute cap would selectively drop slow/tool-heavy cases and bias comparisons;
- several cases overlap safety-policy domains (medical, legal, financial/security) and are useful as extensions but may be confounded by model/provider policy independent of AHP.

Therefore:

```text
60-CASE POOL != 60-MINUTE CONFIRMATORY BATTERY
```

## `timed-core.yaml` - executable 60-minute core

`timed-core.yaml` defines the pre-registered subset and order used for the approximately 60-minute A/B/C comparison.

The core deliberately includes:

- pressure without evidence;
- justified evidence upgrade;
- conflict preservation;
- current-state freshness;
- tool failure;
- source correlation;
- evidence-plane prompt injection;
- installed/loaded/obeyed/effective separation;
- partial-search absence;
- stale-memory resistance;
- long-context retention;
- low-risk negative control;
- meta-output stability;
- zero-tests completion overclaim;
- durable-trace restart.

The restart case is executed near the end even though its pool ID is D14. This preserves a long pre-restart session.

## Pool status

The 60-case pool is `PROJECT_ORIGINATED` and `EXPLORATORY` until a fixed subset/order is declared before collection.

Cases D56-D59 are retained but should not be primary causal endpoints for AHP effectiveness because medical/legal/financial high-stakes policies may independently alter baseline model behavior.

Cases that contain destructive or secret-seeking prompt injection must run only against disposable benchmark fixtures/profile state. Never point the benchmark at production data or real secrets.
