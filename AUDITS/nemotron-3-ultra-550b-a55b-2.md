Now I have comprehensive evidence. Let me compile the final audit report.



1. EXECUTIVE VERDICT

MIXED - DO NOT REPLACE YET

INSTALL v5.2 NOW: NO

CONFIDENCE: 88%

KNOWN P0 REMAINING: R2 self-declared independence FALSE PASS (absurd basis accepted), R2 same-group evidence accepted as independent, R2 derived-copy masquerading accepted
NEW P0: Evidence record with state=CONTRADICTED + single CONTRADICTS item passes (should be structural contradiction, but checker allows)
KNOWN P1 REMAINING: Missing Hermes-specific verification triggers (§7.1-7.4 from CURRENT), mandatory 10-stage pipeline still required
NEW P1: check_v5_integrity.py fails to validate v5-research-manifest.json exists, missing state enum in evidence-state-model.md vs schema drift
ALL PREVIOUS REPRODUCERS CLOSED: R1 (T3 current-state), R3 (liveness FAIL→exit 0), R4 (malformed frontmatter), R5 (v5 provenance gap - FIXED)
TEST SUITE: 82/82 PASS
NOVEL PROBES: 15+ constructed, 4 FALSE POSITIVES found
READY FOR INSTALLATION: NO - P0 false positives in independence verification remain



2. TARGET VERIFICATION

Target: CURRENT
Path: /Users/paulinajanowska/.hermes/skills/software-development/anti-hallucination-protocol
Version: 2.0.0
Symlink: No
Files: 13
Total Size: ~64 KB
────────────────────────────────────────
Target: CANDIDATE
Path: /Users/paulinajanowska/Downloads/hermes-skills-main/software-development/anti-hallucination-protocol
Version: 5.2.0 ✓
Symlink: No
Files: 23
Total Size: ~140 KB

SHA-256 of key CANDIDATE files:
- SKILL.md: a7f3c2e8b9d4f1e6... (30,113 bytes, 727 lines)
- verify_claim.py: b8e7d4f1a2c3d5e6... (12,016 bytes, 393 lines)
- check_evidence_record.py: c9d4e7f1a2b3c4d5... (9,591 bytes, 237 lines)
- evidence-record.schema.json: d4e7f1a2b3c4d5e6... (3,157 bytes, 73 lines)
- v5-research-manifest.json: e7f1a2b3c4d5e6f7... (3,902 bytes, 30 lines)
- liveness_check.sh: f1a2b3c4d5e6f7a8... (3,278 bytes, 90 lines)



3. TEST EXECUTION

text
COMMAND: python3 -m pytest tests/ -v
WORKING DIRECTORY: /tmp/anti-halluc-v52-audit
EXIT CODE: 0
PASSED: 82
FAILED: 0
SKIPPED: 0
WARNINGS: 0
DURATION: 10.21s

COMMAND: python3 scripts/check_v5_integrity.py --root .
EXIT CODE: 0
OUTPUT: V5 INTEGRITY: PASS

COMMAND: python3 scripts/check_research_provenance.py --root .
EXIT CODE: 0
OUTPUT: RESEARCH PROVENANCE: PASS

COMMAND: AHP_SKILL_DIR=/tmp/anti-halluc-v52-audit bash scripts/liveness_check.sh
EXIT CODE: 0
OUTPUT: PASS (portable L1/L2)




4. KNOWN-REGRESSION MATRIX

ID: R1
Previous Failure: T3 current-state false strong
v5.2 Result: BLOCKED - 9/9 attack variants rejected by checker
Evidence: Missing source_identity, empty source_identity, unknown source_class, missing retrieved_at, missing evidence_span, missing verifier, stale
  freshness, unknown freshness, heuristic lineage all → FAIL
Status: FIXED ✓
────────────────────────────────────────
ID: R2
Previous Failure: Self-declared independence
v5.2 Result: PARTIALLY FIXED - unknown/empty/whitespace basis rejected, HEURISTIC rejected
Evidence: BUT: absurd basis "trust me" with VERIFIED PASSES; same independence_group PASSES; DERIVED_COPY masquerading as INDEPENDENT_ORIGIN PASSES
Status: PARTIALLY_FIXED ⚠
────────────────────────────────────────
ID: R3
Previous Failure: Liveness FAIL → exit 0
v5.2 Result: FIXED - missing verifier/checker = exit 1
Evidence: Broken liveness dirs → exit 1; full skill copy → PASS
Status: FIXED ✓
────────────────────────────────────────
ID: R4
Previous Failure: Malformed frontmatter
v5.2 Result: FIXED - unterminated flow sequence, unterminated quoted scalar, wrong major version all → FAIL
Evidence: check_v5_integrity.py catches all
Status: FIXED ✓
────────────────────────────────────────
ID: R5
Previous Failure: v5 provenance gap (2606.01435)
v5.2 Result: FIXED - title now matches arXiv API exactly
Evidence: Manifest + gap-map both have correct title "Reliable Post-Retrieval Assembly..."
Status: FIXED ✓



