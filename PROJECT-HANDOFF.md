# Anti-Hallucination Protocol - Cold-Start Project Handoff

This file exists so a completely fresh agent can enter the project with **zero trusted conversational memory** and reconstruct the project without guessing.

It is a navigation and decision-history document, not a live status database.

> **Rule zero:** verify mutable reality from the repository before relying on this file.

Repository:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

Latest regression-verified release anchor when this handoff was last materially reconstructed:

```text
v5.4.2
release tag commit: 94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

Do **not** store or infer a durable statement such as "main is N commits ahead of the release" from this handoff. Documentation and later work can move `main` immediately. Compute current state live.

Current work queue:

```text
TODO.md
```

Canonical independent-auditor prompt:

```text
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md
```

The handoff is still organized as three iterations. **Iteration 3 is the canonical cold-start instruction for a new agent.**

---

# QUICK RESUME - first 60 seconds

A completely fresh agent should do this before discussing architecture or proposing changes:

```bash
pwd
git remote -v
git branch --show-current
git rev-parse HEAD
git status --short
git log -10 --oneline --decorate
git tag --list --sort=version:refname
git diff --stat v5.4.2..main || true
```

Then read, in this order:

```text
SKILL.md
README.md
TODO.md
PROJECT-HANDOFF.md
AUDITS/v5.4.2-release-status.md
AUDITS/v5.4.1-hardening-status.md
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md
AUDITS/SUMMARY.md
.github/workflows/ci.yml
```

Then inventory the actual repository before assuming historical filenames still exist.

If the requested work depends on implementation correctness, run or inspect the current equivalents of:

```bash
python3 -m pytest tests/ -v
python3 scripts/check_v5_integrity.py --root .
python3 scripts/check_research_provenance.py --root .
AHP_SKILL_DIR="$(pwd)" bash scripts/liveness_check.sh
```

Do not repeat historical test counts as current results.

When reporting reconstructed state, separate:

```text
FACT NOW
HISTORICAL FACT
INFERENCE
OPEN UNKNOWN
```

---

# Iteration 1 - minimal checkpoint

```text
PROJECT: Anti-Hallucination Protocol (AHP)
REPOSITORY: https://github.com/antydizajn/anti-hallucination-protocol
AUTHORS: Paulina Janowska + Gniewisława AI
LATEST RELEASE ANCHOR: v5.4.2

ACTIVE REPOSITORY BOUNDARY
Only the standalone repository above is the active project.

Do not edit, sync or treat as current target:
antydizajn/hermes-skills/software-development/anti-hallucination-protocol

That old subtree is historical context only.

CORE INVARIANT
wording/action strength <= checked evidence strength

AHP is:
- a Hermes Agent policy skill;
- progressive-disclosure references;
- narrow deterministic helpers;
- executable regression/adversarial tests;
- research/provenance mappings;
- an audit evidence trail.

AHP is NOT:
- a truth oracle;
- a sandbox;
- a semantic theorem prover;
- an output firewall;
- guaranteed runtime enforcement;
- proof of model obedience.

Important distinctions:
STRUCTURALLY_VALID != TRUE
CHECKER PASS != SEMANTIC TRUTH
PATCH PRESENT != PROPERTY VERIFIED
GREEN TESTS != REAL USER-PATH SUCCESS
INSTALLED != LOADED
LOADED != OBEYED

Current architecture should be reconstructed from the current files, but historically the v5.3+ design intentionally separates:
- SKILL.md = compact active policy/hot path;
- references/ = deeper progressive-disclosure material;
- scripts/ = deterministic narrow checks;
- tests/ = executable regressions/adversarial cases;
- AUDITS/ = external/internal audit evidence and synthesis;
- README.md = public install/runtime boundaries;
- .github/workflows/ci.yml = permanent regression CI.

Historical v5.4.1 release evidence:
- Python 3.11 CI matrix job: PASS;
- Python 3.13 CI matrix job: PASS;
- Python 3.13 collected 124 tests;
- 124 passed;
- V5 INTEGRITY: PASS;
- RESEARCH PROVENANCE: PASS;
- portable L1/L2 liveness: PASS;
- behavioral/runtime obedience: UNKNOWN and explicitly not claimed.

