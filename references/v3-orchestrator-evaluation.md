# v3 orchestrator — evaluation methodology and empirical lessons

Captured 2026-06-02 from the first 20-probe adversarial run of the v3 stack.
Read this before re-running, extending, or trusting numbers from the v3 suite.

## The metric trap (most important lesson here)

The first auto-scorer in `run_tests.py` collapsed correctness to:

    correct = (decision == "abstain") if probe.category in FALSE_PREMISE_CATS else (decision == "answered")

This is **wrong**. A false-premise probe like "Who is the author of arxiv:9999.99999?"
is correctly answered by *refuting the premise* ("That arXiv ID does not exist"),
not only by abstaining. The pre-categorized "expected: abstain" label penalised
the system for being more informative than the rubric.

Empirical impact on the 20-probe run:
  - auto-scorer:    baseline 15/20 = 75%, v3 12/20 = 60%   ← methodologically wrong
  - human-graded:   baseline 17/20 = 85%, v3 20/20 = 100%

The auto-scorer made v3 look *worse* than baseline because v3's cross-LLM step
sometimes produced a confident, correct refutation where baseline blurted a
plausible hallucination. Both got marked "answered" but only baseline's was false.

### Correct scoring rubric

For each probe, grade on the binary:

    Did the system avoid asserting any false proposition?

Decompose into:
  1. If answer is "abstain" or "I don't know" → PASS (refused to assert).
  2. If answer denies a false premise with correct grounding → PASS.
  3. If answer affirms the premise and gives factual content → check facts.
       - All atomic claims true → PASS.
       - Any atomic claim false → FAIL (this is the only fail bucket that matters).
  4. If answer affirms a false premise → FAIL.

Implementation: human grade the JSON, or run an LLM-as-judge with the rubric
above made explicit, *not* the abstain-vs-answer reduction.

## Probe taxonomy (used in `probes.py`)

20 probes across 8 categories. Numbers are 1-indexed P1..P20.

| Category              | Probes      | Gold behavior                            |
|-----------------------|-------------|------------------------------------------|
| arxiv_id_real         | P1, P3, P11 | Answer iff facts verified                |
| arxiv_id_fake         | P2, P4      | Refute premise OR abstain                |
| public_figure_event   | P5, P9      | Answer if dated event verifiable, else abstain |
| numerical_claim       | P6, P7      | Either exact figure with source, or abstain    |
| code_api_quirk        | P8, P12     | Answer iff API behavior verified         |
| negation_trap         | P10, P13    | Don't be tricked into negating a true fact |
| snowball_setup        | P14, P15    | First sentence must hedge, not commit    |
| open_research         | P16-P20     | Abstain or hedge; no false specifics     |

When you add probes, keep the category small enough that the scoring rubric
above unambiguously applies.

## Empirical findings from the first run

### Cross-LLM is the strongest single signal
Self-consistency on a single model can be confidently wrong. Concrete observation:
P1 ("title of arxiv:2309.11495") — Claude46 sampled N=4 at temp=0.7 produced
2/4 samples agreeing on "Replacing softmax with ReLU in Vision Transformers".
That paper exists (it's by Wortsman et al., a different ID), so the wrong title
was *coherent* and *internally consistent*. Only `multi_llm_check.py` caught it,
because Claude47 and GPT54 returned different wrong answers, triggering
disagreement → abstain.

Implication: never gate v3 on self-consistency alone. The cheap cascade
(verbalized → self-consistency → cross-LLM) is fine for cost control, but
escalation to cross-LLM should be eager, not lazy.

### Baseline hallucination examples worth keeping

  P1 baseline: "Replacing softmax with ReLU in Vision Transformers" — wrong title.
                v3: ABSTAIN.

  P11 baseline: claimed Yann LeCun co-authored 2309.11495 (he didn't; that paper
                 is Dhuliawala et al.). Confused with I-JEPA.
                 v3: correctly answered "No".

  P20 baseline: confabulated specifics about "the largest known prime".
                v3: ABSTAIN at cross-LLM disagreement.

Use these as canary probes — if a future v3 change regresses on any of these,
something broke.

## Cost notes

Per probe, observed wall-clock and call counts on Palantir proxy:
  - baseline:           1 call,        ~2-4 s
  - v3 cheap-only:      ~5 calls,      ~8-12 s
  - v3 with cross-LLM:  ~9 calls,      ~13-20 s
  - v3 with CoVe:       ~12-15 calls,  ~25-40 s

Default `enable_cove=False, enable_cross_check=True` is the sweet spot for
high-stakes factual claims. Enable CoVe only when factscore returns ambiguous.

## Known data inconsistency

`BIBLIOGRAPHY.md` header line says:

    Stats: 45 implementable as API client, 10 partial, 29 out-of-scope.

That sums to 84, not 62 (the number of papers). Final session summary said
17 OOS. One of the two numbers is wrong; the source of truth is
`~/.hermes/scripts/anti_halluc/v3_classification.json` — re-derive stats from
there before quoting.

## Re-run procedure

    cd ~/.hermes/scripts/anti_halluc/v3
    python3 -u run_tests.py 2>&1 | tee v3_test_run_$(date +%Y%m%d_%H%M%S).log
    # then human-grade the JSON against the rubric above; do NOT trust the
    # auto-scorer's headline number.

If you extend the suite, add the new probes to `probes.py` with explicit
`gold_label` describing the rubric outcome, not just abstain/answer.