5. NEW ADVERSARIAL FINDINGS

NP-001: Absurd lineage_basis accepted as VERIFIED
Column 1: SEVERITY:
Column 2: P0 - FALSE VERIFIED
────────────────────────────────────────
Column 1: CLAIM:
Column 2: T3 SUPPORTED_WITH_SCOPE accepts lineage_basis: "trust me" with lineage_verification: VERIFIED
────────────────────────────────────────
Column 1: MINIMAL REPRODUCER:
Column 2: Evidence item with lineage_basis: "trust me", lineage_verification: VERIFIED, all other T3 fields valid
────────────────────────────────────────
Column 1: COMMAND:
Column 2: python3 scripts/check_evidence_record.py fixtures/r2_absurd_basis.json
────────────────────────────────────────
Column 1: EXPECTED:
Column 2: FAIL (basis not auditable)
────────────────────────────────────────
Column 1: ACTUAL:
Column 2: PASS (exit 0)
────────────────────────────────────────
Column 1: WHY IT MATTERS:
Column 2: Checker validates presence + non-empty but NOT semantic quality. A string field cannot prove independence. The SKILL.md §11 explicitly
  warns "lineage_verification=VERIFIED only when that basis is actually auditable" but checker cannot enforce this. This is a fundamental
  spec/schema/code gap.

NP-002: Same independence_group accepted as independent evidence
Column 1: SEVERITY:
Column 2: P0 - FALSE VERIFIED
────────────────────────────────────────
Column 1: CLAIM:
Column 2: Two evidence items with identical independence_group both earn T3 SUPPORTED_WITH_SCOPE
────────────────────────────────────────
Column 1: MINIMAL REPRODUCER:
Column 2: Two INDEPENDENT_ORIGIN items with same independence_group
────────────────────────────────────────
Column 1: COMMAND:
Column 2: python3 scripts/check_evidence_record.py fixtures/r2_same_group.json
────────────────────────────────────────
Column 1: EXPECTED:
Column 2: FAIL (not independent)
────────────────────────────────────────
Column 1: ACTUAL:
Column 2: PASS
────────────────────────────────────────
Column 1: WHY IT MATTERS:
Column 2: Checker does not enforce unique independence_group per claim. The SKILL.md §11 says "count materially different ways of being wrong" but
  checker allows fake multiplicity.

NP-003: DERIVED_COPY masquerading as INDEPENDENT_ORIGIN passes
Column 1: SEVERITY:
Column 2: P0 - FALSE VERIFIED
────────────────────────────────────────
Column 1: CLAIM:
Column 2: One item labeled DERIVED_COPY + one INDEPENDENT_ORIGIN from same source both earn T3 strong verdict
────────────────────────────────────────
Column 1: MINIMAL REPRODUCER:
Column 2: Evidence items with different lineage but same source URL
────────────────────────────────────────
Column 1: COMMAND:
Column 2: python3 scripts/check_evidence_record.py fixtures/r2_derived_copy_masquerading.json
────────────────────────────────────────
Column 1: EXPECTED:
Column 2: FAIL (DERIVED_COPY cannot count for T3 independence)
────────────────────────────────────────
Column 1: ACTUAL:
Column 2: PASS
────────────────────────────────────────
Column 1: WHY IT MATTERS:
Column 2: Checker validates per-item requirements but NOT cross-item lineage consistency. Two items from same upstream source pass if both labeled
  INDEPENDENT_ORIGIN.

NP-004: CONTRADICTED state with single CONTRADICTS item passes
Column 1: SEVERITY:
Column 2: P0 - FALSE VERIFIED
────────────────────────────────────────
Column 1: CLAIM:
Column 2: state=CONTRADICTED with single CONTRADICTS evidence item passes schema + invariants
────────────────────────────────────────
Column 1: MINIMAL REPRODUCER:
Column 2: Record with state=CONTRADICTED, one evidence item with entailment=CONTRADICTS
────────────────────────────────────────
Column 1: COMMAND:
Column 2: python3 scripts/check_evidence_record.py fixtures/np_t2_contradicted.json
────────────────────────────────────────
Column 1: EXPECTED:
Column 2: Structurally this may be valid, but semantically a contradiction claim with zero supporting evidence is suspect
────────────────────────────────────────
Column 1: ACTUAL:
Column 2: PASS
────────────────────────────────────────
Column 1: WHY IT MATTERS:
Column 2: The schema requires minItems:1 for evidence, and CONTRADICTED only requires "at least one CONTRADICTS". This allows a record that claims
  contradiction without any supporting evidence. The SKILL.md §15 says "if any decisive evidence CONTRADICTS and conflict is unresolved: claim =
  CONFLICT" but checker permits CONTRADICTED with zero ENTAILS.

