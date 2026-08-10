# AHP AUDIT TASK — GPT-5.6-SOL (10-iteration protocol)

Repo: antydizajn/anti-hallucination-protocol | Branch: ahp-usage-test
Prepared by: Gniewislawa (Hermes), 2026-08-10
Companion artifact: AUDIT_ITERATIONS/ (this folder)

---

## What is being audited

The Anti-Hallucination Protocol skill (SKILL.md, version on this branch:
5.4.0; version on main: 5.4.2; version installed in Hermes production:
5.4.2) — plus the real-usage evidence collected in AHP_usage_test/
(21 files: test reports, findings, coverage matrix, decision package,
deployment journal).

## Critical context the auditor MUST check first (discrepancy)

AHP_usage_test/ documents testing and deployment of **v5.4.2**
(RAPORT_KONCOWY_FINAL.md: "main, v5.4.2", commit c6ee5f1, sha256
649bcc3e, 126/126 tests PASS). However the SKILL.md checked out on THIS
branch (ahp-usage-test) is **v5.4.0** — the branch was cut before the
v5.4.2 changes landed on main (main HEAD b021bcf9, SKILL.md version
5.4.2). Verify: does AHP_usage_test/ describe behavior of 5.4.0 or 5.4.2?
Any claim in the test reports that references v5.4.2 specifics must be
re-checked against the 5.4.0 file present here. This is itself a test of
the protocol: evidence vs label.

## Scope of the audit

1. SKILL.md (this branch, v5.4.0): hot path rules, evidence definition,
   claim-matched evidence, wording-strength calibration, failure modes,
   limitations. Is the policy coherent? Self-consistent? Enforceable?
2. The 7 hot-path rules and the "what exactly earned this wording?"
   question: are they operational or aspirational?
3. AHP_usage_test/ findings: FINDING_G_glitch.md (recursive meta-collapse,
   prose-only recovery), FINDING_caveman_vs_AHP.md, FINDING_long_session_drift.md,
   FINDING_output_discipline_vs_AHP.md, MATRYCA_POKRYCIA.md,
   PAKIET_DECYZYJNY.md, DZIENNIK_WDROZENIA_v542.md, RAPORT_*.
4. The v5.4.0 vs v5.4.2 gap: what changed between them (if 5.4.2 files
   are reachable on main, diff them) and whether the usage evidence
   applies to the audited artifact at all.
5. scripts/ + tests/ + references/ in the repo root: do the deterministic
   helpers (check_evidence, verify_claim, check_v5_integrity, liveness)
   actually enforce what SKILL.md claims?

## Deliverable format per iteration

1. CRITIQUE — what is wrong, weak, risky, missing, or over-claimed.
2. CONCRETE SUGGESTIONS — numbered, actionable (file/line/mechanism),
   with rationale.
3. IMPROVED PROMPT — the next audit prompt (you improve the prompt each
   iteration too).
4. IMPROVED ANSWER — your improved audit answer for this iteration.
5. CHANGE LOG — what you changed in prompt and answer, and why.

## 10-iteration protocol (MANDATORY)

- Iteration 1: read SKILL.md + AHP_usage_test/ + repo helpers/tests,
  produce first audit, save to `AUDIT_ITERATIONS/iter_01.md`.
- Iterations 2-10: take previous iteration's prompt and answer, improve
  BOTH (prompt: more precise/higher signal; answer: deeper/better
  structured/more actionable), re-run, save `iter_0N.md`.
- Each file MUST be self-contained: full prompt + full answer inside.
- After iteration 10: `AUDIT_ITERATIONS/FINAL_SYNTHESIS.md` — best
  prompt + best answer + top surviving changes with rationale.

## Rules

- Brutal honesty. No praise padding. Critique > agreement.
- Every suggestion actionable (what file/line/mechanism changes).
- Label [VERIFIED] (with evidence) vs [ASSUMPTION] vs [UNVERIFIED].
- If something is already correct, say so briefly — do not invent
  problems to fill space.
- The v5.4.0/v5.4.2 discrepancy is a primary integrity question — start
  there, resolve it explicitly, and report whether the usage-test
  evidence in this repo is evidence for the artifact in this repo.
