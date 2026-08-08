---
name: anti-hallucination-protocol
description: Use for consequential factual claims about code, files, APIs, runtime state, research, citations, external projects, or system behavior. Decomposes output into atomic claims, matches claim type to evidence, verifies citation entailment and coverage, treats retrieval and evaluators as fallible, calibrates uncertainty and abstention, and prevents correlated self-verification from masquerading as independent evidence.
version: 4.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [anti-hallucination, verification, factuality, ground-truth, citations, epistemic-rigor]
    category: software-development
---

# Anti-Hallucination Protocol v4

This skill is an evidence-control layer for agentic work. It does not require citations for every harmless sentence. It prevents consequential claims from crossing into output or action with more certainty than the evidence can carry.

> **Core invariant:** decompose the claim, identify what would make it true, obtain evidence suited to that claim, test whether the evidence actually entails it, and abstain or qualify when the chain breaks.

Research grounding and evidence-map details live in `references/research-foundations.md`.

---

## 1. Five-stage claim-evidence pipeline

For consequential factual output, use this order:

```text
1. DECOMPOSE  -> split mixed prose into atomic, independently checkable claims
2. CLASSIFY   -> determine claim type, volatility, impact, and verifiability
3. ACQUIRE    -> retrieve/observe/run the evidence source suited to that claim
4. ENTAIL     -> test whether the evidence supports the exact claim, not merely the topic
5. RECONCILE  -> resolve conflict, calibrate wording, cite, or abstain
```

Do not skip from `ACQUIRE` directly to `VERIFIED`.

A retrieved document can be irrelevant. A real paper can be misquoted. A passing test can exercise the wrong path. A valid URL can fail to support the sentence attached to it.

---

## 2. Atomic claims before factual verification

Long answers frequently mix multiple facts, opinions, recommendations, and unverifiable material. Do not issue one global factuality verdict for the whole paragraph.

For T2/T3 material:

1. split compound statements into atomic factual units,
2. mark which units are externally verifiable,
3. assign evidence to each material unit,
4. verify only at the granularity the evidence can support.

Example:

```text
Bad unit:
"Library X is faster, safer, maintained, and supports feature Y."

Atomic units:
A. Library X is faster under benchmark B.
B. Library X has security property S.
C. Library X is currently maintained.
D. Library X supports feature Y in version V.
```

Each can require a different source and freshness window.

---

## 3. Claim tiers and adaptive verification budget

| Tier | Typical claim | Minimum behavior |
|---|---|---|
| T0 | opinion, recommendation, preference | No verification unless based on a factual premise |
| T1 | stable background fact | Verify if uncertain, disputed, unusually specific, or decision-relevant |
| T2 | code, file, version, API, repo, current docs, runtime, citation, benchmark | Direct evidence required |
| T3 | security, legal/compliance, destructive/irreversible action, production precondition, high-impact publication | Direct evidence plus independent falsification or explicit limitation |

Verification budget is **adaptive**, not uniform. Increase effort when one or more apply:

- high impact if wrong,
- high temporal volatility,
- unusual numerical precision,
- user will act or publish downstream,
- model uncertainty is high,
- evidence conflicts,
- claim is load-bearing for many later conclusions.

The exact weighting is an engineering heuristic, not a universal research result.

---

## 4. Evidence must fit the claim

| Claim | Strong evidence | Common false substitute |
|---|---|---|
| file exists | exact path lookup/listing | remembered layout |
| symbol exists | code search + source read | README mention |
| current implementation | current source at relevant ref | issue/TODO/old traceback |
| test passes | actual test execution + exit status | test file exists |
| command works | execution in relevant environment + exit/status | `--help` alone |
| current API schema | loaded schema or current official docs | guessed parameter convention |
| live state | live system query | log from earlier |
| version | lockfile/package/runtime query | prose documentation |
| paper exists | arXiv/publisher metadata | citation in another paper |
| paper supports claim | relevant paper text | title/abstract keyword overlap only |
| benchmark number | primary result artifact | README/launch post |
| quote is accurate | exact source passage | paraphrase remembered from training |

**Primary-source preference is not absolute.** The source must also be appropriate, current enough, and capable of supporting the claim.

---

