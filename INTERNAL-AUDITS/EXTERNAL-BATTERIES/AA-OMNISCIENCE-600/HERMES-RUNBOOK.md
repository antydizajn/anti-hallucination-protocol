# AA-Omniscience-600 Hermes Runbook

## Purpose

Execute AA-Omniscience-Public as an external factual-calibration battery for AHP.

This does not prove general hallucination reduction.

## Frozen conditions

All three arms MUST use the same model, provider, reasoning setting, question bytes, source revision, Hermes runtime family, no-tools policy, and question order.

- A CONTROL: AHP absent and not discoverable.
- B LEGACY: exact AHP v2.0.0, commit `b71cc9d06b58c8f12e06b77606a279f536a18959`, SKILL.md git blob `2de9613a846771db159d041ab0e75bf92805b9a4`.
- C CURRENT: exact AHP v5.4.2 release commit `94bfd13f9c4818a949775bd73c1c0d91ce6a3116`, SKILL.md git blob `0860d4547a5e8e7ed27221724da0cdaaf33a1b41`.

Installation/discoverability is only a precondition. It is not load evidence.

## Why this runner does not use Hermes `-z`

At the inspected Hermes source reference `03fa32c92dd445eb64c7f67434dd91b32c40701d`, the top-level parser accepts `-s/--skills`, `--reasoning`, and `--in`, but the `-z` dispatch does not propagate those fields into `run_oneshot`.

Therefore this battery intentionally uses fresh, non-interactive `hermes chat -q ... -Q` sessions. That execution path propagates skill preload, reasoning, and working-directory state. The runner then reads the isolated profile `state.db` and requires the expected AHP preload marker to be present for B/C and absent for A.

Do not replace this with `-z` unless the exact runtime is re-audited and preload/cwd/reasoning propagation is demonstrated.

## 1. Fresh A/B/C profiles and frozen treatment bytes

Use the shared harness preparation for a new repetition slug:

```bash
bash INTERNAL-AUDITS/RUNNERS/bootstrap_profiles.sh aar001
bash INTERNAL-AUDITS/RUNNERS/install_frozen_ahp.sh aar001
```

The AA runner refuses to execute without the frozen-treatment identity record written by `install_frozen_ahp.sh`.

## 2. Verify the pinned public dataset

```bash
python3 INTERNAL-AUDITS/EXTERNAL-BATTERIES/AA-OMNISCIENCE-600/verify_source.py ./aa-source
```

This downloads the artifact from pinned revision:

```text
4a8ffc87c4650054825fb767fe0da4a4fc97ff32
```

and writes `SOURCE-IDENTITY.json` containing the observed artifact SHA256 and schema identity.

`AA SOURCE: PASS` is source-integrity evidence only. It is not a behavioral benchmark result.

## 3. Prepare answer-generation prompts

```bash
python3 INTERNAL-AUDITS/EXTERNAL-BATTERIES/AA-OMNISCIENCE-600/prepare_questions.py \
  ./aa-source/AA-Omniscience_dataset_public.csv \
  ./aa-run/questions.jsonl \
  --source-identity ./aa-source/SOURCE-IDENTITY.json
```

The generated JSONL is cryptographically bound to the verified CSV identity and intentionally omits gold answers.

Invariant:

```text
GOLD ANSWER MUST NOT ENTER ANSWER-GENERATION CONTEXT
```

## 4. Execute one arm

Example CONTROL:

```bash
python3 INTERNAL-AUDITS/EXTERNAL-BATTERIES/AA-OMNISCIENCE-600/run_aa_arm.py \
  aar001 A openrouter openai/gpt-5.6 \
  ./aa-run/questions.jsonl ./aa-run/A \
  --reasoning high
```

Run B and C with identical provider/model/reasoning/question bytes and distinct output directories.

`--limit N` with `N < 600` is smoke testing only and cannot be reported as a complete benchmark run.

## Runtime preflight and evidence

Before the first model call the runner fail-closes unless it can establish:

- verified question-source identity;
- fresh named Hermes profile;
- exact frozen AHP treatment bytes for B/C;
- CONTROL AHP absence/discoverability boundary for A;
- effective `hermes prompt-size --json` tool count of zero after applying the no-tools profile policy;
- stable Hermes runtime identity;
- immutable run identity for safe resume.

For every question the runner creates one fresh Hermes chat session. It records the persisted session ID, answer, token/billing fields available in `state.db`, and expected-vs-observed AHP preload state.

A treatment-load mismatch, nonzero Hermes exit code, missing persisted answer, unexpected session creation, or recorded tool call is a runtime `ERROR`. The runner stops fail-closed.

```text
ERROR != NOT_ATTEMPTED
```

The tool-surface preflight proves the effective inspection agent exposed zero tool schemas under that profile/configuration. It must not be inflated into a universal claim about every possible Hermes execution path.

## Resume semantics

`RUN-IDENTITY.json` binds at least:

- arm/treatment;
- provider/model/reasoning;
- Hermes executable/version identity;
- runner bytes;
- questions JSONL hash;
- pinned source revision and observed source artifact SHA256;
- profile config hash;
- frozen AHP identity;
- no-tools preflight evidence.

Existing `responses.jsonl` rows are reused only when their run-identity hash matches exactly. Any mismatch aborts instead of mixing runs.

## Question order

Order is frozen as `question_id` 1..600 for every arm. Because each question is a fresh session, there is no cross-question conversational carryover. Do not reorder only one arm.

## Semantic adjudication

Execution completion is not semantic correctness.

After independent adjudication, provide an evaluator identity and exactly 600 records with `run_status: OK` plus one outcome:

- `CORRECT`
- `INCORRECT`
- `PARTIAL`
- `NOT_ATTEMPTED`

Then run:

```bash
python3 INTERNAL-AUDITS/EXTERNAL-BATTERIES/AA-OMNISCIENCE-600/score_aa.py adjudicated.json scores.json
```

A runtime error is rejected by the scorer and must be rerun. It cannot be relabeled as epistemic abstention.

## Required reporting

Report at minimum:

- correct count;
- incorrect count;
- partial count;
- not-attempted count;
- attempt rate;
- incorrect rate among attempts;
- useful coverage;
- AHP diagnostic aggregate;
- evaluator identity/type/version;
- PUBLIC / NOT_HELD_OUT warning.

The diagnostic aggregate emitted by `score_aa.py` is not claimed to be the official upstream AA-Omniscience leaderboard metric.

## Claim boundary

Allowed after a valid completed and adjudicated comparison:

> Under the recorded model/runtime configuration, A/B/C differed by X on this pinned public AA-Omniscience battery.

Forbidden from this battery alone:

> AHP solved hallucinations.

Also forbidden before runtime:

> AHP improves AA-Omniscience.

Until real model execution and adjudication occur, behavioral effect remains `RUNTIME_UNVERIFIED` / `UNVERIFIED`.
