# Vetting external project / launch / marketing claims against ground truth

Trigger: user pastes a product launch post, README, "show HN", repo pitch, or
benchmark brag and says "obadaj to" / "is this legit" / "check this out". The
same anti-hallucination discipline that governs YOUR claims applies to THEIR
claims: do not relay marketing copy as fact. Verify each claim against the
primary source (the repo, the API, the data files) before believing or repeating
it. Marketing copy is an UNVERIFIED claim until checked.

## The workflow (verify-first, in this order)

1. **De-obfuscate the link.** Launch posts often mangle URLs to dodge filters
   (`-/github.com/Org/repo`, spaces, zero-width chars). Reconstruct the real
   URL before anything else. A `github.com/<org>/<repo>` is enough to hit the API.

2. **Prove the repo exists and is real, not a husk.** Hit the GitHub API, don't
   browse:
   - `GET api.github.com/repos/<org>/<repo>` -> 404 means it doesn't exist.
     Pull `stargazers_count`, `created_at`, `pushed_at`, `license`, `size`,
     `archived`, `language`.
   - `GET api.github.com/orgs/<org>` -> public_repos, created_at, location,
     contact. Tells you if it's a one-repo throwaway or an established stable.
   - `GET .../repos/<org>/<repo>/contributors` -> bus factor. One author with
     95% of commits is a different risk profile than a team. Look up that author.
   - `GET .../git/trees/<branch>?recursive=1` -> is there real code + a `tests/`
     dir, or just a README and a logo? Count test files.

3. **Find the primary source for every NUMBER in the post.** Benchmark brags
   ("106 -> 61 -> 28, 94% noise reduction") are credible ONLY if the repo ships
   the result file. Look for `examples/`, `bench*/`, `eval*/`, `*result*.json`,
   `*analysis*.json`. Fetch via raw.githubusercontent.com and read the actual
   keys. Match each posted number to a JSON field. Numbers that exist in the file
   = verified. Numbers NOT in the file = the post invented or rounded them.

4. **Separate MEASURED from ESTIMATED.** The highest-value catch. Posts quote the
   flattering number. In the SEC-AF case the post said "~200+ agent calls" but the
   benchmark JSON had `agent_invocations_reported: 44` (measured) and a separate
   `cost_estimation.estimated_agent_calls: {min:166, max:255}` (estimate). The
   "200+" was the cost estimate, not a measurement. Always grep the data for BOTH
   a measured field and an estimate field; report which one the marketing used.

5. **Read the code behind the headline verb.** If the pitch hinges on a strong
   claim ("proves exploitability", "guarantees", "verifies", "autonomous"), open
   the module that supposedly does it and check whether the mechanism matches the
   verb. Red flag: the decisive step is a single LLM call dressed as proof. In
   SEC-AF, `prove/verdict.py` had a 12-module pipeline (tracer, sanitization,
   exploit, sandbox...) BUT the final verdict was `app.ai(schema=VerdictDecision)`
   - one structured LLM call, comment literally said "pure judgment task, no file
   access needed". And `sandbox.py` self-admitted "Future: Docker containers" -
   so "proving" was really "structured LLM reasoning + optional subprocess", not
   PoC-or-it-didn't-happen. The verb was oversold; say so precisely.

6. **Note what the post OMITS.** Cost, wall-clock, model dependency, and partial
   results are usually buried in the data file and absent from the pitch. SEC-AF:
   77 min wall-clock + 22k compute-seconds per audit, ran on a specific model
   (Kimi K2.5 via OpenRouter), and 31 of 61 findings were `findings_not_verified`
   - the post showed only the 28 confirmed. Surface the omissions.

7. **Credit honesty where it's real.** Vetting is not dunking. SEC-AF's
   `tool_comparison` wrote competitors "N/A - no verification" instead of faking
   numbers for them - that's an honesty signal worth stating. Calibrated verdict
   beats reflexive cynicism.

## Verdict shape

End with a one-paragraph calibrated verdict that separates three things:
- **Real**: repo/code/tests/license exist and the core idea is sound.
- **Oversold**: which specific claims the data doesn't fully support (with the
  measured-vs-marketed number side by side).
- **Hidden**: cost / time / model-dependency / partial-results the post skipped.

Avoid both "it's a scam" (usually false - the code is often real) and "looks
great!" (relayed marketing). The deliverable is: which claims survived contact
with the primary source, and which didn't.

## Pitfall: don't run your own stylometric scorer on the wrong language

Tempting to run a PL prose AI-detector on an English bullet-list launch post.
Calibration won't transfer (bullet lists are flat-rhythm by construction; a
PL-calibrated rhythm scorer flags them regardless of authorship). State the
result as orientational only, or skip it. The repo-data verification (steps 2-6)
is the load-bearing evidence; stylometry on the blurb is at most a footnote.
