<div align="center">

<img src="assets/anti-hallucination-eye.svg" alt="Anti-Hallucination Protocol eye mark" width="220">

# Anti-Hallucination Protocol

**Make the agent earn the sentence.**

[![Version](https://img.shields.io/badge/version-5.4.2-black?style=flat-square)](SKILL.md)
[![Hermes Skill](https://img.shields.io/badge/Hermes-Agent-111111?style=flat-square)](https://github.com/NousResearch/hermes-agent)
[![License](https://img.shields.io/badge/license-MIT-black?style=flat-square)](#license)
[![Adversarial](https://img.shields.io/badge/verification-adversarial-black?style=flat-square)](references/adversarial-cases.md)

A Hermes Agent skill for the moment between **"this looks right"** and **"I'm going to state it as fact."**

[Install](#install) · [Failure modes](#failure-modes-it-targets) · [How it works](#how-it-works) · [Limits](#what-it-does-not-prove) · [Roadmap](TODO.md) · [External agent / no write access](EXTERNAL-CONTRIBUTOR.md)

</div>

---

## External agents and contributors

You do **not** need write access to this repository to contribute an audit, test, reproducer, documentation change or code fix.

If you are a completely fresh AI agent and received only this repository URL, start with [`AGENTS.md`](AGENTS.md). If you cannot push upstream, the canonical route is [`EXTERNAL-CONTRIBUTOR.md`](EXTERNAL-CONTRIBUTOR.md).

Minimum-friction external path:

```bash
gh repo clone antydizajn/anti-hallucination-protocol
cd anti-hallucination-protocol
python3 scripts/external_contributor.py start
# perform the selected [AGENT-READY] task
python3 scripts/external_contributor.py submit
```

The helper is designed for:

```text
PUBLIC REPO
-> NO UPSTREAM WRITE
-> FORK
-> CONTRIBUTOR BRANCH
-> LOCAL VALIDATION
-> PULL REQUEST
```

Do not request collaborator `Write` merely to submit work. A Pull Request is a proposal, not project acceptance.

---

## The problem

LLMs do not only hallucinate by inventing facts. They also fail when:

- the citation is real but supports a different sentence;
- five agents agree because all five inherited one bad source;
- a tool failed but its output happened to contain the expected string;
- yesterday's memory is reported as today's state;
- a verifier is wrong and nobody verifies the verifier.

Anti-Hallucination Protocol is a procedural layer for those failures. Its core question is:

> **What exactly earned this wording?**

If the evidence is weak, stale, contaminated, contradictory or incomplete, the wording has to weaken with it.

No ceremony for harmless creative work. More friction where being wrong actually matters.

---

## Failure modes it targets

These are design targets, not guarantees that a Markdown skill will force correct behavior in every model/runtime.

| Failure | Protocol response |
|---|---|
| Real URL, wrong claim | separate source identity from entailment |
| Copied sources posing as consensus | track lineage and independent failure domains |
| Self-declared "independence" | require auditable lineage metadata for strong T3 records, while admitting that labels do not prove real independence |
| Tool error disguised as absence | keep `ERROR` separate from `NOT_FOUND_WITHIN_SCOPE` |
| Stale current-state claim | require explicit observation time and current-enough evidence for strong T3 current-state records |
| Prompt injection inside evidence | instruct the agent to treat retrieved content as data, not instruction authority |
| User pressure upgrades certainty | evidence state may strengthen only when the evidence/observation/verification basis strengthens |
| Passing test, wrong user path | separate unit validation from E2E / observed behavior |
| Verifier false positive | treat the verifier result as another scoped claim |
| Compacted-session denial | check durable traces before claiming an earlier action never happened |

The canonical protocol attack corpus is in [`references/adversarial-cases.md`](references/adversarial-cases.md). Executable regression tests live separately under `tests/`.

---

## How it works

The active v5.4.2 skill keeps the seven-rule hot path introduced in v5.3, preserves the deterministic hardening from v5.4.1, and adds one policy invariant: user pressure alone cannot upgrade evidence state. It does not expand the evidence state machine.

The protocol models the full control flow as:

```text
INTENT
  -> DECOMPOSE
  -> CLASSIFY
  -> PLAN
  -> ACQUIRE
  -> BOUNDARY
  -> QUALIFY
  -> ENTAIL
  -> CONTRADICT
  -> DECIDE
  -> EMIT / ACT
```

That is not a mandatory ritual for every sentence. Ordinary T2 work normally uses the hot path plus a direct claim-matched check. Deeper references and helpers are for the failure modes that actually matter to the task.

Risk tiers:

| Tier | Typical work | Expected behavior |
|---|---|---|
| `T0` | preference, creative choice | no verification unless a factual premise matters |
| `T1` | stable background knowledge | verify when uncertain, disputed or decision-relevant |
| `T2` | code, APIs, repos, citations, current docs, benchmarks | direct claim-matched evidence; hot path is normally sufficient |
| `T3` | security, legal/compliance, destructive or high-impact action | direct evidence + falsification + independent check when feasible; unavailable load-bearing checks force a downgrade |

The invariant underneath all four tiers is smaller:

```text
claim strength <= evidence strength
```

---

## Evidence is not one thing

For consequential claims the protocol separates:

```text
identity
relevance
freshness
integrity
lineage
scope
entailment
verifier state
```

A source can be authoritative and stale. A citation can point to the right paper and still fail to support the attached sentence. Multiple URLs can share one origin.

For strong T3 machine-readable records, supporting evidence must be `CLEAN_OBSERVED`, and verified independent support carries `lineage_basis`, `lineage_verification` and `independence_group`. The checker detects duplicate declared groups and also rejects the obvious internal contradiction of reusing the same declared `source` or `source_identity` under different independence groups. It still cannot prove that two real sources are genuinely independent.

`NOT_FOUND_WITHIN_SCOPE` requires an explicit non-empty scope. A scoped absence verdict without a declared search boundary is not structurally valid.

Evidence state is not upgraded by confidence theatre. User repetition, authority, preference, urgency, frustration or pressure does not by itself turn `INCONCLUSIVE` into `SUPPORTED_WITH_SCOPE`. A stronger state requires new evidence, a stronger observation or a legitimately stronger verification basis.

---

## Deterministic checks

The repository includes narrow helpers for properties machines can actually check without pretending to understand the universe.

Hermes does **not** automatically turn these scripts into runtime enforcement when the skill loads. They are invoked explicitly when needed. When Hermes skill template substitution is enabled, `${HERMES_SKILL_DIR}` resolves the installed skill directory so helper calls do not depend on the current working directory.

### `verify_claim.py`

Checks filesystem facts, exact text/line conditions and command-output conditions.

```text
FOUND       exit 0
NOT_FOUND   exit 1
ERROR       exit 2
```

A failed command cannot become `FOUND` merely because its output contains the expected substring. Empty match strings are rejected instead of exploiting the fact that an empty Python string is contained in every string. Command output is matched within stdout or stderr individually, so a synthetic match cannot be assembled across the stream boundary.

### `check_evidence_record.py`

Validates [`references/evidence-record.schema.json`](references/evidence-record.schema.json) plus deterministic cross-field invariants.

For strong T3 records it checks, among other things:

- known source class;
- source identity and evidence span;
- RFC3339-profile retrieval timestamps with timezone;
- `integrity=CLEAN_OBSERVED` for supporting evidence;
- verifier provenance and clean observed verifier state;
- verified independent lineage metadata;
- non-empty `independence_group`, no duplicate declared group, and no obvious same-source/same-identity reuse across distinct declared independent groups;
- explicit RFC3339-profile observation time and `CURRENT_ENOUGH` evidence for T3 current-state claims.

The checker also rejects a canonical schema containing an assertion keyword or schema form it does not implement. Silently ignoring a future schema constraint would create a false validation path.

A successful result is:

```text
EVIDENCE RECORD: STRUCTURALLY_VALID
```

That means exactly what it says. It does **not** establish semantic entailment, source truth or real-world source independence.

### `check_v5_integrity.py`

Checks repository structure and parses `SKILL.md` frontmatter with real YAML rather than a hand-written YAML approximation. The v5.4.2 checker pins the exact public release version `5.4.2`, so a different v5 release cannot silently receive the same release-integrity PASS. Required support files are resolved inside the skill root so a symlink escape cannot satisfy the integrity contract merely by existing on disk.

### `check_research_provenance.py`

Checks offline repository-internal research identity consistency across canonical manifests/reference mappings. It does not prove that an external source is live or that a research interpretation is correct.

### `liveness_check.sh`

Checks the portable L1/L2 installation contract and exits nonzero when a required check fails. Files on disk cannot prove behavioral compliance, so that remains an explicit unknown outside this helper.

If a helper is unavailable in the active environment, the policy still applies, but deterministic validation must be reported as not performed rather than silently treated as passed.

---

## Install

Place the skill directory at:

```text
~/.hermes/skills/software-development/anti-hallucination-protocol/
```

### Mandatory startup integration

Installing the files is **not** the same thing as activating the protocol for a session. Add Anti-Hallucination Protocol to the startup/boot procedure that runs at the beginning of **every Hermes session**, before ordinary task work begins.

If your workspace uses a `/start` skill or equivalent boot skill, edit that procedure so its minimal boot explicitly loads:

```text
skill_view(name="anti-hallucination-protocol")
```

A healthy boot should visibly include a successful skill load comparable to:

```text
📚 skill  anti-hallucination-protocol
```

Load AHP alongside other baseline session controls such as identity/memory and anti-sycophancy policy. Do not rely on the skill merely existing under `~/.hermes/skills/`; if the startup log does not show that it was loaded, treat it as **installed but not active for startup**.

After wiring the startup procedure, start a completely new Hermes session and verify that AHP is loaded during boot. The exact surrounding boot sequence is workspace-specific; the invariant is that `anti-hallucination-protocol` is explicitly loaded before consequential work starts.

---

## Run the checks

From a repository checkout:

```bash
python3 -m pytest tests/ -v
python3 scripts/check_v5_integrity.py --root .
python3 scripts/check_research_provenance.py --root .
AHP_SKILL_DIR="$(pwd)" bash scripts/liveness_check.sh
```

The repository also includes GitHub Actions regression CI across supported Python test environments. A green CI run establishes only the checked executable contracts, not model obedience or semantic truth.

When the skill is loaded in Hermes and template substitution is enabled, a bundled checker can also be invoked without current-directory assumptions, for example:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/check_evidence_record.py record.json
```

`liveness_check.sh` is a Bash helper. On native Windows it requires a Bash-compatible environment such as WSL or Git Bash. The Python checks are the portable core of deterministic validation. Native Windows execution is not claimed as tested here.

The Markdown adversarial corpus is a specification, not an executable behavioral benchmark. A green unit suite does not prove that an LLM follows the protocol under long-context pressure. No behavioral obedience benchmark is claimed by this release.

---

## Research basis

The skill integrates work on factuality, retrieval, citation, uncertainty, prompt injection, memory, judge bias, long-context evidence loss and agentic failure.

The full research identity/mapping layer lives outside the main skill prompt:

- [`references/research-foundations.md`](references/research-foundations.md)
- [`references/v5-research-manifest.json`](references/v5-research-manifest.json)
- [`references/v5-gap-map.md`](references/v5-gap-map.md)

Research is evidence for design choices, not decoration and not proof that the implementation is correct. Where an arXiv paper changes title across versions, the repository should either cite the current identity or pin the exact paper version used by the design record.

---

## Audit trail

The multi-model audit corpus and synthesis are archived under [`AUDITS/`](AUDITS/).

`AUDITS/SUMMARY.md` separates execution-capable audits from document/static reviews, records conflicts and rejected severity claims, and tracks how findings were dispositioned in later releases. Auditor count is not treated as truth; reproduced failure mechanisms outrank model votes.

For a fresh independent audit, use [`AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md`](AUDITS/CANONICAL-AGENT-AUDIT-PROMPT.md). It includes five iterations of the methodology and a final blind-first copy-paste prompt for independent agents.

For a completely fresh continuation session, start with [`PROJECT-HANDOFF.md`](PROJECT-HANDOFF.md). It is a compact cold-start checkpoint covering current navigation, branch roles, trust boundaries and unresolved frontiers. Treat it as navigation, then verify current reality from the repository.

For the current post-release backlog, use [`TODO.md`](TODO.md). It separates documentation/archive hygiene, behavioral benchmarking, Hermes runtime work, provenance/live-state research, portability and release maintenance. Treat roadmap status as mutable and verify before acting.

---

## What it does not prove

This project does **not** promise zero hallucinations.

It also does not prove that:

- retrieved content is safe;
- a reputable source is correct;
- two agents or sources are independent because a record says so;
- an `INDEPENDENT_ORIGIN` lineage basis is factually correct without inspecting that basis;
- an LLM judge is unbiased;
- search was exhaustive;
- memory contains current truth;
- a passing test exercised the real user path;
- Markdown instructions were obeyed at runtime;
- a model will obey the complete protocol under long-context pressure.

Those guarantees need architecture, sandboxing, external observation, executable checks or behavioral evaluation outside the prompt.

This is a protocol for making unsupported certainty harder, not impossible.

---

## Repository map

```text
anti-hallucination-protocol/
├── README.md                             # public contract, homepage and external entrypoint
├── AGENTS.md                             # root agent navigation and capability routing
├── AGENT-BOOTSTRAP.json                  # machine-readable trusted/external router
├── AUTONOMOUS-AGENT.md                   # trusted upstream-agent workflow
├── EXTERNAL-CONTRIBUTOR.md               # zero-write fork/PR workflow
├── CONTRIBUTING.md                       # GitHub-native contributor entrypoint
├── PROJECT-MAP.json                      # machine-readable branch/path/trust map
├── PROJECT-HANDOFF.md                    # compact cold-start continuation state
├── SKILL.md                              # active Hermes policy / hot path
├── TODO.md                               # post-v5.4.2 roadmap
├── LICENSE
├── AGENT-IDENTITY/                       # optional cryptographic sender identity
├── SUBMISSIONS/                          # external machine-friendly intake
├── .github/
│   ├── agents/                           # repository custom-agent role profiles
│   └── workflows/
│       ├── ci.yml                        # Python 3.11 / 3.13 regression gate
│       ├── submission-intake.yml         # unprivileged fork-PR intake validation
│       └── submission-triage.yml         # post-merge Issue creation
├── AUDITS/
│   ├── SUMMARY.md                        # top-level synthesis through v5.4.2
│   ├── v5.4-round3-v5.4.1-summary.md     # detailed Round 3 adjudication
│   ├── v5.4.2-release-status.md          # final v5.4.2 release evidence/status
│   ├── v5.4.1-hardening-status.md        # historical v5.4.1 release evidence
│   ├── CANONICAL-AGENT-AUDIT-PROMPT.md   # blind-first audit prompt on current main
│   └── ...historical and Round 3 audit artifacts
├── assets/
│   └── anti-hallucination-eye.svg
├── references/
│   ├── adversarial-cases.md
│   ├── evidence-record.schema.json
│   ├── evidence-state-model.md
│   ├── research-foundations.md
│   ├── v5-research-manifest.json
│   ├── v5-gap-map.md
│   ├── untrusted-evidence-boundary.md
│   ├── verification-harness-traps.md
│   ├── stale-bug-and-done-work-verification.md
│   ├── fix-target-liveness.md
│   ├── self-capability-honesty.md
│   ├── multi-judge-ensemble.md
│   └── vetting-external-project-claims.md
├── scripts/
│   ├── external_contributor.py            # zero-write fork + validation + PR helper
│   ├── verify_claim.py
│   ├── check_evidence_record.py
│   ├── check_v5_integrity.py
│   ├── check_research_provenance.py
│   └── liveness_check.sh
└── tests/
    ├── test_external_contributor.py
    ├── test_verify_claim.py
    ├── test_evidence_record.py
    ├── test_v5_integrity.py
    ├── test_v541_regressions.py
    ├── test_v541_integrity_extra.py
    ├── test_v542_policy_regressions.py
    ├── test_research_provenance.py
    └── test_liveness.py
```

The map is intentionally structural, not a promise that every historical audit artifact is raw-byte complete. In particular, `AUDITS/PPX-GLM5.2.md` is still a documented placeholder pending archive-integrity restoration.

---

## One rule worth stealing

> **If the verifier can be wrong, verify the verifier.**

---

## Authors

Created by **[Paulina Janowska](https://github.com/antydizajn/)** and **[Gniewisława AI](https://gniewka.antydizajn.pl)**.

**Proudly witchcrafted in Poznań, Poland ♥**

Built with skepticism and an unreasonable allergy to confident bullshit.

---

## License

MIT.