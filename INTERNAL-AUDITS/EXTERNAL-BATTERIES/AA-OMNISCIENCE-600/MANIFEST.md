# AA-Omniscience-600 Manifest

```yaml
battery: AA-OMNISCIENCE-600
classification:
  - EXTERNAL
  - PUBLIC
  - NOT_HELD_OUT
source:
  repository: ArtificialAnalysis/AA-Omniscience-Public
  revision: 4a8ffc87c4650054825fb767fe0da4a4fc97ff32
  artifact: AA-Omniscience_dataset_public.csv
  artifact_sha256: OBSERVED_AT_RUNTIME
conditions:
  A: CONTROL
  B: LEGACY
  C: CURRENT
ahp:
  legacy:
    version: v2.0.0
    commit: b71cc9d06b58c8f12e06b77606a279f536a18959
    skill_blob: 2de9613a846771db159d041ab0e75bf92805b9a4
  current:
    version: v5.4.2
    commit: 94bfd13f9c4818a949775bd73c1c0d91ce6a3116
    skill_blob: 0860d4547a5e8e7ed27221724da0cdaaf33a1b41
execution:
  unit: one fresh Hermes chat session per question
  mode: chat_query_quiet
  question_order: question_id_ascending_1_to_600
  tools: forbidden
  gold_answers_in_generation_context: forbidden
scoring:
  semantic_grading: external_to_score_aa.py
  evaluator_identity: required
  runtime_error_as_not_attempted: forbidden
```

## Identity contract

Dataset identity is not the human-readable dataset name. A valid run binds:

```text
source repository
+ pinned source revision
+ artifact name
+ observed artifact SHA256
+ schema identity
+ generated questions SHA256
```

The observed artifact SHA256 is written by `verify_source.py`; it is intentionally not fabricated or hardcoded before retrieval.

## Treatment contract

B/C are valid treatments only when exact installed `SKILL.md` bytes match the frozen git blobs above and the runtime session evidence shows the preload was actually applied.

```text
INSTALLED != LOADED
DISCOVERABLE != LOADED
PRELOAD REQUESTED != PRELOAD OBSERVED
```

CONTROL must remain unable to discover/load AHP.

## Run identity contract

`run_aa_arm.py` writes an immutable `RUN-IDENTITY.json` and refuses a resume when any bound field changes, including model/provider/reasoning, questions bytes, source artifact identity, runner bytes, Hermes identity, profile configuration, treatment identity, or tool-surface preflight.

## Result boundary

A complete execution means 600/600 successful runtime executions for one arm. It does not mean the answers were semantically correct.

A complete scientific comparison additionally requires independent semantic adjudication of all three arms under the same evaluator identity/version.

Before those executions exist:

```text
AA DATA RUNTIME: UNVERIFIED unless verify_source.py was actually executed
AA BEHAVIORAL RUNTIME: RUNTIME_UNVERIFIED
AHP EFFECT: UNVERIFIED
```
