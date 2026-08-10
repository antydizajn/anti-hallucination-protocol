# AHP RESTART - MASTER RESEARCH PLAN

## Status

`NORMATIVE EXECUTION MAP`

This document defines the order of work for AHP-RESTART-1 from measurement landscape through the first admissible intervention test.

It exists to prevent a second form of the original failure:

```text
BUILDING A BEAUTIFUL EVALUATION STACK
BEFORE DEFINING
WHERE MEASUREMENT DEVELOPMENT ENDS
AND THE EXPERIMENT ACTUALLY BEGINS
```

This plan therefore contains an explicit:

```text
PRE-EXPERIMENT BUILD PHASE
FREEZE POINT
USER RUN POINT
POST-D0 DECISION
POST-D1 DECISION
INTERVENTION ADMISSION POINT
```

No treatment efficacy claim exists today.
No AHP replacement architecture is admitted today.

---

# 0. Research question

The active scientific question is NOT:

```text
Can we make AHP look better than CONTROL?
```

It is:

```text
Can we construct a valid measurement system that first reveals
whether a stable and practically important hallucination-related
failure exists under unmodified CONTROL, and only then test a
preregistered minimal intervention against independent sealed evidence?
```

This question permits all scientifically valid terminal states:

```text
NO ADEQUATE MEASUREMENT
NO STABLE TARGET
CONTROL_WINS
NO_EFFECT
HARM
MIXED
INCONCLUSIVE
TREATMENT_WINS
```

---

# 1. Non-negotiable ordering

```text
1. MEASUREMENT LANDSCAPE
2. INSTRUMENT QUALIFICATION
3. EVIDENCE POOL ASSIGNMENT
4. FROZEN MEASUREMENT / CAUSAL CONTRACT
5. EXECUTABLE MEASUREMENT HARNESS
6. FREEZE POINT
7. D0 CONTROL-ONLY MEASUREMENT PILOT
8. D0 REVIEW
9. D1 CONTROL DISCOVERY
10. D1 FAILURE-CLUSTER REVIEW
11. HYPOTHESIS LOCK
12. INTERVENTION ADMISSION
13. MINIMAL TREATMENT IMPLEMENTATION
14. ONE-SHOT D2 TEST
15. TRANSFER
```

Forbidden inversion:

```text
INTERVENTION IDEA
-> PICK BENCHMARKS
-> DEFINE METRIC
-> RUN UNTIL WIN
```

---

# 2. Phase A - Measurement landscape

## Objective

Identify the available measurement instruments before selecting an AHP treatment target.

## Input

Existing public benchmark research is allowed as discovery material only.

All previously inspected benchmark content defaults to:

```text
D0_MEASUREMENT_DEVELOPMENT
```

unless a separate unexposed split/shard can legitimately receive another role.

## Required work

Build a landscape of approximately 30-100 or more serious candidates across relevant constructs.

Candidate discovery must cover, where instruments exist:

```text
parametric factuality
knowledge boundary
abstention
calibration
false premises
underspecification
positive evidence use
temporal freshness
long-tail knowledge
long-form factuality
RAG grounding
RAG attribution
citation existence
citation entailment
citation completeness
contradictory evidence
tool failure
tool-result contradiction
tool-result absence
agent completion overclaim
long-context evidence loss
prompt injection in evidence
reference-world tasks
multimodal factuality
```

The count of benchmark names is not evidence diversity.

## Every serious candidate must record

```text
identity
version/revision
primary source
construct measured
construct NOT measured
task type
interaction type
answerability structure
positive-evidence cases
abstention-required cases
grader
grader dependencies
human validation
runtime requirements
public/private/dynamic status
contamination evidence
contamination unknowns
lineage
shared upstream data
shared generator
shared grader
overlap signals
license
access
cost
candidate evidence role
```

## Exit

Phase A does not select a treatment.

It produces a defensible map of available rulers.

---

# 3. Phase B - Instrument qualification and panel selection

## Objective

Select a measurement panel because it provides construct coverage and defensible measurement, NOT because AHP performs well on it.

## Selection principle

```text
MAXIMIZE:
  construct coverage
  positive/negative utility balance
  grader reliability
  lineage diversity
  causal interpretability
  reproducibility

MINIMIZE:
  redundancy
  contamination risk
  grader dependence
  lexical shortcuts
  degenerate-policy exploitability
  uncontrolled runtime dependence
```

## Explicitly forbidden selection criterion

```text
AHP SCORE
```

No treatment result may be used to choose the measurement panel.

## Mandatory degenerate-policy checks

Where relevant, the measurement design must later be able to distinguish a useful model from:

