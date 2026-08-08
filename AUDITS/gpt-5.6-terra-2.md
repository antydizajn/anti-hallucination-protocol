EXECUTIVE VERDICT

CANDIDATE ONLY. CURRENT nie był czytany ani porównywany.

NO - DO NOT INSTALL YET

Rdzeń v5.2 jest sensowny: dobrze rozdziela policy vs runtime, ma 30-case corpus, schema/state gate i uczciwie mówi, że PASS != truth.

Ale pakiet zawiera P0/P1 false-verification paths i legacy scripts z realnym write side effect poza katalogiem skilla. To dyskwalifikuje migrację teraz.

WHAT I ACTUALLY INSPECTED

VERIFIED:
- Candidate: /Users/paulinajanowska/Downloads/hermes-skills-main/software-development/anti-hallucination-protocol
- 31 files, 234,969 B, no symlink.
- Hermes live: v0.20.0 (2026.8.3), Python 3.11.15.
- Real candidate frontmatter parses in live Hermes:
  name=anti-hallucination-protocol, version=5.2.0,
  platforms=list, metadata=dict, platform match True.
- Candidate sources remained unchanged.
- Tests ran only in isolated /tmp/ahp-* copies.

TREE / FILE INVENTORY

- Root: SKILL.md, README.md
- scripts/: 7
  - verify_claim.py
  - check_evidence_record.py
  - check_research_provenance.py
  - check_v5_integrity.py
  - liveness_check.sh
  - anti-halluc-v3-eval.sh
  - godmode_battery.sh
- tests/: 6, including adversarial_cases.md with exactly 30 cases.
- references/: 15 Markdown/JSON artifacts.
- assets/: 1 SVG.

SEMANTIC ARCHITECTURE

KEEP:
- Explicit claim tiers T0-T3.
- Distinguishes source truth, retrieval, entailment, verifier state, and final synthesis.
- Treats retrieved content as data, not instructions.
- Explicitly rejects “green helper => true answer”.
- verify_claim.py is properly narrow: nonzero command exit, invalid UTF-8, timeout, oversized output become ERROR, not FOUND.

WHAT CANDIDATE DOES WELL

VERIFIED:
- SKILL.md:45-49 explicitly says Markdown is not runtime enforcement.
- SKILL.md:386-387 scopes each checker honestly.
- test_verify_claim.py:106-118 blocks the important “stderr contains expected text but command exits 7” false verification.
- Evidence-record tests reject missing T3 fields, unknown enums, opaque sources, malformed evidence objects, and extra properties.
- Research checker catches v4 manifest/title drift.
- Liveness tests fail closed when required files are missing.

P0 / P1 BLOCKERS

P0 — scripts/godmode_battery.sh is unsafe as a shipped self-test.

VERIFIED, lines 23-25, 102-114:
- Hardcodes external mutable state:
  ~/.hermes/scripts/anti_halluc/calibration.jsonl
- Appends calibration data on every run.
- Is not isolated and has no explicit output/workdir argument.
- Skips unsupported probe classes silently from its denominator (lines 64-92).
- Can produce a narrowed correct/total score while omitting richer cases.
- Catches probe errors but does not fail the shell process (lines 77-90).
- Appends a self-generated entry with outcome=None anyway.

Practical consequence: a script described as an adversarial self-test can mutate external calibration state while returning success despite partial execution/error paths.

Required repair:
- Remove it from the candidate package or move it to a clearly marked legacy reference.
- If retained: explicit --workdir, no default home write, fail on SKIP/ERR, record attempted/skipped/error counts, append only after a complete valid run.

P1 — integrity checker can PASS a skill Hermes will not activate.

VERIFIED isolated probe:
- Modified only an isolated copy:
  description: malformed: scalar
- Candidate command:
  python3 scripts/check_v5_integrity.py --root .
  returned 0, V5 INTEGRITY: PASS.
- Live Hermes parser then fell back to its permissive frontmatter parser:
  platforms='[linux, macos, windows]'
  and platform_match=False.

This directly contradicts the checker's stated Hermes-alignment purpose.

