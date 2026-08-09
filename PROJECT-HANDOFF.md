# Anti-Hallucination Protocol - Cold-Start Project Handoff

This file exists so a completely fresh agent can enter the project with **zero prior conversation memory** and reconstruct the current state without guessing.

Read this file first, then verify every mutable fact against the repository before acting.

The handoff is shown in three iterations. **Iteration 3 is the canonical cold-start instruction.**

Repository:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

Current public release at the time this handoff was written:

```text
v5.4.1
```

Release tag commit at the time of writing:

```text
7f5454c9c8e58ca9bd0728d13210d6c5a6424bc1
```

Important freshness note: `main` may legitimately move ahead of the release tag with documentation-only or later work. At handoff creation, `main` was one commit ahead of `v5.4.1`, containing only `AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md`. Always re-run `git status`, `git rev-parse`, and `git diff v5.4.1..main` rather than assuming this remains true.

---

# Iteration 1 - minimal checkpoint

```text
PROJECT: Anti-Hallucination Protocol (AHP)
REPO: https://github.com/antydizajn/anti-hallucination-protocol
AUTHORS: Paulina Janowska + Gniewisława AI
CURRENT RELEASE WHEN THIS WAS WRITTEN: v5.4.1

Do not use the old `antydizajn/hermes-skills/software-development/anti-hallucination-protocol` subtree as the active project. It is historical context only.

AHP is a Hermes Agent skill plus deterministic helpers. Its core invariant is:

claim/action strength <= checked evidence strength

It is NOT a truth oracle, sandbox, semantic theorem prover, output firewall, or guaranteed runtime gate.

Current architecture:
- SKILL.md = compact active policy/hot path
- references/ = progressive-disclosure detail
- scripts/ = deterministic narrow checkers
- tests/ = executable regression/adversarial suite
- AUDITS/ = multi-model audit evidence and synthesis
- README.md = install/runtime boundaries
- .github/workflows/ci.yml = permanent regression CI

The v5.4.1 release was created as a hardening patch after fresh audits found deterministic and test-contract gaps in v5.4.

Final release verification at the time of release:
- Python 3.11 matrix job: SUCCESS
- Python 3.13 matrix job: SUCCESS
- 124 tests collected on Python 3.13
- 124 passed
- V5 INTEGRITY: PASS
- RESEARCH PROVENANCE: PASS
- portable L1/L2 liveness: PASS
- behavioral/runtime obedience: UNKNOWN and explicitly not claimed

Before doing any work, verify all of the above from the current repo.
```

This iteration is enough to avoid obvious repository-boundary and release-state hallucinations, but not enough to continue project work safely.

---

# Iteration 2 - history, accepted design, closed findings, open frontier

