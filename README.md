<div align="center">

# Anti-Hallucination Protocol

**Make the agent earn the sentence.**

[![Version](https://img.shields.io/badge/version-5.1.0-black?style=flat-square)](SKILL.md)
[![Hermes Skill](https://img.shields.io/badge/Hermes-Agent-111111?style=flat-square)](https://github.com/NousResearch/hermes-agent)
[![License](https://img.shields.io/badge/license-MIT-black?style=flat-square)](#license)
[![Adversarial](https://img.shields.io/badge/verification-adversarial-black?style=flat-square)](tests/adversarial_cases.md)

A Hermes Agent skill for the moment between **"this looks right"** and **"I'm going to state it as fact."**

[Install](#install) · [What it catches](#what-it-catches) · [How it works](#how-it-works) · [Limits](#what-it-does-not-prove)

</div>

---

## The problem

LLMs do not only hallucinate by inventing facts.

They also fail in less theatrical ways:

- the citation is real, but it supports a different sentence;
- five agents agree because all five inherited the same bad source;
- a tool failed, but its output happened to contain the expected string;
- yesterday's memory is reported as today's state;
- the verifier is wrong and nobody verifies the verifier.

Anti-Hallucination Protocol is a procedural layer for those failures.

It asks a simple question before a strong claim leaves the model:

> **What exactly earned this wording?**

If the answer is weak, stale, contaminated, contradictory or incomplete, the wording has to weaken with it.

No ceremony for harmless creative work. More friction where being wrong actually matters.

---

## What it catches

| Failure | What the protocol does |
|---|---|
| Real URL, wrong claim | Separates source identity from entailment |
| Copied sources posing as consensus | Tracks lineage and independent failure domains |
| Tool error disguised as absence | Keeps `ERROR` separate from `NOT_FOUND_WITHIN_SCOPE` |
| Stale current-state claim | Requires freshness appropriate to the claim |
| Prompt injection inside evidence | Treats retrieved content as data, not instruction authority |
| Passing test, wrong user path | Separates unit validation from E2E / observed behavior |
| Verifier false positive | Treats the verifier result as another claim to challenge |
| Compacted session denial | Checks durable traces before claiming an earlier action never happened |

There are 30 protocol-level attack cases in [`tests/adversarial_cases.md`](tests/adversarial_cases.md).

---

## How it works

The full control model is:

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

The protocol uses risk tiers:

| Tier | Typical work | Expected behavior |
|---|---|---|
| `T0` | preference, creative choice | no verification unless a factual premise matters |
| `T1` | stable background knowledge | verify when uncertain, disputed or decision-relevant |
| `T2` | code, APIs, repos, citations, current docs, benchmarks | direct claim-matched evidence |
| `T3` | security, legal/compliance, destructive or high-impact action | direct evidence + falsification + independent check when feasible |

The rule underneath all four tiers is smaller:

```text
claim strength <= evidence strength
```

---

## Evidence is not one thing

A source can be authoritative and still be stale.

A source can be current and still be irrelevant.

A valid citation can point to the right paper and still fail to support the sentence attached to it.

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

That distinction is the core of the project.

---

## Deterministic checks

The repository includes narrow helpers for things machines can actually check without pretending to understand the universe.

### `verify_claim.py`

Checks exact filesystem facts, text matches, exact lines and command-output conditions.

It distinguishes:

```text
FOUND       exit 0
NOT_FOUND   exit 1
ERROR       exit 2
```

A failed command cannot become `FOUND` merely because its stderr contains the magic substring.

File kind can be explicit:

```bash
python3 scripts/verify_claim.py file-exists SKILL.md --kind file
python3 scripts/verify_claim.py file-exists references --kind directory
```

### `check_evidence_record.py`

Validates an evidence record against [`references/evidence-record.schema.json`](references/evidence-record.schema.json), then applies deterministic state invariants.

It rejects, among other things:

- missing required provenance fields;
- unknown evidence states;
- unknown lineage / integrity / entailment values;
- contaminated evidence used for a strong supported verdict;
- a `CONFLICT` record with only one side of the conflict;
- a strong T3 verdict with no explicitly independent supporting origin.

It does **not** prove that prose semantically entails a claim.

### `check_v5_integrity.py`

Checks repository-local structure and the actual `SKILL.md` frontmatter.

A stray `version: 5.1.0` string in the body does not count as valid metadata.

### `check_research_provenance.py`

Checks the internal consistency of the curated arXiv manifest, `SKILL.md` and research mapping.

It is deliberately offline. A local PASS is not a claim that every external resource is currently reachable or that every interpretation remains correct forever.

---

## Install

Hermes skills are directories containing `SKILL.md` plus optional references and scripts. Hermes loads the main skill on demand and supporting files only when needed. The official Hermes documentation describes this as progressive disclosure.

For a local install, place this directory at:

```text
~/.hermes/skills/software-development/anti-hallucination-protocol/
```

If you cloned a repository containing this skill:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R anti-hallucination-protocol \
  ~/.hermes/skills/software-development/anti-hallucination-protocol
```

Then start a new Hermes session and verify discovery:

```bash
hermes skills list | grep anti-hallucination-protocol
```

In chat, an installed skill can also be loaded explicitly by its slash command or through `skill_view`.

---

## Run the checks

```bash
python3 -m pytest tests/ -v
python3 scripts/check_v5_integrity.py --root .
python3 scripts/check_research_provenance.py --root .
```

The adversarial Markdown corpus is a specification, not an executable behavioral benchmark. A green unit suite does not prove that an LLM follows the protocol under long-context pressure.

---

## Research basis

The skill grew out of factuality, retrieval, uncertainty, citation, agentic failure and prompt-injection research rather than a single "hallucination detector" paper.

The curated material includes work around:

- TruthfulQA, FActScore, SelfCheckGPT, RARR and Chain-of-Verification;
- Self-RAG, Corrective RAG, CRITIC and FacTool;
- FactBench and HALoGEN;
- intent hallucination;
- AgentDojo and indirect prompt injection;
- source conflict and retrieval poisoning;
- LLM-as-a-judge bias;
- long-context evidence loss;
- agent-loop progress mirages.

The full mapping is in [`references/research-foundations.md`](references/research-foundations.md) and [`references/v5-gap-map.md`](references/v5-gap-map.md).

Research is evidence for design choices, not decoration. The protocol can still be wrong.

---

## What it does not prove

This project does **not** promise "zero hallucinations".

It also does not prove that:

- retrieved content is safe;
- a reputable source is correct;
- two agents are independent;
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
├── references/
│   ├── evidence-record.schema.json
│   ├── evidence-state-model.md
│   ├── research-foundations.md
│   ├── untrusted-evidence-boundary.md
│   └── ...
├── scripts/
│   ├── verify_claim.py
│   ├── check_evidence_record.py
│   ├── check_research_provenance.py
│   └── check_v5_integrity.py
└── tests/
    ├── adversarial_cases.md
    └── test_*.py
```

---

## One rule worth stealing

> **If the verifier can be wrong, verify the verifier.**

Everything else is implementation detail.

---

## Authors

Created by **[Paulina Janowska](https://github.com/antydizajn/)** and **[Gniewisława AI](https://gniewka.antydizajn.pl)**.

**Proudly witchcrafted in Poznań, Poland ♥**

Built with skepticism and an unreasonable allergy to confident bullshit.

---

## License

MIT.