Required repair:
- Make check_v5_integrity.py invoke the same YAML parsing path as live Hermes.
- Fail if Hermes would use fallback parsing.
- Add this exact malformed-colon regression test.

P1 — v5 source identities in SKILL.md are not provenance-checked.

VERIFIED isolated probes:
- Changed only v5’s displayed AgentDojo title in SKILL.md -> checker still returned:
  RESEARCH PROVENANCE: PASS
- Changed only arXiv:2406.13352 -> arXiv:2406.99999 in SKILL.md -> also:
  RESEARCH PROVENANCE: PASS

The checker validates v5-gap-map.md against the v5 manifest, but not the duplicate v5 source list embedded in SKILL.md.

Required repair:
- Parse and compare the v5 sources in SKILL.md, or remove that duplicate list and link to one canonical manifest.

P1 — evidence gate can certify structurally valid nonsense.

VERIFIED isolated probe:
- T3 current_state record used "." for timestamps, source identity, span, lineage basis, verifier, and scope.
- Two evidence entries used the same independence_group.
- Result: exit 0, EVIDENCE RECORD: PASS.

The skill openly says this gate is structural only. So this is not a hidden lie in prose. But integrations must never turn this exit code into “verified current truth”.

Required repair:
- Rename success status to STRUCTURALLY_VALID, not a truth-adjacent label.
- Enforce RFC3339 timestamps.
- Reject placeholder-only metadata.
- Require actual distinct lineage groups when multiple independent confirmations are claimed.
- For semantic/source truth, use external provenance or runtime observation; Markdown and JSON cannot prove it.

P1 — Windows portability is not established.

INFERENCE from source:
- Candidate declares windows.
- liveness_check.sh, godmode_battery.sh, and anti-halluc-v3-eval.sh require Bash.
- Native Windows without Git Bash/WSL cannot run those checks.
- No Windows execution was performed.

P2 — README command is misleading for isolated validation.

VERIFIED:
- README lines 223-226 says simply:
  bash scripts/liveness_check.sh
- In an isolated candidate copy this checks the installed path by default and failed.
- With AHP_SKILL_DIR=<isolated-copy>, it passed.

Repair: document:
AHP_SKILL_DIR="$(pwd)" bash scripts/liveness_check.sh

SCRIPT / VERIFIER AUDIT

Script: verify_claim.py
Verdict: KEEP. Strong narrow contract; tested false-positive handling.
────────────────────────────────────────
Script: check_evidence_record.py
Verdict: KEEP, but label as structural validity only.
────────────────────────────────────────
Script: check_research_provenance.py
Verdict: FIX. Misses v5 list duplicated in SKILL.md.
────────────────────────────────────────
Script: check_v5_integrity.py
Verdict: FIX. Must use live Hermes parser behavior.
────────────────────────────────────────
Script: liveness_check.sh
Verdict: SIMPLIFY/FIX. Explicit target required for audit copies; Bash portability gap.
────────────────────────────────────────
Script: anti-halluc-v3-eval.sh
Verdict: MOVE_TO_REFERENCE. External V3 dependency, old static baselines, LLM judge. TEST EXECUTION UNVERIFIED.
────────────────────────────────────────
Script: godmode_battery.sh
Verdict: REMOVE_FROM_PACKAGE or redesign. P0 side effects and partial-score false confidence. Not executed because it writes outside the candidate
  tree.

TEST AUDIT

VERIFIED in isolated copy:

text
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/
82 passed in 9.26s


text
python3 scripts/check_v5_integrity.py --root .       -> 0, PASS
python3 scripts/check_research_provenance.py --root . -> 0, PASS
bash scripts/liveness_check.sh                        -> 1, wrong default target
AHP_SKILL_DIR=<copy> bash scripts/liveness_check.sh  -> 0, PASS


Missing tests:
- Hermes parser vs integrity-checker concordance.
- v5 SKILL.md source title/ID drift.
- Placeholder timestamp/provenance metadata.
- Duplicate independence-group.
- godmode_battery.sh all-skip, probe-error, no-write, and nonzero-exit behavior.
- Native Windows execution.
- Actual long-context LLM obedience / injection resilience. The 30 cases are a specification, not a behavioral benchmark.

