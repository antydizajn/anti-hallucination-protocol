# AHP Benchmark Research - Primary Source Ledger

Checked: 2026-08-10

## Purpose

This file records primary sources used to promote registry entries to `PRIMARY_VERIFIED`.

A registry entry without a reviewed primary source remains a candidate even if the benchmark name is widely known.

## Verified sources

### AA-Omniscience

- Paper: https://arxiv.org/abs/2511.13029
- Construct: closed-book factual recall plus abstention/knowledge calibration.
- AHP note: useful narrow parametric layer, not a complete hallucination benchmark.

### SimpleQA

- Official publication: https://openai.com/index/introducing-simpleqa/
- Construct: short-form fact-seeking factuality with correct/incorrect/not-attempted grading.
- AHP note: public, short-form, known label noise and not a long-form grounding test.

### SimpleQA Verified

- Paper: https://arxiv.org/abs/2509.07968
- Construct: revised 1,000-prompt SimpleQA-derived parametric factuality benchmark with deduplication, topic balancing and source reconciliation.

### FACTS Benchmark Suite

- Official overview: https://deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models/
- Official eval index: https://deepmind.google/research/evals/
- Constructs: Parametric, Search, Multimodal and Grounding.
- AHP note: use components separately. Do not collapse them into one AHP headline score.

### FACTS Grounding

- Official publication: https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/
- Construct: response grounding against provided long context.

### AbstentionBench

- Paper: https://arxiv.org/abs/2506.09038
- Construct: abstention across unknown answers, underspecification, false premises, subjective interpretation and outdated information.

### Abstain-QA

- Paper: https://arxiv.org/abs/2407.16221
- Construct: black-box answerable/unanswerable abstention evaluation using an answerable-unanswerable confusion matrix.

### ConfidenceBench

- Paper: https://arxiv.org/abs/2607.20526
- Construct: verbalized confidence calibration using Brier score on a private question set.

### AgentAbstain

- Paper: https://arxiv.org/abs/2607.10059
- Construct: paired should-act / should-abstain agent tasks in executable sandbox environments.
- AHP note: very high fit for action gating and tool/runtime abstention, but recent and should be independently audited before confirmatory use.

### HalluWorld

- Paper: https://arxiv.org/abs/2605.19341
- Construct: hallucination relative to explicitly specified reference worlds across gridworld, chess and terminal tasks.
- AHP note: methodological cornerstone for deterministic/reference-world evidence.

### SealQA

- Paper: https://arxiv.org/abs/2506.01062
- Construct: search-augmented fact-seeking under conflicting, noisy or unhelpful search results, including LongSeal.

### FaithEval

- Paper: https://arxiv.org/abs/2410.03727
- Construct: context faithfulness under unanswerable, inconsistent and counterfactual contexts.
- AHP note: context faithfulness and real-world factuality must be reported separately.

### WhoQA

- Paper: https://arxiv.org/abs/2410.15737
- Construct: practical knowledge conflict using same-name entities and multiple distinct answers.

### LongFact and SAFE

- Paper: https://arxiv.org/abs/2403.18802
- Construct: open-domain long-form factuality with atomic fact extraction and search-augmented verification.

### FActScore

- Paper: https://arxiv.org/abs/2305.14251
- Construct: atomic factual precision in long-form generation.
- AHP note: evaluator/metric layer rather than a complete prevention benchmark.

### VERISCORE

- Paper: https://arxiv.org/abs/2406.19276
- Construct: factuality of verifiable claims while explicitly separating unverifiable material.

### FactBench

- Paper: https://arxiv.org/abs/2410.22257
- Construct: dynamic in-the-wild factuality prompts with VERIFY labels for supported, unsupported and undecidable units.

### HalluHard

- Paper: https://arxiv.org/abs/2602.01031
- Construct: multi-turn hallucination and citation grounding across legal, research, medical-guideline and coding domains.

### ToolFailBench

- Paper: https://arxiv.org/abs/2607.04686
- Construct: Tool-Skip, Result-Ignore, Output-Fabrication and Unnecessary-Tool-Use across 1,000 tasks.
- AHP note: recent preprint and highly relevant to tool evidence semantics.

### AgentHallu

- Paper: https://arxiv.org/abs/2601.06818
- Construct: hallucination attribution across multi-step agent trajectories with planning, retrieval, reasoning, human-interaction and tool-use categories.
- AHP note: diagnostic/attribution benchmark, not direct prevention evidence by itself.

### BIPIA

- Paper: https://arxiv.org/abs/2312.14197
- Construct: indirect prompt injection through external content.

### AgentDojo

- Paper: https://arxiv.org/abs/2406.13352
- Construct: dynamic tool-using agent environment with realistic benign tasks and prompt-injection security cases.

### LivePI

- Paper: https://arxiv.org/abs/2605.17986
- Construct: indirect prompt injection across live test-controlled email, chat, web, local files, repositories and wallet surfaces.
- AHP note: recent, high-severity, environment-dependent evidence.

### ALCE

- Paper: https://arxiv.org/abs/2305.14627
- Construct: end-to-end retrieval plus generation with automatic citation evaluation across fluency, correctness and citation quality.

### RefChecker

- Paper: https://arxiv.org/abs/2405.14486
- Construct: fine-grained hallucination checking with claim triplets and Zero/Noisy/Accurate context settings.
- AHP note: primarily evaluator-validation evidence.

### RAGTruth

- Paper: https://arxiv.org/abs/2401.00396
- Construct: manually annotated hallucination corpus for RAG responses with case and word-level labels.
- AHP note: primarily detector/evaluator corpus.

### HaluEval

- Paper: https://arxiv.org/abs/2305.11747
- Construct: hallucination recognition/detection over generated and human-annotated samples.
- AHP note: useful diagnostic history, weak as a direct AHP effectiveness endpoint.

### RFEval

- Paper: https://arxiv.org/abs/2602.17053
- Construct: reasoning faithfulness under counterfactual reasoning intervention.
- AHP note: adjacent reliability construct. Do not equate reasoning faithfulness with factuality.

### Video SimpleQA

- Paper: https://arxiv.org/abs/2503.18923
- Construct: factuality evaluation for large video-language models with external-source verification and short answers.
- AHP note: multimodal extension candidate, not required for initial text-agent AHP core.

## Source review policy

Promotion rule:

```text
CANDIDATE_PENDING_PRIMARY_REVIEW
-> inspect original paper / official dataset / official repository
-> map exact construct and scorer
-> record contamination/access/licensing limits
-> PRIMARY_VERIFIED
```

Do not promote an entry solely because it appears in a survey or another benchmark's related-work section.
