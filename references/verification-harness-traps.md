# Verification-harness traps — when your own check lies to you

Four real instances from one session (2026-06-10, HSDB recall + Hermes patch
work). Each is a case where the VERIFICATION produced a false signal that would
have driven a wrong consequential claim if acted on naively. The pattern is more
valuable than any single bug: a probe/test/assertion you wrote yourself is an
UNVERIFIED claim until you verify the probe.

## Trap 1 — swallowed exception returns [] -> "the thing is dead"

Called an internal helper with the wrong number of positional args
(`_via_direct(query, limit)` when the signature was
`_via_direct(query, limit, metadata_filter)`). The helper had
`except Exception: return []`. So the TypeError was swallowed and the probe
returned an empty list. Reading that as "recall found nothing" almost led to
declaring the entire memory filter dead and ripping it out — when the real DB
held the records fine.

Lesson: a bare `except: return []` (or `return None`) converts a CRASH into a
silent false "nothing here". When a result is empty AND surprising, first prove
your call even reached the real logic: check arg count against the signature,
add a temporary `except Exception as e: print(e)` or remove the catch, and
confirm no exception is being eaten.

## Trap 2 — empty list != None in a fallback chain -> "fact not in DB"

`recall()` fell back from facade to a direct client ONLY when the facade
returned `None` (`if hits is None: hits = _via_direct(...)`). But the facade was
AVAILABLE and returned `[]` (zero hits) for a query where the direct path found
5. The empty list sailed through as "authoritative: nothing found", and the
working direct path was never consulted. Result: facts physically in the DB
reported as absent.

Lesson: `[]` (ran, found zero) and `None` (path unavailable/failed) are
DIFFERENT states and a fallback must branch on the right one. `if not hits:`
(covers both) is usually what you want for "try the other source"; `if hits is
None:` silently trusts an empty success. Audit every fallback for which of the
four states (`[]` / `None` / `0` / raised) it actually keys on.

## Trap 3 — assertion matched the query-echo, not the content -> false "PASS"

Round-trip test: wrote a unique marker to the store, then asserted
`"roundtrip" in recall_text(query)`. It returned True and printed "FOUND my
record". But the recall output format begins with a header that QUOTES THE QUERY
back: `[RECALL for: 'sekretna fraza ... roundtrip']`. The assertion matched that
echo, not the stored record body. The actual write had NOT come back under that
phrasing. A green light from nothing.

Lesson: never assert that a query word appears in output that contains the query.
Match a token that exists ONLY in the stored payload — a random nonce or
timestamp you generated for the write — and look for it in the record BODY
(`metadata._content` / the field that holds real content), not in the whole
response blob. Better: compare by the inserted record's ID.

## Trap 4 — test built the client wrong post-update -> "the patch broke"

After `hermes update` (349 upstream commits) re-applied an in-tree patch, a
verification test called `build_gemini_request(..., model=...)` directly — but
upstream had REMOVED the `model=` kwarg, so the test raised TypeError. A second
attempt constructed `GeminiNativeClient` in a way that didn't carry auth and got
401. Both looked like "the patch is broken". Neither was: the real code path
(`_create_chat_completion`, which the cherry-pick had merged correctly) was fine;
a direct `urllib` call with the exact payload the patch produces returned HTTP
200 on both models.

Lesson: when the production wrapper works but your hand-rolled direct probe of an
internal fails, suspect the PROBE first — wrong/stale API signature, missing auth
the wrapper supplies, a constructor arg you skipped. Re-run through the real entry
point. A TypeError/401 in your test harness is not evidence about the code under
test until you've ruled out your own setup.

## The unifying rule

All four are §3 "confident fabrication" turned inward: "the test says X" is an
unverified claim about your instrumentation. Before letting a check drive a
consequential statement ("broken"/"fixed"/"gone"/"works"), verify the check:
right signature, right code path, empty-vs-error distinguished, assertion bound
to content not echo, real path not a hand-built stub. A lamp you wired yourself
proves nothing until you've checked the wiring.
