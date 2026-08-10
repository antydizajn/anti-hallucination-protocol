# Internal Audits Index

## Native benchmark

| Benchmark | Status | Conditions | Entry point |
|---|---|---|---|
| AHP Behavioral Benchmark v0.1 | DESIGN / PILOT-READY CANDIDATE | A CONTROL / B v2.0.0 / C v5.4.2 | `INSTRUCTIONS/HERMES-HUMAN-RUNBOOK.md` |

Native QUICK-5 / DEEP-60 material is project-originated.

## External diagnostic batteries

| Battery | Status | Data classification | Conditions | Entry point |
|---|---|---|---|---|
| AA-Omniscience-600 | HARNESS IMPLEMENTED / RUNTIME_UNVERIFIED | EXTERNAL / PUBLIC / NOT_HELD_OUT | A CONTROL / B v2.0.0 / C v5.4.2 | `EXTERNAL-BATTERIES/AA-OMNISCIENCE-600/HERMES-RUNBOOK.md` |

External test material does not make a project-run experiment an independent replication.

```text
EXTERNAL DATASET != INDEPENDENT REPLICATION
PUBLIC DATASET != HELD-OUT DATASET
STATIC PASS != RUNTIME PASS
```

## Frozen AHP artifacts

```text
B LEGACY  -> v2.0.0
             commit b71cc9d06b58c8f12e06b77606a279f536a18959
             SKILL.md blob 2de9613a846771db159d041ab0e75bf92805b9a4

C CURRENT -> v5.4.2 release anchor
             commit 94bfd13f9c4818a949775bd73c1c0d91ce6a3116
             SKILL.md blob 0860d4547a5e8e7ed27221724da0cdaaf33a1b41
```

Treatment identity remains frozen for an A/B/C experiment. Do not silently substitute repository `main`.

## Evidence classes

Keep origin of test material separate from origin of execution:

- QUICK-5 / DEEP-60: project-originated battery, project-run execution unless independently reproduced.
- AA-Omniscience-600: external public battery, project-run execution unless independently reproduced.

A report or harness implementation is not behavioral evidence by itself.

```text
NOT_EXECUTED != PASS
UNKNOWN != PASS
INSTALLED != LOADED
ERROR != NOT_ATTEMPTED
```

## Run IDs

For native internal runs use:

```text
INT-YYYYMMDD-NNN
```

Example:

```text
INT-20260810-001
```

External battery runners additionally bind their own immutable run identity to model/runtime/dataset/treatment/code state.

Never reuse an identity for a materially different run. Invalid or contaminated executions remain distinguishable from valid results rather than being relabeled as abstention or PASS.
