# Fix-target liveness: verify that you are fixing a living component

A reported bug can be real while the proposed fix target is stale, deprecated,
renamed, replaced, or never part of the active system. "The error exists" and
"this component should be patched" are separate claims and require separate
evidence.

The safe rule is:

> Before patching a reported bug, verify both the failure and the liveness/identity
> of the exact target you intend to change.

## 1. Failure reality is not target identity

These can all be simultaneously true:

- a log contains a real error,
- a file with a related name exists,
- the proposed patch is wrong because that file is no longer on the live path.

Common shapes:

- deprecated daemon still writing logs while a replacement stack is live,
- stale process running old code after the source was already fixed,
- issue/queue item names a file that never existed,
- component was renamed or moved,
- multiple files share the same basename and a loose resolver finds the wrong one,
- a historical log is interpreted as a current failure.

## 2. Manual pre-patch checklist

Before editing, answer these independently:

```text
QUESTION                                      EVIDENCE
exact target path exists                      exact path lookup / repository tree
proposed target is the intended component     imports, call graph, config, service wiring
component is not deprecated/replaced          current config/docs/source/history
process/service using it is live               process/service/runtime state where applicable
failure is current                            fresh reproduction or current telemetry
the running code matches current source       process restart/version/commit evidence
```

A single loud log line is not sufficient evidence for all six questions.

## 3. Exact-path rule

Do not treat a basename match as proof that a named target exists.

Bad verifier logic:

```python
for candidate_dir in candidate_dirs:
    if (candidate_dir / Path(reported_path).name).exists():
        return True
```

If the report names `legacy/foo/config.py`, finding `current/bar/config.py` does not
verify the reported target. It verifies that **a different file with the same
basename exists**.

Prefer exact repository-relative paths. If a path is ambiguous, resolve the
identity explicitly and report the ambiguity rather than returning VERIFIED.

## 4. Multi-target rule

If a proposal names multiple concrete targets, verify every target independently.
Do not use "any target exists" as a pass condition.

Represent results per target:

```python
[
    {"path": "a.py", "status": "FOUND"},
    {"path": "b.py", "status": "NOT_FOUND"},
]
```

A proposal with mixed results is `PARTIAL`, not VERIFIED.

Recommended decision semantics:

- all required targets `FOUND` -> target-existence gate passes,
- any required target `NOT_FOUND` -> gate fails pending reconciliation,
- any target `ERROR` -> gate is inconclusive/error, not negative verification,
- abstract proposal with no concrete path -> existence gate is not applicable;
  verify behavior through another surface.

## 5. Do not hard-code a tiny extension list as if it were universal

A path extractor that recognizes only `.py` and `.md` will silently miss targets
such as:

- `.ts` / `.tsx` / `.js`,
- `.rs` / `.go` / `.java`,
- `.yaml` / `.yml` / `.toml` / `.json`,
- `.sh`,
- infrastructure files without familiar extensions.

If target extraction is used as a safety gate, either:

1. parse paths from a structured proposal field, or
2. define and document the supported path grammar and treat everything else as
   `UNKNOWN_SCOPE` rather than silently passing.

Structured target fields are preferable to regex mining from prose.

## 6. Freshness cannot be reduced to one universal age threshold

A rule such as:

```text
log mtime > 24h => source is dead
```

is not universally valid. A weekly job can be live with a log older than 24 hours;
a stuck process can update a log every minute while still running obsolete code.

Use freshness relative to expected cadence and runtime context:

- service expected continuously -> minutes/hours may be meaningful,
- daily batch -> compare against daily cadence,
- weekly batch -> a multi-day-old log may be normal,
- manually triggered workflow -> mtime alone says little.

Prefer combining:

- expected schedule,
- last successful/failed run,
- process/service state,
- current source/version,
- fresh reproduction when safe.

## 7. A safer structural target gate

When an automation emits proposals, make targets structured instead of scraping
filenames from prose:

```python
proposal = {
    "surface": "memory recall fallback",
    "targets": [
        {"path": "plugins/memory/recall.py", "required": True},
        {"path": "tests/test_recall.py", "required": False},
    ],
}
```

Then verify exact paths under a defined repository root:

```python
from pathlib import Path


def verify_targets(root: Path, targets: list[dict]) -> list[dict]:
    root = root.resolve()
    results = []

    for item in targets:
        rel = Path(item["path"])
        if rel.is_absolute() or ".." in rel.parts:
            results.append({**item, "status": "ERROR", "reason": "unsafe path"})
            continue

        candidate = (root / rel).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            results.append({**item, "status": "ERROR", "reason": "path escapes root"})
            continue

        results.append({
            **item,
            "status": "FOUND" if candidate.exists() else "NOT_FOUND",
        })

    return results
```

This establishes exact path existence only. It does **not** prove that the target is
live, imported, deployed, or behaviorally relevant. Those are separate gates.

## 8. Liveness gate

After exact-path existence, ask whether the target participates in the active
system.

Possible evidence:

- imported by the active entry point,
- referenced by current configuration,
- loaded by the running service,
- package/module version matches the deployed process,
- service manager points to this path,
- current process command line points to this artifact,
- replacement/deprecation markers are absent or reconciled.

Do not require every signal for every architecture. Require enough evidence to
support the specific liveness claim you make.

## 9. Historical case lesson

A prior incident involved an old camera daemon that continued producing permission
errors after a newer perception stack had replaced it. The errors were real. The
wrong conclusion would have been to harden the obsolete daemon. The correct action
was to identify the replacement/live path and retire the zombie component.

A second proposal in the same class named a target file that had never been part of
the actual orchestration path.

The durable lesson is not the project-specific filenames. It is this split:

```text
BUG EXISTS?       -> failure evidence
TARGET EXISTS?    -> exact path evidence
TARGET IS LIVE?   -> runtime/config/call-path evidence
FIX IS CORRECT?   -> behavioral validation
```

Do not collapse those four questions into one green light.
