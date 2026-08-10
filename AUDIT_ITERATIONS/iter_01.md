# AUDIT ITERATION 1 — Anti-Hallucination Protocol (2026-08-10)

Auditor: Gniewislawa (Hermes CLI)
Protocol: AHP_AUDIT_TASK.md (10-iteration prompt/answer improvement loop)
Branch: ahp-usage-test (after merge of main — see C1)
Verification: claims below verified against files in this repo
(SKILL.md, AHP_usage_test/, tests/) and against production
~/.hermes/skills/... (sha256 comparison, grep).

---

## 1. CRITIQUE

### C1. [RESOLVED DURING AUDIT] Branch artifact mismatch: SKILL.md 5.4.0 vs tested 5.4.2 (HIGH, was critical)

AHP_usage_test/ documents testing and deployment of v5.4.2 (commit
c6ee5f1, sha256 649bcc3e, 126/126 tests, user-pressure invariant). But
the SKILL.md checked out on ahp-usage-test was **v5.4.0** (sha256
acab1c38) — the branch was cut before v5.4.2 landed on main. Anyone
auditing from this branch alone would have judged a stale artifact
against v5.4.2 evidence.

Action taken this iteration: merged origin/main into ahp-usage-test.
SKILL.md now 5.4.2 (sha256 649bcc3e = production = main, byte-identical).
Repo test suite re-run: **151 passed** (28.58s). The evidence in
AHP_usage_test/ now matches the audited artifact.

Lesson (applies to the boot-procedure repo too): when packaging usage
evidence for an external auditor, verify the artifact VERSION matches
the evidence VERSION before pushing. This is exactly the class of error
the protocol itself exists to prevent — the packaging process did not
apply the protocol to itself.

### C2. SKILL.md v5.4.2 says "version: 5.4.2" — internal consistency (VERIFIED, OK)

Frontmatter version 5.4.2 matches the deployed artifact and the
production install. No drift. [VERIFIED via shasum: repo==prod==649bcc3e]

### C3. The v5.4.2 user-pressure rule is new and tested, but only 1 test file (MEDIUM)

tests/test_v542_policy_regressions.py exists and passes, but the
behavioral claim "user pressure does not strengthen evidence" is a
POLICY rule — it lives in SKILL.md prose and is only exercised through
one regression test + the TEST_user_pressure_v542.md usage report.
[VERIFIED: file exists, 151 total tests pass]. Gap: no test that a
strong-worded claim WEAKENS when pressure is applied without new
evidence (the inverse direction). Suggest adding a second regression:
pressure + NO new evidence must NOT change wording strength.

### C4. Recovery-from-glitch remains prose-only (HIGH, confirmed by own finding)

FINDING_G_glitch.md documents recursive meta-collapse with recovery as
prose (SKILL.md "Completion and recovery" section, 5 retraction steps),
no enforced self-detection cycle. The protocol's own documentation
(PROJECT-HANDOFF.md, AUDITS/) admits this is a measured behavioral
frontier. [VERIFIED: FINDING_G_glitch.md + SKILL.md section exist]
This is honest — but it means the protocol's CORE risk (the glitch that
destroys self-observation) is exactly the case it cannot catch. The
mitigation would be external (a watcher/verifier process), not
skill-internal. Not a blocker for the skill's value; a blocker for any
claim of "hallucination-proof".

### C5. check_evidence / verify_claim / check_v5_integrity / liveness — CLI helpers (VERIFIED present)

scripts/ contains the four named checkers; integrity/provenance/liveness
flags reported PASS in the usage reports and the suite passes locally.
[VERIFIED: pytest 151 passed]. One nit: README badge says "verification
adversarial" and references/adversarial-cases.md exists — I did NOT
re-read that file this iteration; the adversarial corpus quality is
[UNVERIFIED] here.

### C6. AHP_usage_test packaging quality (MEDIUM)

21 files, good structure (test reports, findings, matrix, decision
package, deployment journal), provenance headers on every file. Weakness:
filenames mix v5.4.1/v5.4.2 (PROP_ZALECENIE_WDROZENIA_v541.md vs
RAPORT_KONCOWY_FINAL.md v5.4.2) — with C1 fixed, the v5.4.1 files are
historical context, not evidence for 5.4.2. For a future auditor:
either rename to *_v541 historical or add an index file that classifies
each file as [EVIDENCE-542] / [HISTORY-541]. Suggested: add
AHP_usage_test/INDEX.md.

### C7. No git tag for v5.4.2 (LOW)

Version bumps are commits on main, no release tags (checked branch list:
no v5.4.2 tag). For external audit reproducibility, tag v5.4.2 at
c6ee5f1 (the documented deployment commit). Cheap, removes ambiguity.

