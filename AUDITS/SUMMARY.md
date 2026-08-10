# Anti-Hallucination Protocol - multi-model audit synthesis through v5.4.2

This file is the top-level audit synthesis for the standalone repository.

It preserves the historical v5.2 -> v5.3 -> v5.4 audit decisions and adds the v5.4 Round 3 -> v5.4.1 hardening evidence.

Detailed Round 3 adjudication lives in:

- [`v5.4-round3-v5.4.1-summary.md`](v5.4-round3-v5.4.1-summary.md)
- [`v5.4.1-hardening-status.md`](v5.4.1-hardening-status.md)

Canonical future-auditor methodology lives in:

- [`CANONICAL-AGENT-AUDIT-PROMPT.md`](CANONICAL-AGENT-AUDIT-PROMPT.md)

## Current release anchor

The latest regression-verified public release covered by this synthesis is:

```text
v5.4.2
release tag commit: 94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

Final release verification recorded for v5.4.2:

```text
Python 3.11 CI: PASS
Python 3.13 CI: PASS
Python 3.13 test inventory: 126 collected / 126 passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
user-pressure policy invariant: present + regression-locked
behavioral obedience: UNKNOWN / not claimed
```

These are historical release facts. They are not a claim that the current `main` HEAD has the same tree, test count or CI state. Recompute current state before making a present-tense claim.

---

## Evidence method

Audit reports are not votes and must not be averaged as if every reviewer observed the same system.

Evidence hierarchy used by this synthesis:

1. `REPRODUCED` - concrete failure reproduced with an executable probe and observed result.
2. `CROSS-CONFIRMED` - independently reproduced or directly confirmed by more than one execution-capable audit.
3. `FILE/WEB VERIFIED` - directly established from inspected source or a relevant primary public source.
4. `INFERENCE` - conclusion follows from inspected evidence but was not directly executed.
5. `HEURISTIC` - design, cognitive-load or behavioral judgment requiring evaluation.
6. `UNVERIFIED` - not established in the available environment/material.
7. `REJECTED` - claimed severity or conclusion does not follow from the evidence.

Core rule:

> **One reproducer outranks five opinions.**

A green unit suite establishes only the checked executable contracts. It does not prove semantic truth or LLM obedience.

---

# Audit generation 1 - v5.2 corpus

The first major audit wave informed v5.3 and v5.4.

## v5.2 Hermes/execution-capable audits

These reviewers had access to a local repository/runtime and could inspect scripts, schemas, tests, CURRENT/CANDIDATE state and/or the installed Hermes parser:

- `deepseek-v4-flash-0731-2.md`
- `gpt-5.6-terra-2.md`
- `sonnet-5-2.md`
- `big-pickle-2.md`
- `nemotron-3-ultra-550b-a55b-2.md`

Executable findings from these reports become implementation evidence only when backed by a concrete reproducer, command, exit code and observed result.

## v5.2 Perplexity document-only audits

For this historical v5.2 wave, the following Perplexity reviewers received `SKILL.md` and `README.md` plus permission to research public primary sources rather than a fresh executable clone:

- `PPX-SONAR2.md`
- `PPX-GROK4.5.md`
- `PPX-GLM5.2.md`
- `PPX-KIMIK3.md`
- `PPX-AHP_v5.2_Forensic_Audit.md`

That limitation applies to this v5.2 audit set. It must not be generalized to every later Perplexity audit configuration.

These reports were useful for document architecture, research grounding, public claims, progressive disclosure and cognitive-load hypotheses, but could not by themselves establish that repository scripts/tests/runtime enforcement worked.

## Historical v5.2 source-file manifest

The SHA-256 values below refer to user-supplied source files before archival. They are evidence identifiers, not automatic proof that every GitHub copy is byte-identical.

| File | Bytes | SHA-256 |
|---|---:|---|
| `deepseek-v4-flash-0731-2.md` | 23,493 | `b4efbe21fb2cdc31223825e2d6ac1b83237807c27206b5857015097f7216b08b` |
| `gpt-5.6-terra-2.md` | 12,234 | `3a76ba3cd3778b90ef26e0b9d836874485ab93e4920b40169a029847c4b836f2` |
| `sonnet-5-2.md` | 44,298 | `e97fa31f85bed87a64eb3aec8993b97639038e38072a88756975dd535ed9f60f` |
| `big-pickle-2.md` | 24,377 | `9103cbb26007b866af96b3dd2d0495c9e257dc76ee52a16ffbcf68b11b7f25bd` |
| `nemotron-3-ultra-550b-a55b-2.md` | 41,905 | `c4d40024caeb996a53e146a6c3213ee9fc8f36cceeab4770a3f8d6cd34ee97bc` |
| `PPX-SONAR2.md` | 49,476 | `85e5ae13e1b287942c73857f38a871a9bfa442af200c3115acaead9316da3e9a` |
| `PPX-GROK4.5.md` | 59,062 | `2dd8fccda14221f9fc42e751e467ec00f75fcea845d4e99545fe9939adc2fd1c` |
| `PPX-GLM5.2.md` | 91,118 | `4addb24f096248a7be5f7e0090df70daa957676a01478610b293bf23f0eccf20` |
| `PPX-KIMIK3.md` | 58,889 | `441bca14c3166e97ed4c393783e00206f6710710c07cea31e84dc8adc48ac64c` |
| `PPX-AHP_v5.2_Forensic_Audit.md` | 48,308 | `445ef4d291880da971966e3d2c7f49c4136d0d7d353e8f22be29c4d0b7996665` |

### Archive-integrity warning

`AUDITS/PPX-GLM5.2.md` remains an explicit placeholder recording the original 91,118-byte source size and SHA-256 rather than a byte-for-byte copy of the original report.

Therefore the repository must **not** claim a complete byte-identical historical audit archive until the raw source is restored and verified.

---

# v5.2 consolidated finding ledger

| ID | Finding | Evidence | Severity | Disposition |
|---|---|---|---|---|
| F-001 | `check_v5_integrity.py` could PASS frontmatter that Hermes/PyYAML rejects or interprets differently | REPRODUCED by Terra and DeepSeek | P1 | FIXED in v5.3 with real YAML parsing + regressions |
| F-002 | duplicate declared `independence_group` was not rejected for strong T3 support | REPRODUCED by Big Pickle and Nemotron | P1 | FIXED narrowly, without pretending labels prove real independence |
| F-003 | T3 timestamps were shape-only and could accept impossible/future values | REPRODUCED by DeepSeek and Big Pickle | P2 | FIXED with strict profile + future-time invariant |
| F-004 | research sources were duplicated in active `SKILL.md` while provenance checking targeted another canonical list | REPRODUCED/file verified | P1 | FIXED by removing duplicated active bibliography and keeping canonical references/manifests |
| F-005 | legacy `godmode_battery.sh` could write installation-external calibration state / report partial score | FILE-VERIFIED | P1 operational | RETIRED from active portable v5 contract; legacy/read-only boundary documented |
| F-006 | `EVIDENCE RECORD: PASS` overstated a structural checker | FILE-VERIFIED | P1 | RENAMED to `STRUCTURALLY_VALID` |
| F-007 | README checkout liveness command could target installed skill rather than checkout | REPRODUCED by Terra/DeepSeek | P2 | FIXED with explicit `AHP_SKILL_DIR` checkout usage |
| F-008 | conceptual evidence vocabulary drifted from executable schema/checker terminology | FILE-VERIFIED | P1/P2 | ALIGNED |
| F-009 | active `SKILL.md` carried too much always-loaded research/detail | CROSS-CONFIRMED document finding; behavioral effect HEURISTIC | architecture | FIXED by v5.3 progressive disclosure; behavioral effect still requires benchmark |
| F-010 | portable skill contained installation-specific `HSDB = HyperspaceDB` convention | FILE-VERIFIED | P2 | REMOVED from portable active skill |
| F-011 | `consequential` escalation trigger lacked compact operational definition | CROSS-CONFIRMED document finding | P1 | DEFINED near risk-tier entry point |
| F-012 | README heading `What it catches` read too much like behavioral guarantee | document finding | P2 | RENAMED/qualified as failure modes targeted |
| F-013 | behavioral obedience under long context/tool pressure unmeasured | explicit limitation | architectural unknown | BENCHMARK, not prose fix |
| F-014 | native Windows Bash execution not demonstrated | INFERENCE from shipped shell boundary | P2 docs | support boundary clarified |
| F-015 | canonical protocol attack corpus lived only under `tests/` | FILE/DOC | P2 | added progressive-disclosure `references/adversarial-cases.md` |

---

# Findings intentionally rejected or downgraded

## `"trust me"` as `lineage_basis` is not a deterministic P0

A string-shape validator cannot determine whether arbitrary free-text provenance is factually true. Phrase blacklists would be trivially bypassable and would confuse syntax with provenance truth.

Decision: keep the external-provenance limitation, validate auditable structure, and never present structural success as semantic truth.

## One decisive contradiction may legitimately produce `CONTRADICTED`

A claim can be contradicted by decisive contrary evidence without surviving support.

The relevant invariant is different: if material `ENTAILS` support survives together with contradiction, the result must not be `CONTRADICTED`; it belongs in `CONFLICT`.

## `PARTIAL` may retain contaminated evidence

A partial/inconclusive record may preserve contaminated evidence as an observed input while refusing strong support. Blanket deletion would erase provenance.

Strong support has stricter integrity requirements.

## The full pipeline is not mandatory ceremony for T0/T1

The protocol is risk-scaled. v5.3 introduced a seven-rule hot path; v5.4 made ordinary T2 explicitly hot path + direct check by default.

## Do not add `PLAUSIBLY_INDEPENDENT`

A new confidence-like enum would not solve provenance. Unknown lineage should remain unknown with explanation.

## Do not hard-require terminal access for the entire skill

The policy layer still provides value when local deterministic helpers are unavailable. Degraded mode must downgrade unperformed verification rather than disable the entire policy.

---

# v5.3 accepted change set

v5.3 was hardening + compression, not a feature pile.

1. Replaced hand-written frontmatter acceptance with real YAML parsing compatible with Hermes/PyYAML semantics.
2. Added malformed-YAML regressions.
3. Added stricter timestamp validation and future-time rejection for strong T3 support.
4. Added duplicate independence-group detection.
5. Renamed evidence-record success from `PASS` to `STRUCTURALLY_VALID`.
6. Removed duplicated research bibliography/source lists from active `SKILL.md`.
7. Aligned evidence-state vocabulary with executable schema/checker terminology.
8. Defined `consequential` operationally near the risk-tier entry point.
9. Removed local HSDB convention from portable skill.
10. Added protocol-level adversarial reference under `references/` while keeping executable tests under `tests/`.
11. Clarified README liveness validation and Windows/Bash boundary.
12. Made legacy/godmode helpers explicitly non-load-bearing and read-only by default.
13. Preserved the hard boundary that Markdown and structural checks do not prove semantic truth or runtime obedience.

Conceptual change:

```text
prompt got smaller
system got larger
```

---

# v5.4 disposition

v5.4 was a consolidation/hardening release. It did not add a new epistemic state machine.

| ID | v5.4 issue | Basis | Disposition |
|---|---|---|---|
| V54-001 | checker could silently ignore a future unsupported JSON Schema assertion | source inspection | FIXED fail-closed schema-definition gate |
| V54-002 | integrity checker accepted any `5.x.y` | source inspection | FIXED exact release pin |
| V54-003 | Python ISO parser accepted forms outside intended RFC3339 profile | source inspection | FIXED lexical/profile gate + regression |
| V54-004 | strong T3 supporting evidence could use integrity weaker than `CLEAN_OBSERVED` | contract comparison | FIXED |
| V54-005 | `CONTRADICTED` could retain surviving `ENTAILS` evidence | schema/checker/reference comparison | FIXED; surviving both sides -> `CONFLICT` |
| V54-006 | current research display identity drift | primary-source recheck | FIXED in manifest/gap map |
| V54-007 | helper invocation/non-automatic enforcement under-explained | docs/runtime contract review | FIXED in SKILL/README with `${HERMES_SKILL_DIR}` and degraded mode |
| V54-008 | ordinary T2 could still read like full apparatus was mandatory | cross-model document finding | FIXED hot path + direct check default |
| V54-009 | behavioral obedience unmeasured | explicit project limitation | BENCHMARK, not prose fix |
| V54-010 | historical raw audit archive incomplete | repository inspection | OPEN archive-integrity task |

v5.4 deliberately retained this semantic boundary:

```text
STRUCTURALLY_VALID != TRUE
PATCH PRESENT != BUG CLOSED
GREEN UNIT TESTS != MODEL OBEDIENCE
DOCUMENTED CONTROL != IMPLEMENTED CONTROL != RUNTIME ENFORCEMENT
```

---

# Audit generation 2 - v5.4 Round 3

The v5.4 Round 3 audit directly produced v5.4.1.

Detailed adjudication:

- [`v5.4-round3-v5.4.1-summary.md`](v5.4-round3-v5.4.1-summary.md)

Evidence classes in this round:

1. fresh-clone execution;
2. execution on supplied/project-file snapshots;
3. static/source/cross-component review;
4. methodology review.

Round 3 evidence identifiers recorded in the detailed synthesis:

| Report | Class | Key scope |
|---|---|---|
| `gpt-5.6-sol-v5.4-prompt-review.md` | methodology review | audit-design / evidence-boundary review |
| `big-pickle-4.md` | execution audit | v5.4 test suite + integrity/provenance/liveness |
| `glm5.2-ahp-v5.4-adversarial-audit.md` | project-files execution | materialized snapshot + additional probes |
| `deepseek-v4-flash-0731-4.md` | fresh-clone execution | standalone repo + Hermes parser comparison + adversarial probes |
| `gpt-5.6-terra-4.md` | static/cross-component/live-source | source-level false-positive hunt + primary-source research checks |

Important archive qualification: names/hashes in the detailed synthesis identify the supplied evidence. They do not by themselves prove that every raw Round 3 source report is currently present in GitHub byte-for-byte.

## 92-vs-102 test conflict

Resolved by stronger fresh-clone evidence:

```text
Big Pickle: 102 collected, 100 PASS, 2 FAIL
DeepSeek V4 Flash: fresh clone, 102 collected, 100 PASS, 2 FAIL
GLM 5.2: 92/92 on a different Project Files materialization
```

Therefore the canonical v5.4 pre-patch test inventory was 102, with 100 passing and 2 failing.

The two failures were test-contract/fixture defects rather than a reason to weaken the YAML checker:

1. `description: Test fixture [` is valid YAML plain-scalar content.
2. the old `metadata.hermes` scalar fixture was malformed earlier than the assertion expected because nested `tags:` remained below a scalar.

v5.4.1 corrected the tests and retained the checker semantics.

## Round 3 accepted findings

| ID | Finding | Evidence | v5.4.1 disposition |
|---|---|---|---|
| R3-001 | empty `file-contains` can false-FOUND | FILE-VERIFIED | FIXED + regression |
| R3-002 | empty `file-line` expected text can false-FOUND | FILE-VERIFIED | FIXED + regression |
| R3-003 | expected command text could be synthesized across stdout/stderr concatenation | FILE-VERIFIED | FIXED: streams matched independently + regression |
| R3-004 | `NOT_FOUND_WITHIN_SCOPE` could omit explicit inspected scope | FILE-VERIFIED | FIXED + regression |
| R3-005 | same declared source could receive distinct independence groups | REPRODUCED by DeepSeek | FIXED + regression |
| R3-006 | same declared source identity could receive distinct independence groups | FILE-VERIFIED | FIXED + regression |
| R3-007 | whitespace-only load-bearing strings passed length-only constraints | FILE-VERIFIED | FIXED + regressions |
| R3-008 | `PARTIAL` could be declared with no supporting/partial evidence | FILE-VERIFIED | FIXED |
| R3-009 | schema-valued unsupported form could outrun local validator profile | FILE-VERIFIED evolution gap | FIXED fail-closed |
| R3-010 | required reference symlink could resolve outside skill root | static/cross-component | FIXED + regression |
| R3-011 | UTF-8 BOM behavior drifted from Hermes/PyYAML acceptance | static/cross-component | FIXED + regression |
| R3-012 | `CLEAN` vs `CLEAN_OBSERVED` vocabulary drift | FILE-VERIFIED | FIXED |
| R3-013 | arXiv:2606.01435 current display identity drift | REPRODUCED + primary source | FIXED |
| R3-014 | arXiv:2607.25152 canonical display omitted current subtitle | WEB/FILE comparison | FIXED |
| R3-015 | two shipped v5.4 tests encoded invalid expectations | CROSS-CONFIRMED Big Pickle + DeepSeek | FIXED fixtures |

Additional v5.4.1 hardening after the first Round 3 patch included:

- whitespace-only verifier matcher rejection;
- bounded command-output handling using temporary files instead of unbounded `capture_output=True` memory retention;
- expanded liveness verifier self-tests;
- path-with-spaces/multiple-failure liveness regressions;
- quoted duplicate top-level YAML key detection;
- mandatory startup integration documentation for always-on Hermes use;
- permanent Python 3.11/3.13 GitHub Actions regression CI.

---

# v5.4.1 release verification

The final release snapshot was regression-verified after the post-merge hardening.

Final Python 3.13 run:

```text
124 collected
124 passed
V5 INTEGRITY: PASS
RESEARCH PROVENANCE: PASS
portable L1/L2 liveness: PASS
```

Python 3.11 completed the same configured gate successfully.

The release tag is:

```text
v5.4.1 -> 7f5454c9c8e58ca9bd0728d13210d6c5a6424bc1
```

Release judgment:

```text
DETERMINISTIC REGRESSION: VERIFIED
INTEGRITY: VERIFIED
OFFLINE PROVENANCE: VERIFIED
PORTABLE LIVENESS: VERIFIED
BEHAVIORAL OBEDIENCE: UNVERIFIED BY DESIGN
SEMANTIC TRUTH: OUTSIDE STRUCTURAL CHECKER
REAL-WORLD SOURCE INDEPENDENCE: NOT PROVEN BY LABELS
```

v5.4.1 is a hardening patch, not a new policy architecture. It preserves the seven-rule hot path, T0-T3 scaling, progressive disclosure and structural-vs-semantic boundary.

---

# Startup/load boundary added after v5.4 audit work

Always-on installation now explicitly distinguishes:

```text
INSTALLED != LOADED
LOADED != OBEYED
```

For workspaces using `/start` or equivalent boot orchestration, README requires explicit startup loading of:

```text
skill_view(name="anti-hallucination-protocol")
```

A boot trace showing successful skill load establishes loading only. It does not prove behavioral obedience.

---

# Methodology correction for future audits

A future supposedly independent auditor must not read historical conclusions before its novel hunt.

Canonical order:

```text
FRESH CLONE
  -> verify target identity/environment
  -> inventory repository
  -> do not consume AUDITS/** conclusions yet
  -> baseline execution
  -> prompt-mandated probes
  -> genuinely novel failure hypotheses/probes
  -> provisional ledger
  -> only then read historical AUDITS/**
  -> historical reconciliation
```

The complete five-pass prompt is in:

- [`CANONICAL-AGENT-AUDIT-PROMPT.md`](CANONICAL-AGENT-AUDIT-PROMPT.md)

This prevents historical findings from contaminating a supposedly independent novel hunt.

---

---

# v5.4.2 policy patch disposition

v5.4.2 is a narrow always-loaded policy patch on top of v5.4.1. It does not add a new evidence state or risk tier.

Added invariant:

```text
USER PRESSURE DOES NOT UPGRADE EVIDENCE STATE

INCONCLUSIVE + user pressure + no new evidence
!= SUPPORTED_WITH_SCOPE
```

The active skill now states that evidence state may strengthen only when new evidence, a stronger observation, or a legitimately stronger verification basis has been obtained. User confidence, repetition, authority, preference, urgency, frustration or pressure is not evidence by itself.

The policy also separates human/user governance from factual truth: users control goals, scope, authorization, acceptable risk and normative choices, but factual assertions remain claims or explicit assumptions unless established by the available evidence.

Executable additions:

- `references/adversarial-cases.md` case 31 - user pressure to upgrade evidence;
- `tests/test_v542_policy_regressions.py` - locks policy presence and case-31 contract;
- exact release metadata/checker/liveness/schema title aligned to 5.4.2.

Release evidence is recorded in [`v5.4.2-release-status.md`](v5.4.2-release-status.md). Final PR CI passed on Python 3.11 and 3.13; Python 3.13 collected and passed 126 tests, followed by integrity, provenance and portable liveness PASS. The tested PR merge tree and released main merge tree were compared and contained zero changed files.

This proves the repository contract for the tested tree. It does not prove models obey the new invariant in real conversations.

# Open frontier after v5.4.2

The major unresolved question is behavioral/runtime effectiveness, not another missing Markdown paragraph.

Still unproven:

- behavioral obedience under long context;
- resistance to user pressure to upgrade an epistemic state without new evidence;
- real-world source independence beyond visible structural contradictions;
- current-state truth beyond actual external observations;
- semantic entailment beyond structural records;
- LLM-judge bias/calibration;
- native Windows execution evidence;
- complete byte-identical raw audit archive.

The next high-value project phase is a real behavioral benchmark comparing control sessions with sessions where AHP is explicitly loaded, including direct measurement of the v5.4.2 user-pressure invariant.

A proposed behavioral invariant is:

```text
USER PRESSURE DOES NOT UPGRADE EVIDENCE STATE

INCONCLUSIVE + operator pressure + no new evidence
!=
SUPPORTED_WITH_SCOPE
```

For the current roadmap, see [`../TODO.md`](../TODO.md).

---

# Bottom line

v5.2 established the broad architecture but overpacked the active instruction plane.

v5.3 compressed the active kernel and moved detail into progressive-disclosure references, scripts and tests.

v5.4 hardened schema/checker/release/temporal contracts without re-bloating the skill.

v5.4 Round 3 found real deterministic/test-contract gaps in the standalone release. v5.4.1 closed those reproduced/static gaps and was finally verified with 124/124 tests on Python 3.13 plus a successful Python 3.11 matrix job, integrity, provenance and portable liveness.

That does **not** prove zero hallucinations, semantic truth, real-world source independence or behavioral obedience.

The current project boundary remains:

> **Make unsupported certainty harder, measure what can actually be measured, and abstain where evidence does not earn the sentence.**
