# AUDIT_ITERATIONS — AHP

Output folder for the GPT-5.6-SOL 10-iteration audit of the
Anti-Hallucination Protocol (protocol defined in AHP_AUDIT_TASK.md).

Planned files (created by the auditor during its run):

- iter_01.md   first audit: critique + suggestions + prompt + answer
- iter_02.md   improved prompt + improved answer (change log included)
- ...
- iter_10.md   final iteration
- FINAL_SYNTHESIS.md  best prompt + best answer + surviving top changes

Convention per file (MANDATORY):

1. CRITIQUE (what is wrong / weak / risky / missing / over-claimed)
2. CONCRETE SUGGESTIONS (numbered, actionable, with rationale)
3. IMPROVED PROMPT (full text of the next prompt)
4. IMPROVED ANSWER (full text of the improved audit answer)
5. CHANGE LOG (what changed in prompt and answer vs previous iteration)

Every file self-contained: full prompt + full answer inside.