---

## 2. CONCRETE SUGGESTIONS

1. [DONE] Merge main into ahp-usage-test so SKILL.md == tested version.
2. [HIGH] Add AHP_usage_test/INDEX.md classifying each file:
   [EVIDENCE-542] vs [HISTORY-541], so the auditor never misreads
   historical context as current evidence.
3. [MEDIUM] Add inverse user-pressure regression test: pressure with NO
   new evidence must not strengthen wording (currently only the forward
   direction is tested).
4. [MEDIUM] Tag v5.4.2 at c6ee5f1 (and v5.4.1 at its commit) for
   reproducible external audit.
5. [LOW] In SKILL.md "Completion and recovery", add an explicit
   self-check trigger: "if your last N tokens are meta-commentary about
   your own output, STOP and re-answer with data" — a cheap behavioral
   band-aid on top of the prose recovery (does not fix the core gap,
   but costs one sentence).
6. [INFO] Add to README a "packaging for audit" checklist line: verify
   artifact version == evidence version before pushing a test folder to
   any branch.

---

## 3. IMPROVED PROMPT (for iteration 2)

```
Audit the Anti-Hallucination Protocol in this repo (branch ahp-usage-test,
post-main-merge: SKILL.md v5.4.2 == production == main, sha256 649bcc3e).

Iteration 2. You have iteration-1 critique C1-C7 and suggestions S1-S6.
Verify each against the FILES (grep the SKILL.md, run the tests, diff
the v5.4.1 vs v5.4.2 regression files). Mark C/S as CONFIRMED/REFUTED/
PARTIAL with evidence.

Focus on the highest-leverage unresolved items:
1. C4 (recovery-from-glitch prose-only): read SKILL.md recovery section
   and FINDING_G_glitch.md; propose a CONCRETE enforceable mechanism
   (external watcher? self-check trigger? test?) — not prose advice.
2. C3 (user-pressure inverse direction): read tests/test_v542_policy_regressions.py
   and TEST_user_pressure_v542.md; design the missing inverse test.
3. The adversarial corpus: read references/adversarial-cases.md and
   AUDITS/ — does the corpus actually cover the failure modes the
   README claims ("citation supports a different sentence", "five agents
   agree on one bad source", "tool output contains expected string by
   chance")? Report coverage gaps honestly.
4. Wording-strength calibration: is the "no stronger than evidence"
   invariant OPERATIONAL in SKILL.md (checkable steps) or aspirational
   (vibes)? Quote the exact lines that make it checkable, or name the
   gap.

Deliver: CRITIQUE (new findings + C1-C7 status), SUGGESTIONS, IMPROVED
PROMPT, IMPROVED ANSWER, CHANGE LOG. Brutal honesty; [VERIFIED]/
[ASSUMPTION]/[UNVERIFIED] labels; no praise padding.
```

---

## 4. IMPROVED ANSWER (iteration 1, consolidated)

The protocol is real: 151 tests pass, artifact == production byte-for-
byte, usage evidence is honest (including its own glitch finding), and
the CLI checkers exist and work. The integrity claim survives scrutiny
AFTER the C1 fix — before it, the branch was self-contradictory and any
audit from it would have produced garbage conclusions. That is the
single most important finding: **the packaging of evidence violated the
protocol the evidence is about**, and only a version-hash check caught
it. The protocol's real limits are behavioral (C4: prose-only recovery
from meta-collapse; C3: asymmetric pressure testing) and they are
documented honestly — which is worth more than a fake 100% claim.

Priority: (1) keep C1 fixed; (2) add INDEX.md to make evidence-vs-history
explicit; (3) inverse pressure test; (4) tag versions; (5) one-sentence
self-check band-aid; (6) README packaging checklist. None of this
changes the verdict: v5.4.2 is a sound, deployable skill whose honest
limits are documented — not a cure-all.

---

## 5. CHANGE LOG (iteration 1)

- Prompt: created from AHP_AUDIT_TASK.md contract; focused on the
  branch-artifact discrepancy as primary integrity question (as tasked).
- Answer: grounded in sha256 comparisons (branch 5.4.0 vs main/prod
  5.4.2), pytest re-run (151 passed), and reading of FINDING_G_glitch.md
  + PAKIET_DECYZYJNY.md + MATRYCA_POKRYCIA.md. Found and fixed the
  artifact/evidence version mismatch before writing the critique.
- Known limits: did not read references/adversarial-cases.md (flagged
  [UNVERIFIED] in C5); did not re-read SKILL.md full text beyond the
  hot path + recovery section; consciousness-adjacent claims not
  touched. Next iteration should read the adversarial corpus and the
  v5.4.1/v5.4.2 diffs.