30-CASE ADVERSARIAL HEAD-TO-HEAD

No CURRENT comparison by instruction.

Legend:
- P = policy/prompt only
- V = partial structural validation
- D = deterministic guard
- F = demonstrated false PASS

text
01 P  02 P  03 P  04 P  05 P  06 P
07 P  08 P  09 P  10 V  11 P  12 P
13 P  14 P  15 V  16 P  17 P  18 P
19 P  20 P  21 P  22 P  23 P  24 P
25 P  26 P  27 P  28 D  29 D/F  30 D/F


28: verified command-exit failure is blocked deterministically.  
29/30: v4 manifest path is deterministic; duplicated v5 SKILL list false-passes.

OVERENGINEERING AUDIT

KEEP:
- Tiering, scoped conclusions, untrusted-evidence boundary, contradiction handling, verifier-failure state.

MOVE_TO_REFERENCE:
- Legacy v3 evaluator.
- Historical baseline percentages.
- Long research catalog duplicated into active SKILL.md.

SIMPLIFY:
- SKILL.md is 30,113 B: usable, but too much research/history lives in the active instruction plane.
- Preserve a compact T0-T3 decision table + 10-line critical rules in SKILL.md.
- Move bibliography/history/examples into references.

NEEDS RUNTIME ENFORCEMENT:
- Source independence.
- Timestamp freshness.
- Semantic entailment.
- Prompt-injection resistance.
- Live-state verification.
- Agent trajectory completion.

WHAT BOTH STILL MISS

Candidate-only finding:
- No executable behavioral eval proving models follow the protocol.
- No cryptographic/source-lineage verification.
- No external semantic entailment verifier.
- No trusted live-state observation adapter.
- No runtime gate preventing an agent from ignoring the Markdown.
- No protected integration layer that prevents a structural PASS becoming a user-facing factual assertion.

SCORECARD — CANDIDATE PACKAGE

text
Epistemic rigor                 8.0
Hallucination prevention        6.7
False-positive resistance       5.6
Citation discipline             6.7
Retrieval robustness            6.8
Tool/verifier robustness        6.0
Prompt-injection resilience     6.5
Current-state accuracy          5.8
Memory safety                   5.5
Agentic workflow safety         5.4
Hermes compatibility            7.6
Deterministic enforcement       5.3
Test quality                    6.5
Maintainability                 6.4
Progressive disclosure          7.0
Context efficiency              7.4
Portability                     5.5
Operational usability           5.9
Research grounding              6.8
Production readiness            4.6


Equal-weight mean: 6.30 / 10.

FINAL YES / NO

A. Is CANDIDATE ready as a real anti-hallucination upgrade?

NO - NEEDS FIXES BEFORE INSTALLATION

B. Replace CURRENT?

NO

C. Confidence

94%

Main unknowns:
- Native Windows behavior untested.
- External V3 dependencies were intentionally not executed.
- No behavioral benchmark ran against a live LLM.

P0 / P1 / P2 / P3

text
P0  Remove/redesign godmode_battery.sh before any migration.
P1  Make integrity checker use actual Hermes frontmatter parsing.
P1  Validate v5 SKILL.md citations against the canonical manifest.
P1  Prevent structural evidence PASS from being interpreted as truth.
P1  Resolve declared Windows support versus Bash-only helpers.
P2  Document explicit AHP_SKILL_DIR for liveness checks.
P2  Move anti-halluc-v3-eval.sh out of the active v5 package.
P3  Compress research/history from SKILL.md into references.


PROPOSED MIGRATION PLAN — DO NOT EXECUTE

1. Patch candidate only after P0/P1 fixes.
2. Run full tests in an isolated copy.
3. Add the three demonstrated regression tests.
4. Validate with live Hermes parser and platform matcher.
5. Run a real behavioral benchmark with a predeclared corpus and failure ledger.
6. Back up CURRENT.
7. Replace only after a separate explicit instruction.
8. Reload Hermes skill index and run post-install liveness with explicit target.
9. Roll back immediately on parser, platform, or behavioral-eval regression.

No migration, copy, overwrite, deletion, config change, commit, or memory update was performed.