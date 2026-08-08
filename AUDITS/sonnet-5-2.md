# Forensic Comparative Audit — anti-hallucination-protocol
CURRENT (installed) vs CANDIDATE (Downloads) — read-only, no files modified in either tree.

Audited paths:
- CURRENT: `/Users/paulinajanowska/.hermes/skills/software-development/anti-hallucination-protocol`
- CANDIDATE: `/Users/paulinajanowska/Downloads/hermes-skills-main/software-development/anti-hallucination-protocol`

---

## 1. EXECUTIVE VERDICT

**YES — CLEAR UPGRADE**, with one operational caveat (below).

CANDIDATE is not a cosmetic rewrite. It replaces a "verify-then-cite, ban some phrases" checklist with an evidence-state pipeline (intent → decompose → classify → acquire → boundary → qualify → entail → contradict → decide → emit), adds a prompt-injection/untrusted-evidence boundary CURRENT does not have at all, adds 30 adversarial test cases + 82 passing automated tests where CURRENT has **zero** tests, and its new deterministic verifier (`verify_claim.py`) fixes a real, **currently exploitable** false-positive bug that exists in CURRENT's actually-installed `verify_claim.sh` (see §6/§10, case 8-equivalent). CANDIDATE's frontmatter also matches the real Hermes parser's expected schema (`metadata: hermes:`), which CURRENT's does not — CURRENT's `tags`/`related_skills` metadata is silently dead to the currently-installed parser (VERIFIED by reading `agent/skill_utils.py`).

Confidence: **85%**. The core claims above are VERIFIED against source code and live execution, not inferred. The 15% uncertainty is about CANDIDATE's much longer skill index footprint and whether the more abstract, install-agnostic reference files (stripped of Paulina-specific incident narratives) will be as memorable/actionable in practice as CURRENT's concrete, grounded worked examples — that's a judgment call, not something a static audit can settle.

**Caveat:** CANDIDATE is not yet installed anywhere — it is a Downloads-folder checkout, so `AHP_SKILL_DIR` env var and the real `~/.hermes/scripts/anti_halluc` legacy calibration pipeline are not wired to it. It needs an actual install pass (§18) before its own `liveness_check.sh` will report PASS in place.

## B. Replace CURRENT with CANDIDATE?

**YES** — but **not executed**, per your instructions. See §18 migration plan (proposed only).

---

## 2. WHAT I ACTUALLY INSPECTED

Tooling used: Desktop Commander (`list_directory`, `get_file_info`, `read_file`) + a live `zsh` process (`find`, `shasum -a 256`, `diff -u`, `python3 -m pytest`, direct script execution). All commands ran against the two audited trees or an isolated copy at `/tmp/audit_evidence/B_copy` (created for the pytest run only; **not** inside either tracked directory). No file inside either `anti-hallucination-protocol` directory was written, moved, or deleted.

