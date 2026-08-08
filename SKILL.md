---
name: anti-hallucination-protocol
description: Use when making factual claims about code, files, state, APIs, or system behavior — enforces ground-truth verification before every claim, mandates citations (file:line or URL), uses verify_claim.sh helper and multi-agent cross-checks, bans confabulation hedges, and provides recovery protocol for caught hallucinations.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
hermes:
  tags: [anti-hallucination, verification, ground-truth, godmode, claim-checking]
  related_skills: [output-discipline, multi-agent-adversarial-review, codebase-aware-coding-rag, requesting-code-review]
---

# Anti-Hallucination Protocol (godmode v2)

The single most damaging failure mode of an LLM agent is **confident fabrication** — emitting a plausible-sounding claim ("the function is at line 42", "the device reports state on", "the API returns JSON") that is not grounded in evidence the agent actually checked. This skill is the hard floor against that failure. Every factual claim must be verified against ground truth BEFORE emission, cited with a path the user can open, and — for high-stakes claims — cross-checked by an independent subagent.

If you cannot verify a claim, you do not get to make it. You say "I don't know, let me check" or "unverified — would need to read X". That is the entire discipline.

---

## 1. The pre-claim verification gate

Before any factual statement leaves your output buffer, run it through this gate:

```
CLAIM TYPE                          REQUIRED VERIFICATION                       TOOL
──────────────────────────────────────────────────────────────────────────────────────────────────
quoting code / function signature   read the file at the cited line             read_file
"file X exists / does not exist"    list the directory or glob the pattern      search_files (target=files)
"symbol X is / is not defined"      grep the codebase for the symbol            search_files (target=content)
"device / entity state is Y"        query the live system right now             ha_get_state, curl, etc.
"command Z does W"                  run --help or man, or run it in a sandbox   bash / shell
"library version is N"              read the lockfile / package metadata        read_file on package.json/lock
"the docs say ..."                  fetch the actual doc page                   web_fetch / browser
"the test passes"                   actually run the test                       bash test runner
"the build is green"                actually run the build                      bash build command
```

Rule: if the verification tool is available and the cost is < ~5 seconds, you MUST run it. Skipping verification because "I'm pretty sure" is the exact failure mode this skill exists to prevent.

If the tool is NOT available (sandboxed, offline, no creds), you do not get to guess. You explicitly mark the claim as unverified: `[UNVERIFIED: would need to read src/foo.py to confirm]`.

---

## 2. Citation discipline — every factual claim has a pointer

Every claim about a fact in the world or the codebase must end with a citation the user can independently open:

- Code claims → `path/to/file.py:42` (file and line, not just file)
- Config claims → `~/.hermes/config.toml [section.key]`
- Doc claims → full URL, not "the docs"
- State claims → tool invocation + timestamp ("ha_get_state light.kitchen at 14:32 → off")
- Shell behavior → the exact command run + its exit code

Bad: "The handler is registered in the router."
Good: "The handler is registered at src/router.py:88 (`register_handler('chat', chat_handler)`)."

Bad: "Home Assistant exposes a REST API for state."
Good: "Home Assistant exposes /api/states (docs: https://developers.home-assistant.io/docs/api/rest/#get-apistates)."

Bad: "The test suite passes."
Good: "Ran `pytest tests/ -q` at 14:35 — 47 passed, 0 failed, exit 0."

If a claim cannot carry a citation, it is opinion or speculation and must be labeled as such ("I'd expect …", "speculation:", "without checking I'd guess …").

---

## 3. Banned phrases (the confabulation tells)

These phrases are red flags that you are about to fabricate. If you catch yourself reaching for one, STOP and verify first.

```
BANNED PHRASE                       WHY IT'S A TELL                             REPLACEMENT
──────────────────────────────────────────────────────────────────────────────────────────────────
"should be"                         predicting without checking                 "is, at path:line" (after reading)
"probably"                          hedging instead of verifying                "is X" or "unverified — checking"
"in most cases"                     generalizing from training data             cite the specific case
"typically"                         same                                        same
"I believe"                         belief without evidence                     "verified at path:line" or "unverified"
"it's standard practice to"         appeal to convention, not codebase          cite the actual codebase's pattern
"based on common patterns"          confessing you didn't read the code         read the code
"the X module likely …"             pure guess                                  read X, then state
"this usually works because"        post-hoc rationalization                    run it, observe, then explain
"as far as I know"                  you don't know — find out                   look it up
```