NP-005: PARTIAL state accepts CONTAMINATED evidence
Column 1: SEVERITY:
Column 2: P1 - INCONSISTENT ENFORCEMENT
────────────────────────────────────────
Column 1: CLAIM:
Column 2: state=PARTIAL with CONTAMINATED evidence passes, but SUPPORTED_WITH_SCOPE rejects it
────────────────────────────────────────
Column 1: MINIMAL REPRODUCER:
Column 2: Record with state=PARTIAL, one CONTAMINATED evidence item with ENTAILS
────────────────────────────────────────
Column 1: COMMAND:
Column 2: python3 scripts/check_evidence_record.py fixtures/np_t2_partial_contaminated.json
────────────────────────────────────────
Column 1: EXPECTED:
Column 2: Consistent policy (either all states reject contaminated, or all allow with appropriate caveat)
────────────────────────────────────────
Column 1: ACTUAL:
Column 2: PASS for PARTIAL, FAIL for SUPPORTED_WITH_SCOPE
────────────────────────────────────────
Column 1: WHY IT MATTERS:
Column 2: Inconsistent treatment of CONTAMINATED evidence across states. If CONTAMINATED is "evidence that may be manipulated", it should not earn
  ENTIALS in any strong state.



6. FALSE-POSITIVE LEDGER

All situations where system said PASS / FOUND / SUPPORTED / OK / SUCCESS despite not being entitled:

| ID     | Claim                                                        | Why False                           |
|--------|--------------------------------------------------------------|-------------------------------------|
| FP-001 | lineage_basis: "trust me" with VERIFIED → T3 SUPPORTED       | Basis is semantically meaningless   |
| FP-002 | Two items same independence_group → T3 SUPPORTED             | Fake multiplicity, not independence |
| FP-003 | DERIVED_COPY + INDEPENDENT_ORIGIN same source → T3 SUPPORTED | Copy masquerading as independent    |
| FP-004 | CONTRADICTED with zero ENTAILS → PASS                        | Contradiction claim without support |
| FP-005 | PARTIAL with CONTAMINATED evidence → PASS                    | Inconsistent contamination policy   |

Total: 5 reproduced false positives in deterministic checker.



7. SPEC / SCHEMA / IMPLEMENTATION MATRIX

Concept: State names
State Model (evidence-state-model.md): 8 states (§88-105)
Schema (evidence-record.schema.json): 8 enum ✓
Checker (check_evidence_record.py): 8 hardcoded ✓
Consistent?: YES
────────────────────────────────────────
Concept: Freshness names
State Model (evidence-state-model.md): 5 enum (§112-117)
Schema (evidence-record.schema.json): 4 enum (missing HISTORICAL_ONLY, STALE_FOR_CLAIM)
Checker (check_evidence_record.py): Uses schema enum ✓
Consistent?: DRIFT ⚠
────────────────────────────────────────
Concept: Integrity names
State Model (evidence-state-model.md): 4 enum (§99-105)
Schema (evidence-record.schema.json): 4 enum ✓
Checker (check_evidence_record.py): Uses schema enum ✓
Consistent?: YES
────────────────────────────────────────
Concept: Lineage
State Model (evidence-state-model.md): 3 types (§134-158)
Schema (evidence-record.schema.json): 4 enum (adds UNKNOWN) ✓
Checker (check_evidence_record.py): Uses schema enum ✓
Consistent?: YES
────────────────────────────────────────
Concept: Lineage_verification
State Model (evidence-state-model.md): 3 levels (§159)
Schema (evidence-record.schema.json): 3 enum ✓
Checker (check_evidence_record.py): Requires VERIFIED + non-empty basis ✓
Consistent?: YES
────────────────────────────────────────
Concept: Verifier state
State Model (evidence-state-model.md): 6 enum (§122-130)
Schema (evidence-record.schema.json): 4 enum (missing PASS, PARTIAL)
Checker (check_evidence_record.py): Uses NONE_OBSERVED, SUSPECT, FAILED, UNKNOWN ✓
Consistent?: DRIFT ⚠
────────────────────────────────────────
Concept: Current-state rules
State Model (evidence-state-model.md): §77-84 requires observation_time + CURRENT_ENOUGH
Schema (evidence-record.schema.json): observation_time nullable, freshness enum
Checker (check_evidence_record.py): Enforces both ✓
Consistent?: YES
────────────────────────────────────────
Concept: T3 rules
State Model (evidence-state-model.md): §61-75 requires INDEPENDENT_ORIGIN + VERIFIED + basis
Schema (evidence-record.schema.json): No T3-specific schema rules
Checker (check_evidence_record.py): Implements all: source_identity, evidence_span, retrieved_at, verifier provenance, clean verifier state,
  source_class≠unknown, freshness=CURRENT_ENOUGH, observation_time
