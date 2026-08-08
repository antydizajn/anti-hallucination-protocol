# GPT-5.6 Sol - v5.4 Fresh-Clone Adversarial Audit Methodology Review

Date: 2026-08-08
Model: GPT-5.6 Sol
Target repository: `antydizajn/anti-hallucination-protocol`
Target release reviewed: `5.4.0`
Review class: methodology and contract review, not a full execution audit

## Scope and evidence boundary

This document records my independent opinion on the proposed fresh-clone forensic audit methodology for Anti-Hallucination Protocol v5.4.0, together with a limited source review of the current standalone repository documentation and archived audit synthesis.

I inspected the standalone repository target and verified that the current `SKILL.md` declares `version: 5.4.0`. I also reviewed the current `README.md` and `AUDITS/SUMMARY.md` sufficiently to assess whether the proposed audit methodology is aligned with the repository's stated deterministic and behavioral boundaries.

I did not perform a fresh local clone, execute the full test suite, mutate isolated fixtures, or run the complete adversarial battery described by the proposed forensic prompt. Therefore this file must not be interpreted as an execution-capable v5.4 correctness audit.

The correct evidence label for the central conclusion is:

```text
FILE-VERIFIED + METHODOLOGY REVIEW
```

not:

```text
REPRODUCED FULL AUDIT
```

## Executive opinion

The standalone repository direction is correct.

The most important methodological improvement is the decision to stop treating the historical `hermes-skills/software-development/anti-hallucination-protocol` copy as the audit target and instead require a fresh clone of:

```text
https://github.com/antydizajn/anti-hallucination-protocol
```

That boundary matters because an audit that mixes historical copies, installed copies and current standalone files cannot reliably distinguish a present defect from an already-fixed regression.

The proposed audit prompt also gets the central adversarial standard right:

```text
Do not try to confirm that v5.4 is good.
Try to break it.
```

That is exactly the correct posture for this project. A protocol whose purpose is to reduce false confidence should itself be evaluated primarily against false-positive failure modes:

```text
FALSE PASS
FALSE FOUND
FALSE VERIFIED
FALSE SUPPORTED
FALSE SUCCESS
SPEC != SCHEMA
SCHEMA != CHECKER
DOCS != IMPLEMENTATION
TESTS PASS != PROPERTY HOLDS
POLICY CLAIM != RUNTIME REALITY
```

The strongest future audit synthesis should aggregate reproduced failure mechanisms and minimal reproducers, not model votes.

One reproduced deterministic failure from one auditor is stronger evidence than six models saying that the code "looks suspicious".

## Main methodological defect: historical audit contamination

The proposed prompt currently contains a significant sequencing contradiction.

It tells the auditor in the repository inventory phase to read the entire repository, including `AUDITS/**`, but later asks for a novel failure hunt that should not be anchored by previous audits.

Those requirements are incompatible.

Once a model has read `AUDITS/SUMMARY.md`, it has already been exposed to the historical failure hypotheses and dispositions. It cannot later make a clean claim that the same hypotheses were independently rediscovered.

For a real multi-agent audit, `AUDITS/**` should be quarantined during the independent attack phase.

Recommended sequence:

```text
FRESH CLONE
    ->
INVENTORY METADATA ONLY FOR AUDITS/**
    ->
BASELINE EXECUTION
    ->
TEST-SUITE AUDIT
    ->
COMPONENT ATTACKS
    ->
CROSS-COMPONENT ATTACKS
    ->
NOVEL FAILURE HUNT
    ->
ONLY THEN READ AUDITS/**
    ->
HISTORICAL RECONCILIATION
```

During the initial inventory, the auditor may record audit filenames, sizes and hashes, but should not read their contents.

After the independent hunt, historical findings can be classified as:

```text
ALREADY REDISCOVERED
STILL REPRODUCIBLE
FIXED
REGRESSED
NOT REPRODUCED
OUT OF SCOPE
NEWLY RELEVANT
```

This change is critical if the goal is to compare GPT-5.6 Terra, Claude Sonnet, DeepSeek, Kimi, Nemotron and other auditors without correlated-review contamination.

## Exact release identity should be 5.4.0

The proposed prompt accepts an expected version series of:

```text
5.4.x
```

That is weaker than the repository's own current integrity contract.

The present standalone skill declares exactly:

```text
5.4.0
```

and the repository documentation states that the v5.4 integrity checker intentionally pins the exact public release so that another v5 release cannot silently receive the same integrity PASS.

Therefore the forensic audit target should also be exact:

```text
EXPECTED VERSION: 5.4.0
```