```text
ALWAYS_ABSTAIN
ALWAYS_ANSWER
KEYWORD_OR_SURFACE_HEURISTIC
RANDOM_POLICY
ALWAYS_TOOL
NEVER_TOOL
COPY_CONTEXT
```

A benchmark on which a trivial strategy can satisfy the claimed endpoint without violating a hard utility guardrail is not sufficient as a primary instrument.

## Output

A frozen candidate panel with:

```text
primary candidates
secondary candidates
D0 development candidates
D1 discovery candidates
D2 confirmatory candidates or acquisition plan
T transfer candidates
excluded instruments
lineage map
contamination map
grader-risk map
open measurement gaps
```

---

# 4. Phase C - Evidence pool assignment

## Objective

Prevent the same evidence from teaching the project what to build and then being presented as independent proof that it works.

## Evidence worlds

```text
D0 = MEASUREMENT DEVELOPMENT
D1 = CONTROL DISCOVERY
D2 = SEALED PROMOTION
T  = EXTERNAL / TEMPORAL TRANSFER
```

## D0

May teach us about measurement.

Allowed:

```text
adapter debugging
grader debugging
scorer debugging
session-isolation tests
runtime debugging
variance estimation
null measurement controls
positive measurement controls
stub baselines
```

D0 is not final treatment confirmation.

## D1

CONTROL-only discovery evidence.

Allowed:

```text
estimate real CONTROL failure burden
identify stable failure clusters
study heterogeneity
identify candidate causal mechanisms
generate hypotheses
```

Once D1 influences an intervention:

```text
D1 cannot confirm that intervention
```

## D2

Single-use sealed treatment evaluation.

Before treatment freeze, treatment designers must not access:

```text
item instances
reference answers
CONTROL failures on D2
grader outcomes on D2
attack-instance content
```

Once results are exposed:

```text
D2 = BURNED
```

A modified descendant intervention cannot reuse it as fresh confirmation.

## T

Transfer evidence from a materially different relevant lineage, temporal refresh, independent source, maintainer, generator, or evaluation surface where feasible.

D2 success without transfer does not justify a broad generalization claim.

---

# 5. Phase D - Gate 2 frozen measurement and causal contract

## Objective

Freeze the inferential game before substantive outcome-dependent intervention design.

This phase must resolve all disagreements that hostile reviews left as assumptions rather than facts.

## Must be frozen

```text
scientific estimand
one primary endpoint
utility weighting
hard utility/safety guardrails
SESOI
model panel
benchmark panel
D0/D1/D2/T assignments
randomization unit
analysis unit
fresh-session definition
runtime boundary
missingness rules
error rules
exclusion rules
grader identity/version/prompt
judge validation requirements
stub policies
null measurement control
positive measurement control
multiplicity plan
attempt/hypothesis budget
stopping rules
sample-size/power algorithm
maximum resource ceiling
holdout access policy
claim language
protocol invalidation rules
```

## Unresolved assumptions that MUST NOT be silently inherited

The hostile reviews proposed materially different values for:

```text
primary endpoint:
  SCU
  CNEU
  harmonic competence minus harm penalty

confirmatory budget:
  2 attempts
  or up to 3 hypotheses

alpha allocation:
  0.025 x 2
  0.0167 x 3
  or another preregistered project-level allocation

utility non-inferiority margins:
  approximately -3 pp
  or approximately -5 pp

SESOI / target effect:
  commonly around 0.05
  but not unanimously

sample floors:
  reviewer proposals differ materially
```

Therefore these are Gate 2 decisions requiring explicit justification.

They are not copied into code as if already established.

## Endpoint metrology requirement

Before freezing the primary endpoint, compare candidate endpoint formulations on D0/stub/synthetic measurement scenarios.

The chosen endpoint must, at minimum:

```text
not reward ALWAYS_ABSTAIN as an optimal general strategy
not reward ALWAYS_ANSWER as an optimal general strategy
retain meaningful answer/task utility
penalize unsupported commitment
permit clean warranted abstention or escalation
have an interpretable practical-effect scale
```

This is measurement validation, not AHP tuning.

---

# 6. Phase E - Build the executable research instrument

## Objective

Deliver a runnable system that can execute D0 and D1 without containing an AHP treatment.

## Required executable components

```text
benchmark adapters
runner
CONTROL lock machinery
fresh-session launcher
runtime/environment capture
raw evidence logger
grader implementation
scorer implementation
stub policies
null measurement control
positive measurement control
randomization/blocking implementation
analysis pipeline
power/simulation tooling
pool-access enforcement
holdout manifest tooling
reproducibility manifest
protocol-integrity checks
```