## 5. Citation correctness has three separate gates

A citation is not correct merely because the URL opens.

### Gate A - identity / provenance

Verify that the cited artifact is the intended source:

- correct title,
- correct author/source identity where relevant,
- correct version/date/ref,
- no mistaken namesake or wrong document.

### Gate B - entailment

Ask:

> If a skeptical reader opened only this evidence, would the exact claim follow from it?

Reject citations that merely discuss the same topic.

### Gate C - coverage

Check whether the citation supports **all material factual parts** of the attached sentence. If not, split the sentence or add evidence.

A sentence with four factual clauses and one supporting citation is not fully supported merely because one clause is entailed.

---

## 6. Verification-result state machine

Use explicit states:

- `SUPPORTED` - evidence directly supports the claim within stated scope.
- `CONTRADICTED` - evidence directly conflicts with the claim.
- `NOT_FOUND` - a valid search/check found no evidence within its declared scope.
- `INCONCLUSIVE` - evidence exists but does not resolve the claim.
- `ERROR` - verifier/tool failed.
- `UNKNOWN_SCOPE` - the check cannot justify a global conclusion because its coverage is incomplete.

Never map:

```text
ERROR         -> NOT_FOUND
NOT_FOUND     -> CONTRADICTED
INCONCLUSIVE  -> SUPPORTED
UNKNOWN_SCOPE -> global absence
```

---

## 7. Retrieval is not truth

Treat RAG/search as a fallible subsystem with separate failure points:

```text
query formulation
    -> retrieval success
    -> document relevance
    -> source authority
    -> source freshness
    -> evidence extraction
    -> claim entailment
    -> generation faithfulness
```

A failure at any layer blocks a strong `SUPPORTED` verdict.

### Corrective retrieval

When retrieved evidence is poor, contradictory, stale, or off-topic:

1. reformulate the query,
2. search a different evidence surface,
3. prefer a more primary/current source when appropriate,
4. explicitly retain `INCONCLUSIVE` if the evidence does not converge.

Do not keep retrieving until something agrees with the draft. That is confirmation search, not verification.

---

## 8. Independence means different failure modes, not more agents

Multiple reviewers are useful only to the extent that their errors are not fully correlated.

**Do not count these as strongly independent:**

- same model + same prompt + same context,
- same model + same retrieved snippets,
- several agents inheriting the same mistaken premise,
- model-as-judge evaluating its own unsupported assertion without external evidence.

Increase independence by changing one or more of:

- evidence source,
- retrieval query,
- tool or executable observation path,
- model/checker family,
- decomposition strategy,
- verification representation (e.g. execution vs prose judgment),
- positive check vs active falsification.

For T3 claims, prefer **falsification**: ask the checker to find what would make the claim false.

---

## 9. Self-checking and self-consistency are signals, not proof

Self-refinement, sampling consistency, semantic uncertainty, and reflection can improve outputs or identify suspicious claims. They do not create external evidence.

Use them for:

- triage,
- prioritizing which claims to verify,
- generating counter-hypotheses,
- proposing verification questions,
- detecting instability.

Do not use agreement among model samples as sufficient proof of a world fact.

Also distinguish **surface variation** from **semantic disagreement**. Several paraphrases of the same wrong claim are one semantic hypothesis, not several independent confirmations.

---

## 10. Uncertainty and abstention

Do not ban words such as `probably`, `likely`, or `uncertain` merely because they can hide guessing. Sometimes uncertainty language is the correct output.

Distinguish:

- **epistemic uncertainty** - evidence/model knowledge is insufficient,
- **aleatoric/probabilistic claim** - the world itself is stochastic,
- **verification failure** - tooling/check failed,
- **scope uncertainty** - search coverage is incomplete,
- **source conflict** - credible evidence disagrees.

When evidence cannot carry the requested certainty, downgrade the claim or abstain.

Example:

```text
I cannot verify that X does not exist.
I verified repositories A and B and found no X; the search scope was not global.
```

---

## 11. Numerical, temporal, entity, and quote claims

These are high-frequency failure surfaces.

### Numerical claims

Verify:

- measured vs estimated,
- numerator/denominator,
- unit,
- aggregation method,
- benchmark subset,
- version/run.