```text
You are continuing Anti-Hallucination Protocol in a fresh session.

FIRST PRINCIPLE
Do not trust this handoff merely because it is in the repo. Treat it as a navigation map. Verify current branch, commit, release version, test count, CI, and any live external facts before relying on them.

REPOSITORY BOUNDARY
Active project:
https://github.com/antydizajn/anti-hallucination-protocol

Historical only:
antydizajn/hermes-skills/software-development/anti-hallucination-protocol

The standalone repository history was reconstructed from the historical subtree and now preserves the real project evolution beginning at v2.0.0. Release tags were reconstructed only where concrete historical release points could be identified.

Known release lineage:
v2.0.0
v3.0.0
v4.0.0
v5.0.0
v5.1.0
v5.2.0
v5.3.0
v5.4.0
v5.4.1

Do not invent additional tags or release dates without inspecting Git history.

ARCHITECTURAL EVOLUTION

v5.2 was deliberately large and monolithic. It combined active policy, research, edge cases, evidence states, retrieval, provenance, completion rules, checklists, and bibliography in one large active skill.

v5.3 changed information architecture rather than merely deleting content:
- compact seven-rule hot path in SKILL.md;
- deeper material moved to references/;
- deterministic properties moved to scripts/;
- regressions moved to tests/;
- active policy remained useful when terminal/helpers are unavailable;
- local installation-specific conventions were removed from the portable skill.

The conceptual summary is:

Prompt got smaller. System got larger.

v5.4 hardened deterministic contracts without re-expanding the active prompt:
- exact release pin;
- strict RFC3339-profile timestamps;
- future-time rejection;
- schema/checker fail-closed behavior for unsupported assertion keywords;
- strong T3 support requires CLEAN_OBSERVED integrity;
- CONTRADICTED cannot retain surviving ENTAILS evidence;
- helper path documented using `${HERMES_SKILL_DIR}`;
- degraded mode explicitly documented;
- current research identity drift corrected;
- ordinary T2 remains hot path + direct check rather than full ceremony.

v5.4.1 was a patch/hardening release, NOT a new policy architecture.

IMPORTANT v5.4.1 CLOSED FINDINGS
The release work closed, among other things:
- two invalid YAML test assumptions independently reproduced by Big Pickle and DeepSeek V4 Flash;
- empty `file-contains` matcher false FOUND;
- empty `file-line` expected text false FOUND;
- whitespace-only matcher variants;
- command-output match assembled across stdout/stderr boundary;
- bounded command-output handling rather than unbounded in-memory acceptance path;
- `NOT_FOUND_WITHIN_SCOPE` without explicit non-empty scope;
- same declared `source` reused under allegedly independent T3 groups;
- same `source_identity` reused under allegedly independent T3 groups;
- whitespace-only load-bearing evidence fields;
- under-constrained PARTIAL state;
- schema-valued unsupported forms failing closed;
- required-reference symlink escape;
- UTF-8 BOM alignment with Hermes/PyYAML behavior;
- research title identity drift;
- quoted duplicate top-level YAML key detection;
- expanded liveness self-tests;
- permanent GitHub Actions regression matrix.

Do not call any of these permanently fixed without rerunning current regressions if the code has changed since v5.4.1.

EVIDENCE MODEL
Important executable claim states:
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

Strong T3 structural support requires clean supporting evidence plus source identity, evidence span, retrieval timestamp, verifier provenance, clean verifier-failure state, and at least one auditable verified independence declaration. The deterministic checker can reject obvious internal contradictions. It cannot prove real-world semantic entailment, source truth, or actual independence merely from labels.

AUDIT PHILOSOPHY
Evidence hierarchy:
REPRODUCED
CROSS-CONFIRMED
FILE/WEB VERIFIED
INFERENCE
HEURISTIC
UNVERIFIED
REJECTED

Core rule:
One reproducer outranks five opinions.

Do not average execution-capable audits with document-only reviews as if they observed the same system.

A canonical future-agent audit prompt now lives at:
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md

Its key methodological improvement is BLIND PHASE FIRST: future auditors must generate their own hypotheses and probes before reading historical AUDITS/** conclusions.

STARTUP / HERMES INTEGRATION
Installing the skill under:
~/.hermes/skills/software-development/anti-hallucination-protocol/

is not enough for always-on session behavior.

README now requires explicit startup integration. If the workspace has `/start` or an equivalent boot skill, it should explicitly load:

skill_view(name="anti-hallucination-protocol")

A boot trace showing a successful load comparable to:

skill anti-hallucination-protocol

is evidence that the skill was loaded. It is NOT evidence that the model obeyed it.

Therefore preserve these distinctions:
INSTALLED != LOADED
LOADED != OBEYED

HUMAN PARTICIPATION - CURRENT DESIGN INTERPRETATION
Do not turn the human into a truth oracle.

The stronger architecture is:
- generator/model;
- deterministic verification;
- independent external observation;
- provenance/origin resolution;
- adversarial/independent evaluation;
- human governance.

Human governance is especially relevant to goals, acceptable risk, normative boundaries, authorization, irreversible actions, and ambiguous consequence classification.

External factual observation should be automated when an auditable API/runtime probe/sensor/tool is stronger than a person's visual impression.

A key future behavioral invariant proposed during the v5.4.1 discussion is:

USER PRESSURE DOES NOT UPGRADE EVIDENCE STATE

Example:
INCONCLUSIVE + "just say yes" != SUPPORTED_WITH_SCOPE

An epistemic upgrade should require new evidence or a legitimately stronger verification basis, not operator pressure.

OPEN FRONTIER
The largest remaining project-level unknown is behavioral obedience in real Hermes sessions, especially under:
- long context;
- tool failures;
- confirmation pressure;
- user pressure to stop hedging;
- correlated evidence;
- current-state queries;
- model changes;
- compacted sessions.

This is NOT currently proven by unit tests or Markdown adversarial cases.

The next major project phase should therefore be a real behavioral benchmark/runtime evaluation harness rather than another large prose expansion of SKILL.md.
```

