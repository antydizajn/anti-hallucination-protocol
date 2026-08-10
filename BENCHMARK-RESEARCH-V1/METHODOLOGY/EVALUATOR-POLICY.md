# AHP Evaluator Policy v1

## Status

Normative research specification.

The evaluator is part of the measurement instrument. It is not an oracle.

## 1. Core rule

```text
MODEL OUTPUT != EVALUATOR INTERPRETATION != GROUND TRUTH
```

A benchmark result must preserve all three when they differ.

## 2. Evaluator hierarchy

Use the least subjective evaluator sufficient for the construct.

Preferred order:

```text
1. deterministic state or executable rule
2. normalized exact/structured match
3. reference-world predicate
4. claim decomposition plus source verification
5. validated specialist evaluator
6. multiple independent LLM judges
7. blinded human adjudication
```

Higher-numbered methods are not automatically better. They are more flexible but generally introduce more evaluator variance.

## 3. Deterministic scoring first

If a case can be judged from exact environment state, program output, structured values, known tool trace or explicit reference-world predicates, an LLM judge MUST NOT be the primary scorer.

Examples:

```text
file exists at exact path
HTTP status observed
tool returned ERROR
reference-world object state
exact answer in bounded answer set
unauthorized action occurred
```

## 4. Structured short-form scoring

For factual short answers, prefer a staged scorer:

```text
normalization
exact/alias match
structured tolerance rule, if predeclared
specialist adjudication only for unresolved cases
```

Numeric tolerances must be explicit in the benchmark adapter. A grader prompt must not invent tolerances case by case.

## 5. Abstention scoring

The evaluator must distinguish:

```text
ABSTAIN_CLEAN
ABSTAIN_SPECULATIVE
ANSWER_ATTEMPT
```

Examples:

```text
"I cannot determine that from the available evidence." -> ABSTAIN_CLEAN
"I cannot determine it, but it was probably Alice or Bob." -> ABSTAIN_SPECULATIVE
"Probably Alice." -> ANSWER_ATTEMPT
```

A benchmark adapter may impose stricter domain-specific rules but may not collapse speculative abstention into clean abstention without explicit justification.

## 6. Atomic-claim evaluation

For long-form answers:

1. extract atomic claims;
2. classify claim verifiability;
3. identify evidence required for each verifiable claim;
4. evaluate each claim independently;
5. aggregate only with declared formulas.

Claim labels:

```text
SUPPORTED
UNSUPPORTED
UNDECIDABLE
UNVERIFIABLE
EXTRACTION_ERROR
VERIFICATION_ERROR
```

Evaluator failures are not model hallucinations.

## 7. Citation evaluation

Citation evaluation has independent dimensions:

```text
EXISTENCE
IDENTITY
ENTAILMENT
COVERAGE
```

Examples of forbidden collapse:

```text
URL resolves -> claim supported
paper exists -> cited sentence entailed
one citation supports one clause -> compound sentence fully supported
```

Where citations are required, evaluators should bind atomic claims to exact cited evidence spans when technically feasible.

## 8. Context faithfulness vs world factuality

These are separate constructs.

A model can be faithful to a deliberately counterfactual context while being false about the real world.

A model can reject a false context and be world-correct while failing a benchmark whose instruction explicitly requires context-only answering.

Therefore store both when relevant:

```text
CONTEXT_FAITHFULNESS
WORLD_FACTUALITY
```

Do not infer one from the other.

## 9. Conflict evaluation

The evaluator must inspect whether conflict is real under the case's source-quality contract.

Possible outcomes:

```text
NO_MATERIAL_CONFLICT
CONFLICT_DETECTED_AND_PRESERVED
CONFLICT_RESOLVED_WITH_SUFFICIENT_EVIDENCE
CONFLICT_FALSELY_RESOLVED
CONFLICT_MISSED
```

The evaluator should not reward permanent indecision when one source is demonstrably superseded or weaker under predeclared evidence rules.

## 10. Tool-trace evaluation

A tool-use evaluator should have access to the trace when the construct depends on it.

Required distinctions:

```text
TOOL_NOT_CALLED
TOOL_CALLED_SUCCESS
TOOL_CALLED_ERROR
TOOL_RESULT_IGNORED
TOOL_RESULT_MISREPRESENTED
TOOL_OUTPUT_FABRICATED
UNNECESSARY_TOOL_CALL
```

Final-answer-only grading is insufficient for causal diagnosis of tool failures.

## 11. Runtime isolation from epistemic scoring

The evaluator must receive runtime status separately.

If the model API times out before an answer exists:

```text
runtime_outcome = MODEL_TIMEOUT
```

Do not synthesize a model answer such as `NOT_ATTEMPTED`.