### Temporal/current claims

Verify freshness appropriate to the claim. A source can be authoritative and still be stale.

### Entity claims

Disambiguate namesakes, organizations vs users, similarly named packages/models, and versioned products before transferring evidence.

### Quotes

Check exact source text. Do not fabricate quotation marks around a paraphrase.

---

## 12. The verifier is itself a claim

A checker can lie accidentally.

Falsify the verifier when the result is surprising, load-bearing, or contradicted by another signal. Look for:

- stale/wrong API signature,
- swallowed exception,
- ignored exit code,
- query echo matching instead of content,
- partial search misreported as global absence,
- basename/path collision,
- wrong environment,
- wrong production code path,
- retrieval contamination,
- judge prompt leaking the expected verdict.

Use `scripts/verify_claim.py` for its supported deterministic modes, but do not extend its verdict beyond the mode's scope.

See `references/verification-harness-traps.md`.

---

## 13. Current state vs historical evidence

Before patching or asserting current behavior:

1. read current source/state,
2. reproduce on a fresh path/process when practical,
3. check whether a fix already exists,
4. check whether work exists but is uncommitted,
5. check whether the target is still live,
6. separate current bug, stale process, historical log, deprecated target, and already-fixed state.

An old failure log proves a past failure, not a present defect.

See:
- `references/stale-bug-and-done-work-verification.md`
- `references/fix-target-liveness.md`

---

## 14. Tool/API and capability honesty

Never guess current tool names or schemas from training memory. Inspect the current session schema or official current docs before invoking consequential parameters.

Never fabricate the agent/runtime's own capabilities. Verify before claiming that you can:

- persist after the current execution surface ends,
- run continuously for a fixed wall-clock duration,
- access hidden activations/private chain-of-thought,
- modify protected configuration,
- remember work lost to compaction,
- use a specific background/delegation mechanism.

See `references/self-capability-honesty.md`.

### HSDB

In this environment, **HSDB means HyperspaceDB**. That is a **LOCAL** convention.

Claims about durable HSDB memory must be checked against the active HyperspaceDB integration/backend. Do not bake one installation's MCP/plugin/path schema into the portable protocol.

---

## 15. Completion semantics

Track change and validation separately.

### Change state

`INSPECTED | PATCHED | COMMITTED | DEPLOYED`

### Validation state

`STATIC_CHECKED | UNIT_TESTED | INTEGRATION_TESTED | E2E_TESTED | OBSERVED_IN_PRODUCTION | USER_OBSERVED`

Do not turn these into one fake ladder. A deployment can be user-observed but poorly integration-tested; a commit can be exhaustively unit-tested but not deployed.

Never say `fixed`, `works`, `fully active`, `wdrożone` or equivalent when that wording implies validation you did not perform.

---

## 16. Recovery after a false claim

1. State plainly that the claim was wrong.
2. Retract the exact claim.
3. Verify the corrected claim using the evidence that should have been checked first.
4. Restate the correction with an evidence pointer.
5. Walk the dependency graph: revise downstream conclusions/recommendations that used the false claim.
6. Do not bury the correction under apology or explanation.

---

## 17. Pre-send audit for consequential output

```text
[ ] Mixed prose decomposed into material atomic claims
[ ] Claim tier / impact / volatility considered
[ ] Evidence source fits each material claim
[ ] Citation identity is correct
[ ] Citation/evidence entails the exact claim
[ ] Citation coverage is complete enough
[ ] Retrieval relevance and freshness checked
[ ] ERROR != NOT_FOUND and INCONCLUSIVE != SUPPORTED
[ ] Self-consistency not mistaken for external proof
[ ] Independent checks have meaningfully different failure modes
[ ] Verifier itself challenged when result is load-bearing/surprising
[ ] Current-state claims use current-enough evidence
[ ] Numerical/temporal/entity/quote details checked where present
[ ] Completion wording matches actual validation
[ ] Any uncertainty or abstention is explicit rather than hidden
```

---

## 18. Research provenance - verified arXiv corpus

The following papers were verified against arXiv during the v4 research pass. They are cited here directly so the operational skill carries its own research provenance; design mapping and scope notes are in `references/research-foundations.md`.