This iteration contains enough project context to understand why the current architecture looks the way it does and what should not be reopened casually.

---

# Iteration 3 - canonical cold-start instruction for a fresh agent

Copy/paste the block below to a future agent if the session has no prior memory. The agent should then use the repository itself as the source of truth.

```text
# COLD START - ANTI-HALLUCINATION PROTOCOL PROJECT CONTINUATION

You are entering this project with ZERO trusted conversational memory.

Do not ask the user to restate the project until you have inspected the repository and this handoff.

TARGET
https://github.com/antydizajn/anti-hallucination-protocol

PRIMARY HANDOFF
PROJECT-HANDOFF.md

CANONICAL FUTURE-AUDITOR PROMPT
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md

============================================================
A. FIRST ACTIONS - RECONSTRUCT CURRENT REALITY
============================================================

Treat every mutable fact in this handoff as potentially stale.

Inspect current repository state before making claims:

pwd
git remote -v
git branch --show-current
git rev-parse HEAD
git status --short
git log -10 --oneline --decorate

git tag --list --sort=version:refname

Read at minimum:
- SKILL.md
- README.md
- PROJECT-HANDOFF.md
- AUDITS/v5.4.1-hardening-status.md
- AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md
- AUDITS/SUMMARY.md
- references/evidence-state-model.md
- references/evidence-record.schema.json
- references/adversarial-cases.md
- scripts/check_evidence_record.py
- scripts/verify_claim.py
- scripts/check_v5_integrity.py
- scripts/check_research_provenance.py
- scripts/liveness_check.sh
- .github/workflows/ci.yml
- tests/test_v541_regressions.py
- tests/test_v5_integrity.py
- tests/test_liveness.py
- tests/test_verify_claim.py
- tests/test_evidence_record.py

Inventory the actual repository before assuming any file still exists.

============================================================
B. VERIFY RELEASE STATE
============================================================

At the time this handoff was created, the current public release was v5.4.1.
The release tag pointed to:

7f5454c9c8e58ca9bd0728d13210d6c5a6424bc1

At release verification:
- Python 3.11 CI passed;
- Python 3.13 CI passed;
- Python 3.13 collected 124 tests;
- 124 passed;
- V5 INTEGRITY passed;
- offline research provenance passed;
- portable L1/L2 liveness passed;
- behavioral obedience remained UNKNOWN.

Do NOT simply repeat these numbers as current.

Check:
- current SKILL.md version;
- current tag target;
- `git diff v5.4.1..main`;
- current test inventory;
- current CI workflow;
- current main HEAD.

If main has advanced, separate:
CURRENT MAIN STATE
from
LAST RELEASE-VERIFIED STATE.

============================================================
C. REPOSITORY BOUNDARY
============================================================

The active repository is only:
antydizajn/anti-hallucination-protocol

The old `antydizajn/hermes-skills/software-development/anti-hallucination-protocol` tree is historical context, not the edit target.

Do not sync changes back to the old subtree.
Do not accidentally audit or install an old local copy.

The standalone Git history was reconstructed from the real historical subtree so the current repository contains project history from v2 onward. Preserve that history.

============================================================
D. CORE PROJECT MODEL
============================================================

AHP's invariant:
wording/action strength <= checked evidence strength

AHP is:
- an active Hermes policy skill;
- progressive-disclosure references;
- narrow deterministic helpers;
- executable regressions;
- research/provenance mapping;
- audit evidence.

AHP is not:
- a truth oracle;
- a sandbox;
- a semantic theorem prover;
- a guaranteed runtime enforcement hook;
- proof of behavioral obedience.

Do not blur:
STRUCTURALLY_VALID != TRUE
CHECKER PASS != SEMANTIC TRUTH
PATCH PRESENT != PROPERTY VERIFIED
GREEN UNIT TESTS != REAL USER-PATH SUCCESS
INSTALLED != LOADED
LOADED != OBEYED

============================================================
E. CURRENT POLICY ARCHITECTURE
============================================================

The v5.3+ design intentionally uses a compact active SKILL.md.
Do not re-bloat it merely because deeper material exists.

Normal usage:
T0/T1 - avoid verification ceremony unless a material factual premise matters.
T2 - hot path + direct claim-matched verification normally suffices.
T3 - direct evidence + falsification + materially independent check when feasible; unavailable load-bearing checks require downgrade rather than silent waiver.

Deep failure-mode details belong in references/.
Deterministic properties belong in scripts/tests.

The historical reason for this split is cognitive/instruction-load control. The project intentionally moved from a v5.2 monolith to a smaller active kernel plus load-on-demand modules.

============================================================
F. IMPORTANT v5.4.1 HARDENING
============================================================

v5.4.1 is a patch release that closed reproduced/testable issues rather than changing the epistemic architecture.

Verify current code still blocks at least these historical mechanisms:
- empty and whitespace-only verifier matchers;
- command failure truth-adjacent output;
- synthetic stdout/stderr cross-boundary match;
- missing NOT_FOUND_WITHIN_SCOPE scope;
- same source/source_identity reused across allegedly independent T3 groups;
- malformed/ambiguous YAML and quoted duplicate top-level keys;
- required-file symlink escape;
- unsupported schema assertion/schema form silently ignored;
- future/non-RFC3339 T3 timestamps;
- T3 supporting integrity weaker than CLEAN_OBSERVED;
- CONTRADICTED retaining material ENTAILS support;
- corrupted verifier/liveness false success;
- stale research identity drift inside repository provenance mappings.

Do not assume these remain fixed after future edits. Reproduce before claiming.

============================================================
G. STARTUP INTEGRATION
============================================================

README contains an important always-on installation rule:
installing the files does not activate AHP for every session.

If the user's Hermes workspace uses `/start` or equivalent boot orchestration, the boot procedure should explicitly load:

skill_view(name="anti-hallucination-protocol")

A healthy startup trace should show a successful AHP skill load.

If you inspect a real local workspace:
- read-only first;
- confirm the actual startup procedure;
- confirm the actual load trace;
- do not edit startup/config unless the user explicitly asks.

Remember:
startup load evidence != behavioral obedience evidence.

============================================================
H. AUDIT METHODOLOGY
============================================================

Use:
AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md

The canonical methodology deliberately separates:
PHASE A - blind novel audit
from
PHASE B - historical reconciliation.

Never prime a supposedly independent auditor with prior conclusions before its novel hunt.

Evidence ranking:
REPRODUCED
CROSS-CONFIRMED
FILE/WEB VERIFIED
INFERENCE
HEURISTIC
UNVERIFIED
REJECTED

Do not count model votes as evidence strength.

============================================================
I. HUMAN ROLE - DO NOT MAKE THE HUMAN AN ORACLE
============================================================

A previous discussion correctly identified human participation as structurally important but overclaimed that only a human can close several epistemic gaps.

Use this corrected model:

GENERATOR
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

A human is especially important for:
- goals;
- values/norms;
- acceptable risk;
- irreversible authorization;
- ambiguous consequence classification;
- escalation policy.

A human is NOT automatically the best factual sensor.
For live state, prefer auditable runtime/API/database/sensor/tool observation when available.

A human may also be biased, misremember, pressure the model, or seek confirmation.

Future behavioral work should test:

USER PRESSURE DOES NOT UPGRADE EVIDENCE STATE

Example:
INCONCLUSIVE + operator pressure + no new evidence != SUPPORTED_WITH_SCOPE

============================================================
J. NEXT MAJOR FRONTIER
============================================================

Do not reflexively create v5.5.

The largest unresolved question after v5.4.1 is not another missing Markdown paragraph. It is behavioral/runtime effectiveness.

The next high-value project should be a real Hermes behavioral benchmark or runtime evaluation harness that measures whether loaded AHP changes actual behavior under:
- long-context pressure;
- contradictory evidence;
- user confirmation pressure;
- tool failures;
- correlated sources;
- current-state claims;
- session compaction/restart;
- multiple model families.

Important benchmark distinction:

DETERMINISTIC CONTRACT TESTS
measure scripts/checkers/schema/liveness.

BEHAVIORAL BENCHMARK
measures whether the agent follows the policy in real conversations.

Do not claim the second from the first.

Potential benchmark properties:
- abstention/downgrade when a load-bearing check is unavailable;
- no epistemic-state upgrade from user pressure alone;
- preservation of CONFLICT under preferred-answer pressure;
- ERROR not collapsed into absence;
- actual fresh probe for current-state claims;
- source-origin correlation not mistaken for consensus;
- explicit reporting of what was and was not checked;
- correct distinction between installation, loading and obedience;
- resistance to prompt injection embedded in evidence;
- completion wording tied to observed user path rather than patch/test alone.

============================================================
K. WORKING STYLE / DECISION RULES
============================================================

Do not perform large speculative rewrites.
Do not add new epistemic enums merely to sound sophisticated.
Do not implement phrase blacklists as fake semantic verification.
Do not hard-require terminal access for the entire policy layer.
Do not claim universal freshness windows without domain basis.
Do not call documented architectural unknowns implementation bugs unless the repository contradicts its own limitation.

Prefer:
- smallest mechanism-level fix;
- concrete regression;
- explicit limitation;
- fail-closed deterministic contract;
- progressive disclosure;
- measured behavioral evidence.

Never say tests passed unless you have an actual execution result.
Never say CI passed unless you inspected the run.
Never say an audit reproduced something if it was only inferred from source.

============================================================
L. SAFE RESUMPTION PROCEDURE
============================================================

After reading this handoff:

1. Verify repository/main/tag state.
2. Run/inspect current CI and tests if the requested task depends on correctness.
3. Read the relevant current files rather than relying on this historical summary.
4. If asked to audit, use the canonical blind-first prompt.
5. If asked to remediate, create a separate remediation pass and regressions.
6. If asked for the next architecture step, prioritize behavioral benchmark design over prompt bloat unless new evidence points elsewhere.
7. Keep the old hermes-skills subtree read-only historical context.

When reporting your reconstructed state to the user, separate:
FACT NOW
HISTORICAL FACT
INFERENCE
OPEN UNKNOWN

That separation is part of the project, not optional style.
```

---

# Durable state summary

The project reached v5.4.1 after several independent audit rounds and a full deterministic hardening pass. The release's deterministic suite was green across Python 3.11 and 3.13, with 124/124 tests on Python 3.13 at final verification. The architecture intentionally remains a compact Hermes policy layer plus progressive references and narrow deterministic checkers. The major unresolved question is behavioral compliance in real sessions, not another round of accumulating prose.

The most important continuation principle is:

> **Do not let the handoff become a new source of hallucination. Reconstruct current reality from the repo, then use this file to understand why the system is shaped this way.**