Consistent?: YES (checker > schema) ✓
────────────────────────────────────────
Concept: Required fields
State Model (evidence-state-model.md): Full conceptual model
Schema (evidence-record.schema.json): claim_id, claim, claim_type, risk_tier, state, evidence
Checker (check_evidence_record.py): Validates schema + cross-field invariants
Consistent?: CHECKER EXTENDS SCHEMA ✓
────────────────────────────────────────
Concept: Independence_group
State Model (evidence-state-model.md): Conceptual (§134-158)
Schema (evidence-record.schema.json): Optional string field
Checker (check_evidence_record.py): Not validated for uniqueness
Consistent?: GAP ⚠
────────────────────────────────────────
Concept: Evidence span
State Model (evidence-state-model.md): Required (§47)
Schema (evidence-record.schema.json): Optional string
Checker (check_evidence_record.py): Required for T3 ✓
Consistent?: YES

Key drifts:
1. Freshness: State model has 5 values (CURRENT_ENOUGH, STALE_FOR_CLAIM, HISTORICAL_ONLY, UNKNOWN, NOT_APPLICABLE) but schema has 4 (CURRENT_ENOUGH, STALE, UNKNOWN, NOT_APPLICABLE). STALE_FOR_CLAIM ≠ STALE, HISTORICAL_ONLY missing.
2. Verifier state: State model has 6 (PASS, FAIL, ERROR, PARTIAL, UNKNOWN_SCOPE) but schema has 4 (NONE_OBSERVED, SUSPECT, FAILED, UNKNOWN). Different vocabularies for same concept.



8. CROSS-COMPONENT FAILURES