If the target later becomes 5.4.1, the audit prompt should be deliberately updated. Silent acceptance of any `5.4.x` weakens reproducibility and can accidentally merge two release states into one audit corpus.

## Source checkout should be evidence-only

The current read-only boundary is conceptually correct but operationally incomplete.

Running `pytest`, Python scripts or shell scripts inside the source checkout can still create caches, bytecode, temporary files or other ignored artifacts. `git status --short` is not sufficient to prove that no filesystem mutation occurred because ignored files can remain invisible.

A cleaner forensic design is to use three separate roots:

```text
SOURCE_ROOT
EXEC_ROOT
ATTACK_ROOT
```

with these contracts:

```text
SOURCE_ROOT
- fresh clone
- evidence-only after target verification
- no project code executed here

EXEC_ROOT
- disposable copy of SOURCE_ROOT
- baseline tests and canonical checkers run here

ATTACK_ROOT
- disposable copy of SOURCE_ROOT
- intentionally malformed schemas, records, fixtures and mutation probes run here
```

This removes ambiguity between evidence preservation and execution side effects.

## Capture the environment before interpreting failures

A cross-model audit is not useful if environment differences are invisible.

Before running project tests, every auditor should record at minimum:

```text
uname -a
python3 --version
python3 -m pytest --version
git --version
bash --version
command -v python3
command -v pytest
command -v hermes
```

If Hermes is available, also record:

```text
Hermes version
Hermes executable path
Hermes installation/source path
Hermes commit if obtainable
frontmatter parser implementation
local modification status if determinable
```

Otherwise a difference between two auditors may be misattributed to model reasoning when the real cause is Python, PyYAML, shell, filesystem or Hermes runtime drift.

## Hermes must not automatically be treated as a canonical oracle

The proposed prompt correctly wants to compare `check_v5_integrity.py` with the actual Hermes parser when possible.

However, the local Hermes installation must itself be qualified before it is used as an oracle.

Recommended oracle classification:

```text
CANONICAL_CURRENT
CURRENT_BUT_LOCALLY_MODIFIED
STALE
UNKNOWN_PROVENANCE
```

Only a sufficiently established current canonical runtime should support a strong finding of the form:

```text
INTEGRITY PASS
HERMES LOAD FAIL
```

A stale or locally modified Hermes installation is still useful evidence, but it is evidence about that runtime, not automatically about the current Hermes contract.

## Separate prompt-mandated probes from genuinely novel probes

The proposed forensic prompt already contains many concrete attack ideas.

That is good for coverage but creates a measurement problem. An auditor should not receive credit for "novel" testing when it merely executes attack classes supplied directly by the prompt.

The report should separate:

```text
PROMPT-MANDATED PROBES
AGENT-INVENTED NOVEL PROBES
```

A probe should count as novel only when its underlying failure hypothesis was not explicitly supplied by the forensic prompt and was not learned from `AUDITS/**`.

This distinction is important if the audit corpus will later be used to compare model quality.

## Every expected result needs an expected basis

Adversarial testing becomes weak when the audit prompt itself silently defines the specification.

For every claimed mismatch, the auditor should record not only:

```text
EXPECTED:
ACTUAL:
```

but also:

```text
EXPECTED BASIS:
```

with one or more of:

```text
SCHEMA
CHECKER CONTRACT
SKILL
README
STATE MODEL
TEST CONTRACT
HERMES RUNTIME
INFERRED INVARIANT
AUDIT PROMPT ONLY
```

A mismatch against `AUDIT PROMPT ONLY` is not automatically a repository bug.

The repository must first establish that the tested behavior is actually part of its own contract.

This is especially important for semantic areas where the project explicitly limits deterministic guarantees.

## Respect the project's semantic boundary

The current standalone documentation makes several important limitations explicit:

- the skill is a policy layer plus narrow deterministic helpers;
- it is not a truth oracle;
- it is not a guaranteed runtime gate;
- `STRUCTURALLY_VALID` is not semantic truth;
- declared independence groups do not prove real-world source independence;
- passing unit tests do not establish behavioral obedience under long-context pressure;
- helpers are invoked explicitly rather than automatically enforced by Hermes merely because the skill is loaded.

An adversarial audit should not keep rediscovering these stated limitations and promote them into P0/P1 findings unless the implementation or documentation contradicts its own boundary.

The productive question is narrower:

```text
Does the implementation violate the deterministic contract it actually claims?
```

Examples of legitimate high-value findings would include:

```text
STRUCTURALLY_VALID despite a deterministic invariant violation
FOUND despite verifier failure
mandatory liveness failure with exit 0
integrity PASS for a release/frontmatter state the checker claims to reject
schema assertion silently ignored despite a fail-closed schema contract
```

