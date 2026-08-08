# Research foundations for Anti-Hallucination Protocol v4

Verification date: 2026-08-08.

Scope note: every entry below was checked against an `arxiv.org` abstract page or arXiv search result resolving to the abstract page. Titles and arXiv IDs were matched to arXiv metadata. The research pass read the abstract and, where needed for the design implication, the relevant arXiv-rendered material available from that paper. This file does **not** claim that every paper was read cover-to-cover.

## Evidence labels

- **SUPPORTED** - the cited work directly motivates or evaluates the mechanism.
- **DERIVED** - an engineering consequence synthesized from multiple results.
- **HEURISTIC** - a local engineering rule; useful, but not claimed as a research result.
- **LOCAL** - installation-specific convention, not a general scientific claim.

## Verified corpus and design implications

| # | arXiv | Paper | Research signal used by v4 | Design implication |
|---|---|---|---|---|
| 1 | [2202.03629](https://arxiv.org/abs/2202.03629) | Survey of Hallucination in Natural Language Generation | Hallucination is heterogeneous across tasks and metrics. | Do not reduce all factual failure to one binary label. **SUPPORTED** |
| 2 | [2109.07958](https://arxiv.org/abs/2109.07958) | TruthfulQA: Measuring How Models Mimic Human Falsehoods | Models can reproduce common misconceptions rather than merely random errors. | Popularity or model confidence is not evidence. **SUPPORTED** |
| 3 | [2309.01219](https://arxiv.org/abs/2309.01219) | Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models | Hallucination spans input conflict, context conflict, and world-knowledge conflict. | Classify the relation a claim is supposed to satisfy before choosing a checker. **SUPPORTED** |
| 4 | [2311.05232](https://arxiv.org/abs/2311.05232) | A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions | Retrieval can mitigate hallucination but is itself failure-prone. | Retrieval output is evidence candidate, not ground truth. **SUPPORTED** |
| 5 | [2210.08726](https://arxiv.org/abs/2210.08726) | RARR: Researching and Revising What Language Models Say, Using Language Models | External research plus revision improves attribution while preserving content. | Separate research/evidence acquisition from revision. **SUPPORTED** |
| 6 | [2309.11495](https://arxiv.org/abs/2309.11495) | Chain-of-Verification Reduces Hallucination in Large Language Models | Planning verification questions and answering them independently can reduce hallucination. | Decompose verification and avoid conditioning each check on the draft conclusion when practical. **SUPPORTED** |
| 7 | [2303.08896](https://arxiv.org/abs/2303.08896) | SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models | Sample inconsistency can signal hallucination without external databases. | Self-consistency is a useful signal but not proof. **SUPPORTED** |
| 8 | [2410.05801](https://arxiv.org/abs/2410.05801) | Retrieving, Rethinking and Revising: The Chain-of-Verification Can Improve Retrieval Augmented Generation | Retrieval queries and retrieved context can themselves require correction. | Verify retrieval quality separately from answer correctness. **SUPPORTED** |
| 9 | [2310.00741](https://arxiv.org/abs/2310.00741) | FELM: Benchmarking Factuality Evaluation of Large Language Models | LLM factuality evaluators remain imperfect even with retrieval/reasoning. | Never treat an LLM judge as an oracle; evaluator performance itself must be considered. **SUPPORTED** |
| 10 | [2403.18802](https://arxiv.org/abs/2403.18802) | Long-form factuality in large language models | SAFE decomposes long responses into individual facts and checks them with search. | Long-form verification should operate on atomic/verifiable claims, not one global verdict. **SUPPORTED** |
| 11 | [2406.19276](https://arxiv.org/abs/2406.19276) | VERISCORE: Evaluating the factuality of verifiable claims in long-form text generation | Not every sentence in long-form text is externally verifiable. | Distinguish verifiable factual claims from opinions, instructions, and unverifiable content. **SUPPORTED** |
| 12 | [2510.22967](https://arxiv.org/abs/2510.22967) | MAD-Fact: A Multi-Agent Debate Framework for Long-Form Factuality Evaluation in LLMs | Long-form claims differ in importance; multi-agent evaluation can be structured around claim importance. | Allocate verification budget by claim salience/impact, not equal cost per sentence. **SUPPORTED for importance weighting; debate is not treated as proof** |
| 13 | [2401.15884](https://arxiv.org/abs/2401.15884) | Corrective Retrieval Augmented Generation | Retrieval quality should be evaluated and corrective retrieval triggered when evidence is poor. | Add explicit retrieval-quality gate and corrective branch. **SUPPORTED** |
| 14 | [2310.11511](https://arxiv.org/abs/2310.11511) | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | Retrieval need and evidence usefulness can be adaptive rather than fixed. | Do not retrieve mechanically for every claim; use adaptive verification budget. **SUPPORTED** |
| 15 | [2305.11738](https://arxiv.org/abs/2305.11738) | CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing | External tools improve critique/revision across factual and executable tasks. | Prefer tool-grounded correction over intrinsic self-critique for consequential claims. **SUPPORTED** |
| 16 | [2305.14251](https://arxiv.org/abs/2305.14251) | FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation | Long-form outputs contain mixtures of supported and unsupported atomic facts. | Decompose mixed passages into atomic claims before factual scoring. **SUPPORTED** |
| 17 | [2307.13528](https://arxiv.org/abs/2307.13528) | FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios | Fact checking requires task-appropriate tools and evidence. | Evidence method should depend on claim domain: web, code execution, math, scientific literature, runtime. **SUPPORTED** |
| 18 | [2404.10774](https://arxiv.org/abs/2404.10774) | MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents | Grounding evaluation requires checking whether evidence actually supports each fact; small checkers can be effective but still need evaluation. | Separate evidence retrieval from evidence-to-claim entailment. **SUPPORTED** |
| 19 | [2303.17651](https://arxiv.org/abs/2303.17651) | Self-Refine: Iterative Refinement with Self-Feedback | Iterative self-feedback can improve outputs across tasks. | Revision loops can help, but do not by themselves create independent evidence. **SUPPORTED with limitation from paper #20** |
| 20 | [2310.01798](https://arxiv.org/abs/2310.01798) | Large Language Models Cannot Self-Correct Reasoning Yet | Intrinsic self-correction without external feedback can fail or degrade performance. | Never promote same-model self-critique to independent verification. **SUPPORTED** |
| 21 | [2303.11366](https://arxiv.org/abs/2303.11366) | Reflexion: Language Agents with Verbal Reinforcement Learning | Agents can improve using explicit feedback signals and episodic reflection. | Treat reflection as learning/revision context, not factual evidence unless feedback itself is grounded. **DERIVED** |
| 22 | [2210.03629](https://arxiv.org/abs/2210.03629) | ReAct: Synergizing Reasoning and Acting in Language Models | Acting against external environments can reduce hallucination/error propagation on QA/fact verification. | For environment claims, observe the environment instead of extending internal reasoning. **SUPPORTED** |
| 23 | [2005.11401](https://arxiv.org/abs/2005.11401) | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Non-parametric retrieval improves factuality/provenance relative to parametric-only generation in studied tasks. | Prefer external evidence for knowledge-intensive current claims; provenance remains explicit. **SUPPORTED** |
| 24 | [2305.06983](https://arxiv.org/abs/2305.06983) | Active Retrieval Augmented Generation | Long generation may require retrieval during generation rather than only once at the start. | Re-verify as new claims are introduced; do not assume initial evidence covers later claims. **SUPPORTED** |
| 25 | [2112.08542](https://arxiv.org/abs/2112.08542) | QAFactEval: Improved QA-Based Factual Consistency Evaluation for Summarization | QA-based and entailment-based factuality metrics can provide complementary signals. | For high-impact text claims, combine heterogeneous verification signals rather than repeated copies of one checker. **SUPPORTED** |
| 26 | [2111.09525](https://arxiv.org/abs/2111.09525) | SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization | Granularity mismatch can break an otherwise reasonable factuality checker. | Match claim granularity to verifier granularity; sentence/document mismatch is a known failure mode. **SUPPORTED** |
| 27 | [1910.12840](https://arxiv.org/abs/1910.12840) | Evaluating the Factual Consistency of Abstractive Text Summarization | Factual consistency models can identify supporting and conflicting spans rather than only issue a score. | Require evidence pointers/counter-evidence where feasible, not naked judge labels. **SUPPORTED** |
| 28 | [2207.05221](https://arxiv.org/abs/2207.05221) | Language Models (Mostly) Know What They Know | Models can show useful self-evaluation/calibration signals, with generalization limitations. | Model confidence may guide verification priority, but cannot replace evidence. **SUPPORTED** |
| 29 | [2205.14334](https://arxiv.org/abs/2205.14334) | Teaching Models to Express Their Uncertainty in Words | Verbalized uncertainty can be calibrated in studied settings and shifts. | Preserve calibrated uncertainty language instead of banning words such as "probably" categorically. **SUPPORTED** |
| 30 | [2302.09664](https://arxiv.org/abs/2302.09664) | Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation | Surface-form variation must be collapsed by meaning when estimating uncertainty. | Do not treat paraphrase diversity as factual disagreement; compare semantic claims. **SUPPORTED** |
| 31 | [2305.11747](https://arxiv.org/abs/2305.11747) | HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models | LLMs struggle to recognize hallucinated text; external knowledge/reasoning can help. | Detection capability must be tested adversarially; fluent judging is not enough. **SUPPORTED** |
| 32 | [2305.14627](https://arxiv.org/abs/2305.14627) | Enabling Large Language Models to Generate Text with Citations | Citation quality includes whether citations actually support generated statements and whether support is complete. | A valid URL is insufficient: check citation entailment and coverage/completeness. **SUPPORTED** |

## Synthesis: what v3 was missing

### 1. Atomicity before verification

FActScore, SAFE, and VERISCORE make the same architectural problem impossible to ignore: a paragraph is usually not one factual claim. A single paragraph can contain supported, unsupported, unverifiable, and opinion-like material. v4 therefore decomposes consequential output into **atomic verifiable claims** before evidence assignment. This is a **SUPPORTED** design choice from #10, #11, and #16.

### 2. Citation existence != citation correctness

ALCE and grounding/fact-checking work motivate a three-part citation check:

1. **existence/provenance** - does the cited artifact exist and is it the intended source?
2. **entailment** - does the cited evidence actually support the claim?
3. **coverage** - are all material factual parts supported, or only a convenient subset?

This is **SUPPORTED** by #18, #27, and #32.

### 3. Retrieval is a fallible subsystem

RAG is useful, but Self-RAG, CRAG, CoV-RAG and the hallucination surveys show why `retrieved == true` is invalid. v4 separates:

- retrieval success,
- retrieval relevance,
- source authority/freshness,
- evidence entailment,
- generation faithfulness to the evidence.

This separation is **SUPPORTED/DERIVED** from #4, #8, #13, #14, #23, and #24.

### 4. Verification independence is about failure modes, not headcount

CoVe benefits from independent verification questions, CRITIC benefits from external tools, and Huang et al. show intrinsic self-correction can fail. Therefore:

> Five agents using the same model, same prompt, same evidence and same mistaken premise are not five independent verifiers.

This exact sentence is an engineering **DERIVED** rule from #6, #15, #20, #25. Independence should be increased by changing evidence sources, tools, representations, or decision procedures where practical.

### 5. Self-consistency is a signal, not evidence

SelfCheckGPT shows disagreement across stochastic samples can be useful for detection, while semantic-uncertainty work shows surface variation must be grouped by meaning. v4 uses self-consistency/semantic uncertainty for **triage**, never as sufficient proof of truth. **SUPPORTED/DERIVED** from #7 and #30.

### 6. Uncertainty must be calibrated, not stylistically suppressed

Kadavath et al. and Lin et al. support treating model uncertainty as a useful imperfect signal. The v3-style temptation to ban uncertainty phrases is therefore wrong. v4 instead distinguishes:

- epistemic uncertainty,
- evidence insufficiency,
- verifier failure,
- genuine probabilistic claims.

**SUPPORTED/DERIVED** from #28 and #29.

### 7. Verification budget should be adaptive

Not all claims deserve equal verification cost. Self-RAG/FLARE motivate adaptive retrieval, while long-form evaluation motivates decomposition. v4 prioritizes verification by a combination of:

- impact if wrong,
- volatility,
- specificity,
- user reliance,
- uncertainty,
- claim salience.

The exact scoring policy is an engineering **HEURISTIC**, informed by #12, #14, #24, #28.

### 8. Evaluators need evaluation

FELM and HaluEval directly warn against assuming that an LLM can reliably detect hallucinations merely because it can discuss them. v4 adds evaluator-falsification and adversarial tests for false `VERIFIED`. **SUPPORTED** by #9 and #31.

## Research integrity rules for future edits

1. A paper may be cited only after its arXiv metadata has been checked.
2. A correct arXiv ID with the wrong title is a failed citation.
3. A real paper cited for a claim it does not support is a failed citation.
4. A paper's abstract supports only claims actually present in the abstract unless deeper sections were read.
5. `SUPPORTED` must not be upgraded to "proven universally"; benchmark/model/task scope matters.
6. Engineering synthesis must be marked `DERIVED` or `HEURISTIC` rather than laundered through a citation.
7. Multiple papers sharing the same data/model/judge are not automatically independent evidence.
8. Citation count is not evidence quality.