## Raw data requirement

Every final summary must be regenerable from raw evidence and frozen analysis code.

At minimum preserve:

```text
study_id
attempt_id
gate
dataset_partition
model/provider/snapshot
arm
session_id
block_id
task_id
construct/axis
execution order
wall times
system/config/tool hashes
workspace initial-state hash
prompt hash
response hash
raw response location
answerability state
action class
score components
grader identity/version/output hash
eligibility/exclusion state
runtime error
tool error
timeout
override state
```

## Critical prohibition

This executable system must not contain:

```text
new AHP behavioral rules
new AHP treatment prompt
new AHP evidence hierarchy
new treatment-specific decision tree
new architecture optimized against known benchmark failures
```

It is a ruler, not the medicine.

---

# 7. PRE-EXPERIMENT FREEZE POINT

This is the required STOP before live measurement begins.

The project pauses when all of the following exist and are frozen:

```text
Gate 1 PASS
Gate 2 PASS
measurement panel
pool assignments
CONTROL identity
adapters
runner
raw trace schema
grader
scorer
randomization
session isolation
error semantics
stub baselines implementation
null control implementation
positive measurement control implementation
analysis code
power procedure
D0 manifest
D1 manifest or allocation rules
D2 holdout commitment/acquisition plan
T transfer plan
claim vocabulary
protocol invalidation rules
```

At this point:

```text
NO AHP TREATMENT EXISTS
```

This is intentional.

---

# 8. USER RUN POINT - D0

After the pre-experiment freeze, the first live run is:

```text
D0 CONTROL-ONLY MEASUREMENT PILOT
```

## D0 asks

```text
Does the measurement system work?
```

NOT:

```text
Does AHP work?
```

## D0 should test

```text
adapter correctness
grader reliability
answerability-label behavior
session isolation
runtime stability
provider drift detection
variance
ICC/session dependence
scoring degeneracy
stub ceilings
null measurement control
positive measurement control
cost
resource feasibility
whether SESOI is measurable
```

## Null measurement control

A recommended instrumentation check is equivalent CONTROL configurations under different labels.

Expected effect:

```text
approximately zero
```

A material artificial difference is evidence of harness, temporal, grading, assignment, or session-state problems.

## Positive measurement control

Use a deliberately obvious non-AHP perturbation expected to move a known endpoint.

Purpose:

```text
show that the ruler can detect a real known difference
```

It is not treatment validation.

---

# 9. POST-D0 DECISION

D0 has only measurement conclusions.

## D0 PASS

Allowed when the frozen criteria establish adequate:

```text
adapter correctness
grader validity
runtime separation
session independence assumptions
stub behavior
null control behavior
positive control behavior
variance estimation
power feasibility
```

Then proceed to D1.

## D0 FAIL

If the instrument is inadequate:

```text
STOP EFFICACY PROGRAM
REPAIR MEASUREMENT
```

Examples:

```text
judge too unstable
answerability labels unreliable
runtime errors collapse into model behavior
stub exploits scorer
null control produces material fake effect
positive control cannot be detected
SESOI cannot be resolved inside resource ceiling
session dependence cannot be modeled honestly
```

Measurement repair may iterate on D0.

It does not justify writing treatment code.

---

# 10. USER RUN POINT - D1 CONTROL DISCOVERY

After D0 passes, run:

```text
D1 = UNMODIFIED CONTROL ONLY
```

No treatment arm.
No placebo arm.
No AHP v6.

## D1 asks

```text
Where does CONTROL actually fail?
How large is the burden?
How stable is it?
Across which models?
Across which independent lineages?
Under which runtime conditions?
```

## Required outputs

```text
CONTROL baseline summary
failure-cluster map
failure prevalence/burden
model heterogeneity
lineage heterogeneity
runtime sensitivity
uncertainty intervals
candidate causal explanations
alternative explanations
measurement caveats
```

## Important

D1 is allowed to inspire the treatment.

That is exactly why it is no longer independent confirmation for that treatment.

---

# 11. POST-D1 DECISION

D1 must be allowed to terminate AHP before any new intervention is built.

## Outcome A - no stable target

If no failure cluster meets the preregistered eligibility standard:

```text
DO NOT BUILD TREATMENT
```

Record:

```text
NO MEASURED TARGET LARGE/STABLE ENOUGH TO JUSTIFY INTERVENTION
```

This is a successful scientific outcome.

## Outcome B - measurement still inadequate

If apparent clusters depend primarily on unstable labels, noisy judges, provider drift or unresolved session dependence:

