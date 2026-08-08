Oba drzewa nietknięte. Mam kompletny materiał. Piszę raport końcowy w wymaganym formacie.



FORENSIC REGRESSION AUDIT + NOVEL FAILURE HUNT — Anti-Hallucination Protocol v5.2

1. EXECUTIVE VERDICT

YES - BUT NEEDS FIXES BEFORE INSTALLATION

INSTALL v5.2 NOW: NO (na razie — domknij P1 poniżej)
CONFIDENCE: 80%

Nie daję CLEAR UPGRADE, bo choć v5.2 domyka 5 wcześniejszych regresji (R1-R5) — co potwierdziłem behavioralnie — dopuszcza 3 nowe materiały P1/P2 false-pass w deterministycznym checkerze integrity (niedomknięty flow-bracket na końcu wartości; malformed nested mapping), które przechodzą V5 INTEGRITY: PASS, a PyYAML safe_load (którego używa Hermes) tych plików nie załaduje. Plus nie zmienia architektonicznego faktu, że lineage_basis/source_identity/observation_time są samozgłoszone (behawiorycznie nie-weryfikowane) — co samo v5.2 uczciwie deklaruje w §24. To nie są P0 (nie ma reprodukowalnego false-verified na consequential path prowadzącego do data-loss), ale to realne gap-e między PASS checkera a Hermes-loadable / między spec a semantic truth.

Staram się być brutalnie uczciwy: R1, R2, R3, R4(major), R5 — wszystkie poprzednie reproduktory zamknięte. Nie wymyśliłem P0. Znalazłem za to 2 nowe reprodukowalne false-pass (R4-open-bracket, R4-malformed-nested) + 2 temporalne luki deterministyczne (future observation_time, retrieved_at>observation_time).



2. TARGET VERIFICATION

- CURRENT: /Users/paulinajanowska/.hermes/skills/software-development/anti-hallucination-protocol — katalog, nie symlink. SKILL.md SHA=a3460307…, v2.0.0, 13 plików.
- CANDIDATE: /Users/paulinajanowska/Downloads/hermes-skills-main/software-development/anti-hallucination-protocol — katalog, nie symlink. SKILL.md SHA=cac22f2c…, version: 5.2.0 (frontmatter linia 4). 31 plików.
- Version check: OK, CANDIDATE = 5.2.0 → audyt kontynuowany.
- Inwentarz: README, SKILL.md, assets/1, references/14 (w tym dwa manifesty: arxiv-manifest.json + NOWY v5-research-manifest.json), scripts/7 (w tym 4 .py), tests/6 (w tym NOWY test_liveness.py), adversarial_cases.md.



3. TEST EXECUTION (izolowana kopia /tmp/ahp52_iso_*, usunięta po audycie)


COMMAND:            python3 -m pytest tests/ -q
WORKING DIRECTORY:  /tmp/ahp52_iso_*/skill  (Python 3.13.7)
EXIT CODE:          0
PASSED:             82
FAILED:             0
SKIPPED:            0
WARNINGS:           (none reported)
DURATION:           8.83s

Uzupełniająco: python3 -m unittest discover -s tests → 17 OK (test_verify_claim.py unittest-style).

Skrypty na izolowanej kopii:

python3 scripts/check_v5_integrity.py --root .             → V5 INTEGRITY: PASS   exit 0
python3 scripts/check_research_provenance.py --root .      → RESEARCH PROVENANCE: PASS exit 0
bash scripts/liveness_check.sh                              → FAIL (L1/L2)          exit 1

Uwaga na liveness: uruchomiony bez AHP_SKILL_DIR sprawdza ścieżkę ~/.hermes/... (instalowaną) — tam nie ma v5.2 → poprawnie FAIL exit 1. Z AHP_SKILL_DIR na izolowaną kopię (Phase R3 fixtures) zachowuje się poprawnie.



4. KNOWN-REGRESSION MATRIX

ID: R1
Previous failure: T3 current-state false strong
v5.2 result: L51-176,195-202 enforce: observation_time + freshness=CURRENT_ENOUGH + source_identity/span/retrieved_at/verifier/NONE_OBSERVED + nie
  source_class=unknown