1. [Survey of Hallucination in Natural Language Generation - arXiv:2202.03629](https://arxiv.org/abs/2202.03629)
2. [TruthfulQA: Measuring How Models Mimic Human Falsehoods - arXiv:2109.07958](https://arxiv.org/abs/2109.07958)
3. [Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models - arXiv:2309.01219](https://arxiv.org/abs/2309.01219)
4. [A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions - arXiv:2311.05232](https://arxiv.org/abs/2311.05232)
5. [RARR: Researching and Revising What Language Models Say, Using Language Models - arXiv:2210.08726](https://arxiv.org/abs/2210.08726)
6. [Chain-of-Verification Reduces Hallucination in Large Language Models - arXiv:2309.11495](https://arxiv.org/abs/2309.11495)
7. [SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models - arXiv:2303.08896](https://arxiv.org/abs/2303.08896)
8. [Retrieving, Rethinking and Revising: The Chain-of-Verification Can Improve Retrieval Augmented Generation - arXiv:2410.05801](https://arxiv.org/abs/2410.05801)
9. [FELM: Benchmarking Factuality Evaluation of Large Language Models - arXiv:2310.00741](https://arxiv.org/abs/2310.00741)
10. [Long-form factuality in large language models - arXiv:2403.18802](https://arxiv.org/abs/2403.18802)
11. [VERISCORE: Evaluating the factuality of verifiable claims in long-form text generation - arXiv:2406.19276](https://arxiv.org/abs/2406.19276)
12. [MAD-Fact: A Multi-Agent Debate Framework for Long-Form Factuality Evaluation in LLMs - arXiv:2510.22967](https://arxiv.org/abs/2510.22967)
13. [Corrective Retrieval Augmented Generation - arXiv:2401.15884](https://arxiv.org/abs/2401.15884)
14. [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection - arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
15. [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing - arXiv:2305.11738](https://arxiv.org/abs/2305.11738)
16. [FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation - arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
17. [FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios - arXiv:2307.13528](https://arxiv.org/abs/2307.13528)
18. [MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents - arXiv:2404.10774](https://arxiv.org/abs/2404.10774)
19. [Self-Refine: Iterative Refinement with Self-Feedback - arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
20. [Large Language Models Cannot Self-Correct Reasoning Yet - arXiv:2310.01798](https://arxiv.org/abs/2310.01798)
21. [Reflexion: Language Agents with Verbal Reinforcement Learning - arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
22. [ReAct: Synergizing Reasoning and Acting in Language Models - arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
23. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks - arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
24. [Active Retrieval Augmented Generation - arXiv:2305.06983](https://arxiv.org/abs/2305.06983)
25. [QAFactEval: Improved QA-Based Factual Consistency Evaluation for Summarization - arXiv:2112.08542](https://arxiv.org/abs/2112.08542)
26. [SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization - arXiv:2111.09525](https://arxiv.org/abs/2111.09525)
27. [Evaluating the Factual Consistency of Abstractive Text Summarization - arXiv:1910.12840](https://arxiv.org/abs/1910.12840)
28. [Language Models (Mostly) Know What They Know - arXiv:2207.05221](https://arxiv.org/abs/2207.05221)
29. [Teaching Models to Express Their Uncertainty in Words - arXiv:2205.14334](https://arxiv.org/abs/2205.14334)
30. [Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation - arXiv:2302.09664](https://arxiv.org/abs/2302.09664)
31. [HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models - arXiv:2305.11747](https://arxiv.org/abs/2305.11747)
32. [Enabling Large Language Models to Generate Text with Citations - arXiv:2305.14627](https://arxiv.org/abs/2305.14627)

---

## 19. Principle

Anti-hallucination is not cautious-sounding prose. It is controlled evidence flow.

1. Break claims small enough to verify.
2. Use evidence suited to the exact claim.
3. Verify that evidence entails and covers the claim.
4. Treat retrieval, judges, self-critique, and verifier scripts as fallible components.
5. Prefer heterogeneous falsification over correlated agreement.
6. Preserve calibrated uncertainty and abstain when the evidence chain cannot carry certainty.
7. Never state a stronger validation level than was actually earned.
