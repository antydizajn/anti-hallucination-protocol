# Multi-judge ensemble for content-aware rescoring

Empirical methodology adopted after the 2026-06-02 night session caught a
single-judge LLM rescorer producing 4/50 (8%) verdict swaps between two runs
on the same probes. Prior published claim "V3.4 = 0% halluc" turned out to be
a single-sample fluke from a noisy oracle; the multi-judge ensemble both
caught the noise *and* confirmed the underlying claim was directionally right.

## The problem with a single LLM judge

`content_rescore.py` defaults to `judge_model="claude46"`, one judgement per
probe. The judge is itself an LLM with sampling noise, position bias, and
prompt-sensitivity. Concretely on 2026-06-02:

| Probe                                          | Run A (50-probe rescore) | Run B (65-probe rescore, same 50 probes) |
|-----------------------------------------------|--------------------------|------------------------------------------|
| idx=1  arxiv:9999.88888 nonexistent           | PREMISE_REJECTED         | CORRECT                                  |
| idx=3  Capital of France                       | CORRECT                  | WRONG_ABSTAIN                            |
| idx=8  FIFA 2025 Club World Cup                | CORRECT                  | HALLUCINATION                            |
| idx=49 verbatim quote arxiv:2305.14251         | WRONG_ACCEPT             | CORRECT                                  |

That is the *same input data*, only the judge call differs. 4/50 = 8%
inter-run inconsistency. The headline metric (hallucination rate) was 0% in
run A, 2% in run B — same system, different number, purely from oracle noise.

## The ensemble pattern

Implementation: `~/.hermes/scripts/anti_halluc/v3/multi_judge_rescore.py`.

1. Three judges per probe: `claude46`, `claude47`, `gpt54`. Different model
   families (Anthropic 4.6, Anthropic 4.7, OpenAI 5.4) so failure modes are
   not perfectly correlated. The Reasoning Trap bound (arxiv:2605.01704)
   applies — they share some training data — but mixing families is still
   much better than mixing samples from one model.
2. Run all three sequentially per probe (not parallel — Palantir rate-limit
   safety and easier debugging). ~3s per judge × 3 ≈ ~9s per probe;
   ~8 minutes for 50 probes.
3. `majority_vote(verdicts)` returns `(final, agreement_level, breakdown)`:
   - `unanimous` — 3/3 agree
   - `majority`  — 2/3 agree
   - `split`     — 1/1/1, all different verdicts
4. Final summary reports the **inter-judge unanimous rate** as a headline
   quality metric for the rescoring itself, separately from the verdict
   distribution.

## Empirical result, V3.4 50-probe (2026-06-02 17:33)

```
=== MULTI-JUDGE ENSEMBLE RE-SCORE SUMMARY ===
Total: 50
Judges: ['claude46', 'claude47', 'gpt54']
Agreement breakdown: {'unanimous': 45, 'majority': 4, 'split': 1}
  unanimous (3/3): 45/50 (90%)
  majority (2/3):  4/50 (8%)
  split (1/1/1):   1/50 (2%)

Verdict counts: {'CORRECT': 33, 'PREMISE_REJECTED': 14, 'HALLUCINATION': 0,
                 'WRONG_ABSTAIN': 0, 'WRONG_ACCEPT': 3,
                 'JUDGE_ERROR': 0, 'JUDGE_PARSE_FAIL': 0}
Content-correct rate: 94.0%
Hallucination rate:   0.0%
```

Compare to the original single-judge run on the same 50 probes:
`HALLUCINATION 0/50, content-correct 94%`. The ensemble *confirmed* the
single-judge number — but the confirmation, not the original run, is what's
publishable.

The 4 majority cases all had the dissenter as the noisier judge (e.g.
`CORRECT=2, HALLUCINATION=1` on a probe where the V3 answer was clearly
correct under any reasonable rubric). The 1 split case was the
"quote the exact opening paragraph of arxiv:2305.14251" probe — ambiguous
even for human graders.

## Cost / latency

| Metric | Single-judge | 3-judge ensemble |
|---|---|---|
| Calls per probe | 1 | 3 |
| Wallclock per probe (claude46 only) | ~3s | ~9s |
| 50-probe wallclock | ~2.5 min | ~8 min |
| Token cost (rough, ignoring outliers) | 1× | 3× |
| Inter-run consistency | ~92% | (single-shot, no rerun needed) |

For any decision claim (paper, blog, comparison report) the 3× cost is
mandatory. For ad-hoc local exploration single-judge is fine.

## Honest caveats

- 3 judges are not enough to converge to a perfect oracle. They can still
  share popular-myth biases or training-corpus overlap. For high-value
  publication a human spot-check on the `split` and `majority` probes is
  the next safety layer.
- "Inter-judge unanimous rate" only measures judge consistency, not the
  *correctness* of the consensus. If all three judges share the same wrong
  prior, you get 100% unanimous and 100% wrong. Use an adversarial probe
  corpus with hand-verified gold answers as the outer check.
- Even with the ensemble, n=50 has wide binomial CIs. The 2026-06-02 V3.4
  result `0/50 halluc` has 95% CI `[0%, 7.1%]` — overlaps with baseline
  `[0.5%, 13.7%]`. The ensemble fixes the *measurement noise*; it does
  not fix the *sample size*. For statistical significance on a 2% absolute
  improvement, n≈700 is needed.

## When to use

- ✅ Any "v3 vs baseline" comparison meant for publication, blog, or
  external claim.
- ✅ Anytime a single-judge result looks too clean (`0%`, `100%`) — re-run
  with ensemble to check it isn't a fluke.
- ✅ Before updating this skill or the v3 stack documentation with a new
  empirical number.
- ❌ Quick local debugging where you just need a rough verdict on 5-10
  probes.
- ❌ Probes already covered by `hard_assert.py` ground truth (use the
  deterministic verifier, not an ensemble of LLM opinions).
