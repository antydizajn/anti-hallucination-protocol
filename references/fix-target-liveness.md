# Fix-target liveness: don't repair a corpse (OKO-zombie, 2026-06-20)

Companion to SKILL.md §7.8.1. The lesson: a bug can be *real* (a log really is
flooding) while its *target* is a deprecated/phantom/dead component. The right
move is removal, not a patch. And when you own an auto-fix/proposal pipeline,
make the check STRUCTURAL so it can't be forgotten.

## The two traps caught in one session

1. **Deprecated target (zombie).** An auto-proposer mined `oko_grawitacyjne.err`
   (macOS TCC "not authorized to capture video" x40) and proposed adding backoff
   logic to `oko_grawitacyjne.py`. Verified facts: the log WAS flooding (mtime =
   minutes ago), the file DID exist. But:
   - `grep -c 'cv2\|opencv\|ffmpeg' oko_grawitacyjne.py` → 9 ; `grep -c yolo` → 0
     → it's the OLD USB/OpenCV camera daemon.
   - The live perception stack is YOLO: `WORKSPACE/kamery/{presence_watcher,
     border_watcher,face_id,fall_detector}.py` + `yolo11n/m.pt`, with real running
     PIDs (`ps aux | grep -E '[p]resence_watcher|[b]order_watcher'` → 2 procs).
   - The old daemon was a launchd ZOMBIE: `com.antigravity.oko.plist` kept
     re-spawning it (running since Thursday).
   - User confirmed: "that's gone, we use YOLO now."
   → Right fix: `launchctl bootout gui/$(id -u)/com.antigravity.oko` + archive
     script+plist+logs to `EXTERNAL/deprecated_oko_*/` (reversible, with README).
     Patching its backoff would have been medicine for a corpse.

2. **Phantom target (never built).** Another queue item proposed implementing
   "drift-corrected voting" in `multi_model_orchestrator.py`. That file does not
   exist — the synod uses a different orchestrator. A proposal aimed at a file
   that was never built.

Both passed the naive "is the bug/need real?" test and failed the "is the target
part of the living system?" test.

## Manual pre-patch checklist (always)

```
the target file/module actually exists      search_files target=files  (trust disk, not the report)
it's not deprecated/archived/moved          grep for the replacement stack; `git log --diff-filter=R`
its writer/process is still running         ps aux | grep ; launchctl list | grep
the log source isn't a frozen dead writer   stat -f '%Sm' <log>  -> mtime stale (>24h) = history
```

## Programmatic guard (when you own the proposal pipeline)

Two defense-in-depth layers. Proven by attack test below (6/6: phantom +
deprecated REJECT; real + abstract + live-workspace PASS).

### Layer 1 — target-existence gate (reject proposals aimed at files that don't exist)

```python
def verify_target_exists(proposal: dict, base: "str | None" = None) -> tuple[bool, str]:
    """Reject a proposal whose named file targets do NOT exist on disk.
    Scans surface/minimal_change/evidence for concrete *.py/*.md paths.
    No concrete path -> pass (abstract surface; behavioral gate handles it).
    """
    import os, re
    base = base or os.path.expanduser("~/AI/ANTIGRAVITY")
    blob = " ".join(str(proposal.get(k, "")) for k in
                    ("surface", "minimal_change", "evidence"))
    paths = re.findall(r"[\w./-]+\.(?:py|md)\b", blob)
    paths = [p for p in paths if "<" not in p and ">" not in p]  # drop <module>.py placeholders
    if not paths:
        return True, "no concrete target path to verify (abstract surface)"
    found, missing = [], []
    for rel in paths:
        rel = rel.lstrip("/")
        cands = [os.path.join(base, rel),
                 os.path.join(base, "scripts", "core", os.path.basename(rel)),
                 os.path.join(base, "scripts", os.path.basename(rel)),
                 os.path.join(base, "WORKSPACE", "kamery", os.path.basename(rel)),
                 os.path.expanduser(os.path.join("~/.hermes/scripts", os.path.basename(rel)))]
        (found if any(os.path.exists(c) for c in cands) else missing).append(rel)
    if found:
        return True, "target(s) exist: " + ", ".join(found)
    return False, ("targets file(s) that do NOT exist: " + ", ".join(missing) +
                   " - phantom/deprecated target; verify the surface is real and live")
```

Wire it into the contract gate (`validate_contract(..., verify_target=True)`) and
turn it on where proposals get queued.

### Layer 2 — staleness gate on the log miner (don't mine dead sources)

```python
import time, os
STALE_LOG_HOURS = 24
now = time.time()
for fn in os.listdir(logs_dir):
    if not (fn.endswith(".err") or fn.endswith(".jsonl")):
        continue
    p = os.path.join(logs_dir, fn)
    try:
        age_h = (now - os.path.getmtime(p)) / 3600.0
    except OSError:
        continue
    if age_h > STALE_LOG_HOURS:
        continue  # dead writer -> errors are history, not a live weakness
    # ... mine this file ...
```

## Attack test shape (lock the behavior)

```python
# phantom file -> REJECT
verify_target_exists({"surface": "edit multi_model_orchestrator.py ..."})[0] is False
# deprecated/moved module -> REJECT
verify_target_exists({"surface": "scripts/core/oko_grawitacyjne.py behavior"})[0] is False
# real file -> PASS
verify_target_exists({"surface": "scripts/core/gnosis_toolkit.py ..."})[0] is True
# abstract surface (no path) -> PASS (nothing to verify)
verify_target_exists({"surface": "cron watchdog policy"})[0] is True
# live workspace file resolved via candidate paths -> PASS
verify_target_exists({"surface": "presence_watcher.py behavior"})[0] is True
```

## Why this is the same family as §7.8

§7.8: "the reported bug may be STALE — read source before you fix." This is the
target-side mirror: the bug report may point at a component that is no longer part
of the living system (deprecated) or never was (phantom). The miner/automaton
cannot know about deprecation; the human carries that context. The cheapest
insurance — a path-existence check + a log-mtime check — prevents the most
embarrassing error: giving medicine to a corpse, or fixing a file that was never
born.
