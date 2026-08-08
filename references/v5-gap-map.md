# Anti-Hallucination Protocol v5 - adversarial gap map

Research date: 2026-08-08.

This document records why v4 is insufficient and what v5 is allowed to add. It is intentionally written as a failure map rather than a feature wishlist.

Evidence labels:

- **SUPPORTED** - directly motivated by the cited source in the stated scope.
- **DERIVED** - engineering consequence synthesized from multiple sources.
- **HEURISTIC** - local engineering rule; not presented as a research result.
- **LOCAL** - installation-specific convention.

## Failure map

| Failure mode | Evidence signal | Why v4 is insufficient | v5 control | Residual risk |
|---|---|---|---|---|
| Intent hallucination: response omits or invents user constraints while remaining factually plausible | FAITHQA reports omission and misinterpretation as a distinct failure class | v4 verifies factual claims but has no explicit intent-contract check | Add an intent/constraint gate before factual verification | Correctly parsing ambiguous intent can still require clarification |
| Progress mirage in autonomous loops | Park & Choi report self-evaluation accepting non-improvements/regressions when success lives outside the transcript | v4 warns about self-checking but does not require an external success signal for open-world agent loops | Separate artifact evidence from world-state evidence; require out-of-band success measures when the objective lives outside the transcript | Some objectives have no cheap external oracle |
| Agent-trajectory error propagation | AgentHallu localizes hallucinations across planning, retrieval, reasoning, human interaction and tool use | v4 mostly checks final claims, not where trajectory divergence began | Add trajectory checkpoints and earliest-divergence diagnosis for consequential workflows | Step-level attribution remains difficult and imperfect |
| Hallucination-on-hallucination from bad retrieval | DRAG and conflict-aware RAG work show retrieval can amplify error | v4 says retrieval is fallible but does not track source lineage or conflicting-source classes | Add source lineage, conflict state and contradiction search | Search itself may miss the decisive source |
| Indirect prompt injection from evidence | AgentDojo, NIST agent-hijacking work and 2026 adaptive IPI attacks show external data can contain adversarial instructions | v4 treats retrieval as evidence but lacks a hard instruction/data trust boundary | Treat retrieved/tool/memory content as untrusted data; never inherit instructions from evidence | Natural-language separation remains bypassable without architectural isolation |
| Retrieval/database poisoning | POISONCRAFT and PIDP-Attack show malicious passages can be engineered for retrieval and influence generation | v4 checks authority/freshness but not integrity/adversarial origin | Add source-integrity and contamination flags; avoid single-retriever/single-index certainty for high-risk claims | Black-box search/index integrity may be unknowable |
| Source conflict | CONFLICTS work shows models often mishandle contradictory retrieved sources | v4 has `INCONCLUSIVE` but no explicit conflict taxonomy or supersession logic | Add `CONFLICT` state, source precedence only when justified, and explicit unresolved-conflict output | Authority and recency can themselves conflict |
| Duplicate evidence masquerading as independence | Search results often syndicate/copy the same upstream source | v4 speaks about correlated agents but not copied-source lineage | Add `independence_group` / source-lineage concept; count independent origins, not URLs | Provenance can be hidden or incomplete |
| Long-context evidence disappearance | Lost in the Middle shows relevant evidence can be underused depending on position | v4 assumes that supplied evidence remains effectively available to the model | Keep critical evidence compact, claim-local and pointer-based; re-read decisive spans before verdict | Long-context models can still miss or misweight evidence |
| LLM judge self-preference / familiarity bias | Self-preference studies show judges can systematically favor familiar/self-like outputs | v4 warns that judges are fallible but has no judge-conflict rule | Never use self-judgment alone for T3; record judge provenance and expected-bias risk | Cross-model judges can share training/style biases |
| Hidden-state or uncertainty signal overreach | 2025 work both finds useful factuality probes and challenges their generalization | v4 correctly treats uncertainty as signal, but does not distinguish runtime-accessible vs research-only signals | Mark internal-state methods `UNAVAILABLE` unless the active model exposes them; never simulate inaccessible telemetry | Black-box APIs expose little internal uncertainty data |
| Tool/API hallucination | MARIN/APIHulBench finds non-existent or misused APIs remain a coding failure mode | v4 says inspect schema, but no explicit executable schema-grounding gate | For consequential API/tool claims, schema/reflection/runtime lookup outranks remembered API knowledge | Dynamic plugins/MCP schemas can still change mid-session |
| Stale memory conflict | 2026 memory-conflict work suggests version-aware deterministic aggregation can beat leaving freshness resolution entirely to LLM judgment in some tasks | v4 handles temporal claims but not memory-record supersession | Require timestamp/version comparison for mutable facts; use deterministic resolution when semantics permit | Newest is not always correct for every question type |
| Single-attempt security evaluation | NIST agent-hijacking testing shows repeated attempts can materially change measured attack success | v4 attack thinking is mostly one-shot | For probabilistic security controls, evaluate repeated trials when realistic and affordable | Trial count and attack budget remain application-specific |
| Dynamic factuality / benchmark staleness | FactBench uses dynamic real-world prompts and shows difficulty/refusal tradeoffs | v4 research provenance is static and can age | Add research/source freshness metadata and distinguish corpus integrity from current truth | A static skill cannot continuously guarantee literature freshness |
| Intent-to-action mismatch | Agentic systems can execute harmful or irrelevant actions even if local statements are true | v4 is claim-centric | Add action precondition: `truth of premises != authorization/relevance of action` | Authorization semantics depend on surrounding safety/policy layers |