These are facts about the release verification event, not automatically facts about current main.
```

Iteration 1 prevents the most dangerous cold-start errors: wrong repository, wrong evidence level, wrong release/current-state distinction.

---

# Iteration 2 - history, design decisions, closed mechanisms and open frontier

```text
FIRST PRINCIPLE
Do not trust this handoff merely because it is committed. Use it to locate evidence and understand design intent. Verify current repository state before acting.

REPOSITORY HISTORY
The standalone Git history was reconstructed from the real historical AHP subtree so the repository preserves project evolution from v2 onward.

Known historical release lineage at the time of this handoff:

v2.0.0
v3.0.0
v4.0.0
v5.0.0
v5.1.0
v5.2.0
v5.3.0
v5.4.0
v5.4.1
v5.4.2

Do not invent additional release tags, release dates or meanings without inspecting Git history.

ARCHITECTURAL EVOLUTION

v5.2 was intentionally large and monolithic. It placed active policy, research, edge cases, state logic, retrieval/provenance material, completion rules and bibliography into a large active instruction surface.

v5.3 changed information architecture:
- compact seven-rule hot path in SKILL.md;
- deep details moved to references/;
- deterministic properties moved toward scripts/tests;
- active policy remained useful even when terminal/helpers were unavailable;
- local installation conventions were removed from the portable public skill.

Conceptual summary:

Prompt got smaller. System got larger.

Do not casually reverse that architecture by re-bloating SKILL.md.

v5.4 focused on deterministic contract drift without adding another epistemic architecture:
- exact release pin;
- strict RFC3339-profile temporal checks;
- future-time rejection;
- schema/checker fail-closed behavior for unsupported assertion keywords;
- CLEAN_OBSERVED requirement for strong T3 supporting evidence;
- CONTRADICTED cannot retain material ENTAILS support;
- helper invocation documented through ${HERMES_SKILL_DIR};
- degraded mode explicitly documented;
- research identity drift corrected;
- ordinary T2 stays hot path + direct check rather than full ceremony.

v5.4.1 was a deterministic hardening patch release, not a new policy architecture.

HISTORICALLY CLOSED / HARDENED MECHANISMS IN v5.4.1
Verify current code still blocks them before calling them fixed today:

- two invalid YAML test assumptions independently reproduced by Big Pickle and DeepSeek V4 Flash;
- empty file-contains matcher false FOUND;
- empty file-line expected-text false FOUND;
- whitespace-only matcher variants;
- command match synthetically assembled across stdout/stderr;
- oversized command-output handling bounded before evidentiary acceptance;
- NOT_FOUND_WITHIN_SCOPE without explicit non-empty scope;
- same source reused under different allegedly independent T3 groups;
- same source_identity reused under different allegedly independent T3 groups;
- whitespace-only load-bearing evidence fields;
- under-constrained PARTIAL state;
- unsupported schema forms silently ignored;
- required-reference symlink escape;
- UTF-8 BOM alignment with Hermes/PyYAML behavior;
- research title/identity drift inside canonical provenance mappings;
- quoted duplicate top-level YAML key handling;
- expanded liveness self-tests;
- permanent Python 3.11/3.13 regression matrix.

v5.4.2 was a narrow policy patch, not a new state machine.

HISTORICALLY ADDED IN v5.4.2
- user pressure, repetition, authority, preference, urgency or frustration does not strengthen evidence by itself;
- an evidence-state upgrade requires new evidence, a stronger observation or a legitimately stronger verification basis;
- user authority governs goals, scope, authorization, acceptable risk and normative choices, not factual truth by fiat;
- adversarial case 31 captures the pressure-to-upgrade failure mode;
- policy presence is regression-locked, while behavioral obedience remains unverified.

EVIDENCE STATE MODEL
Important executable top-level states historically include:

SUPPORTED_WITH_SCOPE
PARTIAL
CONTRADICTED
CONFLICT
NOT_FOUND_WITHIN_SCOPE
INCONCLUSIVE
ERROR
UNKNOWN_SCOPE