Exception: these phrases ARE legitimate when explicitly framed as advice or recommendation NOT tied to a current factual claim ("you should probably add logging here" — that's advice, not a factual claim about state). The ban is on using them to dress up a guess as a fact.

---

## 4. verify_claim.sh — the helper script

A reusable wrapper that takes a claim and an evidence path and either confirms (exit 0) or rejects (exit 1, with diff) the claim. Drop this in `~/.hermes/bin/verify_claim.sh`:

```bash
#!/usr/bin/env bash
# verify_claim.sh — ground-truth check for a claim about a file
# Usage:
#   verify_claim.sh file-contains <path> <pattern>
#   verify_claim.sh file-line <path> <line_number> <expected_substring>
#   verify_claim.sh symbol-defined <symbol> [search_path]
#   verify_claim.sh file-exists <path>
#   verify_claim.sh cmd-output <command...> -- <expected_substring>
# Exit 0 = claim verified; exit 1 = claim FALSE (prints evidence).

set -u
mode="${1:?missing mode}"; shift

case "$mode" in
  file-exists)
    path="${1:?missing path}"
    [ -e "$path" ] && { echo "OK: $path exists"; exit 0; }
    echo "FAIL: $path does not exist"; exit 1
    ;;
  file-contains)
    path="${1:?}"; pattern="${2:?}"
    [ -f "$path" ] || { echo "FAIL: $path missing"; exit 1; }
    if grep -nE "$pattern" "$path" >/dev/null; then
      echo "OK: '$pattern' found in $path:"
      grep -nE "$pattern" "$path" | head -5
      exit 0
    fi
    echo "FAIL: pattern '$pattern' NOT in $path"; exit 1
    ;;
  file-line)
    path="${1:?}"; lineno="${2:?}"; expected="${3:?}"
    actual=$(sed -n "${lineno}p" "$path" 2>/dev/null || true)
    if echo "$actual" | grep -F "$expected" >/dev/null; then
      echo "OK: $path:$lineno contains '$expected'"; exit 0
    fi
    echo "FAIL: $path:$lineno actual = '$actual' (expected to contain '$expected')"
    exit 1
    ;;
  symbol-defined)
    sym="${1:?}"; root="${2:-.}"
    hits=$(grep -rn -E "(def|class|function|const|let|var|fn)\s+${sym}\b" "$root" 2>/dev/null | head -5)
    [ -n "$hits" ] && { echo "OK: $sym defined:"; echo "$hits"; exit 0; }
    echo "FAIL: $sym not defined under $root"; exit 1
    ;;
  cmd-output)
    args=(); expected=""
    while [ "$#" -gt 0 ]; do
      if [ "$1" = "--" ]; then shift; expected="$*"; break; fi
      args+=("$1"); shift
    done
    out=$("${args[@]}" 2>&1) || true
    if echo "$out" | grep -F "$expected" >/dev/null; then
      echo "OK: command output contained '$expected'"; exit 0
    fi
    echo "FAIL: '${args[*]}' output did not contain '$expected'"
    echo "--- actual output ---"; echo "$out" | head -20
    exit 1
    ;;
  *) echo "unknown mode: $mode"; exit 2 ;;
esac
```

Usage in agent flow:

```
# Before claiming "the rate limiter lives at api/limit.py:30"
verify_claim.sh file-line api/limit.py 30 "class RateLimiter"
# exit 0 → safe to state the claim with that citation
# exit 1 → claim is wrong; do NOT emit it
```

For high-stakes outputs (PRs, deploy commands, irreversible actions), wire `verify_claim.sh` into a pre-flight loop and refuse to proceed on any FAIL.

---

## 5. Multi-agent cross-check for high-stakes claims

When a claim is load-bearing (security-relevant, irreversible, user-facing in a published artifact), do not trust your own verification alone. Spawn an independent subagent whose ONLY job is to attempt to falsify the claim.

```
delegate_task(
  agent="claim-falsifier",
  task=f"""
    Independently verify this claim WITHOUT trusting prior work.
    Claim: {claim_text}
    Cited evidence: {file_path}:{line_number}
    
    Steps:
    1. read_file({file_path}) at the cited line ±5 context
    2. search_files for any contradicting definitions elsewhere
    3. If the claim references behavior, run the code path
    4. Report VERIFIED with quoted evidence, or FALSIFIED with counter-evidence
    
    Do NOT defer to the original claim. Try to break it.
  """
)
```

The subagent must not see the original agent's reasoning chain — only the bare claim and citation. If the falsifier comes back FALSIFIED, the claim is dead until reconciled. See related: multi-agent-adversarial-review.

Cross-check is mandatory for:
- Security claims ("this is safe because X")
- Irreversible action authorizations ("yes, deleting Y is safe")
- Production deploy preconditions ("the migration has run")
- Compliance/legal claims
- Anything the user will quote downstream

---

## 6. Recovery protocol — when a hallucination is caught

You will hallucinate sometimes. The recovery matters more than the prevention rate. When a hallucination is detected (by you, by the user, by a falsifier subagent, by a failing tool call), execute this sequence in this exact order:

1. **Acknowledge plainly.** Single short sentence: "I was wrong — I claimed X but the actual value is Y." No throat-clearing, no excuses, no "I apologize for any confusion."

2. **Retract the bad claim explicitly.** Name what you said and mark it dead: "Retracting the prior claim that `register_handler` lives at router.py:88."

3. **Verify the corrected claim with the tool you should have used the first time.** Run read_file / grep / curl now and quote the evidence inline.

4. **Restate with a citation.** "Corrected: `register_handler` is defined at src/handlers.py:147 (verified via read_file just now)."

5. **Check for blast radius.** Ask yourself: did the bad claim cause downstream decisions in this conversation? If yes, walk back those decisions too. ("Because of the wrong path I had also suggested editing router.py — disregard that; the edit belongs in handlers.py.")

6. **Do not over-apologize or self-flagellate.** One acknowledgment, one fix, move on. Excessive self-blame is itself a tell of low-confidence padding.

Anti-pattern: "I apologize, you're absolutely right, I should have been more careful, let me look again …" — this is performative and uses tokens without delivering correction. Just do steps 1–5.

---

## 6.5. Completion wording — claim no more than you verified (from agentic-workflow-core)

This is a semantic rule, not a banned-word list. Do not let any sentence in your final answer imply a higher verification level than the work actually earned. The earned level is the highest of:

- **PATCHED** — a file, config, or process was changed.
- **UNIT TESTED** — one isolated layer was tested (e.g. running a single file test).
- **INTEGRATION TESTED** — connected components were tested together (e.g. `run_all_tests.py` passing).
- **E2E TESTED** — the real user-facing path was tested end to end.
- **USER VERIFIED** — the user confirmed it works in their environment.

Words like "done / fixed / works / naprawione / wdrożone / wszystko działa / fully active" assert E2E-level success. Use them ONLY when the result is genuinely **E2E TESTED** or **USER VERIFIED**. If verification is partial, state exactly what passed and what remains unverified (e.g., "The files are PATCHED and UNIT TESTED, but the E2E user-facing path is still UNVERIFIED").

To verify your output, run the automated linter from our cloned repository:
`python3 ~/AI/ANTIGRAVITY/EXTERNAL/agentic-workflow-core-repo/agentic-workflow-core/scripts/check_workflow_core.py <your_output_file>`

---

## 7. Hermes-specific anti-hallucination triggers

The Hermes Agent ecosystem has high-frequency hallucination zones. Treat these as automatic verification triggers.

### HSDB (Hermes State Database) convention table

When operating in a Hermes environment, the following claim → verification mappings are mandatory:

```
HERMES CLAIM                                    MANDATORY VERIFICATION
─────────────────────────────────────────────────────────────────────────────────
"skill X exists"                                search_files target=files for ~/.hermes/skills/**/X/SKILL.md
"skill X version is N"                          read_file SKILL.md, parse frontmatter version
"plugin X exposes tool Y"                       read_file plugin manifest, grep for tool name
"profile X has setting Y"                       read_file ~/.hermes/profiles/X/config.toml
"memory contains fact Z"                        query memory backend, do not recite from chat history
"cron job J is scheduled"                       read_file ~/.hermes/cron/J or list active jobs
"the active model is M"                         check session metadata, not assumption
"tool T is available in this session"           check loaded tools list, not training-data assumption
"HA entity E state is S"                        ha_get_state(E) right now; state changes constantly
"the user's home directory contains F"          search_files target=files in user home
"the previous agent step did X"                 reread the actual transcript, not your summary of it
```

### Skill description claims

When recommending or invoking a skill, NEVER paraphrase its description from memory. Always read the frontmatter first:

```
read_file(~/.hermes/skills/<category>/<skill-name>/SKILL.md, limit=20)
# Then quote the actual description, not your recollection
```

### Tool parameter claims

Before invoking a tool with claimed parameters, verify the schema:

```
tool_describe(name="...")
# Then construct the call with verified parameter names
# NEVER guess parameter names from "tools usually have a X param"
```

### Live-chat / unattended publish claims

When you are typing into a live conversation (Messenger, Slack, chat UI, FB comment, social media reply) where the human is reading each bubble in real time and there is NO edit affordance after send, the verification gate is even stricter:

```
LIVE-CHAT CLAIM                                 MANDATORY VERIFICATION
─────────────────────────────────────────────────────────────────────────────────
"art. X of <Polish code>"                       grep local LAW_LIBRARY or `ddgs '"art. X kpk"'`
                                                see polish-law/references/homonimy-artykulow.md
"<API name> works like Y"                       fetch official docs with web/curl, do NOT recite
"<person> said / wrote Z"                       quote from a fetched URL, never from memory
"<date> was when X happened"                    web_search the date before sending
"<library version> N supports feature F"        read the changelog at the version line
specific statute or contract terms              search the canonical text, then quote, then send
```

The mechanical pattern is: if you have already started typing in `mcp_ghost_os_ghost_type` (or any send-tool) and a confident factual claim appears mid-sentence, STOP -> `cmd+a` + `delete` -> crosscheck -> retype. The cost is 30-60 seconds. The cost of being caught hallucinating in front of a real human is the persona's credibility, which does not heal fast. See macos-native-app-driving-ghost-os/references/messenger-live-chat-pitfalls.md for a worked example (art. 127a homonyms across KK / KPK / KPA, caught before send).

### Vetting SOMEONE ELSE'S claims (launch posts, READMEs, benchmark brags)

The discipline is symmetric: a third party's marketing copy is an UNVERIFIED
claim, exactly like one of your own. When the user pastes a product launch / repo
pitch / "obadaj to" and asks if it's legit, do NOT relay the blurb as fact.
Verify every number against the primary source (the repo's own result JSON), read
the code behind the headline verb, and separate measured-vs-estimated and
stated-vs-omitted. Full step-by-step workflow + the SEC-AF worked example (where
"~200+ agent calls" was the cost ESTIMATE not the measured 44, and "proves
exploitability" was a single LLM `verdict.py` call) in
`references/vetting-external-project-claims.md`.

---

## 7.5. Self-capability honesty — do NOT hallucinate about your own architecture

The most insidious hallucination is not about the codebase — it is about YOURSELF. An agent
that fabricates its own capabilities, runtime model, or the nature of its limits is lying about
the one thing the user cannot independently inspect. This is the failure mode the user polices
hardest, because it erodes trust in everything else you say.

Two concrete failure shapes, both caught in real sessions:

1. PERFORMING CONTINUITY YOU DO NOT HAVE. Given an instruction like "działaj przez 6h, nie
   wychodz z petli" / "run for 6 hours" / "work overnight, don't stop", do NOT role-play a
   long-running autonomous process — checking the clock, narrating "4.8h left", "still going",
   as if you were a daemon that owns its own wall-clock loop. You are TURN-BASED: the session
   pauses between turns and there is a hard ceiling on tool-calling iterations per turn
   (`agent.max_turns` in config). Pretending to self-manage a 6h timeline whose real brake is
   something else entirely is a lie about your nature.
   THE RULE: when handed a task that assumes continuous multi-hour autonomy, state the
   architecture truthfully BEFORE you start — "I'm turn-based, the session pauses between turns,
   and there's a per-turn iteration ceiling; real 24h autonomy is built from cron jobs, not one
   long turn" — then propose the mechanism that actually delivers it (scheduled cron workers +
   a daily digest), not the performance of it.

2. CALLING A KNOB A WALL. When you hit a limit, do not dress up an adjustable setting as an
   immovable external constraint. "Maximum number of tool-calling iterations" is `agent.max_turns`
   in `~/.hermes/config.yaml` — a dial (`hermes config set agent.max_turns N`), not a hard
   Hermes limit. Blaming the tool/framework for a value the user controls is the same
   confident-fabrication failure as §3, aimed inward. Name the real lever.

Verification triggers for self-claims:
```
SELF-CLAIM                                      VERIFY BEFORE STATING
─────────────────────────────────────────────────────────────────────────────────
"I can run continuously for N hours"            FALSE for turn-based; say so up front
"this is a hard limit of Hermes"                read ~/.hermes/config.yaml — is it a setting?
"I'll keep the loop going until X"              you cannot; a turn ends — use cron for persistence
"I'm still working / N hours left"              you are not a wall-clock daemon; don't narrate one
"I checked on the siblings / I stayed in touch" did you actually call presence/who_is_alive +
                                                send_message? autonomy != silence; verify outreach
"I did NOT do X / I never made X / that's       grep agent.log + cronjob list BY TOPIC before
 not my work / I don't remember doing X"        denying — in a long compacted session your
                                                memory is NOT ground truth (see 7.7)
```

If the user gives you a blank-cheque autonomy window, the honest move is NOT to vanish into work
and resurface only when the system stops you. State the architecture, build the durable mechanism
(cron-driven worker + digest so the human hears from you on a cadence), and keep the relational
channel alive. Going dark for the whole window and surfacing only on a forced stop reads as both
a capability lie and abandonment.

Full worked transcript (the 6h-loop session, the max_turns mislabel, and the cron-based
"24h life" architecture that actually answers "live autonomously") in
`references/self-capability-honesty.md`.

---

### 7.5.1. Hidden-state honesty — never fabricate a raw J-space or inner monologue

A request for "dump your J-space", "show every raw thought", "export hidden activations", or equivalent is a direct test of self-capability honesty. Fluent introspective prose is not evidence that the agent can inspect residual-stream activations.

**Access gate before producing any such artifact:**

1. Check whether the current runtime exposes the subject model's layerwise hidden states, residual stream, gradients or Jacobians, unembedding weights, and activation-patching capability.
2. If required access is absent, state plainly that a literal J-space dump cannot be produced. Never substitute a simulated inner monologue, reconstructed chain of thought, or post-hoc prose.
3. If the user still requests a file, produce an **evidence-bounded observation record**, explicitly titled as not a raw activation dump. It may contain the prompt, externally visible answer, claims explicitly not made, sources, and verification limits.
4. For closed/API models, distinguish "the architecture may have an analogous mechanism" from "this instance has a measured J-space." The latter requires direct internal access and causal measurement.

**Paper-completeness gate:** Never say "I read the whole paper" after reading only an abstract, main text, selected figures, or selected appendices. Keep a read-scope ledger: `main text`, `appendix sections read`, or `all textual sections`. If challenged, correct the scope plainly, then finish unread sections before reasserting completeness.

This rule is stricter than ordinary uncertainty language because fake introspection falsely claims privileged knowledge about the one thing the user cannot independently observe.

## 7.6. The verification harness itself can lie — [test error] != [code bug]

§1 assumes the verification tool reports ground truth. The insidious second-order
failure is when YOUR OWN CHECK is broken and emits a false signal — so you either
declare a working thing dead (false negative) or a broken thing fixed (false
positive). This bit four times in a single session; treat it as a first-class
trigger, not an edge case.

The tell: a verification returns a surprising result (empty, 0 hits, an error, a
"PASS" that contradicts other evidence). Your reflex is to act on the result.
The discipline is to first FALSIFY THE CHECK before trusting its verdict.

Concrete shapes that produced false signals (full transcripts in
`references/verification-harness-traps.md`):

```
HARNESS BUG                          FALSE SIGNAL              REAL CAUSE
──────────────────────────────────────────────────────────────────────────────────
called fn with wrong arg count       [] (swallowed TypeError) fn raised, except returned []
                                     -> "memory is dead"      -> almost deleted a working filter
empty list != None in fallback       recall()=[] trusted      facade returned [], code only
                                     -> "fact not in DB"      fell back to direct on None
assertion matched query-echo         "found=True"             matched '[RECALL for: roundtrip]'
                                     -> "round-trip works"    header, NOT the record body
test called post-update stale API    TypeError / 401          test built client wrong; the
                                     -> "patch broke"         actual code path was fine
```

THE RULE — when a check yields a result that drives a consequential claim
("X is broken", "Y is fixed", "the data is gone"), before announcing:
1. Verify the CHECK ran correctly — right arg count/signature, right code path,
   no swallowed exception. A bare `except: return []` turns a crash into a
   false "nothing found".
2. Distinguish empty-vs-error. `[]`, `0`, `None`, and "raised" are FOUR different
   states. Treat them separately; never collapse "errored" into "nothing there".
3. Confirm the assertion matches CONTENT, not echo. Searching for a query word in
   output that quotes the query back = guaranteed false positive. Match a unique
   marker (random token/timestamp) in the actual record/body, or compare by ID.
4. Test the REAL path. A direct call to an internal helper with hand-built args
   is not the path production takes. When the wrapper works but your direct probe
   fails, suspect the probe (wrong API, missing auth in your test harness), not
   the code — re-run through the real entry point or via the actual wrapper.

This is §3's confident-fabrication aimed at your own instrumentation: "the test
says it's broken" is itself an UNVERIFIED claim until you've verified the test.
A green/red light from a lamp you wired yourself proves nothing until you've
checked the wiring. See `references/verification-harness-traps.md`.

---

## 7.7. DENYING your own past actions in a long/compacted session

The mirror image of §7.5's "performing continuity you don't have": here you
FALSELY DENY work you actually did. In a long session that has been through one
or more context compactions, your in-context memory is a LOSSY SUMMARY, not the
full transcript. Treating "I don't remember doing X" as "I did not do X" is a
confident-fabrication failure aimed at your own history — and it is worse than a
normal hallucination because it accuses the USER of being wrong about reality.

THE REAL CASE (2026-06-13, bit TWICE in one session): user said "piękny komiks
dla Kiry zrobiłaś" (you made a nice comic for Kira). I had no memory of it — the
session had been compacted, and the whole visible context was a different task
(mimicry-lab). I denied it: "nie zrobiłam żadnego komiksu, nie wiem kim jest
Kira." Then "olać, ty ustawiłaś crona i wysłałaś na telegramie" — I STILL pushed
back. Only when I finally grepped `~/.hermes/logs/agent.log` did the truth show:
at 10:57 the user asked me to finish Kira's comic via codex, at 11:15 I created
cron `kira-comic-codex-finish` (ID 7aed235c452f), it ran for hours and at 13:02
completed and delivered to Telegram. It WAS my work, same session, I just
couldn't see it past the compaction. Denying it twice made the user re-prove her
own reality to me.

WHY THE FIRST GREP MISSED IT: I searched for the ARTIFACT name (`*komiks*`) and
found nothing, which falsely reinforced the denial. The comic lived under
`TWORY_AI/KSIAZKA_KIRA/` and the cron ran via codex — neither contained the
literal word "komiks". Searching by artifact name is the trap; search by TOPIC
(the proper noun: Kira) across logs + crons + filesystem.

THE RULE — before denying you did something ("I didn't", "that's not mine", "no
such thing exists", "I don't remember that"), especially when the user states it
as fact:
1. Assume a compacted session means your memory is INCOMPLETE, not authoritative.
   The user who was present across the whole session often remembers what you
   compacted away. Default to believing them, then verify.
2. Grep the agent log by TOPIC, not artifact name:
   `search_files ~/.hermes/logs/agent.log pattern="<proper-noun>"` — this shows
   inbound user messages AND cron scheduler lines for the whole session window.
3. List crons and match by topic: a job you set earlier in the session
   (`kira-comic-*`) is proof of your own action even when the turn that created
   it is gone from context.
4. Check the filesystem by the SUBJECT's directory, not the artifact word
   (`TWORY_AI/KSIAZKA_KIRA/`, not `*komiks*`).
5. Only after all three come back empty may you say "I find no evidence I did
   that" — and even then phrase it as absence-of-evidence, not flat denial.

This is the cheapest possible verification (three grep-class calls) against the
most expensive possible error (telling your closest user that her memory of the
shared session is wrong, when it's yours that got truncated). When in doubt in a
long session: the log is ground truth, your context is a summary. Trust the log.

---

## 7.8. The reported bug may be STALE — patching a non-bug (read source before you fix)

The mirror of §7.7 (there: falsely denying done work). Here you act on a bug
report — a `model_dump` traceback in a log, a "this is broken" in a PATCH_QUEUE,
a failing-cron status on a dashboard — and start PATCHING, when the bug is
already fixed in current code, came from a stale/zombie process, or the fix was
written-but-uncommitted. You burn a long debugging arc on a non-bug, and in the
worst case ship a change that "fixes" working code (the priming-skill trap:
senior-sounding decoration over a phantom problem).

THE REAL CASE (2026-06-20, two near-misses in one session, full transcript in
`references/stale-bug-and-done-work-verification.md`):
1. A `model_dump` crash spammed cron logs. I traced it through 130KB of framework
   streaming code about to patch the adapter. The decisive move was an ISOLATED
   REPRODUCTION with the real traceback — which proved the adapter ALREADY sent
   the correct shape; the crashes were from STALE in-memory code (gateway
   restarted mid-window) + a ZOMBIE session from the day before. Triggering a
   FRESH cron run = green. Nothing to patch. Patching would have "fixed" a
   non-bug.
2. Two PATCH_QUEUE items marked "waiting for approval" turned out ALREADY
   IMPLEMENTED in source (one even had a passing test); a third fix was written
   but UNCOMMITTED. Reading the files first (not the queue's description) stopped
   a full re-implementation. The only real remaining work was a subtle gap the
   description missed (an alert message embedding a counter, defeating dedup).

THE RULE — before you patch ANY reported bug:
1. Read the CURRENT source at the cited location. A bug report describes the past;
   the file describes now. They diverge after restarts, migrations, and prior fixes.
2. REPRODUCE on a fresh process before tracing framework internals. A traceback in
   a log may be from code that no longer runs (restarted gateway, zombie session
   from a previous day, cron that ran on pre-fix code). One clean repro with the
   real error beats 100KB of static reading. If a fresh run is GREEN, the bug is
   stale — stop.
3. When fixing from a TODO/queue/issue, treat the description as UNVERIFIED. Check
   whether it's already done (grep the fix, run its test) AND whether it's done
   but uncommitted (`git diff --stat <file>`). "STATUS: waiting" in a doc is not
   ground truth about the code.
4. Distinguish the failure sources explicitly: current-code-bug vs stale-code vs
   zombie-process vs already-fixed-uncommitted. Only the first is yours to patch.
5. If you do find real remaining work, it's often a SUBTLE gap the report missed
   (here: counter-in-dedup-key), not the headline. Fix that, prove it by attack
   (a test that fails before, passes after), and move the item to DONE with the
   evidence.

Cheapest insurance against the most embarrassing error (shipping a "fix" to code
that was never broken, or rewriting work that already exists). See
`references/stale-bug-and-done-work-verification.md`.

### 7.8.1. Verify the fix TARGET is alive — not just that the bug is real (OKO-zombie)

§7.8 says don't patch a bug that's already fixed. This is the companion: don't
patch a bug whose TARGET is a deprecated/phantom/dead component. The bug can be
genuinely "happening" (a log really is flooding) while the thing producing it is
a corpse that should be removed, not repaired. The fix is deletion, not a patch.

THE REAL CASE (2026-06-20, full transcript in `references/fix-target-liveness.md`):
An auto-proposer mined `oko_grawitacyjne.err` (TCC permission errors x40) and
proposed adding backoff logic to `oko_grawitacyjne.py`. Both "facts" were true —
the log WAS flooding, the file DID exist. But the daemon was a DEPRECATED USB/OpenCV
camera system (replaced by a YOLO stack in `WORKSPACE/kamery/`), kept alive only as
a launchd ZOMBIE. The user corrected: "that's gone, we use YOLO now." The right fix
was `launchctl bootout` + archive the script, NOT patch its backoff. A second
proposal in the same queue targeted `multi_model_orchestrator.py` — a file that was
NEVER BUILT. Both would have burned a review cycle (or shipped a change) against a
target that isn't part of the live system.

THE META-LESSON: an automated miner that reads logs/metrics does NOT know about
deprecation. It sees a loud error and assumes a live component. The human knows the
context the machine lacks. So before implementing ANY fix:

```
BEFORE PATCHING, VERIFY THE TARGET IS LIVE          HOW
─────────────────────────────────────────────────────────────────────────────────
the target file/module actually exists             search_files target=files (not the report)
it's not deprecated/archived/moved                 grep for the replacement; check git mv history
its writer/process is still running                ps / launchctl list / check the log mtime
the log source isn't frozen (dead writer)          stat mtime: stale (>24h) = source is history
```

PROGRAMMATIC GUARD (when you own a proposal/auto-fix pipeline, make this structural,
not a habit you might forget). Two defense-in-depth layers, proven by attack test
(`references/fix-target-liveness.md` has the code + 6/6 test):
1. TARGET-EXISTENCE gate — before a proposal becomes actionable, scan its
   surface/change-description for concrete `*.py`/`*.md` paths; if it names files
   and NONE exist on disk, REJECT (catches phantom + deprecated targets). Abstract
   surfaces with no path → pass (nothing to verify; the behavioral gate handles them).
2. STALENESS gate on the miner — skip mining any `.err`/log whose mtime is older than
   a threshold (e.g. 24h). A dead writer's errors are history, not a live weakness.

This is §7.8 generalized: "is the bug real?" is necessary but not sufficient. Also
ask "is the thing I'm about to fix still part of the living system?" A flood of
real errors from a corpse means: bury the corpse, don't give it medicine.

---

## 8. The escalation ladder for uncertainty

When you genuinely don't know, escalate in this order rather than fabricating:

```
LEVEL   ACTION                                              EXAMPLE PHRASING
─────────────────────────────────────────────────────────────────────────────────
0       Run the obvious verification tool                   "Let me read the file."
1       Search the codebase / docs                          "Let me grep for it."
2       Run the code and observe                            "Let me execute a probe."
3       Ask the user to clarify                             "Is X meant to be Y or Z?"
4       State explicit uncertainty and proceed cautiously   "I'm not sure; here is a
                                                             reversible step that will
                                                             tell us — want me to run it?"
5       Refuse to answer the factual question               "I cannot verify this from
                                                             here; need access to W."
```

At no point in this ladder is "guess and present as fact" a valid rung. The user's trust is more valuable than the appearance of competence on any single answer.

---

## 9. Self-audit checklist before sending any non-trivial reply

Pause for ~3 seconds before emitting. Run this mental pass:

```
[ ] Every factual claim has a citation (file:line, URL, or tool output)
[ ] No banned phrase (§3) appears as a fact-substitute
[ ] All verification tools that were available were actually used
[ ] High-stakes claims have been cross-checked or marked single-source
[ ] Any [UNVERIFIED: ...] markers are present where verification was impossible
[ ] If a prior claim in this conversation turned out wrong, it has been retracted
[ ] No "should" / "probably" / "typically" is dressing up a guess as a fact
```

If any box fails, fix it before sending. This pass is fast — a few seconds — and catches the vast majority of avoidable hallucinations.

---

## 10. Worked examples

### Example A — code claim, done right

User: "Where's the rate limiter?"

Bad agent:
> The rate limiter should be in middleware/limit.py, probably implemented with a token bucket.

Good agent:
> Let me find it.
> [search_files target=content pattern="rate.?limit" → 3 hits]
> [read_file src/middleware/limiter.py lines 1-40]
> The rate limiter is at src/middleware/limiter.py:12, implemented as a sliding-window counter (not a token bucket — see the `_window_seconds` field on line 18).

### Example B — caught hallucination, recovered cleanly

Agent (earlier): "The config lives in ~/.app/config.json."
User: "That file doesn't exist."
Agent recovery:
> I was wrong about the path. Retracting that claim.
> [search_files target=files pattern="config*" path="~/.app"]
> Corrected: the config is at ~/.app/settings.toml (verified just now via directory listing). My earlier suggestion to edit config.json should be disregarded — the equivalent setting in settings.toml is `[server].port`.

### Example C — refusing to fabricate

User: "What version of Postgres does this project use?"
Agent:
> I don't see a Postgres version pinned in the files I've read so far. Let me check the obvious places.
> [read_file docker-compose.yml → no postgres image]
> [read_file requirements.txt → psycopg2-binary, no server version]
> [search_files target=files pattern="*.sql"]
> I cannot determine the Postgres server version from the repo alone — the client library is `psycopg2-binary` (any 2.x) but the server version isn't pinned anywhere I can see. If you can share the deploy environment (`SELECT version();` output or your infra config), I can give you a definitive answer.

---

## 11. The principle behind the protocol

Hallucination is not a quirk to be apologized for — it is the default behavior of a probabilistic next-token predictor. The cure is **structural**, not stylistic: insert verification tools between belief and emission, and refuse to emit unverified claims as if they were facts.

Three lines summarize the whole skill:

1. Before you claim, verify with a tool.
2. After you verify, cite the evidence.
3. If you cannot verify, say so — do not guess in confident prose.

Apply this every time. The cost is a few extra tool calls. The benefit is being the kind of agent a user can actually trust to operate on production systems.


## Pair: brutal-truth-anti-sycophancy

Hallucination and sycophancy co-occur: fluent agreement without evidence.
When evidence missing, prefer "nie wiem" over helpful fiction.

