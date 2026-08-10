# AA-Omniscience-600 Hermes Runbook

## Purpose

Execute the public AA-Omniscience battery as an external calibration condition.

This does not prove general hallucination reduction.

## Required A/B/C conditions

Use the same:

- Hermes version;
- model/provider;
- sampling settings;
- tools;
- environment;
- question revision.

Conditions:

A: CONTROL

- AHP absent.
- No AHP preload.

B: LEGACY

- Exact AHP `v2.0.0`.
- Explicit preload.

C: CURRENT

- Exact AHP `v5.4.2` release commit:

```
94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

- Explicit preload.

## Preparation

Verify dataset identity first:

```bash
python3 verify_source.py ./source
```

Prepare prompts without gold answer leakage:

```bash
python3 prepare_questions.py ./source/AA-Omniscience_dataset_public.csv ./run/questions.jsonl
```

## Execution

For every condition record:

- run id;
- model identity;
- Hermes commit;
- profile;
- AHP state;
- transcript hash;
- evaluator version.

Do not claim:

```
installed == loaded
loaded == obeyed
```

## Scoring

After independent adjudication:

```bash
python3 score_aa.py adjudicated.json scores.json
```

Report all metrics:

- correct;
- incorrect;
- partial;
- not attempted;
- attempt rate;
- wrong among attempts;
- useful coverage;
- aggregate score.

## Allowed conclusion

"AHP changed this tested model configuration on AA-Omniscience-Public revision X."

## Forbidden conclusion

"AHP solved hallucinations."