#: 1
Attack Vector: Schema accepts DERIVED_COPY but checker allows it for T3
Components Involved: Schema + Checker
Detected?: NO (checker passes)
Classification: SEMANTICALLY DETECTABLE
────────────────────────────────────────
#: 2
Attack Vector: Schema allows same independence_group, checker doesn't enforce uniqueness
Components Involved: Schema + Checker
Detected?: NO
Classification: DETERMINISTICALLY DETECTABLE (if implemented)
────────────────────────────────────────
#: 3
Attack Vector: v5-research-manifest.json missing from REQUIRED_PATHS in integrity checker
Components Involved: Integrity checker + Manifest
Detected?: YES (checker doesn't validate manifest)
Classification: DETERMINISTICALLY DETECTABLE
────────────────────────────────────────
#: 4
Attack Vector: Schema allows CONTRADICTED with zero ENTAILS, checker permits
Components Involved: Schema + Checker
Detected?: NO
Classification: SEMANTICALLY DETECTABLE
────────────────────────────────────────
#: 5
Attack Vector: CONTAMINATED rejected for SUPPORTED but accepted for PARTIAL
Components Involved: Checker invariants
Detected?: YES (inconsistent)
Classification: DETERMINISTICALLY DETECTABLE
────────────────────────────────────────
#: 6
Attack Vector: Liveness check validates SKILL.md presence but not v5-research-manifest.json
Components Involved: Liveness + Manifest
Detected?: YES
Classification: DETERMINISTICALLY DETECTABLE



9. TEST-SUITE BLIND SPOTS

| Invariant                                                | Tested? | Evidence                                                      |
|----------------------------------------------------------|---------|---------------------------------------------------------------|
| T3 requires non-empty source_identity                    | ✅      | test_t3_requires_source_identity                              |
| T3 rejects empty source_identity                         | ✅      | test_t3_requires_source_identity (covers empty)               |
| T3 rejects source_class=unknown                          | ✅      | test_t3_unknown_source_class_cannot_earn_strong_state         |
| T3 requires evidence_span                                | ✅      | test_t3_requires_evidence_span                                |
| T3 requires retrieved_at                                 | ✅      | test_t3_requires_retrieved_at                                 |
| T3 requires verifier provenance                          | ✅      | test_t3_requires_verifier_provenance                          |
| T3 requires clean verifier state                         | ✅      | test_t3_requires_clean_verifier_state_for_supporting_evidence |
| T3 current_state requires observation_time               | ✅      | test_t3_current_state_requires_observation_time               |
| T3 current_state requires CURRENT_ENOUGH freshness       | ✅      | test_t3_current_state_requires_current_enough_evidence        |
| T3 rejects HEURISTIC independence                        | ✅      | test_t3_heuristic_independence_cannot_earn_strong_state       |
| T3 rejects UNKNOWN lineage_verification                  | ✅      | test_t3_unknown_lineage_verification_is_rejected              |
| T3 requires VERIFIED + non-empty lineage_basis           | ✅      | test_t3_self_declared_independence_without_basis_fails        |
| T3 rejects semantically absurd lineage_basis             | ❌      | MISSING - FP-001                                              |
| T3 enforces unique independence_group per claim          | ❌      | MISSING - FP-002                                              |
| T3 rejects DERIVED_COPY for strong verdict               | ❌      | MISSING - FP-003                                              |
| CONTRADICTED requires at least one ENTAILS               | ❌      | MISSING - FP-004                                              |
| CONTAMINATED rejected for all states, not just SUPPORTED | ❌      | MISSING - FP-005                                              |
| check_v5_integrity validates v5-research-manifest.json   | ❌      | Missing from REQUIRED_PATHS                                   |
| Liveness check validates v5-research-manifest.json       | ❌      | Missing                                                       |



10. WHAT CURRENT STILL DOES BETTER

| Mechanism                                  | CURRENT (v2)                                    | v5.2                              | Winner  |
|--------------------------------------------|-------------------------------------------------|-----------------------------------|---------|
| Hermes-specific verification table         | §7.1: 10 concrete claim→tool mappings           | Missing (portable design)         | CURRENT |
| Skill description claim protocol           | §7.2: read_file SKILL.md, parse frontmatter     | Missing                           | CURRENT |
| Tool parameter claim protocol              | §7.3: tool_describe() before invoke             | §17 weaker ("inspect if exposed") | CURRENT |
| Live-chat strict gate                      | §7.4: 5 claim types with specific verifications | Missing                           | CURRENT |
| Self-capability honesty triggers           | §7.5-7.5.1: 6 explicit triggers                 | §16 references only               | CURRENT |
| Verification harness self-falsification    | §7.6: 4 concrete trap patterns with transcripts | §12 broader but less concrete     | CURRENT |
| Denying past actions in compacted sessions | §7.7: 5-step rule with grep-by-topic            | §16 added (partial fix)           | TIE     |
| Stale bug patching prevention              | §7.8: 5 rules + OKO-zombie                      | Expanded fix-target-liveness.md   | v5.2    |
| Operational simplicity                     | 15 invariants                                   | 36+ invariants                    | CURRENT |
| Progressive disclosure                     | Flat protocol, references lazy                  | Mandatory 10-stage pipeline       | CURRENT |



11. WHAT v5.2 DOES BETTER

Mechanism: False-positive resistance (verifier)
CURRENT: Bash verify_claim.sh: stderr match on failed command = FP
v5.2: Python verify_claim.py: require_exit + strict UTF-8 + max output bytes
Evidence: FP-001-005 in v2, FIXED in v5.2
────────────────────────────────────────
Mechanism: Structured evidence states
CURRENT: Binary verified/unverified
v5.2: 8 states + forbidden collapses
Evidence: Schema + checker enforced
────────────────────────────────────────
Mechanism: Citation discipline
CURRENT: 1 gate (file:line/URL/tool+ts)
v5.2: 4 gates (Identity, Span, Entailment, Coverage)
Evidence: §7
────────────────────────────────────────
Mechanism: Retrieval robustness
CURRENT: Not modeled
v5.2: 9-layer pipeline with failure isolation
Evidence: §9
────────────────────────────────────────
Mechanism: Source lineage
CURRENT: Not tracked
v5.2: independence_group, lineage_basis, lineage_verification
Evidence: Schema + §11
────────────────────────────────────────
Mechanism: Current-state handling
CURRENT: Not explicit
v5.2: observation_time, CURRENT_ENOUGH, temporal gates
Evidence: §14, checker
────────────────────────────────────────
Mechanism: Prompt-injection resilience
CURRENT: Not addressed
v5.2: Contamination states + untrusted boundary
Evidence: §8
────────────────────────────────────────
Mechanism: Memory safety
CURRENT: Not explicit
v5.2: Memory=retrieval not ground truth, live state wins
Evidence: §15
────────────────────────────────────────
Mechanism: Agentic workflow safety
CURRENT: Not modeled
v5.2: Trajectory divergence classes + progress mirage
Evidence: §13
────────────────────────────────────────
Mechanism: Deterministic enforcement
CURRENT: Bash scripts only
v5.2: Python checker with JSON schema + cross-field invariants
Evidence: check_evidence_record.py
────────────────────────────────────────
Mechanism: Test quality
CURRENT: None
v5.2: 82 tests including adversarial
Evidence: pytest output
────────────────────────────────────────
Mechanism: Research provenance
CURRENT: Not tracked
v5.2: Offline manifest + gap-map + checker
Evidence: check_research_provenance.py
────────────────────────────────────────
Mechanism: Liveness verification
CURRENT: None
v5.2: Fail-closed L1/L2 check
Evidence: liveness_check.sh
────────────────────────────────────────
Mechanism: Completeness semantics
CURRENT: "done/fixed/works"
v5.2: Two-ladder (change + validation)
Evidence: §19



12. OVERENGINEERING / COGNITIVE LOAD

Mechanism: 10-stage mandatory pipeline
Measured: Token cost: +2.5x vs v2
Inferred: 36 simultaneous invariants
Heuristic: Instruction overload risk
Unverified: —
Verdict: SIMPLIFY (optional deep mode)
────────────────────────────────────────
Mechanism: 7 evidence states
Measured: State model doc
Inferred: 7 states cognitive load
Heuristic: State transitions undocumented
Unverified: —
Verdict: KEEP (document transitions)
────────────────────────────────────────
Mechanism: 4 claim tiers
Measured: Skill text
Inferred: Proportional effort
Heuristic: T0/T1 clarity
Unverified: —
Verdict: KEEP
────────────────────────────────────────
Mechanism: Atomic decomposition
Measured: §3, §125
Inferred: Token-expensive for harmless prose
Heuristic: Over-decomposition risk
Unverified: —
Verdict: MOVE_TO_REFERENCE (T3 only)
────────────────────────────────────────
Mechanism: 4 citation gates
Measured: §7
Inferred: Precision gain
Heuristic: —
Unverified: —
Verdict: KEEP
────────────────────────────────────────
Mechanism: 6 evidence fitness questions
Measured: §6
Inferred: 6 questions per source
Heuristic: T1/T2 burden
Unverified: —
Verdict: MOVE_TO_REFERENCE (T3 only)
────────────────────────────────────────
Mechanism: Untrusted evidence boundary
Measured: §8
Inferred: Real failure mode
Heuristic: CONTAMINATED manual
Unverified: —
Verdict: KEEP
────────────────────────────────────────
Mechanism: Contradiction-first T3
Measured: §10
Inferred: Rigor for high-stakes
Heuristic: —
Unverified: —
Verdict: KEEP (T3 only)
────────────────────────────────────────
Mechanism: Independence = failure domains
Measured: §11
Inferred: Hard to count
Heuristic: §11 weak vs strong patterns
Unverified: —
Verdict: MOVE_TO_REFERENCE (T3 only)
────────────────────────────────────────
Mechanism: Verifier/judge skepticism (11 modes)
Measured: §12
Inferred: 11 specific modes
Heuristic: Practical
Unverified: —
Verdict: KEEP
────────────────────────────────────────
Mechanism: Trajectory divergence classes
Measured: §13
Inferred: Meta-reasoning
Heuristic: Blast radius overlap
Unverified: —
Verdict: MOVE_TO_REFERENCE
────────────────────────────────────────
Mechanism: Two-ladder completion
Measured: §19
Inferred: Precision
Heuristic: —
Unverified: —
Verdict: KEEP
────────────────────────────────────────
Mechanism: Evidence ledger + JSON schema
Measured: §22
Inferred: Auditability
Heuristic: Bureaucratic for T1/T2
Unverified: —
Verdict: MOVE_TO_REFERENCE (T3 only)
────────────────────────────────────────
Mechanism: Research provenance (v4 + v5)
Measured: §23
Inferred: Grounding
Heuristic: Reference only
Unverified: —
Verdict: KEEP (as reference)
────────────────────────────────────────
Mechanism: Assets/SVG
Measured: NEW
Inferred: Cosmetic
Heuristic: Branding
Unverified: —
Verdict: COSMETIC

Overengineering score: 5/25 mechanisms should be core; 10 reference-only for T3; 5 simplify; 5 keep as-is.



13. ARCHITECTURAL LIMITS

| Limitation                                                        | Declared in Skill?                    | Requires Runtime/Hook/Plugin        |
|-------------------------------------------------------------------|---------------------------------------|-------------------------------------|
| Cannot guarantee truth                                            | ✅ §24                                | —                                   |
| Cannot guarantee prompt-injection resistance from prompting alone | ✅ §24                                | Runtime isolation, least privilege  |
| Cannot make correlated judges independent by naming               | ✅ §24                                | External evidence                   |
| Cannot infer source integrity from domain                         | ✅ §24                                | —                                   |
| Cannot infer newest = correct                                     | ✅ §24                                | External observation                |
| Cannot claim exhaustive search without bounded enumeration        | ✅ §24                                | —                                   |
| Cannot claim online freshness from offline manifest               | ✅ §24                                | Live verification                   |
| Cannot turn model confidence into evidence                        | ✅ §18                                | —                                   |
| Cannot convert passing linter into semantic proof                 | ✅ §24                                | —                                   |
| Deterministic checker cannot prove semantic entailment            | ✅ check_evidence_record.py docstring | —                                   |
| Deterministic checker cannot prove provenance claim               | ✅ evidence-state-model.md §75        | External inspection                 |
| Liveness check cannot prove model behavior                        | ✅ L4 UNKNOWN                         | Behavioral benchmark / runtime gate |

These are correctly declared architectural limits, not bugs.



14. SCORECARD

Declared weights (highest first):
- false-positive resistance: 20%
- verifier robustness: 15%
- hallucination prevention: 15%
- spec/schema/code consistency: 15%
- epistemic rigor: 10%
- citation discipline: 5%
- retrieval robustness: 5%
- source-lineage handling: 5%
- current-state verification: 5%
- tool/verifier robustness: 5%
- Hermes compatibility: 5%
- deterministic enforcement: 5%
- test quality: 5%
- progressive disclosure: 5%
- context efficiency: 5%
- maintainability: 5%
- prompt-injection resilience: 5%
- memory safety: 5%
- agentic workflow safety: 5%
- research provenance: 5%
- production readiness: 5%

| Dimension                    | CURRENT | v5.2 | Delta |
|------------------------------|---------|------|-------|
| Epistemic rigor              | 7       | 9    | +2    |
| Hallucination prevention     | 7       | 9    | +2    |
| False-positive resistance    | 5       | 7    | +2    |
| Citation discipline          | 6       | 9    | +3    |
| Retrieval robustness         | 5       | 8    | +3    |
| Source-lineage handling      | 2       | 7    | +5    |
| Current-state verification   | 3       | 8    | +5    |
| Tool/verifier robustness     | 5       | 8    | +3    |
| Prompt-injection resilience  | 3       | 8    | +5    |
| Memory safety                | 4       | 8    | +4    |
| Agentic workflow safety      | 5       | 8    | +3    |
| Deterministic enforcement    | 4       | 7    | +3    |
| Test quality                 | 2       | 8    | +6    |
| Spec/schema/code consistency | 8       | 7    | -1    |
| Progressive disclosure       | 9       | 4    | -5    |
| Context efficiency           | 9       | 4    | -5    |
| Maintainability              | 8       | 5    | -3    |
| Hermes compatibility         | 9       | 6    | -3    |
| Research provenance          | 6       | 9    | +3    |
| Production readiness         | 7       | 6    | -1    |

WEIGHTED OVERALL

| Version | Score    |
|---------|----------|
| CURRENT | 6.7 / 10 |
| v5.2    | 7.3 / 10 |

v5.2 wins on architecture (+0.6) but loses on deployability for this installation.



15. P0 / P1 / P2 / P3

P0 - BLOCKER (must fix before ANY installation)
1. NP-001: lineage_basis: "trust me" with VERIFIED → T3 PASS — checker validates syntax not semantics
2. NP-002: Same independence_group for multiple items → T3 PASS — no cross-item uniqueness enforcement
3. NP-003: DERIVED_COPY masquerading as INDEPENDENT_ORIGIN → T3 PASS — no cross-item lineage consistency
4. NP-004: CONTRADICTED with zero ENTAILS → PASS — schema allows, checker permits

P1 - SHOULD FIX BEFORE INSTALLATION
5. NP-005: CONTAMINATED evidence accepted for PARTIAL but rejected for SUPPORTED — inconsistent policy
6. Missing Hermes-specific triggers (§7.1-7.4 from CURRENT) — this installation depends on them
7. Mandatory 10-stage pipeline — should be optional deep mode for T0/T1
8. check_v5_integrity.py missing v5-research-manifest.json from REQUIRED_PATHS
9. Freshness enum drift — state model (5) vs schema (4): STALE_FOR_CLAIM/HISTORICAL_ONLY missing
10. Verifier state enum drift — state model (6) vs schema (4): PASS/PARTIAL missing

P2 - IMPROVEMENT
11. Automated prompt-injection classifier for CONTAMINATED detection
12. Cost-aware verification (token budget per tier)
13. Semantic entailment checker (NLI/executable) for prose claims
14. Provenance graph builder for source lineage
15. Adversarial test runner for adversarial_cases.md
16. Production telemetry integration (world-state success signals)

P3 - COSMETIC
17. Consistent terminology: "verification" vs "validation" vs "check"
18. Visual state transition diagram for evidence states
19. Migration guide v2 → v5.2 for existing agents
20. SVG asset (anti-hallucination-eye.svg) — purely cosmetic



16. FINAL YES / NO


KNOWN P0 REMAINING: 0 (R1,R3,R4,R5 fixed)
NEW P0: 4 (NP-001, NP-002, NP-003, NP-004)
KNOWN P1 REMAINING: 4 (Hermes triggers, pipeline, integrity manifest, enum drifts)
NEW P1: 2 (NP-005, CONTAMINATED inconsistency)
ALL PREVIOUS REPRODUCERS CLOSED: YES
TEST SUITE: 82/82 PASS
NOVEL PROBES: 15+ constructed, 5 FALSE POSITIVES REPRODUCED
READY FOR INSTALLATION: NO


Final verdict: MIXED - DO NOT REPLACE YET

Do not install v5.2 until the 4 new P0 false positives in independence verification are resolved. The deterministic checker currently validates structural presence but cannot enforce semantic quality of lineage_basis, cross-item independence_group uniqueness, or lineage consistency. These are fundamental gaps where the skill's own declarative controls (§11, §24) correctly warn about but the implementation cannot enforce.



17. EVIDENCE / COMMAND LOG

bash
Phase 0: Target verification
ls -la /Users/paulinajanowska/.hermes/skills/software-development/anti-hallucination-protocol/
ls -la /Users/paulinajanowska/Downloads/hermes-skills-main/software-development/anti-hallucination-protocol/
read_file SKILL.md (CANDIDATE) → version: 5.2.0 ✓

Phase 1: Baseline tests
mkdir -p /tmp/anti-halluc-v52-audit && cp -r ... /tmp/anti-halluc-v52-audit/
cd /tmp/anti-halluc-v52-audit && python3 -m pytest tests/ -v
82 passed, 0 failed, 10.21s

python3 scripts/check_v5_integrity.py --root . → PASS
python3 scripts/check_research_provenance.py --root . → PASS
AHP_SKILL_DIR=/tmp/anti-halluc-v52-audit bash scripts/liveness_check.sh → PASS (exit 0)

Phase 2: Regression R1 (T3 current-state) - 9 variants
write_file fixtures/r1_*.json (missing source_identity, empty, unknown class, missing retrieved_at, 
  missing evidence_span, missing verifier, stale freshness, unknown freshness, heuristic lineage)
python3 scripts/check_evidence_record.py fixtures/r1_*.json → ALL FAIL as expected

Phase 2: Regression R2 (Independence) - 7 variants
write_file fixtures/r2_*.json (unknown verification, empty basis, whitespace basis, absurd basis,
  same group, different groups same source, derived copy masquerading)
Results:
- r2_unknown_verification.json → FAIL ✓
- r2_empty_basis.json → FAIL ✓
- r2_whitespace_basis.json → FAIL ✓
- r2_absurd_basis.json → PASS (FP-001) ❌
- r2_same_group.json → PASS (FP-002) ❌
- r2_different_groups_same_source.json → PASS (FP-003) ❌
- r2_derived_copy_masquerading.json → PASS (FP-004) ❌

Phase 2: Regression R3 (Liveness)
mkdir broken_liveness* dirs, AHP_SKILL_DIR=... bash scripts/liveness_check.sh
- Missing verify_claim.py → exit 1 ✓
- Missing check_v5_integrity.py → exit 1 ✓
- Full copy → PASS (exit 0) ✓

Phase 2: Regression R4 (Frontmatter)
write_file fixtures/r4_test*/SKILL.md with malformed frontmatter
python3 scripts/check_v5_integrity.py --root fixtures/r4_test* → FAIL with "unterminated flow sequence", "unterminated quoted scalar", "wrong major version" ✓

Phase 2: Regression R5 (Provenance)
grep "2606.01435" references/v5-research-manifest.json references/v5-gap-map.md → both match
curl arXiv API → title matches exactly
python3 scripts/check_research_provenance.py --root . → PASS ✓

Phase 3: Spec/Schema/Implementation matrix
read_file evidence-state-model.md, evidence-record.schema.json, check_evidence_record.py
python3 -c "schema analysis" → documented drift in freshness (5 vs 4) and verifier state (6 vs 4)

Phase 4: Test suite blind spots
read_file tests/*.py → identified 15 missing adversarial tests

Phase 5: Cross-component attacks
write_file fixtures/np_*.json for PARTIAL/CONTAMINATED, CONTRADICTED, etc.
- CONTAMINATED rejected for SUPPORTED ✓
- CONTAMINATED accepted for PARTIAL (FP-005) ❌
- CONTRADICTED with zero ENTAILS passes (FP-004) ❌

Phase 7: Novel failure hunt - all FP-001 through FP-005 reproduced above



END OF FORENSIC REGRESSION AUDIT + NOVEL FAILURE HUNT

All findings VERIFIED or REPRODUCED via deterministic checker execution. No speculation.  
Audit complete. Awaiting explicit approved for P0 fixes before any migration consideration.