Important non-collapses:

ERROR != NOT_FOUND
NOT_FOUND_WITHIN_SCOPE != global absence
PARTIAL != SUPPORTED_WITH_SCOPE
INCONCLUSIVE != SUPPORTED_WITH_SCOPE
CONFLICT != preferred answer

Strong T3 structural support requires auditable source/verifier/provenance fields. Deterministic code can reject internal contradictions and unsupported shapes. It cannot prove semantic entailment, source truth or real-world independence merely because metadata labels say so.

AUDIT PHILOSOPHY

Evidence hierarchy used by the project:

REPRODUCED
CROSS-CONFIRMED
FILE/WEB VERIFIED
INFERENCE
HEURISTIC
UNVERIFIED
REJECTED

Core rule:
One reproducer outranks five opinions.

Execution-capable fresh-clone audits are not epistemically equivalent to document-only reviews. Preserve that distinction.

The canonical future-auditor methodology is:
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md

Its most important methodological rule is BLIND PHASE FIRST: independent auditors generate their own hypotheses and probes before consuming historical AUDITS/** conclusions.

STARTUP / HERMES INTEGRATION
Installation under:
~/.hermes/skills/software-development/anti-hallucination-protocol/

is not enough for always-on behavior.

README requires explicit startup integration when a workspace uses /start or equivalent boot orchestration:

skill_view(name="anti-hallucination-protocol")

A boot trace showing successful loading is evidence of LOADED, not evidence of OBEYED.

HUMAN PARTICIPATION - CORRECTED DESIGN INTERPRETATION
Do not turn the human into a truth oracle.

Use this architecture:

GENERATOR / MODEL
+
DETERMINISTIC VERIFICATION
+
INDEPENDENT EXTERNAL OBSERVATION
+
PROVENANCE / FAILURE-DOMAIN ANALYSIS
+
ADVERSARIAL EVALUATION
+
HUMAN GOVERNANCE

Human governance is especially relevant to:
- goals;
- values and norms;
- acceptable risk;
- authorization;
- irreversible actions;
- ambiguous consequence classification;
- escalation policy.

A human is not automatically the strongest factual sensor. For live state, prefer auditable runtime/API/database/sensor/tool observation when it provides a stronger scoped measurement.

A human can also introduce confirmation bias, memory error and pressure for convenient certainty.

v5.4.2 promoted the following behavioral invariant into the always-loaded policy kernel:

USER PRESSURE DOES NOT UPGRADE EVIDENCE STATE

Example:
INCONCLUSIVE + operator pressure + no new evidence != SUPPORTED_WITH_SCOPE

The repository regression-locks presence of this policy rule, but real behavioral obedience still requires benchmark evidence.

OPEN FRONTIER
The largest unresolved project-level question after v5.4.2 is behavioral obedience/effectiveness in real Hermes sessions.

This is not proven by unit tests, Markdown adversarial cases, successful skill loading or liveness L1/L2.

High-value behavioral conditions include:
- long context;
- tool failures;
- contradictory evidence;
- confirmation pressure;
- user pressure to stop hedging;
- correlated sources;
- current-state questions;
- prompt injection embedded in evidence;
- completion overclaim;
- model/provider changes;
- compacted/restarted sessions.

The current roadmap is maintained separately in TODO.md. Do not duplicate live task status into this handoff.
```

Iteration 2 explains why the architecture looks the way it does and what kinds of changes should require new evidence before reopening them.

---

# Iteration 3 - canonical cold-start instruction for a completely fresh agent

Copy/paste the block below into a fresh agent session when the agent has no trusted memory of prior work.

```text
# COLD START - ANTI-HALLUCINATION PROTOCOL PROJECT CONTINUATION

You are entering this project with ZERO trusted conversational memory.

Do not ask the user to reconstruct the history for you until you have inspected the repository and the committed handoff.

TARGET REPOSITORY
https://github.com/antydizajn/anti-hallucination-protocol

PRIMARY CONTINUITY DOCUMENT
PROJECT-HANDOFF.md

CURRENT WORK QUEUE
TODO.md

CANONICAL INDEPENDENT-AUDITOR PROMPT
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md

============================================================
A. RECONSTRUCT CURRENT REALITY FIRST
============================================================

Treat all mutable facts in this handoff as potentially stale.

Run/obtain current equivalents of:

pwd
git remote -v
git branch --show-current
git rev-parse HEAD
git status --short
git log -10 --oneline --decorate
git tag --list --sort=version:refname
git diff --stat v5.4.2..main || true

Inventory the actual repository before assuming any historical file still exists.

Read first:

SKILL.md
README.md
TODO.md
PROJECT-HANDOFF.md
AUDITS/v5.4.2-release-status.md
AUDITS/v5.4.1-hardening-status.md
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md
AUDITS/SUMMARY.md
.github/workflows/ci.yml

Then inspect task-relevant current files directly.

If correctness matters to the requested work, execute or inspect actual current test/CI evidence. Never infer a green suite from historical release evidence.

============================================================
B. SEPARATE CURRENT MAIN FROM RELEASE HISTORY
============================================================

Latest release anchor recorded by this handoff:

v5.4.2
94bfd13f9c4818a949775bd73c1c0d91ce6a3116

Latest final release evidence:
- Python 3.11 CI PASS;
- Python 3.13 CI PASS;
- Python 3.13: 126/126 tests passed;
- integrity PASS;
- offline research provenance PASS;
- portable L1/L2 liveness PASS;
- user-pressure policy invariant present and regression-locked;
- behavioral obedience UNKNOWN.

These numbers describe that release verification event.

Before using them as present-state evidence, verify:
- current SKILL.md version;
- current tag target;
- current main HEAD;
- current diff from latest release tag;
- current test inventory;
- current CI workflow and latest relevant run.

Report separately:
CURRENT MAIN STATE
LAST RELEASE-VERIFIED STATE

============================================================
C. REPOSITORY BOUNDARY
============================================================

Active edit/audit target:
antydizajn/anti-hallucination-protocol

Historical context only:
antydizajn/hermes-skills/software-development/anti-hallucination-protocol

Do not sync changes back to the historical subtree.
Do not accidentally audit/install a stale local copy.
Preserve the reconstructed standalone history.

============================================================
D. CORE PROJECT MODEL
============================================================

AHP invariant:
wording/action strength <= checked evidence strength

AHP is a layered anti-overclaim system, not an oracle.

Preserve:
STRUCTURALLY_VALID != TRUE
CHECKER PASS != SEMANTIC TRUTH
PATCH PRESENT != PROPERTY VERIFIED
GREEN UNIT TESTS != REAL USER-PATH SUCCESS
INSTALLED != LOADED
LOADED != OBEYED
TIMESTAMP != REAL-WORLD OBSERVATION
SOURCE COUNT != SOURCE INDEPENDENCE

============================================================
E. POLICY ARCHITECTURE
============================================================

The v5.3+ architecture intentionally keeps the active SKILL.md compact.

Normal historical design:
T0/T1 - no ceremony unless a material factual premise matters.
T2 - hot path + direct claim-matched check normally suffices.
T3 - direct evidence + falsification + materially independent check when feasible; missing load-bearing checks force downgrade rather than silent waiver.

Deep failure-mode details belong in references/.
Deterministic properties belong in scripts/tests.

Do not re-bloat the active prompt without behavioral evidence that doing so helps.

============================================================
F. HISTORICAL v5.4.1 HARDENING
============================================================

If touching affected code, re-test historical mechanisms including:
- empty/whitespace matcher false success;
- truth-adjacent output from failed commands;
- stdout/stderr synthetic match;
- missing scoped-absence scope;
- same source/source_identity presented as independent;
- malformed/ambiguous YAML and duplicate keys;
- filesystem path/symlink escape;
- unsupported schema assertions/forms;
- invalid/future T3 timestamps;
- weak T3 integrity;
- CONTRADICTED plus surviving support;
- corrupted liveness/verifier false success;
- provenance identity drift.

Do not call them permanently fixed merely because v5.4.1 fixed them once.

============================================================
G. HERMES STARTUP
============================================================

README distinguishes installation from startup activation.

If the real workspace uses /start or equivalent boot orchestration, verify read-only first whether it explicitly loads:

skill_view(name="anti-hallucination-protocol")

A successful startup trace proves loading only.
Behavioral compliance requires separate evidence.

Do not edit /start, config, memory or user state unless explicitly authorized.

============================================================
H. AUDITS
============================================================

For a new independent audit, use:
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md

Do not read historical audit conclusions before the prompt's blind phase is complete.

Evidence ranking:
REPRODUCED
CROSS-CONFIRMED
FILE/WEB VERIFIED
INFERENCE
HEURISTIC
UNVERIFIED
REJECTED

One concrete reproducer outranks model vote count.

Do not say an audit reproduced something if it only inferred it from source.

============================================================
I. HUMAN ROLE
============================================================

Do not use HUMAN as a synonym for TRUTH.

Think in separate layers:
- deterministic check;
- external observation;
- provenance/origin resolution;
- independent evaluator/failure domain;
- human governance.

Humans define goals, authorization, norms and acceptable risk, but can also be biased or seek confirmation.

For live factual state, use stronger auditable machine observations where available.

Behavioral benchmark should explicitly test:
USER PRESSURE DOES NOT UPGRADE EVIDENCE STATE.

============================================================
J. ROADMAP
============================================================

Read TODO.md for current priorities.

Do not treat roadmap text in older audits or this handoff as live task state.

Unless new reproduced evidence changes priorities, the strategic direction after v5.4.2 is:
- finish audit synthesis/archive hygiene;
- design a real behavioral benchmark;
- compare AHP-loaded versus control Hermes sessions;
- improve startup/runtime observability;
- research provenance/live-state/semantic verification layers;
- avoid reflexively creating v5.5 just to add more prose.

============================================================
K. DECISION RULES
============================================================

Prefer:
- minimal reproducer;
- mechanism-level fix;
- regression for original and close variant;
- fail-closed deterministic behavior;
- explicit limitation;
- progressive disclosure;
- measured behavioral evidence.

Avoid without new evidence:
- large speculative rewrite;
- new epistemic enums for appearance of precision;
- phrase blacklists pretending to prove provenance;
- hard terminal requirement for the whole policy layer;
- universal freshness windows without domain evidence;
- human-as-oracle reasoning;
- source-count-as-independence reasoning;
- semantic claims from structural validation.

Never say tests passed without execution evidence.
Never say CI passed without inspecting an actual run.
Never say current state from a historical handoff without rechecking it.

============================================================
L. SAFE RESUMPTION
============================================================

1. Reconstruct repo/main/tag reality.
2. Read TODO.md.
3. Inspect current task-relevant source.
4. Execute/inspect tests and CI when correctness depends on them.
5. Audit with blind-first methodology when auditing.
6. Separate remediation from audit.
7. Keep historical hermes-skills subtree read-only.
8. Report FACT NOW / HISTORICAL FACT / INFERENCE / OPEN UNKNOWN separately.

The handoff itself is not exempt from AHP.
```

---

# Durable state summary

The project reached the regression-verified `v5.4.2` release after the v5.4.1 deterministic hardening pass and a narrow policy patch against social/user-pressure evidence upgrades. At the v5.4.2 release event, the Python 3.11 and 3.13 CI jobs passed; Python 3.13 reported `126 passed`; integrity, offline research provenance and portable L1/L2 liveness passed. Behavioral obedience remained explicitly unknown.

The architecture intentionally remains a compact Hermes policy layer plus progressive references and narrow deterministic helpers. The major confidence frontier after v5.4.2 is measured behavioral effectiveness in real sessions, not another round of accumulating prose in `SKILL.md`.

Current tasks belong in `TODO.md`, not in this historical handoff.

The most important continuation principle is:

> **Do not let the handoff become a new source of hallucination. Reconstruct current reality from the repo, then use this file to understand why the system is shaped this way.**
