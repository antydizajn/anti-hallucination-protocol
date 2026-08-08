<div align="center">

<img src="assets/anti-hallucination-eye.svg" alt="Anti-Hallucination Protocol eye mark" width="220">

# Anti-Hallucination Protocol

**Make the agent earn the sentence.**

[![Version](https://img.shields.io/badge/version-5.3.0-black?style=flat-square)](SKILL.md)
[![Hermes Skill](https://img.shields.io/badge/Hermes-Agent-111111?style=flat-square)](https://github.com/NousResearch/hermes-agent)
[![License](https://img.shields.io/badge/license-MIT-black?style=flat-square)](#license)
[![Adversarial](https://img.shields.io/badge/verification-adversarial-black?style=flat-square)](references/adversarial-cases.md)

A Hermes Agent skill for the moment between **"this looks right"** and **"I'm going to state it as fact."**

[Install](#install) · [Failure modes](#failure-modes-it-targets) · [How it works](#how-it-works) · [Limits](#what-it-does-not-prove)

</div>

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

| Failure | Protocol response |
|---|---|
| Real URL, wrong claim | separate source identity from entailment |
| Copied sources posing as consensus | track lineage and independent failure domains |
| Self-declared "independence" | require auditable lineage metadata for strong T3 records, while admitting that labels do not prove real independence |
| Tool error disguised as absence | keep `ERROR` separate from `NOT_FOUND_WITHIN_SCOPE` |
| Stale current-state claim | require explicit observation time and current-enough evidence for strong T3 current-state records |
| Prompt injection inside evidence | treat retrieved content as data, not instruction authority |
| Passing test, wrong user path | separate unit validation from E2E / observed behavior |
| Verifier false positive | treat the verifier result as another scoped claim |
| Compacted-session denial | check durable traces before claiming an earlier action never happened |

The canonical protocol attack corpus is in [`references/adversarial-cases.md`](references/adversarial-cases.md). Executable regression tests live separately under `tests/`.

---

## How it works

The active v5.3 skill is intentionally smaller than v5.2. The hot path is seven rules, with deeper material loaded only when needed.

The protocol still models the full control flow as:

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

That is not a mandatory ritual for every sentence.

Risk tiers:

| Tier | Typical work | Expected behavior |
|---|---|---|
| `T0` | preference, creative choice | no verification unless a factual premise matters |
| `T1` | stable background knowledge | verify when uncertain, disputed or decision-relevant |
| `T2` | code, APIs, repos, citations, current docs, benchmarks | direct claim-matched evidence |
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

For strong T3 machine-readable records, verified independent support carries `lineage_basis`, `lineage_verification` and `independence_group`. The checker can detect internal contradictions such as reused declared groups. It cannot prove that two real sources are genuinely independent.

---

## Deterministic checks

The repository includes narrow helpers for properties machines can actually check without pretending to understand the universe.

### `verify_claim.py`

Checks filesystem facts, exact text/line conditions and command-output conditions.

```text
FOUND       exit 0
NOT_FOUND   exit 1
ERROR       exit 2
```

A failed command cannot become `FOUND` merely because its output contains the expected substring.

### `check_evidence_record.py`

Validates [`references/evidence-record.schema.json`](references/evidence-record.schema.json) plus deterministic cross-field invariants.

For strong T3 records it checks, among other things:

- known source class;
- source identity and evidence span;
- RFC3339 retrieval timestamps;
- verifier provenance and clean observed verifier state;
- verified independent lineage metadata;
- non-empty `independence_group` and no duplicate declared group among verified independent supporting items;
- explicit RFC3339 observation time and `CURRENT_ENOUGH` evidence for T3 current-state claims.

A successful result is:

```text
EVIDENCE RECORD: STRUCTURALLY_VALID
```

That means exactly what it says. It does **not** establish semantic entailment, source truth or real-world source independence.

### `check_v5_integrity.py`

Checks repository structure and parses `SKILL.md` frontmatter with real YAML rather than a hand-written YAML approximation. This specifically prevents integrity PASS from certifying metadata that Hermes/PyYAML cannot parse correctly.

### `check_research_provenance.py`

Checks offline repository-internal research identity consistency across canonical manifests/reference mappings. It does not prove that an external source is live or that a research interpretation is correct.

### `liveness_check.sh`

Checks the portable L1/L2 installation contract and exits nonzero when a required check fails. Files on disk cannot prove behavioral compliance, so that remains an explicit unknown outside this helper.

---

## Install

Place the skill directory at:

```text
~/.hermes/skills/software-development/anti-hallucination-protocol/
```

Then start a new Hermes session and verify discovery using the currently available Hermes skill tooling.

---

## Run the checks

From a repository checkout:

```bash
python3 -m pytest tests/ -v
python3 scripts/check_v5_integrity.py --root .
python3 scripts/check_research_provenance.py --root .
AHP_SKILL_DIR="$(pwd)" bash scripts/liveness_check.sh
```

`liveness_check.sh` is a Bash helper. On native Windows it requires a Bash-compatible environment such as WSL or Git Bash. The Python checks are the portable core of deterministic validation. Native Windows execution is not claimed as tested here.

The Markdown adversarial corpus is a specification, not an executable behavioral benchmark. A green unit suite does not prove that an LLM follows the protocol under long-context pressure.

---

## Research basis

The skill integrates work on factuality, retrieval, citation, uncertainty, prompt injection, memory, judge bias, long-context evidence loss and agentic failure.

The full research identity/mapping layer lives outside the main skill prompt:

- [`references/research-foundations.md`](references/research-foundations.md)
- [`references/v5-research-manifest.json`](references/v5-research-manifest.json)
- [`references/v5-gap-map.md`](references/v5-gap-map.md)

Research is evidence for design choices, not decoration and not proof that the implementation is correct.

---

## Audit trail

The raw v5.2 multi-model audit corpus and synthesis are archived under [`AUDITS/`](AUDITS/).

`AUDITS/SUMMARY.md` separates execution-capable Hermes audits from Perplexity document-only audits, records conflicts and rejected severity claims, and lists the evidence used to define v5.3.

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
- Markdown instructions were obeyed at runtime.

Those guarantees need architecture, sandboxing, external observation, executable checks or behavioral evaluation outside the prompt.

This is a protocol for making unsupported certainty harder, not impossible.

---

## Repository map

```text
anti-hallucination-protocol/
├── SKILL.md
├── README.md
├── AUDITS/
│   ├── SUMMARY.md
│   └── ...raw audit reports
├── assets/
│   └── anti-hallucination-eye.svg
├── references/
│   ├── adversarial-cases.md
│   ├── evidence-record.schema.json
│   ├── evidence-state-model.md
│   ├── research-foundations.md
│   ├── v5-research-manifest.json
│   └── ...
├── scripts/
│   ├── verify_claim.py
│   ├── check_evidence_record.py
│   ├── check_research_provenance.py
│   ├── check_v5_integrity.py
│   └── liveness_check.sh
└── tests/
    ├── adversarial_cases.md
    └── test_*.py
```

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