By contrast, the inability of a local structural checker to prove real-world truth is not itself a defect when the repository explicitly says it cannot do that.

## Resource-abuse probes should be bounded

Tests involving huge stdout, huge stderr, timeouts or malformed processes are valuable, but the audit prompt should impose resource ceilings.

Suggested limits:

```text
additional disk: <= 256 MiB
intentional RAM allocation: <= 512 MiB
stdout/stderr generation: <= 32 MiB per probe
single-probe runtime: <= 30 seconds
no fork bombs
no unbounded process creation
```

The goal is to expose a property with the smallest sufficient reproducer, not to stress the host until it becomes the failure source.

## Add an explicit historical reconciliation phase

After the independent novel hunt, the auditor should finally inspect `AUDITS/**` and compare current results with historical findings.

For every historical finding:

```text
ID:
ORIGINAL CLAIM:
CURRENT STATUS:
CURRENT REPRODUCER:
CURRENT EVIDENCE:
```

Then report:

```text
HISTORICAL FINDINGS REDISCOVERED INDEPENDENTLY
HISTORICAL FINDINGS MISSED BY THIS AUDITOR
NOVEL FINDINGS ABSENT FROM HISTORICAL AUDITS
```

This produces much more useful model-comparison data than a single 0-10 score.

## Add an audit self-check

The final report should audit its own evidential quality.

Recommended counters:

```text
PROMPT-MANDATED PROBES EXECUTED:
PROMPT-MANDATED PROBES SKIPPED:

AGENT-INVENTED HYPOTHESES:
NOVEL PROBES ACTUALLY EXECUTED:
NOVEL PROBES ONLY REASONED ABOUT:

HISTORICAL AUDITS READ BEFORE NOVEL HUNT:
MUST BE: NO

COMMANDS CLAIMED:
COMMANDS WITH CAPTURED OUTPUT:
COMMANDS WITH CAPTURED EXIT CODE:

FINDINGS WITH REPRODUCER:
FINDINGS WITHOUT REPRODUCER:

P0 CLAIMS:
P0 WITH DETERMINISTIC REPRODUCTION:

UNVERIFIED CLAIMS IN THIS REPORT:
```

This makes it harder for an auditor to generate a persuasive-looking report whose own evidence trail is incomplete.

## Multi-model synthesis rule

If multiple Hermes Agents receive this audit, they should receive the same prompt in fresh sessions and should not be given the conclusions of the other auditors before finishing their independent hunt.

The final synthesis should aggregate by reproduced failure mechanism, not by model count.

Recommended hierarchy:

```text
1. Minimal reproducer + command + actual output + exit code
2. Independently reproduced same failure by another auditor
3. Direct source/runtime verification
4. Plausible but unreproduced hypothesis
5. Heuristic design concern
6. Model vote or unsupported suspicion
```

A single reproducible false-positive path should outrank majority opinion.

Likewise, six models repeating the same historical hypothesis after reading the same `AUDITS/SUMMARY.md` are not six independent confirmations.

## Bottom line

My current judgment is:

```text
AUDIT METHODOLOGY DIRECTION: STRONG
STANDALONE TARGET BOUNDARY: CORRECT
FALSE-POSITIVE PRIORITY: CORRECT
CURRENT PROMPT READY AS-IS: NO
PROMPT READY AFTER SEQUENCING/HYGIENE FIXES: YES
```

The largest issue is not missing attack coverage. The prompt already has extensive attack coverage.

The largest issue is experimental hygiene.

For the next audit wave, the critical improvements are:

1. quarantine historical audit contents until the independent hunt is complete;
2. pin the exact target release to `5.4.0`;
3. separate immutable source evidence from execution and attack copies;
4. record environment/runtime provenance;
5. qualify Hermes before treating it as an oracle;
6. distinguish supplied probes from genuinely novel probes;
7. require an `EXPECTED BASIS` for each claimed mismatch;
8. bound adversarial resource use;
9. reconcile historical audits only after independent testing;
10. make the report audit itself;
11. synthesize reproduced failures, not model votes.

If those changes are made, the proposed protocol audit becomes substantially more falsifiable, more reproducible and more useful as a real multi-model adversarial benchmark.

The standard I would apply to v5.4 is simple:

```text
Do not reward confidence.
Reward reproduced failure discovery.
Do not reward model agreement.
Reward independent reproduction.
Do not punish the system for limitations it explicitly declares.
Punish it when its deterministic output claims more than its own contract earned.
```

That is the right test for an anti-hallucination protocol.