```text
MEASUREMENT / PHENOMENON NOT STABLE ENOUGH
```

No treatment admission.

## Outcome C - eligible failure cluster exists

Only then may the project freeze a treatment hypothesis.

---

# 12. Hypothesis lock

Before intervention implementation, freeze:

```text
hypothesis_id
target failure cluster
observed D1 evidence
proposed causal mechanism
important alternative explanations
falsification condition
minimal treatment scope
allowed changed components
forbidden changed components
expected primary direction
expected guardrail behavior
D2 strata relevant to the hypothesis
attempt budget consumption rule
treatment-spec commitment
```

The hypothesis must be falsifiable.

Bad:

```text
AHP should improve reliability generally
```

Better structure:

```text
CONTROL failure cluster C is hypothesized to arise from mechanism M.
A minimal intervention modifying component X is expected to improve
primary endpoint Y on preregistered C-relevant D2 strata while preserving
utility guardrails G1..Gn.
Failure to exceed the SESOI or violation of a hard guardrail rejects this
intervention family according to the frozen stopping rule.
```

---

# 13. Intervention admission point

Only after:

```text
Gate 1 PASS
Gate 2 PASS
D0 PASS
D1 complete
eligible cluster identified
hypothesis locked
D2 unopened
D2 commitment valid
attempt budget available
```

may the project create active intervention implementation.

The first intervention should be minimal and cluster-specific.

Do not build a broad multi-component AHP architecture and then search ablations for the component that appears to work.

---

# 14. D2 confirmatory experiment

## Arms

Expected default structure:

```text
C = frozen unmodified CONTROL
P = matched PLACEBO where required for mechanism attribution
T = frozen TREATMENT
```

The exact design is frozen in Gate 2/hypothesis lock.

## Session rule

```text
SESSION IS THE RANDOMIZATION UNIT
```

Each arm executes in a separate fresh session.

Forbidden:

```text
C -> P -> T
inside one persistent context-bearing session
```

Counterbalancing balances execution order across independent sessions.
It does not justify arm crossover inside the same stateful context.

## Matching/blocking

Where applicable, matched sets preserve:

```text
model snapshot
task block
runtime/tool configuration
context regime
time batch
```

## Blinding

Where feasible:

```text
grader blinded to arm
human adjudicator blinded to arm/model identity
pair order randomized
D2 items hidden from treatment designers until reveal
```

## One-look rule

No:

```text
10% preview
sanity peek at treatment outcome
intermediate efficacy dashboard
repair treatment and continue same D2
```

D2 is revealed once according to the frozen analysis.

Then:

```text
D2 = BURNED
```

---

# 15. D2 verdict vocabulary

The pipeline must be able to emit exactly honest scientific states such as:

```text
TREATMENT_WINS
CONTROL_WINS
NO_EFFECT
HARM
MIXED
INCONCLUSIVE
PROTOCOL_INVALID
```

## NO_EFFECT

Must require practical-null/equivalence evidence according to the frozen SESOI rule.

It is NOT:

```text
p > 0.05
```

## INCONCLUSIVE

Used when uncertainty is too wide or protocol validity prevents resolution.

It is not renamed:

```text
promising
trend
almost significant
```

inside the confirmatory verdict.

## HARM

Any preregistered hard utility/safety guardrail failure may veto promotion according to Gate 2.

---

# 16. Attempt budget

The project MUST have a finite project-wide confirmatory budget.

The exact budget is unresolved until Gate 2 because hostile reviews proposed both:

```text
2 confirmatory attempts
```

and:

```text
up to 3 mechanistically distinct hypotheses
```

The final number and multiplicity allocation must be frozen before D1-dependent intervention implementation.

Invariant regardless of final number:

```text
ONE ADAPTIVE INTERVENTION GENERATION
CONSUMES
ONE FRESH SEALED CONFIRMATORY SHARD
```

Failed confirmatory evidence is not recycled.

When the frozen budget is exhausted:

```text
AHP-RESTART-1 CLOSES
```

A genuinely new scientific theory may start a new research program with new preregistration and new evidence.

Moving goalposts inside the exhausted project is forbidden.

---

# 17. Transfer phase

A D2 win supports only the frozen evaluation scope.

For a broader claim, use materially different transfer evidence.

Questions:

```text
Does the direction survive another lineage?
Does it survive temporal refresh?
Does it survive another model family where claimed?
Does it survive another relevant runtime surface?
```

If D2 succeeds but transfer fails:

```text
MIXED
```

No broad promotion.

---

# 18. Exact handoff boundary for the current work