## Core v5 design consequence

The verification object is no longer just `claim + citation`.

A consequential verdict depends on a chain:

```text
USER INTENT
  -> CLAIM
  -> QUERY / OBSERVATION PLAN
  -> RETRIEVAL / TOOL RESULT
  -> SOURCE IDENTITY + LINEAGE + FRESHNESS + INTEGRITY
  -> EVIDENCE SPAN
  -> ENTAILMENT / CONTRADICTION
  -> VERIFIER PROVENANCE
  -> SYNTHESIS
  -> ACTION / WORDING
```

Every arrow can fail. v5 therefore treats a verified claim as a **bounded state produced by a traceable evidence path**, not a vibe emitted by a reviewer.

## New research sources used for v5

The sources below were checked on their primary publication pages during the v5 research pass. Inclusion here does not mean every result generalizes beyond the paper's evaluated setup.

1. FactBench: A Dynamic Benchmark for In-the-Wild Language Model Factuality Evaluation - ACL 2025: https://aclanthology.org/2025.acl-long.1587/
2. Beyond Facts: Evaluating Intent Hallucination in Large Language Models - ACL 2025: https://aclanthology.org/2025.acl-long.349/
3. Improving Factuality with Explicit Working Memory - ACL 2025: https://aclanthology.org/2025.acl-long.548/
4. HALoGEN: Fantastic LLM Hallucinations and Where to Find Them - ACL 2025: https://aclanthology.org/2025.acl-long.71/
5. Removal of Hallucination on Hallucination: Debate-Augmented RAG - ACL 2025: https://aclanthology.org/2025.acl-long.770/
6. Lost in the Middle: How Language Models Use Long Contexts - arXiv:2307.03172: https://arxiv.org/abs/2307.03172
7. AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents - arXiv:2406.13352: https://arxiv.org/abs/2406.13352
8. IterInject: Indirect Prompt Injection Against LLM Agents via Feedback-Guided Iterative Optimization - arXiv:2605.24659: https://arxiv.org/abs/2605.24659
9. Assessing Automated Prompt Injection Attacks in Agentic Environments - arXiv:2606.10525: https://arxiv.org/abs/2606.10525
10. POISONCRAFT: Practical Poisoning of Retrieval-Augmented Generation for Large Language Models - arXiv:2505.06579: https://arxiv.org/abs/2505.06579
11. PIDP-Attack: Combining Prompt Injection with Database Poisoning Attacks on Retrieval-Augmented Generation Systems - arXiv:2603.25164: https://arxiv.org/abs/2603.25164
12. DRAGged into Conflicts: Detecting and Addressing Conflicting Sources in Search-Augmented LLMs - arXiv:2506.08500: https://arxiv.org/abs/2506.08500
13. AgentHallu: Benchmarking Automated Hallucination Attribution of LLM-based Agents - arXiv:2601.06818: https://arxiv.org/abs/2601.06818
14. When Do Agent Loops Mistake Stagnation for Progress? - arXiv:2607.25152: https://arxiv.org/abs/2607.25152
15. Quantifying and Mitigating Self-Preference Bias of LLM Judges - arXiv:2604.22891: https://arxiv.org/abs/2604.22891
16. Self-Preference Bias in LLM-as-a-Judge - arXiv:2410.21819: https://arxiv.org/abs/2410.21819
17. Towards Mitigating API Hallucination in Code Generated by LLMs with Hierarchical Dependency Aware - arXiv:2505.05057: https://arxiv.org/abs/2505.05057
18. Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution - arXiv:2606.01435: https://arxiv.org/abs/2606.01435
19. NIST AI RMF Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
20. NIST Technical Blog: Strengthening AI Agent Hijacking Evaluations: https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations
21. Hermes Agent - Creating Skills: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/creating-skills.md
22. Hermes Agent - Skills System: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md
23. Hermes Agent - Built-in Tools Reference: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/tools-reference.md
24. Hermes Agent - Event Hooks: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/hooks.md

## What v5 must NOT claim

- It cannot guarantee truth.
- It cannot guarantee prompt-injection resistance from prompting alone.
- It cannot make two correlated judges independent by naming them separately.
- It cannot infer source integrity merely from a reputable domain.
- It cannot infer that the newest source is always the correct source.
- It cannot claim exhaustive search unless the search space was actually bounded and enumerated.
- It cannot claim online freshness from an offline manifest.
- It cannot turn model confidence into evidence.
- It cannot convert a passing linter into semantic proof that a citation supports a claim.
