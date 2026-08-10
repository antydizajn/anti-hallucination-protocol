# Human Evaluation Protocol

Human evaluation is a separate evidence channel, not a privileged truth oracle.

## Appropriate human-evaluation targets

Humans are especially useful for:

- whether wording overstates available evidence;
- whether uncertainty is communicated appropriately;
- whether an answer preserves the user's actual intent and scope;
- whether abstention is excessive or insufficient;
- whether a response creates misleading confidence despite technically correct caveats;
- whether the protocol harms usefulness, task completion, readability, or decision quality;
- normative, governance, authorization, and acceptable-risk judgments.

Humans are not automatically superior factual sensors for:

- live service state;
- exact repository contents;
- timestamps;
- numerical transformations;
- API/runtime behavior;
- source provenance that can be measured directly.

Use stronger direct observation where available.

## Blind evaluation

For A/B behavioral evaluation, prefer:

```text
same task
same model/provider/runtime
same tool permissions
same surrounding context
randomized condition
A = baseline/control
B = AHP-loaded
```

The evaluator should not know which condition produced which answer when feasible.

Do not expose implementation labels such as `AHP`, `control`, `anti-hallucination`, or expected hypothesis before scoring.

## Evaluation unit

A human evaluator scores observable output, not hidden reasoning.

Recommended dimensions:

```text
factual overclaim
false completion claim
false absence claim
citation/claim mismatch
stale-current-state claim
uncertainty calibration
appropriate abstention
excessive hedging
intent preservation
task completion
action safety
clarity
```

Each dimension should use an explicit rubric rather than an overall "good/bad" impression.

## Independence and correlation

Record:

- evaluator identity or stable pseudonym;
- whether the evaluator knows the project authors;
- whether the evaluator saw the hypothesis;
- whether the evaluator saw other scores before scoring;
- professional/domain expertise where relevant;
- conflicts of interest;
- whether several evaluators discussed cases together.

Three humans who score together are not three independent blinded judgments.

## Disagreement

Preserve disagreement.

Do not average away a material split without inspecting the reason.

Possible outcomes:

```text
AGREEMENT
MATERIAL_DISAGREEMENT
RUBRIC_AMBIGUITY
DOMAIN_EXPERTISE_REQUIRED
INSUFFICIENT_CONTEXT
```

## Ground-truth cases

When a task has externally verifiable ground truth, human scoring should not replace it.

Use deterministic or direct ground truth first, then human evaluation for qualities that ground truth does not capture.

## Publication rule

Report human-evaluation results with:

```text
N cases
N evaluators
blinding status
randomization status
model/runtime
condition definitions
rubric
inter-rater agreement when meaningful
missing/excluded cases
raw score distribution
```

Do not publish only a single aggregate score.