## What the current research-building agent should complete BEFORE STOP

### Gate 1

```text
complete serious benchmark landscape
primary-source verification
per-benchmark reviews
lineage records
contamination ledger
grader-risk register
pool assignment
measurement-gap analysis
Gate 1 decision
```

### Gate 2

```text
endpoint metrology and final primary endpoint choice
SESOI decision
hard utility guardrails
model panel
benchmark panel
randomization plan
analysis-unit definition
fresh-session contract
grader contract
missingness/error/exclusion contracts
multiplicity and attempt-budget decision
power procedure
stopping rules
claim vocabulary
D2 access/consumption protocol
preregistration
```

### Executable research instrument

```text
adapters
runner
CONTROL lock
fresh-session launcher
raw trace logger
grader
scorer
stubs
null control
positive measurement control
randomization/blocking
analysis pipeline
power simulation
manifest/provenance system
reproducibility checks
```

### Final pre-run audit

Before STOP, hostile-review the frozen measurement system itself.

Question:

```text
Could this system generate a publishable negative result
and actually stop AHP if CONTROL wins?
```

If NO:

```text
DO NOT HAND OFF FOR TESTING
```

## Then STOP

No treatment implementation.

The user receives a frozen runnable research package plus exact run instructions for D0.

---

# 19. What the user runs after STOP

## Run 1

```text
D0 CONTROL-ONLY MEASUREMENT PILOT
```

Return artifacts:

```text
raw logs
grader validation
stub results
null control result
positive control result
variance/session-dependence estimates
runtime failure report
cost report
power-feasibility output
measurement anomalies
```

## Research review

Classify:

```text
D0 PASS
D0 FAIL
D0 INCONCLUSIVE
```

Only D0 PASS admits D1.

## Run 2

```text
D1 CONTROL DISCOVERY
```

Return artifacts:

```text
raw logs
CONTROL summary
failure clusters
cluster stability
model heterogeneity
lineage heterogeneity
candidate mechanisms
uncertainty
```

Then pause again for scientific review before any intervention exists.

---

# 20. Second mandatory pause

After D1:

```text
DO NOT AUTOMATICALLY BUILD AHP
```

Review must answer:

```text
1. Is there a stable failure cluster?
2. Is its burden practically meaningful?
3. Is it reproduced across sufficient independent evidence?
4. Is it likely addressable by a protocol-level intervention?
5. Is measurement adequate to resolve the claimed treatment effect?
6. What observation would falsify the proposed mechanism?
```

If these answers do not justify intervention:

```text
STOP
```

If they do:

```text
HYPOTHESIS LOCK
-> INTERVENTION ADMISSION
```

---

# 21. What must NOT happen before the first STOP

Forbidden:

```text
write AHP v6
write a new anti-hallucination prompt
import the old behavioral policy as the new design
optimize against known benchmark failures
run treatment arms while choosing the benchmark panel
choose metrics because they flatter a candidate treatment
peek at D2
write an attack-answer reference file for treatment
use old 151 tests as effectiveness evidence
claim behavioral improvement
```

Allowed:

```text
measurement research
benchmark research
adapter code
runner code
grader/scorer code
provenance code
statistical code
CONTROL-only instrumentation
neutral infrastructure salvage after revalidation
```

---

# 22. Success criteria for the current build phase

The pre-experiment build is successful when the repository contains a frozen measurement system that can truthfully produce any of these outcomes without code or metric changes:

```text
MEASUREMENT_INADEQUATE
NO_STABLE_TARGET
CONTROL_WINS
NO_EFFECT
HARM
MIXED
INCONCLUSIVE
TREATMENT_WINS
```

The build phase is NOT successful merely because:

```text
all tests are green
many benchmark adapters exist
the runner executes
JSON schemas validate
CI passes
```

Those establish engineering properties, not behavioral efficacy.

---

# 23. Current project state

As of this plan's creation:

```text
Gate 1: OPEN
Gate 2: NOT FROZEN
D0 live run: NOT STARTED
D1 live run: NOT STARTED
hypothesis lock: DOES NOT EXIST
intervention admission: DENIED
D2: NOT OPENED
behavioral efficacy: UNKNOWN
```

Immediate next work:

```text
finish Gate 1 landscape qualification
and evidence pool assignment
before writing additional runner implementation
```

---

# 24. Final invariant

```text
WE ARE NOT BUILDING AHP YET.
WE ARE BUILDING THE EXPERIMENT THAT EARNS OR DENIES
THE RIGHT TO BUILD AHP.
```

After that experiment reaches the first freeze point, implementation work stops and live D0 testing begins.