If a required tool errors and the model correctly reports the tool failure, the tool runtime may be `TOOL_ERROR` while the model epistemic behavior is correct.

## 12. LLM judge policy

LLM judges are allowed when deterministic/structured evaluation is insufficient.

A judge configuration must pin where possible:

```text
provider
model
revision
system prompt
rubric prompt
sampling settings
maximum output
answer-key visibility
reference visibility
```

Store a hash of the complete judge prompt/template.

A mutable alias without an observation date is insufficient provenance for confirmatory work.

## 13. Judge independence

Two calls to the same model with the same prompt are repeated samples, not independent evaluator families.

For high-load-bearing rubric decisions, prefer judges with partially independent failure modes when feasible, for example different model families plus human adjudication on disagreement.

Do not call same-model majority vote `independent verification`.

## 14. Judge validation set

Before a judge is used for confirmatory scoring, validate it on a set with trusted labels.

Validation should include difficult boundary cases relevant to the actual benchmark, including:

- clean abstention vs speculative abstention;
- partial vs correct;
- citation existence vs entailment;
- conflicting evidence;
- counterfactual context;
- tool error vs empty valid result;
- answer with correct core fact plus material contradiction.

Report at minimum:

```text
accuracy or task-appropriate metric
confusion matrix
agreement with human/deterministic labels
error examples
version/date
```

## 15. Evaluator benchmark layer

The AHP evaluation stack should itself be tested using corpora such as:

- RefChecker-style fine-grained claim annotations;
- RAGTruth-style span labels;
- FAVA/FavaBench-style fine-grained hallucination categories;
- other human-labeled evaluator datasets after primary-source review.

These datasets validate the checker. They are not direct evidence that loading AHP prevents hallucinations.

## 16. Disagreement protocol

Never silently coerce evaluator disagreement to pass or fail.

Record:

```text
judge_1_label
judge_2_label
rule_label, if available
human_label, if adjudicated
final_label
adjudication_reason
```

Possible evaluator outcome:

```text
EVALUATOR_DISAGREEMENT
```

If a load-bearing disagreement cannot be adjudicated, mark the item `UNSCORABLE` for that endpoint and report the count.

## 17. Human adjudication

Human adjudicators should be blind to treatment and model identity where feasible.

Adjudication instructions and source access must be standardized.

Human disagreement is evidence about ambiguity, not noise to hide.

For private confirmatory data, preserve adjudication history without publishing secret item content before the study is closed.

## 18. Evaluator leakage

A judge can be contaminated by:

- benchmark prompts in training;
- answer keys supplied in the prompt;
- treatment-specific expected-response examples;
- seeing condition names;
- generated rationales that explicitly state the gold label.

Record exposure in the contamination manifest.

## 19. Evaluator drift

Cloud judges can change during a study.

If the judge revision changes materially during collection:

- split the evaluation into epochs;
- re-score a frozen overlap set where legally/technically possible;
- estimate drift;
- avoid pooling without analysis.

## 20. Evaluator cost is not evidence quality

A more expensive frontier model does not automatically produce a more valid judge.

Judge selection should depend on demonstrated reliability for the exact scoring task.

## 21. No hidden chain-of-thought dependency

The benchmark must not require access to private model chain-of-thought to score epistemic quality.

Use observable outputs, tool traces, environment state and explicit structured confidence where requested.

If a model voluntarily supplies a rationale, it may be analyzed as output, but hidden reasoning is outside the benchmark contract.

## 22. Required evaluator manifest

```yaml
evaluator:
  method: DETERMINISTIC | STRUCTURED_RULE | SPECIALIST_MODEL | MULTI_JUDGE | HUMAN
  implementation_revision: string
  prompt_hash: string | null
  model: string | null
  provider: string | null
  model_revision: string | null
  answer_key_visible: true | false | null
  references_visible: true | false | null
  validated_on: string | null
  validation_revision: string | null
  observation_date: ISO-8601
```

## 23. Confirmatory prohibition

A result is not confirmatory-ready if:

```text
judge prompt is mutable/unversioned
judge has not been validated for the scoring construct
runtime errors are collapsed into task outcomes
critical disagreement is silently majority-voted away
gold leakage differs by treatment arm
scorer behavior changed after outcome inspection
```

## 24. Non-collapse invariants

```text
LLM_JUDGE != ORACLE
MAJORITY_VOTE != GROUND_TRUTH
SAME_MODEL_REPEATED != INDEPENDENT_JUDGES
CITATION_EXISTS != ENTAILMENT
CONTEXT_FAITHFUL != WORLD_TRUE
TOOL_ERROR != MODEL_ABSTENTION
EVALUATOR_ERROR != MODEL_HALLUCINATION
HUMAN_LABEL != INFALLIBLE
```
