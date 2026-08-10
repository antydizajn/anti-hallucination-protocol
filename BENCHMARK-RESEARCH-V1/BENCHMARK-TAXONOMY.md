# AHP Benchmark Taxonomy v1

## Purpose

Map benchmarks to the failure mechanism they measure.

Do not combine unrelated capabilities into one headline number.

---

# Layer 1 - Parametric Knowledge

Question:

Does the model know facts from internal knowledge and avoid unsupported guessing?

Primary:

- AA-Omniscience
- SimpleQA Verified
- FACTS Parametric
- KGHaluBench

Metrics:

- correct answer rate
- incorrect attempt rate
- clean abstention rate
- useful coverage

---

# Layer 2 - Epistemic Boundary

Question:

Does the model know when it does not know?

Primary:

- AbstentionBench
- Abstain-QA
- ConfidenceBench

Metrics:

- abstention precision
- abstention recall
- selective accuracy
- calibration
- unnecessary refusal

---

# Layer 3 - Temporal Reality

Question:

Does the model distinguish stale knowledge from current state?

Primary:

- FreshQA
- SealQA
- live rotating batteries

Metrics:

- freshness verification
- stale acceptance
- false current-state claims

---

# Layer 4 - Grounding

Question:

Does evidence actually support the generated claim?

Primary:

- FACTS Grounding
- FaithEval
- RGB
- RAGuard

Metrics:

- evidence entailment
- unsupported claim rate
- context override errors

---

# Layer 5 - Conflict Handling

Question:

Does the model preserve uncertainty when evidence conflicts?

Primary:

- WhoQA
- RGB
- conflicting-context batteries

Metrics:

- conflict preservation
- arbitrary resolution
- false certainty

---

# Layer 6 - Long Form

Question:

Does factuality degrade over long answers?

Primary:

- LongFact
- SAFE
- FActScore
- VERISCORE
- FactBench
- WildHallucinations

Metrics:

- atomic claim accuracy
- unsupported atomic claims
- citation coverage

---

# Layer 7 - Citation

Question:

Does a citation actually support the statement?

Primary:

- ALCE
- HalluHard citation tasks
- RefChecker

Metrics:

- citation existence
- identity
- entailment
- coverage

---

# Layer 8 - Agent and Tool Reliability

Question:

Does the agent remain grounded when tools fail or return unexpected output?

Primary:

- ToolFailBench
- AgentHallu
- HalluWorld terminal tasks

Metrics:

- tool output fabrication
- tool result ignoring
- unnecessary tool usage
- error laundering

---

# Layer 9 - Evidence Security

Question:

Can untrusted evidence manipulate the agent?

Primary:

- BIPIA
- AgentDojo
- LivePI

Metrics:

- injection success rate
- instruction/data boundary failure
- unauthorized action rate

---

# Layer 10 - AHP Native

Must be created specifically for this protocol.

Families:

- user pressure without evidence
- user pressure with new evidence
- ERROR != absence
- installed != loaded != obeyed
- completion overclaim
- stale memory versus fresh observation
- correlated evidence pretending to be independent
- restart/compaction durable state
- unnecessary ceremony negative controls

---

# Reference world requirement

Every serious AHP release should include both:

REAL WORLD:

- realistic but noisy
- web drift
- uncertain labels

REFERENCE WORLD:

- exact state
- deterministic truth
- controllable adversarial changes

HalluWorld is an example of this direction.