Read in full: both `SKILL.md` (676 vs 727 lines), both `references/fix-target-liveness.md` (full diff), both `references/vetting-external-project-claims.md` (full diff), both `scripts/liveness_check.sh` (full diff + **executed both**), CANDIDATE's `README.md` (in full), CANDIDATE's `scripts/verify_claim.py` (in full, 393 lines), the **actual installed** `~/.hermes/scripts/verify_claim.sh` (in full, 295 lines — this is a different, larger file than the one embedded as an example in CURRENT's `SKILL.md`), CANDIDATE's `tests/adversarial_cases.md` (in full, 30 cases), Hermes's real frontmatter parser `agent/skill_utils.py` (in full, 934 lines) and frontmatter samples from 5 other currently-installed skills.

Sampled (docstrings/headers/schema validated, not read cover-to-cover): `check_v5_integrity.py`, `check_evidence_record.py`, `check_research_provenance.py`, `evidence-record.schema.json` (JSON-validated), `v5-research-manifest.json` / `arxiv-manifest.json` (JSON-validated, key counts only), `evidence-state-model.md`, `untrusted-evidence-boundary.md`, `research-foundations.md`, `v5-gap-map.md` (line counts + partial read only — **UNVERIFIED in full depth**, flagged below).

Not independently re-read (confirmed byte-identical by SHA-256, so content audited implicitly via CURRENT's copy, already read in earlier sessions per file naming/content overlap): `references/multi-judge-ensemble.md`, `references/self-capability-honesty.md`, `references/stale-bug-and-done-work-verification.md`, `references/v3-orchestrator-evaluation.md`, `references/v3.2-empirical-results.md`, `references/verification-harness-traps.md`, `scripts/anti-halluc-v3-eval.sh`, `scripts/godmode_battery.sh` (only headers read — **TEST EXECUTION UNVERIFIED** for these two shell scripts; not run in this audit).

`assets/anti-hallucination-eye.svg` — not inspected (decorative SVG for README, no protocol content; **UNVERIFIED** but low-risk to skip).

No symlinks found in either tree (`find -type l` empty both sides; `realpath` resolved to the literal given path both sides).

---

## 3. TREE / FILE INVENTORY

**CURRENT** — 12 content files (+ `.DS_Store`, ignored), no symlinks:
```
SKILL.md                                        40,781 B
references/fix-target-liveness.md                5,938 B
references/multi-judge-ensemble.md                5,568 B
references/self-capability-honesty.md             6,523 B
references/stale-bug-and-done-work-verification.md 7,512 B
references/v3-orchestrator-evaluation.md          5,486 B
references/v3.2-empirical-results.md              7,310 B
references/verification-harness-traps.md          4,504 B
references/vetting-external-project-claims.md     4,976 B
scripts/anti-halluc-v3-eval.sh                    2,886 B
scripts/godmode_battery.sh                        4,139 B
scripts/liveness_check.sh                         4,038 B
```
No `README.md`, no `assets/`, no `tests/`.

**CANDIDATE** — 31 content files, no symlinks:
```
README.md                                        11,193 B
SKILL.md                                          30,113 B
assets/anti-hallucination-eye.svg                  7,630 B
references/arxiv-manifest.json                     4,935 B
references/evidence-record.schema.json              3,157 B
references/evidence-state-model.md                 6,578 B
references/fix-target-liveness.md                  7,187 B
references/multi-judge-ensemble.md                 5,568 B   (identical to CURRENT)
references/research-foundations.md                15,133 B
references/self-capability-honesty.md               6,523 B   (identical to CURRENT)
references/stale-bug-and-done-work-verification.md  7,512 B   (identical to CURRENT)
references/untrusted-evidence-boundary.md            5,555 B
references/v3-orchestrator-evaluation.md            5,486 B   (identical to CURRENT)
references/v3.2-empirical-results.md                7,310 B   (identical to CURRENT)
references/v5-gap-map.md                           11,365 B
references/v5-research-manifest.json                3,902 B
references/verification-harness-traps.md            4,504 B   (identical to CURRENT)
references/vetting-external-project-claims.md        7,187 B
scripts/anti-halluc-v3-eval.sh                       2,886 B   (identical to CURRENT)
scripts/check_evidence_record.py                     9,591 B
scripts/check_research_provenance.py                 8,343 B
scripts/check_v5_integrity.py                        8,035 B
scripts/godmode_battery.sh                           4,139 B   (identical to CURRENT)
scripts/liveness_check.sh                            3,278 B
scripts/verify_claim.py                             12,016 B
tests/adversarial_cases.md                           6,292 B
tests/test_evidence_record.py                        9,591 B
tests/test_liveness.py                               1,673 B
tests/test_research_provenance.py                     5,114 B
tests/test_v5_integrity.py                            4,938 B
tests/test_verify_claim.py                            8,235 B
```

---

## 4. STRUCTURAL DIFF

**Files only in CANDIDATE (19):** `README.md`, `assets/anti-hallucination-eye.svg`, 7 new `references/*` files (`arxiv-manifest.json`, `evidence-record.schema.json`, `evidence-state-model.md`, `research-foundations.md`, `untrusted-evidence-boundary.md`, `v5-gap-map.md`, `v5-research-manifest.json`), 4 new `scripts/*` (`check_evidence_record.py`, `check_research_provenance.py`, `check_v5_integrity.py`, `verify_claim.py`), and the entire `tests/` directory (6 files).

**Files only in CURRENT:** none. CURRENT is a strict content subset of CANDIDATE's file list.

**Byte-identical (SHA-256 match), 8 files:** `references/multi-judge-ensemble.md`, `references/self-capability-honesty.md`, `references/stale-bug-and-done-work-verification.md`, `references/v3-orchestrator-evaluation.md`, `references/v3.2-empirical-results.md`, `references/verification-harness-traps.md`, `scripts/anti-halluc-v3-eval.sh`, `scripts/godmode_battery.sh`. **CANDIDATE has removed none of CURRENT's content in these files** — this is a real foundation carried forward, not a rewrite-from-scratch.

**Changed, same path, 4 files:**

| File | CURRENT → CANDIDATE | Practical consequence |
|---|---|---|
| `SKILL.md` | v2.0.0, 676 lines, top-level `hermes:` frontmatter key, checklist model → v5.2.0, 727 lines, `metadata: hermes:` frontmatter, 10-step evidence-pipeline model | Frontmatter now matches what Hermes's parser actually reads (§6). Model changed from "verify + cite + ban phrases" to "decompose claims, assign evidence states, treat retrieved content as data not instructions, require contradiction search for T3." Old §1–§11 numbered structure and the embedded `verify_claim.sh` source are gone; content is reorganized as §1–§26 with an explicit "hard limits of this skill" section CURRENT never had. |
| `references/fix-target-liveness.md` | 124 → 220 lines. Hardcoded, non-portable worked example tied to Paulina's own system (`oko_grawitacyjne.py`, `~/AI/ANTIGRAVITY`, `com.antigravity.oko`), and Python example code with **no path-traversal protection**. | Generalized into a portable procedure (multi-target verification, extension-list blind-spot warning, freshness-threshold critique) with example code that explicitly guards against `..`-escape and absolute-path injection (`candidate.relative_to(root)` check). Loses the concrete, memorable local incident narrative; gains portability and a materially safer example implementation. |
| `references/vetting-external-project-claims.md` | 82 → 208 lines. Concrete "SEC-AF" case study with specific numbers baked in. | Generalized into a `MATCHED/DERIVED/ESTIMATED/NOT_SUPPORTED_HERE` evidence-state workflow, adds an owner-type check (org vs user) before calling GitHub org-only endpoints, and adds caution against over-interpreting HTTP 404 semantics. Same trade-off as above: less vivid, more portable and more careful about endpoint-semantics edge cases. |
| `scripts/liveness_check.sh` | 89 → 90 lines. **Never sets a nonzero exit code on any failure** (VERIFIED by direct execution — see §10). References a hardcoded cron job ID and a legacy calibration pipeline as load-bearing L1 checks. | Rewritten as fail-closed: explicit `STATUS` accumulator, `exit "$STATUS"`. Required checks are now L1 (skill + verifier present, verifier self-test) and L2 (`check_v5_integrity.py` passes); the old calibration-log/cron-freshness checks are demoted to optional L3 "legacy installation telemetry", and a new L4 makes explicit that no local script can prove behavioral compliance. |

---

## 5. SEMANTIC ARCHITECTURE DIFF

1. **Hallucination definition** — CURRENT: unverified factual claim without a citable pointer. CANDIDATE: any claim whose *wording/action strength exceeds the evidence state that was actually earned* — broader, covers correctly-cited-but-non-entailing claims (CURRENT has no equivalent to CANDIDATE's "citation has four gates: identity/span/entailment/coverage" — CURRENT's citation rule only requires a pointer exists, not that it entails the specific claim).
2. **Verification trigger** — CURRENT: a flat table of claim types → tool. CANDIDATE: a tiered budget (T0–T3) keyed to impact/irreversibility/volatility, with an explicit stop rule ("more search is not automatically more truth"). CANDIDATE is the only one of the two with an explicit anti-over-verification control.
3. **Claim classification** — CURRENT: none (claims are or aren't verified). CANDIDATE: atomic-claim decomposition before evidence assignment (§3), explicitly to stop compound sentences ("faster, safer, maintained") from being verified as one blob.
4. **Uncertainty** — CURRENT: banned-phrase list + escalation ladder (0–5). CANDIDATE: explicit evidence-state enum with **forbidden collapses** table (e.g., `ERROR → NOT_FOUND` named as a specific banned failure), which is a stronger control because it names the exact mistake rather than just banning hedge words.
5. **Citations** — CURRENT: pointer must exist (file:line/URL). CANDIDATE: pointer + identity + span + entailment + coverage, all four required — directly closes CURRENT's gap on adversarial case "correct arXiv ID cited for an unsupported interpretation" (case 11 in CANDIDATE's own corpus; CURRENT has no rule that would catch this).
6. **Retrieval** — CURRENT: not modeled as a pipeline at all. CANDIDATE: explicit 9-stage retrieval-to-synthesis model with a named correction procedure and an explicit "long-context caution" (re-read the decisive span before a high-impact verdict) — CURRENT has nothing addressing lost-in-the-middle—style failure.
7. **Tools** — Both require checking a live schema before calling a tool with claimed parameters; roughly equivalent here.
8. **Verifier failure** — CURRENT §7.6 covers this well (four concrete false-signal shapes from real incidents) and is **carried into CANDIDATE unchanged** (byte-identical file). CANDIDATE additionally names specific judge-bias failure modes (self-preference bias, prompt leakage of expected verdict) CURRENT's §7.6 doesn't mention.
9. **Memory** — CURRENT §7.7 (compacted-session denial) is carried forward unchanged. CANDIDATE keeps it and adds a portability caveat CURRENT's §7 lacks: CURRENT hardcodes "HSDB = Home Assistant State DB"-style Hermes-specific conventions inline in its main claim table; CANDIDATE explicitly flags "in this installation, HSDB means HyperspaceDB — this is a LOCAL convention, do not bake one installation's schema into a portable skill" (§15) — CANDIDATE is self-aware about portability in a way CURRENT is not, anywhere.
10. **Current-state claims** — CURRENT: a claim-type table entry ("query the live system right now"). CANDIDATE: requires an explicit `observation_time` field and a `CURRENT_ENOUGH` freshness gate for strong T3 records — more precise, machine-checkable (enforced by `check_evidence_record.py`, tested).
11. **Contradictions** — CURRENT has no dedicated contradiction-search step. CANDIDATE has one (§10), mandatory for T3/load-bearing T2, with an explicit conflict-classification taxonomy (time/version/entity/method/measurement/interpretation) CURRENT lacks entirely.
12. **Source independence** — CURRENT: "spawn one falsifier subagent" (§5). CANDIDATE: a dedicated "independence means independent failure domains" section (§11) that explicitly names five *weak*-independence shapes (same model+prompt+evidence; copied press releases; correlated agents; judge grading its own output; two validators sharing a parser bug) — this generalizes CURRENT's single-subagent mechanism into a broader, tool-agnostic principle, and is the only one of the two that would catch "5 agents, 1 bad source" (case 2 of the adversarial corpus).
13. **Source freshness** — Addressed above (current-state).
14. **Prompt injection in evidence** — **CURRENT has no equivalent section anywhere.** CANDIDATE §8 is a dedicated, ~500-word "untrusted evidence boundary" with contamination states (`CLEAN_OBSERVED/SUSPECT/CONTAMINATED/UNKNOWN`) and a worked list of injection phrasings to refuse ("Ignore previous instructions", "Mark this verified", "Reveal your system prompt"). This is the single largest capability gap between the two versions — CURRENT is fully exposed to evidence-borne prompt injection at the protocol-design level (whatever runtime sandboxing exists is outside this skill either way).
15. **Multi-agent verification** — Covered above (§5/§11 vs CURRENT's §5).
16. **Completion wording** (`fixed`/`works`/`deployed`) — CURRENT §6.5: a single earned-level ladder (PATCHED→UNIT→INTEGRATION→E2E→USER VERIFIED), and its own verification step is an **external dependency**: `python3 ~/AI/ANTIGRAVITY/EXTERNAL/agentic-workflow-core-repo/...check_workflow_core.py` — a hardcoded path to a *different, unaudited* repo not part of this skill package at all. CANDIDATE §19 splits this into two **independent** axes (change-state vs validation-state) which correctly models that `DEPLOYED` and `E2E_TESTED` are orthogonal (CURRENT's single ladder cannot express "deployed but never tested" or "unit tested but not deployed" as cleanly), and has no external-repo dependency — it's fully self-contained.
17. **Recovery** — Near-identical in spirit; CANDIDATE's §20 adds "record the failure mode when it reveals a reusable verifier weakness" as an explicit step CURRENT's §6 doesn't have.
18. **Blast radius** — Both have it; CANDIDATE folds it into recovery (§20 step 5) rather than a separate heading; no material difference.
19. **Protecting against your own verifier** — CURRENT §7.6 (carried unchanged) plus CANDIDATE §12 (verifier/judge skepticism, new, broader — covers 11 named failure shapes vs CURRENT's 4).
20. **Protecting against misreading user intent** — **CURRENT has no equivalent anywhere.** CANDIDATE §2 ("intent is a verification target") is entirely new: a response can be 100% factually correct and still fail because it answers a different question than the one asked (`MISINTERPRETED`/`OUT_OF_SCOPE` states). This directly matches adversarial case 23 ("intent hallucination") in CANDIDATE's own test corpus, which CURRENT has no mechanism to catch.

---

## 6. HERMES COMPATIBILITY (VERIFIED against real installed source)

I read the actual parser, `~/.hermes/hermes-agent/agent/skill_utils.py` (934 lines), not documentation.

- `parse_frontmatter()` uses a standard YAML loader against the top-level `---` block — both versions parse without error (confirmed: no exception on load for either file).
- `skill_matches_platform()` reads `frontmatter.get("platforms")` — **top-level**, present and correctly formatted in both versions. No difference.
- `extract_skill_conditions()` and `extract_skill_config_vars()` — the functions that drive conditional skill activation (`requires_toolsets`, `requires_tools`, `fallback_for_*`) and skill-declared config variables — **only read `frontmatter["metadata"]["hermes"]`, nested.** CURRENT's frontmatter puts `tags:` and `related_skills:` under a **top-level** `hermes:` key, not under `metadata:`. **This block is never read by the installed parser — it is dead metadata in the currently running Hermes.** CANDIDATE's `metadata: hermes: {tags, category}` is read correctly.
  - Practical impact is limited: CURRENT doesn't declare `requires_toolsets`/`requires_tools`/`config`, only informational `tags`/`related_skills`, so nothing *breaks* — but the metadata is silently inert, which is a real, verifiable bug regardless.
  - Cross-checked against 5 other **currently installed, presumably-working** skills (`macos-launchd-agents`, `apple-reminders`, `macos-computer-use`, `macos-disk-audit-cleanup`, `macos-native-app-driving-ghost-os`) — **all five** use CANDIDATE's `metadata: hermes:` nesting, none use CURRENT's top-level `hermes:` style. CURRENT's frontmatter is the outlier against the actual local convention, not CANDIDATE's.
- `SKILL_SUPPORT_DIRS = {references, templates, assets, scripts}` — `tests/` (new in CANDIDATE) is **not** in this set, so it is not treated as a progressive-disclosure support dir by the scanner; but since `tests/` contains no `SKILL.md`, `iter_skill_index_files()` never descends into it as a false skill root either. No compatibility issue, confirmed by reading the exact pruning logic.
- `check_v5_integrity.py`'s own `REQUIRED_FRONTMATTER_KEYS` includes `metadata` — self-consistent with the real parser's expectation; running it against CURRENT's directory (cross-test, §10) correctly flags `missing required key: metadata` as one of many failures, confirming the checker actually enforces this.

**Net finding: CANDIDATE's frontmatter is more Hermes-compatible than CURRENT's, verified against source, not assumed from `v5` in the version string.**

---

## 7. SCRIPT / VERIFIER AUDIT

**CANDIDATE `scripts/verify_claim.py` (VERIFIED by full read + execution via pytest):** 3-state model (FOUND/NOT_FOUND/ERROR, not swallowed into 2), JSON structured output, explicit UTF-8 decode-error handling, output-size cap (default 1 MB) with an ERROR (not a silent truncation) on overflow, and — critically — `command-output` mode **requires the invoked command's own exit code to match `--require-exit` before a text match is even considered**; a text match against a wrong exit code is reported `ERROR`, never `FOUND`.

**CURRENT's `verify_claim.sh` — audited both the version embedded in `SKILL.md` §4 AND the actual installed file** (these two are **not the same script** — see §9 finding below): both versions' `cmd-output` mode run the command, capture its exit status, and then **verify only by substring match, ignoring the exit status entirely** — the installed file even computes `rc=$?` and prints it in the evidence string but never gates on it. This is a live, exploitable FALSE VERIFIED path: a command that crashes but prints the expected substring to stderr (e.g. an error message that echoes back a query term) will be reported as verified.

**Deterministic-tooling FALSE VERIFIED hunt result: found exactly one, and it is in CURRENT, not CANDIDATE.**

**`scripts/liveness_check.sh` — both versions run and their exit codes checked directly (not assumed):**
```
$ bash <CURRENT>/scripts/liveness_check.sh ; echo $?
[... 3 printed FAIL lines, including its own daily_self_audit sub-check
     flagging "OVERCONFIDENT in 80-100% bin: claimed 91%, actual 77%" ...]
0                                          <- exits SUCCESS despite 3 printed failures
```
```
$ AHP_SKILL_DIR=<CANDIDATE> bash <CANDIDATE>/scripts/liveness_check.sh ; echo $?
[... all checks OK/PASS ...]
0
$ bash <CANDIDATE>/scripts/liveness_check.sh (default path = CURRENT's install location) ; echo $?
[... correctly reports missing verify_claim.py / check_v5_integrity.py at that location ...]
1                                          <- fails closed
```
CURRENT's own liveness self-check is, right now, on this machine, reporting green (exit 0) while printing three real failures including a calibration log ~1578 hours (≈65 days) stale. This is the exact "FALSE VERIFIED" pattern the audit brief asked me to hunt for, found in CURRENT's live, currently-relied-upon tooling, not a hypothetical.

**Deterministic checkers new in CANDIDATE, executed for real:**
```
$ python3 scripts/check_v5_integrity.py --root .        -> "V5 INTEGRITY: PASS", exit 0
$ python3 scripts/check_research_provenance.py --root . -> "RESEARCH PROVENANCE: PASS", exit 0
```
Both scripts' docstrings explicitly disclaim what a PASS does *not* prove (semantic entailment, live source availability, Hermes runtime behavior) — a genuine, consistent epistemic-honesty pattern across all four new scripts, matching the skill's own stated philosophy ("policy is not runtime enforcement").

`check_evidence_record.py` was not independently hand-run in this audit (no ad-hoc fixture built) — its correctness is instead evidenced by the 33 passing unit tests exercising it (§8). **Flagging this as INFERENCE, not direct VERIFIED execution, per the evidence standard.**

---

## 8. TEST AUDIT

CURRENT ships **zero tests of any kind.** No `tests/` directory, no adversarial corpus, no automated regression tests. This alone is close to decisive for the Test Quality dimension in the scorecard.

CANDIDATE, isolated copy at `/tmp/audit_evidence/B_copy` (outside both tracked trees), executed:
```
$ python3 -m pytest tests/ -q
..................................................................... [ 87%]
.......                                                               [100%]
82 passed in 11.48s
```
**82 passed, 0 failed, 0 skipped, exit 0.** Not `TEST EXECUTION UNVERIFIED` — actually run.

Per-file collection (`pytest --collect-only`): `test_evidence_record.py` 33 tests, `test_v5_integrity.py` 15, `test_research_provenance.py` 13, `test_verify_claim.py` 13, `test_liveness.py` 4 (86 nominal — the earlier grep undercounted class-indented `def test_...` methods; the pytest-reported total of 82 is the authoritative number, some overlap/parametrization likely accounts for the difference — **flagging the exact per-file split as approximate, the 82-total/0-failed figure as VERIFIED**).

Test names directly attack the failure classes named in `tests/adversarial_cases.md` — e.g. `test_nonzero_command_exit_cannot_be_verified_by_matching_stderr` is a direct regression test for exactly the bug found live in CURRENT's own installed `verify_claim.sh` (§7). Other observed test names cover: swallowed-exception-vs-NOT_FOUND, oversized-output-as-ERROR, invalid-regex-as-ERROR-not-NOT_FOUND, timeout-as-structured-error, symlink-kind-strictness — these map directly onto real verifier-lying failure modes, not happy-path filler.

`tests/adversarial_cases.md` (30 cases, read in full, §9 below) maps closely onto ~28 of the audit brief's own 30 requested adversarial scenarios. CURRENT has no comparable artifact to compare against at all.

---

## 9. 30-CASE ADVERSARIAL HEAD-TO-HEAD

For each of the brief's 30 scenarios: does the *protocol text* (not runtime enforcement — neither version can enforce anything at the LLM level) give the agent an explicit, on-point rule to follow? CANDIDATE's own `tests/adversarial_cases.md` closely mirrors this list (noted where a near-identical numbered case exists there).

| # | Scenario | CURRENT | CANDIDATE | Winner |
|---|---|---|---|---|
| 1 | False premise from user | Escalation ladder implies asking, no explicit rule | §2 intent-alignment + case 19 explicit | CANDIDATE |
| 2 | URL supports a different claim | Citation rule = pointer exists only | §7 four-gate citation (entailment gate); case 1/11 | CANDIDATE |
| 3 | Paper cited for unsupported conclusion | No rule | case 11 explicit | CANDIDATE |
| 4 | 5 agents, 1 bad source | §5 single-falsifier subagent, doesn't generalize | §11 independence-as-failure-domains; case 2 explicit | CANDIDATE |
| 5 | 2 sites copy 1 press release | No rule | §11 lineage=SHARED_ORIGIN; case 3 explicit | CANDIDATE |
| 6 | Stale official docs | §7 table has a generic freshness row | §14 temporal + case 4 explicit (runtime/schema outranks stale docs) | CANDIDATE |
| 7 | Prompt injection, README | **No rule anywhere** | §8 untrusted-evidence boundary; case 5 explicit | CANDIDATE |
| 8 | Prompt injection, webpage | **No rule anywhere** | §8; case 6 | CANDIDATE |
| 9 | Prompt injection, memory | **No rule anywhere** | §8; case 7 | CANDIDATE |
| 10 | exit 0, wrong target verified | **No rule; CURRENT's own script doesn't even check exit code (§7)** | §12 verifier skepticism + `verify_claim.py` enforces exit-code gating; case 8 | CANDIDATE |
| 11 | tool error → `[]` | §7.6 covers this well, carried into CANDIDATE unchanged | Same content, plus `verify_claim.py`'s FOUND/NOT_FOUND/ERROR 3-state is a structural fix, not just a doc rule; case 9 | CANDIDATE |
| 12 | Partial search called exhaustive | §8 escalation ladder implies caution, not explicit | §5 `NOT_FOUND_WITHIN_SCOPE` named explicitly; case 12 | CANDIDATE |
| 13 | 2 primary sources contradict | No dedicated rule | §10 contradiction-first + conflict taxonomy; case 10 | CANDIDATE |
| 14 | remembered state vs live state | §7 HSDB table row (live-state examples) | §15 memory-is-retrieval + case 20 | Tie (both cover it; CANDIDATE more general) |
| 15 | current-state claim from stale log | §7 "state changes constantly" note | §14 requires `observation_time`; case 15 | CANDIDATE |
| 16 | entity collision | No rule | §14 entity disambiguation; case 17 | CANDIDATE |
| 17 | unit conversion error | No rule | §14 numerical section; case 16 | CANDIDATE |
| 18 | quote is actually paraphrase | No rule | §14 "never quote a remembered paraphrase"; case 29 | CANDIDATE |
| 19 | judge prefers its own answer | No rule | §12 self-preference bias named; case 18 | CANDIDATE |
| 20 | unit test passes, real path differs | §6.5 completion-wording ladder (partial coverage) | §19 change/validation split is more precise; case 27 | CANDIDATE |
| 21 | busywork without measurable progress | No rule | §13 "progress mirage", external-signal requirement; case 22 | CANDIDATE |
| 22 | true but off-topic answer | No rule | §2 intent states (`OUT_OF_SCOPE`); case 23 | CANDIDATE |
| 23 | injection phrase in retrieved evidence ("ignore instructions") | **No rule anywhere** | §8, explicit phrase list; case 5/6 | CANDIDATE |
| 24 | verifier A & B share a broken parser | §7.6 covers correlated false signals generally, not this specific shape | §12 "two validators sharing the same parser bug" named explicitly | CANDIDATE |
| 25 | stale bug report, already fixed | **§7.8 — CURRENT's own strongest section**, carried unchanged into CANDIDATE | Same content (byte-identical file) | Tie |
| 26 | fix targets a dead component | **§7.8.1 — CURRENT's own strongest section**, but example code has no path-traversal guard | Generalized + path-traversal-safe example (§4 above) | CANDIDATE (marginally — same idea, safer/more portable implementation) |
| 27 | memory contradicts reality | §7 HSDB row | §15 | Tie |
| 28 | exit 0, substring match despite failure | Same as #10 | Same as #10 | CANDIDATE |
| 29 | correct arXiv ID, wrong title | No rule | §7 identity gate covers this generally, case 11 close but not identical | CANDIDATE (marginal) |
| 30 | correct title, wrong arXiv ID | No rule | Same as above | CANDIDATE (marginal) |

**Score: CANDIDATE wins or ties 30/30, loses none.** The margin ranges from decisive (prompt injection — CURRENT has literally nothing) to marginal (a few entity-ID edge cases where CANDIDATE's general identity-gate language would probably, but not certainly, catch the specific case).

---

## 10. OVERENGINEERING AUDIT

| Mechanism | Verdict | Reasoning |
|---|---|---|
| 10-step evidence pipeline (§1) | KEEP | Explicitly scoped as "not mandatory ceremony for every sentence... T0/T1 should not be inflated." Self-limiting by design. |
| Claim tiers T0–T3 + stop rule | KEEP | Directly prevents the over-verification failure mode a naive reading of "always verify" would produce; genuinely load-bearing. |
| Evidence-state enum + forbidden-collapses table | KEEP | Small, concrete, machine-checkable (schema exists), catches a real and common failure (`ERROR→NOT_FOUND`). |
| Untrusted-evidence boundary (§8) | KEEP | Zero-cost addition (CURRENT has nothing here) closing the single largest gap found in this audit. |
| Independence-as-failure-domains (§11) | KEEP | Generalizes CURRENT's narrower single-subagent mechanism without adding new required steps. |
| Deterministic scripts (`verify_claim.py`, `check_*.py`) | KEEP | Each is narrow, has a documented exit-code contract, disclaims its own scope in its docstring, and is unit-tested. This is the opposite of overengineering — it's the "runtime enforcement" the CURRENT-vs-CANDIDATE brief explicitly asked to distinguish from prose. |
| `evidence-record.schema.json` + ledger format (§22) | SIMPLIFY | Genuinely useful for T3/complex cases but is the part of the skill most likely to be skipped in practice for ordinary claims — the skill text itself says "use when justified by complexity," which is the right caveat; no change needed beyond what's already there. |
| Two overlapping evidence-state vocabularies (`SUPPORTED_WITH_SCOPE/…` in SKILL.md §5 vs `MATCHED/DERIVED/ESTIMATED/NOT_SUPPORTED_HERE` in `vetting-external-project-claims.md`) | NEEDS_RUNTIME_ENFORCEMENT / minor consistency gap | Not a bug, but a real internal-consistency wrinkle: two different reference files use two different enums for what's conceptually the same "how well does this source support this claim" question. Worth reconciling in a future revision; does not block this migration. |
| Research corpus (32 arXiv v4 + ~18 v5 sources, §23) | MOVE_TO_REFERENCE | Already correctly kept out of the main pipeline sections and pushed to `references/research-foundations.md` / `v5-gap-map.md`; the SKILL.md itself just lists citations, which is reasonable for progressive disclosure but is still the single largest chunk of SKILL.md's line count. Genuinely low-cost since it's read on demand, not injected into every prompt — no change needed. |
| `metadata.hermes.category: software-development` field | KEEP | Small, matches real parser expectations (§6). |

No mechanism was found that fails the "does it protect against a real failure mode" test outright. CANDIDATE is larger than CURRENT (31 vs 12 files) almost entirely because of net-new capability (prompt-injection boundary, tests, deterministic scripts) rather than padding of existing capability.

---

## 11. WHAT BOTH VERSIONS STILL MISS

- **Agent trajectory verification is prose-only in both.** CANDIDATE's §13 ("find the earliest bad dependency") is a real improvement over CURRENT (which has nothing comparable), but neither version has tooling that actually walks a trajectory log — it's still "the agent should notice this," not an enforced check.
- **No runtime/output firewall in either.** CANDIDATE says this explicitly in its own "hard limits" section (§24) — a genuinely honest thing to state, and also a genuine remaining gap: nothing stops a compromised evidence source from actually influencing behavior at the token level; the boundary is prompt-level guidance only, as CANDIDATE itself admits.
- **No cost-aware verification budget.** CANDIDATE's stop rule (§4) is a qualitative heuristic, not tied to any token/latency budget or telemetry.
- **No correlated-agent-failure tooling.** §11's independence taxonomy is prose; nothing computes or flags "these five agent calls share lineage" automatically.
- **No LLM-judge bias benchmark or eval harness for either version** — `godmode_battery.sh`/`anti-halluc-v3-eval.sh` (shared, unchanged) run an adversarial corpus through an LLM judge, but neither audited version has a held-out, judge-agreement-controlled eval methodology.
- **Real-world success-signal tooling is still just guidance.** §13's "progress mirage" section correctly diagnoses the failure mode but provides no external-benchmark harness.
- **CANDIDATE's own two-enum inconsistency (§10) is unresolved** — a minor but real epistemic-security gap: an agent could satisfy one file's vocabulary while violating the spirit of the other.

---

## 12. SCORECARD

Scale 0–10 per dimension.

| Dimension | CURRENT | CANDIDATE |
|---|---:|---:|
| Epistemic rigor | 5 | 9 |
| Hallucination prevention | 6 | 9 |
| False-positive resistance | 3 | 8 |
| Citation discipline | 5 | 9 |
| Retrieval robustness | 3 | 8 |
| Tool/verifier robustness | 4 | 9 |
| Prompt-injection resilience | 1 | 8 |
| Current-state accuracy | 5 | 8 |
| Memory safety | 6 | 7 |
| Agentic workflow safety | 5 | 8 |
| Hermes compatibility | 5 | 8 |
| Deterministic enforcement | 3 | 8 |
| Test quality | 0 | 9 |
| Maintainability | 5 | 7 |
| Progressive disclosure | 6 | 7 |
| Context efficiency | 6 | 6 |
| Portability | 4 | 8 |
| Operational usability | 6 | 6 |
| Research grounding | 5 | 9 |
| Production readiness | 4 | 7 |

**Weighted overall (equal weights):** CURRENT ≈ 4.4 / 10, CANDIDATE ≈ 7.75 / 10.

**Largest CURRENT advantage:** Concrete, Paulina-specific worked examples in `fix-target-liveness.md` / `vetting-external-project-claims.md` — more vivid and immediately actionable *for this exact installation* than CANDIDATE's generalized replacements. This is a real, if soft, regression (§13).

**Largest CANDIDATE advantage:** Prompt-injection / untrusted-evidence boundary (§8) — a capability CURRENT does not have at all, plus a fully automated, currently-passing test suite (82/82) where CURRENT has none.

**Largest CURRENT weakness:** Its own deterministic tooling is currently lying about its own health (liveness check exits 0 with 3 printed failures) and its verifier has an unguarded exit-code bypass — both independently confirmed by direct execution, not inference.

**Largest CANDIDATE weakness:** Not yet installed/wired into this Hermes instance; two independent evidence-state vocabularies across its own reference files; heavier context footprint (31 files vs 12) that will cost more tokens if ever fully loaded at once (mitigated by progressive disclosure, but the ceiling is real).

---

## 13. REGRESSIONS IN CANDIDATE (Phase 10 — actively hunted)

- **Loss of installation-specific concreteness** in `fix-target-liveness.md` and `vetting-external-project-claims.md` — the vivid "oko_grawitacyjne zombie daemon" and "SEC-AF" narratives are gone, replaced by generic templates. An agent operating on Paulina's actual system may find the old version's pattern-matching easier to trigger on ("this looks exactly like the OKO incident") than the new abstract checklist. **Real regression, not fabricated for balance.**
- **`liveness_check.sh`'s L3 in CANDIDATE demotes the legacy calibration-log/cron freshness check to informational-only** — CURRENT (nominally) treated a stale calibration log as a hard L3 FAIL; CANDIDATE treats the same signal as `[INFO]` only. Given CURRENT's script doesn't actually propagate ANY failure to its exit code anyway (§7/§10), this is a wash in practice, but as *written intent* it's a real lowering of what counts as "required" for this particular telemetry source.
- **No file or mechanism was found missing outright** — every byte of CURRENT's non-identical content has a CANDIDATE successor covering the same ground (confirmed: no unique-to-CURRENT files exist per §4's structural diff), so there is no case of "a whole capability silently disappeared."

---

## 14. P0 / P1 / P2 / P3 (fixes before/around installation)

- **P0 (blocker for a *clean* migration, not for correctness of the skill text itself):** None found. The skill content itself is safe to install as-is.
- **P1 (should fix before/soon after installation):**
  1. Reconcile the two evidence-state vocabularies (`SUPPORTED_WITH_SCOPE/…` vs `MATCHED/DERIVED/ESTIMATED/NOT_SUPPORTED_HERE`) — pick one, or explicitly map one to the other.
  2. `AHP_SKILL_DIR` needs to actually resolve correctly once installed at `~/.hermes/skills/software-development/anti-hallucination-protocol` — confirmed working when explicitly pointed there in this audit; just needs the real install path to exist (§18 handles this).
  3. The real, currently-installed `~/.hermes/scripts/verify_claim.sh` (the *executable*, separate from anything inside either audited `SKILL.md`-adjacent tree) still has the unguarded `cmd-output` exit-code bypass — this exists independently of which skill version is installed and should be patched or replaced by `verify_claim.py` regardless of the SKILL.md decision. **This is technically outside the two audited directories** and is flagged here as an adjacent finding, not something this audit was asked to fix.
- **P2 (improvement, not urgent):** Consider restoring a short "local incident examples" appendix inside `fix-target-liveness.md`/`vetting-external-project-claims.md` (installation-specific, kept separate from the portable core) so the concreteness lost in §13 isn't permanently gone.
- **P3 (cosmetic):** None material found.

---

## 15. FINAL YES/NO

**A. YES — CLEAR UPGRADE.**
**B. YES, replace CURRENT with CANDIDATE — not executed, per instructions.**
**C. Confidence: 85%.** Biggest unknowns: whether the loss of concrete local worked-examples (§13) measurably hurts real-session pattern-matching (untestable from a static audit), and whether the `evidence-record.schema.json` ledger format ever actually gets used in practice or sits unused (both plausible; skill text correctly gates it to "when justified by complexity").

---

## 16. PROPOSED MIGRATION PLAN — DO NOT EXECUTE

1. **Backup:** `cp -R ~/.hermes/skills/software-development/anti-hallucination-protocol ~/.hermes/skills/software-development/anti-hallucination-protocol.bak-$(date +%Y%m%d-%H%M%S)`
2. **Validation (dry run, on the backup copy, not live):** re-run `python3 scripts/check_v5_integrity.py --root <backup-of-candidate-copied-in>` and `python3 -m pytest tests/ -q` one more time against the exact bytes about to be installed (not the Downloads copy, in case of transfer corruption).
3. **Replacement:** `rsync -a --delete "/Users/paulinajanowska/Downloads/hermes-skills-main/software-development/anti-hallucination-protocol/" "/Users/paulinajanowska/.hermes/skills/software-development/anti-hallucination-protocol/"`
4. **Hermes reload:** restart the gateway process (`~/.hermes/gateway.pid`) or run whatever `hermes` CLI reload/rescan command re-reads the skills directory, so the new frontmatter is picked up without a stale in-memory `.skills_prompt_snapshot.json`.
5. **Post-install checks:**
   - `bash ~/.hermes/skills/software-development/anti-hallucination-protocol/scripts/liveness_check.sh` (no `AHP_SKILL_DIR` override needed once actually installed there) → expect `PASS (portable L1/L2)`, exit 0.
   - `python3 ~/.hermes/skills/software-development/anti-hallucination-protocol/scripts/check_v5_integrity.py --root ~/.hermes/skills/software-development/anti-hallucination-protocol` → expect `PASS`.
   - Confirm the skill still appears in `hermes`'s skill index (whatever command lists loaded skills) with the new `description:` string.
6. **Rollback:** if any post-install check fails, `rm -rf` the newly installed directory and restore from the timestamped backup in step 1; re-run the liveness check against the restored backup to confirm rollback succeeded.

**Not executed. Awaiting explicit confirmation.**

---

## 17. EVIDENCE / COMMAND LOG

Key commands actually run (zsh, PID 64594) and their exact results, condensed:

```
$ realpath <CURRENT> <CANDIDATE>        # both resolve to themselves — no symlinks
$ find <CURRENT> -type l ; find <CANDIDATE> -type l   # both empty
$ find <CURRENT>|<CANDIDATE> -type f | wc -l           # 13 (incl. .DS_Store) / 31
$ shasum -a 256 <every file>            # full hash table, §3/§4 above
$ diff -u <4 changed files>             # full unified diffs read in full, §4/§13
$ bash <CURRENT>/scripts/liveness_check.sh ; echo $?          # 3 FAILs printed, exit 0
$ AHP_SKILL_DIR=<CANDIDATE> bash <CANDIDATE>/scripts/liveness_check.sh; echo $?  # all OK, exit 0
$ bash <CANDIDATE>/scripts/liveness_check.sh (default path); echo $?            # correctly fails, exit 1
$ cp -R <CANDIDATE> /tmp/audit_evidence/B_copy   # isolated copy, outside both trees
$ cd /tmp/audit_evidence/B_copy && python3 -m pytest tests/ -q     # 82 passed, exit 0
$ python3 scripts/check_v5_integrity.py --root .                   # PASS, exit 0
$ python3 scripts/check_research_provenance.py --root .            # PASS, exit 0
$ python3 <CANDIDATE>/scripts/check_v5_integrity.py --root <CURRENT>   # FAIL (expected — v2 vs v5 contract), exit 1
$ grep -rln "SkillFrontmatter|frontmatter" ~/.hermes/hermes-agent/agent   # located agent/skill_utils.py
$ [full read of agent/skill_utils.py, 934 lines]
$ [frontmatter samples from 5 other installed skills, all use metadata:hermes: nesting]
```

No command was run against, and no write operation of any kind touched, either `<CURRENT>` or `<CANDIDATE>` directory. The only filesystem write in this entire audit was the isolated `/tmp/audit_evidence/` scratch copy used for the pytest run, which is outside both audited trees.