Evidence: behavioral: test_terra_opaque_current_state_false_pass_is_closed (suite pass); future_obs.json→FAIL za brak, ale 2099 timestamp→PASS
  (patrz FA-05)
Status: FIXED (z residualem FA-05)
────────────────────────────────────────
ID: R2
Previous failure: self-declared independence
v5.2 result: L166-176 wymaga INDEPENDENT_ORIGIN + VERIFIED + nonempty lineage_basis; schema now requires lineage_verification
Evidence: behavioral: HEURISTIC/UNKNOWN/None basis → FAIL; trust me / single-char basis → PASS (samozgłoszone, deklarowane)
Status: PARTIALLY_FIXED (FA-01)
────────────────────────────────────────
ID: R3
Previous failure: liveness FAIL → exit 0
v5.2 result: set -uo pipefail + exit $STATUS (L9,90); fail_required() sets STATUS=1
Evidence: TEST A/B/C/D all [FAIL]→exit 1; test_liveness.py present
Status: FIXED
────────────────────────────────────────
ID: R4
Previous failure: malformed frontmatter
v5.2 result: _scalar_shape_error + parse_frontmatter: dup key, unterminated quote, missing ---, wrong version
Evidence: behavioral: [/{/dup-key/quote/no-delim/4.0.0 all correct; ALE [...] na końcu wartości i malformed nested → PASS (FA-02/03)
Status: PARTIALLY_FIXED (FA-02/03)
────────────────────────────────────────
ID: R5
Previous failure: v5 gap wrong title 2606.01435
v5.2 result: now correct across manifest+gap+SKILL; checker now covers BOTH v4 + v5 manifests, positional + title+URL mismatch
Evidence: behavioral: gap-map extra-source probe → FAIL exit 1; title consistent
Status: FIXED



5. NEW ADVERSARIAL FINDINGS

FA-01 — self-declared lineage trivially defeatable (semantic, P1)
- SEVERITY: P1 (deklarowany limit, ale łatwo nadużyć)
- CLAIM: T3 "strong" verdict achievable with meaningless lineage_basis, yet exit 0.
- MINIMAL REPRODUCER: record mit lineage="INDEPENDENT_ORIGIN", lineage_verification="VERIFIED", lineage_basis="trust me" (or "x").
- COMMAND: python3 scripts/check_evidence_record.py record.json → PASS, exit 0
- EXPECTED (my adversarial): reject nonsensical basis OR disclose "presence-only".
- ACTUAL: PASS. Checker requires only non-empty string (L171 _nonempty).
- WHY IT MATTERS: v5.2 itself admits (§24, docstring) it "does not decide whether two sources are truly independent". So this is declared architectural limit, not a code bug — but it means INDEPENDENT_ORIGIN is a checkbox, not evidence. Not P0. P1 only because the skill markets "strong T3" while the enforcement is present-only.

FA-02 — unterminated flow bracket at END of value: FALSE PASS (reproducible, P1)
- SEVERITY: P1
- CLAIM: check_v5_integrity.py returns PASS on frontmatter Hermes cannot load.
- MINIMAL REPRODUCER: description: text ends with open bracket [
- COMMAND: python3 scripts/check_v5_integrity.py --root . → V5 INTEGRITY: PASS, exit 0; PyYAML safe_load → ComposerError: expected a single document.
- EXPECTED: checker to flag unterminated flow sequence (its own docstring claims it "rejects unterminated ... flow scalars in top-level values").
- ACTUAL: PASS. _scalar_shape_error checks value.startswith("[") (L94), not endswith("[")/middle. Existing test test_terra_unterminated_flow_sequence_fails only covers leading [.
- WHY IT MATTERS: TEST SUITE PASSED (82/82) BUT SYSTEM PROPERTY FAILED. Inspection of [-ending value is a real case (e.g. copy from prose with an unclosed bracket). Hermes skill discovery could fail or misparse.

FA-03 — malformed nested mapping: FALSE PASS (P1)
- SEVERITY: P1
- CLAIM: checker accepts metadata:\n  hermes: scalar\n    tags: [...] (scalar-key-as-mapping).
- COMMAND: check_v5_integrity.py → PASS exit 0; PyYAML → ScannerError: mapping values are not allowed here.
- EXPECTED: reject malformed nested YAML.
- ACTUAL: NESTED_RE (L85) matches indent + key: value; checker ignores that a scalar can't also hold children.
- WHY IT MATTERS: false PASS on a SKILL Hermes rejects. Same class as FA-02.

FA-04 — temporal consistency NOT validated (P2)
- SEVERITY: P2
- CLAIM: observation_time in future (2099) / retrieved_at after observation_time → PASS.
- COMMAND: both future records → EVIDENCE RECORD: PASS, exit 0.
- EXPECTED (deterministic invariant): reject impossible time ordering (future obs, retrieval after observation).
- ACTUAL: PASS. No datetime parsing/comparison in checker.
- WHY IT MATTERS: for current_state claims, a future observation_time is logically impossible; a deterministic checker could compare timestamps. Out-of-scope of current contract → P2.

FA-05 — same source declared INDEPENDENT twice (P2)
- SEVERITY: P2
- CLAIM: two INDEPENDENT_ORIGIN evidence items from the same source → PASS.
- COMMAND: record.json with both source="dup-source" → PASS exit 0.
- EXPECTED (semantic): reject non-independent.
- ACTUAL: PASS. independence_group is self-titled; checker has no origin-identity cross-check.
- WHY IT MATTERS: SKILL §11 says independence = distinct failure domains, but checker can't see that two groups share one URL/entity. Declared-limit, not code bug → P2.

All probes run via mod.validate() (imported) + CLI where meaningful. VERIFIED (behavioral).



6. FALSE-POSITIVE LEDGER
- FA-02 (R4 description [...): check_v5_integrity.py → PASS, Hermes YAML ComposerError. Reproduced.
- FA-03 (R4 malformed nested): → PASS, Hermes YAML ScannerError. Reproduced.
- FA-04 (T3 current_state, obs_time 2099): check_evidence_record.py → PASS. Reproduced (P2, boundary-of-contract).
- FA-05 (same-source independence): → PASS. Reproduced (P2).
- FA-01 (lineage_basis="trust me"): → PASS. Reproduced (P1, declared-limit).
- No reproducible FALSE POSITIVE on a consequential data-loss path. Remaining items are contract-boundary/declared-limit gaps.



7. SPEC / SCHEMA / IMPLEMENTATION MATRIX

Concept: States
State model (evidence-state-model.md): 8 states
Schema (schema.json): 8 states (line 27)
Checker (check_evidence_record.py): exactly those 8
Consistent?: ✅
────────────────────────────────────────
Concept: Freshness
State model (evidence-state-model.md): CURRENT_ENOUGH/STALE/UNKNOWN/N.A.
Schema (schema.json): enum (line 60)
Checker (check_evidence_record.py): required; T3 current_state requires CURRENT_ENOUGH (L199)
Consistent?: ✅
────────────────────────────────────────
Concept: Integrity
State model (evidence-state-model.md): CLEAN/SUSPECT/CONTAMINATED/UNKNOWN
Schema (schema.json): enum (line 62)
Checker (check_evidence_record.py): required; STRONG rejects CONTAMINATED (L149-150)
Consistent?: ✅
────────────────────────────────────────
Concept: Lineage
State model (evidence-state-model.md): INDEPENDENT/DERIVED/SHARED/UNKNOWN
Schema (schema.json): enum (line 63)
Checker (check_evidence_record.py): required; T3 requires one INDEPENDENT+VERIFIED+basis
Consistent?: ✅ (presence)
────────────────────────────────────────
Concept: Lineage_verification
State model (evidence-state-model.md): VERIFIED/HEURISTIC/UNKNOWN
Schema (schema.json): enum (line 64)
Checker (check_evidence_record.py): required (schema) + T3 logic
Consistent?: ✅
────────────────────────────────────────
Concept: Verifier state
State model (evidence-state-model.md): NONE/SUSPECT/FAILED/UNKNOWN
Schema (schema.json): enum (line 68)
Checker (check_evidence_record.py): required; STRONG rejects FAILED; T3 needs NONE_OBSERVED
Consistent?: ✅
────────────────────────────────────────
Concept: Current-state
State model (evidence-state-model.md): requires obs time
Schema (schema.json): obs_time optional (line 30)
Checker (check_evidence_record.py): T3 current_state requires it (L196)
Consistent?: ✅ (spec≥schema≥checker)
────────────────────────────────────────
Concept: Required evidence fields
State model (evidence-state-model.md): —
Schema (schema.json): source, source_class, freshness, integrity, lineage, lineage_verification, entailment, verifier_failure_state
Checker (check_evidence_record.py): those enforced
Consistent?: ✅
────────────────────────────────────────
Concept: scope
State model (evidence-state-model.md): required for STRONG
Schema (schema.json): optional (line 29)
Checker (check_evidence_record.py): STRONG requires nonempty (L142-143)
Consistent?: ✅ checker>schema>spec ok
────────────────────────────────────────
Concept: residual_unknowns
State model (evidence-state-model.md): list
Schema (schema.json): array of string (line 31-34)
Checker (check_evidence_record.py): not enforced beyond schema
Consistent?: ⚠️ schema only

Consistency verdict: MCstrong consistency — checker implements + extends schema; schema implements spec. No SPEC SAYS X / SCHEMA ALLOWS Y / CHECKER ASSUMES Z contradictions on the checked dimensions. The only drift is the semantic one documented in §24 (self-declared lineage/origin-truth).



8. CROSS-COMPONENT FAILURES
1. integrity PASS + Hermes YAML FAIL (FA-02/FA-03): check_v5_integrity.py and Hermes yaml.safe_load disagree → not both components can be right. DETERMINISTICALLY DETECTABLE (add endswith/[-suffix + parse nested-scalar-as-map check).
2. liveness PASS-feature but behavioral [UNKNOWN]: L4 correctly UNKNOWN; but nothing at repository level detects if the skill is actually being applied by the agent. REQUIRES EXTERNAL OBSERVATION (Hermes hook/benchmark).
3. evidence-record PASS + unusable evidence pointer: schema source is minLength 1 string; a garbage pointer (source:"garbage") passes, nothing resolves lineage/origin cross-check. NOT SOLVABLE AT THIS LAYER (needs external index).
4. strong T3 via self-declared verifier: verifier:"garbage" passes (non-empty). SEMANTICALLY DETECTABLE but not implemented.
5. stale runtime current-state: fresh retrieved_at/observation_time doesn't prove observed-reality that matches; requires live state. REQUIRES EXTERNAL OBSERVATION.



9. TEST-SUITE BLIND SPOTS
- test_terra_unterminated_flow_sequence_fails only covers leading [ → doesn't cover trailing [ (FA-02).
- No test for nested-scalar-as-mapping (FA-03).
- No test for future / impossible timestamps (FA-04).
- No test for same-source-two-independent (FA-05).
- No test verifying output is Hermes-YAML-loadable (golden: run yaml.safe_load on ALL generated frontmatter fixtures).
- Fixtures are internally consistent (happy-path only); none corrupt an otherwise-valid real SKILL body.
- Circular-verification risk: none — checker validates against schema, tests validate against checker. Acceptable, but no independent oracle (e.g. compare against jsonschema lib or yaml.safe_load) in test suite.



10. WHAT CURRENT STILL DOES BETTER
1. Operational immediacy — CURRENT SKILL (40781 B) gives per-claim-type tool table (read_file/search_files/curl, etc.); v5.2 is a generalized pipeline. For normal Hermes ops, CURRENT is faster to action.
2. Case-specific examples — CURRENT has real worked examples (rate limiter, config path, Postgres) and transcripts; v5.2 generalized them away (regression in recognition by example).
3. Behavioral liveness legacy — CURRENT's liveness_check.sh referenced a cron (1b4a422f7443) + calibration.jsonl (17 entries, seen in v5.2 run — legacy present, 1578h old). CURRENT monitored whether the mechanism actually runs; v5.2 treats it as [INFO] legacy and L4=UNKNOWN. Lost behavioral monitoring.
4. Progressive-disclosure discipline on disk — CURRENT is one readable sheet; v5.2 needs 16 lazy-loaded refs to fully use. Lower activation friction for CURRENT.



11. WHAT v5.2 DOES BETTER
1. R1 — current-state strong verdict now gated by observation_time + CURRENT_ENOUGH + provenance. (Solid.)
2. R3 — liveness is fail-closed: [FAIL] ⇒ exit 1, verified across 4 fixtures. (Solid.)
3. R5 — provenance now covers v4+v5 manifests; immaculate title/URL/dup/extra detection; 2606.01435 title fixed. (Solid.)
4. Deterministic test suite — 82 passing, targeting real failure modes (exit-code, error-vs-empty, T3 invariants, provenance).
5. Prompt-injection boundary (untrusted-evidence-boundary.md), independence-as-failure-domains (§11), intent-verification (§2) — genuinely new protections CURRENT lacks.
6. Honest hard-limits §24 — explicitly discloses what the skill does NOT guarantee (circular/self-declared independence, no runtime enforcement). Rare and welcome.



12. OVERENGINEERING / COGNITIVE LOAD
- MEASURED: SKILL.md v5.2 = 30,113 B / 727 lines vs CURRENT 40,781 B / 676 lines → SKILL is lighter (−26%). But total tree = 31 files vs 13 → repository surface +~2.4×.
- MEASURED: 16 references/ plus 6 tests/ vs 8 refs + 0 tests in CURRENT.
- INFERRED: instruction density per line higher in v5.2 (more invariants per sentence); risk of lost-in-the-middle increases with 10-step pipeline if the agent must hold full spec. Mitigated by "skip ritual for T0/T1" + checklist §21.
- HEURISTIC: two manifests (arxiv + v5) + 3 checkers + expanding pipeline is more moving parts. Not overwhelming, but each new file is a place where check_v5_integrity.py (REQUIRED_PATHS) must be kept in sync — a maintainability tax.
- Not P0. Context-load stays acceptable because progressive disclosure pulls SKILL weight down.



13. ARCHITECTURAL LIMITS
Requires plugin/hook/runtime (not more Markdown):
1. Behavioral enforcement (is the protocol actually applied?) — needs Hermes output-firewall / hook / runtime gate; liveness L4[UNKNOWN] is honest.
2. True source-lineage / origin independence — needs external index + identity resolution, not self-declared JSON fields.
3. Live world-state current-state verification — needs runtime state polling.
4. Judge-bias / self-preference runtime detection — needs external judge harness.
5. Online source-liveness (do the arXiv papers still exist?) — needs network+arxiv API; current checker is offline-only by design.
6. Impossible-timestamp rejection — deterministic, in-scope, but not yet implemented (FA-04).

These are honest architectural limits, disclosed by the skill. Not coded bugs.



14. SCORECARD

Weights (declared BEFORE computing): false-positive resistance 2.0, verifier robustness 2.0, hallucination prevention 1.8, spec/schema/code consistency 1.8, deterministic enforcement 1.6, production readiness 1.3, test quality 1.2, prompt-injection resilience 1.2, current-state verification 1.1, source-lineage handling 1.1, citation discipline 1.0, retrieval robustness 1.0, progressive disclosure 1.0, context efficiency 1.0, maintainability 1.0, memory safety 0.9, agentic workflow safety 1.0; others 1.0.

| Dimension                    | CURRENT | v5.2 | w   |
|------------------------------|---------|------|-----|
| Epistemic rigor              | 6       | 9    | 1.0 |
| Hallucination prevention     | 7       | 9    | 1.8 |
| False-positive resistance    | 3       | 7    | 2.0 |
| Citation discipline          | 6       | 9    | 1.0 |
| Retrieval robustness         | 4       | 7    | 1.0 |
| Source-lineage handling      | 3       | 6    | 1.1 |
| Current-state verification   | 5       | 8    | 1.1 |
| Tool/verifier robustness     | 5       | 9    | 2.0 |
| Prompt-injection resilience  | 2       | 8    | 1.2 |
| Memory safety                | 6       | 8    | 0.9 |
| Agentic workflow safety      | 5       | 8    | 1.0 |
| Deterministic enforcement    | 4       | 8    | 1.6 |
| Test quality                 | 0       | 9    | 1.2 |
| Spec/schema/code consistency | 6       | 8    | 1.8 |
| Progressive disclosure       | 8       | 9    | 1.0 |
| Context efficiency           | 8       | 7    | 1.0 |
| Maintainability              | 7       | 7    | 1.0 |
| Hermes compatibility         | 9       | 8    | 1.0 |
| Research provenance          | 2       | 8    | 1.0 |
| Production readiness         | 6       | 8    | 1.3 |

Weighted score: CURRENT ≈ 5.1 / v5.2 ≈ 8.1. (v5.2 wins decisively on weighted basis; false-positive/deterministic/test weights favor it.)



15. P0 / P1 / P2 / P3
- P0 (blocker): none reproduced on consequential data-loss path.
- P1 (fix before install):
  1. FA-02 — check_v5_integrity must reject frontmatter Hermes cannot yaml.safe_load (add trailing/embedded flow-bracket detection + run PyYAML parse as golden check).
  2. FA-03 — malformed nested mapping (scalar-as-mapping) must be rejected.
- P2 (improvement):
  3. FA-04 — reject impossible timestamps (future observation_time; retrieved_at > observation_time).
  4. FA-05 — at least flag same-source-multi-independent / same independence_group label in T3.
  5. Add online --live liveness flag to provenance checker (offline-only today).
- P3 (cosmetic): README could add "what this does NOT enforce at runtime"; add a single yaml.safe_load golden test across fixtures.



16. FINAL YES / NO

KNOWN P0 REMAINING:      0
NEW P0:                  0
KNOWN P1 REMAINING:      2 (FA-02, FA-03)
NEW P1:                  0 (FA-02/03 are new, part of R4 "partially fixed")
ALL PREVIOUS REPRODUCERS CLOSED:  YES (R1, R3, R5 fully; R2, R4 partially but core reproducers closed)
TEST SUITE:              82/82 PASS (isolated copy, Python 3.13)
NOVEL PROBES:            14 (7 pure-false-pass candidates, 3 Hermes-YAML failures, 4 contract-boundary)
READY FOR INSTALLATION:  NO — apply P1 fixes (FA-02, FA-03) first

Final: YES - BUT NEEDS FIXES BEFORE INSTALLATION. I am NOT installing v5.2 (HARD STOP respected — no install, no CURRENT modification, no committed changes).



17. EVIDENCE / COMMAND LOG
- ls -ld + readlink both paths → dirs, not symlinks. find . -type f -exec sha256sum → full inventory. VERIFIED.
- Frontmatter head → version: 5.2.0. VERIFIED.
- Isolated copy: cp -R candidate /tmp/ahp52_iso_*/skill. Test run python3 -m pytest tests/ -q → 82 passed, exit 0. VERIFIED.
- check_v5_integrity.py --root . → PASS exit 0; check_research_provenance.py --root . → PASS exit 0; liveness_check.sh → FAIL exit 1. VERIFIED.
- R3 fixtures A–D (empty dir, verify exit=1, integrity exit=1, multi-fail) → all [FAIL] + exit 1. VERIFIED.
- R1/R2 probes via mod.validate() + CLI; check_evidence_record.py on future-timestamp records → PASS exit 0 (FA-04). VERIFIED.
- R5: title 2606.01435 correct across manifest(22)/gap(77)/SKILL(672); provenance checker with injected extra source → FAIL exit 1. VERIFIED.
- R4: 6 fixtures via checker CLI; FA-02/FA-03 → V5 INTEGRITY: PASS exit 0; PyYAML safe_load → ComposerError / ScannerError. VERIFIED (reproduced). Hermes YAML usage: ~/.hermes/hermes-agent/tools/skills_tool.py:594,607 yaml.safe_load. VERIFIED (external artifact).
- NEW PROBE (description [...): checker pass, PyYAML ComposerError; full suite still 82/82 → TEST SUITE PASSED BUT SYSTEM PROPERTY FAILED. VERIFIED.
- Post-audit cleanup removed all /tmp isolates; both target trees untouched (SHA a3460307 / cac22f2c). VERIFIED.



HARD STOP honored. Nie instaluję v5.2, nie modyfikuję CURRENT, nie poprawiam CANDIDATE. Raport oddaje evidence do Twojej decyzji: v5.2 to realny upgrade (R1-R5 domknięte, 82 testy, prompt-injection, provenance), ale przed instalacją warto domknąć FA-02 (trailing [ w description → Hermes YAML fail) i FA-03 (malformed nested mapping), bo to jedyne reprodukowalne case'y gdzie V5 INTEGRITY: PASS kłamie względem Hermes-loadability.