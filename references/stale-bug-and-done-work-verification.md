# Stale-bug & done-work verification — worked transcripts (2026-06-20)

Backing detail for SKILL.md §7.8. Session: repairing ~9 failing Hermes/ANTIGRAVITY
crons plus two "approved" PATCH_QUEUE items. Two near-misses where reading the
description instead of the source would have produced wasted or harmful work.

---

## Case 1 — the `model_dump` crash that was already fixed (stale code + zombie)

### Symptom
Multiple agent-mode crons (`use-audit-hourly`, `adr-index-rebuild`,
`autonomous-worker`, `palantir-watchdog`) showed `last_status: error`. Logs:
```
Streaming failed before delivery: 'dict' object has no attribute 'model_dump'
```
780 occurrences, all on the NEW Palantir region (`usw-16`), zero on the dead
`euw-3`. So "region move broke it" (the user's first hypothesis) was FALSE for
this subset — a separate streaming bug on the new region.

### The trap I almost fell into
I started tracing `.model_dump()` through 130KB+ of framework streaming code
(`anthropic_adapter.py`, `chat_completion_helpers.py`), hunting an unguarded
call to patch. Static tracing across that much code = high risk of guessing wrong.

### The decisive move: isolated reproduction with the REAL traceback
Wrote a throwaway repro using the gateway venv + the agent's own Palantir client,
sending the same shape a cron sends (system + user + tools + thinking config):

```python
# EXTERNAL/repro_palantir_stream_20260620.py (key parts)
import anthropic, palantir_config as pc
client = anthropic.Anthropic(
    api_key="unused", base_url=pc.ANTHROPIC_BASE,
    default_headers={"Authorization": f"Bearer {pc.load_token()}"},  # Palantir wants Bearer, NOT x-api-key
)
# minimal call -> WORKS (stream + non-stream)
# + tools + thinking={"type":"enabled"} -> 400 from Palantir:
#   "thinking.type.enabled is not supported for this model.
#    Use thinking.type.adaptive and output_config.effort"
# + thinking={"type":"adaptive"} + extra_body={"output_config":{"effort":"high"}} -> WORKS
```

The 400 (not a code bug) is what surfaces as `model_dump` downstream — the error
dict gets `.model_dump()`'d in the streaming error path. So the question became:
does Hermes' adapter send the bad `thinking.enabled` shape for the opus-4.8 RID?

### Verifying the adapter directly
```python
from agent.anthropic_adapter import build_anthropic_kwargs
rid = "ri.language-model-service..language-model.anthropic-claude-4-8-opus"
k = build_anthropic_kwargs(rid, [{"role":"user","content":"hi"}], None, 16000, {"effort":"high"})
# -> thinking={"type":"adaptive","display":"summarized"}, output_config={"effort":"high"}
```
The adapter (dated Jun-17) ALREADY emits the correct adaptive shape. So current
code is fine. Why did crons crash?

### Root cause: stale code + zombie, not a code bug
- The gateway PID had restarted at 11:11 (mid-failure-window); failures were from
  the OLD in-memory code before that.
- A session from the previous day (`20260619_192454`) was retrying 8/8 forever —
  a zombie holding old code.
- A FRESH cron trigger (`cronjob run use-audit-hourly`) came back
  `last_status: ok` with full output. Triggering the others (`adr-index`,
  `autonomous-worker`, `godmode-self-evolve`) showed healthy API calls #1-4,
  tools completing, ZERO model_dump in the 12:1x-12:2x log window.

VERDICT: nothing to patch. The Jun-17 fix already handled it; the errors were
stale. Patching the framework would have been "fixing" working code — and would
have been reverted by the next `hermes update` (git reset) anyway.

LESSON: a traceback in a log is a claim about the PAST. Reproduce on a fresh
process before believing the bug still exists. `model_dump`-style downstream
symptoms often mask a clean upstream 400 (provider param mismatch) — reproduce to
see the REAL error.

---

## Case 2 — two PATCH_QUEUE items already done (read source, not the queue)

User: "oceń, zaimplementuj co warto i przesuń do done, patch queue, masz approved."

Both "waiting for approval" items, when I READ THE SOURCE instead of trusting the
queue description:

1. **recall chunk dedup** (`hsdb_memory.py _reassemble_chunks`): the `seen_idx`
   dedup-by-chunk_index was ALREADY in the code, with a passing regression test
   (`test_recall_dedup_repro_20260620.py`: 112 records -> 7, zero dup). It was
   just UNCOMMITTED (`git diff --stat` showed +12/-1). Action: verify test, commit.
   NOT re-implement.

2. **memory_immune one-sided safe_mode**: variant A (no early-return) was already
   applied Jun-15. The queue said "fix the deadlock" — but that part was done. The
   REAL remaining gap, which the description did NOT call out: the UNSAID alert
   embedded `{error_count}` in its message. error_count climbs 3,4,5… each tick,
   so every alert was a DISTINCT string -> `add_unsaid_alert`'s dedup never matched
   -> spam every 5 min persisted despite the "fix". The subtle fix: fire once per
   safe-mode EPISODE (transition guard `was_safe False->True`) + a STABLE message
   with no counter.

Proved by attack (`test_memory_immune_alert_dedup_20260620.py`): 5 fails -> 1
alert (not 3+), heal clears safe_mode, new episode -> +1 alert (re-arms). PASS.

LESSON: a TODO/queue/issue entry is an UNVERIFIED claim about the code. Before
implementing: (a) grep the fix — is it already there? (b) `git diff --stat <file>`
— is it done-but-uncommitted? (c) if real work remains, it's usually a SUBTLE gap
the description missed, not the headline.

---

## Reusable technique surfaced this session — cron launcher that does heavy work inline

Not a hallucination lesson, but a clean fix pattern worth recording. A `no_agent`
cron whose script runs heavy compute INLINE (e.g. `timeout 800 python heavy.py`)
will be killed by the cron runner's ~120s ceiling and forever report `error`,
even though the compute ran. The launcher's job is to LAUNCH, not block.

FIX — parent gates + detaches, returns in ~1s; child does the work:
```bash
PIDFILE=/tmp/job_active.pid
if [ "${JOB_DETACHED:-0}" != "1" ]; then
    # PARENT: gate (load, overlap), then re-exec detached and return fast
    [ "$(load_int)" -ge 16 ] && exit 0
    [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null && exit 0
    export JOB_DETACHED=1
    setsid bash "$0" >/dev/null 2>&1 &
    echo "$!" > "$PIDFILE"   # record worker PID so the overlap guard works next tick
    exit 0                    # silent success: cron returns in ~1s, worker runs on
fi
# CHILD (JOB_DETACHED=1): gates already passed by parent -> straight to the compute
```
Pitfall caught: if BOTH parent and the re-exec'd child run the gate/PID-guard, the
child sees the parent's just-written PID via `kill -0` and exits as "already
running". Fix: gates live ONLY in the parent branch; the child branch skips them.
Verified: parent returned in 1s, detached worker ran the real Ramsey hunter_E
search to completion in the background. (Never pause the user's Ramsey crons —
they're her infra; fix the wrapper, not the search logic.)

Another deterministic cron fix from the same session: a cron `script` field
CANNOT carry CLI args — `script: "digest.py --report"` fails with
`Script not found: digest.py --report` (the whole string is treated as a filename).
Fix: a thin per-mode wrapper script that injects the arg via `runpy`:
```python
import os, runpy, sys
REAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "digest.py")
sys.argv = [REAL, "--report"]
runpy.run_path(REAL, run_name="__main__")
```
Then point the cron `script` at the wrapper (no args).
