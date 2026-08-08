# Anti-Hallucination Protocol v5.2 - multi-model audit synthesis

This directory archives the raw audit reports that informed the v5.3 hardening pass.

## Method

The reports are deliberately split into two evidence classes. They must not be averaged as if every reviewer observed the same system.

### Hermes Agent execution audits

These reviewers had access to the local repository/runtime and could inspect scripts, schemas, tests, CURRENT, CANDIDATE and/or the installed Hermes parser:

- `deepseek-v4-flash-0731-2.md`
- `gpt-5.6-terra-2.md`
- `sonnet-5-2.md`
- `big-pickle-2.md`
- `nemotron-3-ultra-550b-a55b-2.md`

Executable findings from these reports can become implementation evidence when they include a concrete reproducer, command, exit code and observed result.

### Perplexity document-only audits

These reviewers received exactly `SKILL.md` and `README.md`, plus permission to research public primary sources:

- `PPX-SONAR2.md`
- `PPX-GROK4.5.md`
- `PPX-GLM5.2.md`
- `PPX-KIMIK3.md`
- `PPX-AHP_v5.2_Forensic_Audit.md`

They are useful for document architecture, research grounding, public claims, progressive disclosure and cognitive-load hypotheses. They cannot establish whether repository scripts, tests, schemas or runtime enforcement actually work.

## Evidence hierarchy used in this synthesis

From strongest to weakest:

1. `REPRODUCED` - concrete failure reproduced by an execution-capable audit.
2. `CROSS-CONFIRMED` - independently reproduced or directly confirmed by more than one execution-capable audit.
3. `FILE/WEB VERIFIED` - directly established from inspected source or primary public source.
4. `PLAUSIBLE` - technically credible but not reproduced.
5. `HEURISTIC` - design/cognitive-load judgment requiring behavioral evaluation.
6. `REJECTED` - severity or conclusion does not follow from the evidence.

Model count is not truth. A single minimal reproducer outranks five reviewers repeating the same unsupported intuition.

## Original audit-file manifest

The SHA-256 values below refer to the user-supplied source files before archival. Raw audit files are evidence inputs and should not be edited in place.

| File | Bytes | SHA-256 |
|---|---:|---|
| `deepseek-v4-flash-0731-2.md` | 23493 | `b4efbe21fb2cdc31223825e2d6ac1b83237807c27206b5857015097f7216b08b` |
| `gpt-5.6-terra-2.md` | 12234 | `3a76ba3cd3778b90ef26e0b9d836874485ab93e4920b40169a029847c4b836f2` |
| `sonnet-5-2.md` | 44298 | `e97fa31f85bed87a64eb3aec8993b97639038e38072a88756975dd535ed9f60f` |
| `big-pickle-2.md` | 24377 | `9103cbb26007b866af96b3dd2d0495c9e257dc76ee52a16ffbcf68b11b7f25bd` |
| `nemotron-3-ultra-550b-a55b-2.md` | 41905 | `c4d40024caeb996a53e146a6c3213ee9fc8f36cceeab4770a3f8d6cd34ee97bc` |
| `PPX-SONAR2.md` | 49476 | `85e5ae13e1b287942c73857f38a871a9bfa442af200c3115acaead9316da3e9a` |
| `PPX-GROK4.5.md` | 59062 | `2dd8fccda14221f9fc42e751e467ec00f75fcea845d4e99545fe9939adc2fd1c` |
| `PPX-GLM5.2.md` | 91118 | `4addb24f096248a7be5f7e0090df70daa957676a01478610b293bf23f0eccf20` |
| `PPX-KIMIK3.md` | 58889 | `441bca14c3166e97ed4c393783e00206f6710710c07cea31e84dc8adc48ac64c` |
| `PPX-AHP_v5.2_Forensic_Audit.md` | 48308 | `445ef4d291880da971966e3d2c7f49c4136d0d7d353e8f22be29c4d0b7996665` |

## Consolidated finding ledger

| ID | Finding | Evidence | Severity | Decision |
|---|---|---|---|---|
| F-001 | `check_v5_integrity.py` can return PASS for frontmatter that Hermes/PyYAML rejects or misparses | REPRODUCED by Terra and DeepSeek with different malformed YAML shapes | P1 | FIX |
| F-002 | `independence_group` exists in the model/schema but is not checked for duplicate declared groups in strong T3 support | REPRODUCED by Big Pickle and Nemotron | P1 | FIX narrowly, without pretending group labels prove real independence |
| F-003 | `observation_time`/`retrieved_at` are shape-only strings; impossible/future timestamps can pass | REPRODUCED by DeepSeek and Big Pickle | P2 | FIX deterministic syntax and future-time invariant |
| F-004 | v5 research sources are duplicated in the active `SKILL.md`, while provenance checking does not validate that duplicate list | REPRODUCED by Terra and Big Pickle | P1 | REMOVE duplicate list from active skill and keep canonical manifests/references |
| F-005 | `godmode_battery.sh` writes to installation-external calibration state by default and can produce a partial score after skips/errors | FILE-VERIFIED by Terra against the shipped script | P1/P0 operational hazard | RETIRE from active v5 contract / make legacy status explicit; do not execute during validation |
| F-006 | `EVIDENCE RECORD: PASS` is truth-adjacent wording for a checker that only establishes schema + deterministic invariants | FILE-VERIFIED contract issue; Terra explicitly identified integration risk | P1 | Rename success to `STRUCTURALLY_VALID` |
| F-007 | README checkout liveness command targets the installed skill unless `AHP_SKILL_DIR` is set | REPRODUCED by Terra and DeepSeek | P2 | FIX README command |
| F-008 | Conceptual evidence-state vocabulary drifts from executable schema (`SUPPORTS` vs `ENTAILS`, freshness labels, verifier outcome vs verifier-failure state) | FILE-VERIFIED by Big Pickle/Nemotron and current source inspection | P1/P2 | ALIGN conceptual reference to executable contract; explicitly distinguish execution outcome from failure-state field |
| F-009 | Main `SKILL.md` is dense and carries a large bibliography/reference inventory in always-loaded context | CROSS-CONFIRMED by all document-only PPX audits; behavioral effect remains HEURISTIC | P1 document architecture | FIX packaging; benchmark obedience separately |
| F-010 | The portable public skill includes a local `HSDB = HyperspaceDB` installation convention | FILE-VERIFIED, repeatedly flagged by PPX | P2 | REMOVE from portable main skill |
| F-011 | `consequential` is the main escalation trigger but lacks a compact operational definition | CROSS-CONFIRMED document finding | P1 | DEFINE in the hot path |
| F-012 | README heading `What it catches` can be read as a behavioral guarantee | Document-level finding | P2 | Rename to `Failure modes it targets` / qualify deterministic-vs-policy scope |
| F-013 | Behavioral obedience under long-context/tool pressure is not established by unit tests or Markdown attack cases | Explicitly admitted by v5.2 and cross-confirmed by both audit classes | Architectural unknown | BENCHMARK, not another prose rule |
| F-014 | Native Windows support is not demonstrated for Bash-only liveness/legacy helpers | INFERENCE from shipped shell scripts; no native Windows execution | P2 docs | Clarify support boundary rather than claiming unverified shell portability |
| F-015 | Protocol attack corpus lives under `tests/`, which is not a Hermes progressive-disclosure support directory in the inspected local parser | FILE-VERIFIED by Sonnet | P2 | Add canonical `references/adversarial-cases.md`; keep executable tests under `tests/` |

## Findings intentionally rejected or downgraded

### `"trust me"` as `lineage_basis` is not a deterministic P0

Nemotron labels this a P0. That severity is rejected. A string-shape validator cannot determine whether an arbitrary provenance statement is factually true. The correct contract is to validate that an auditable basis is supplied, clearly state that semantic provenance remains external, and prevent machine PASS from being presented as truth. A blacklist for phrases such as `trust me` would create security theatre.

Decision: KEEP the external-provenance limitation, rename structural PASS, and benchmark/runtime-verify provenance when it matters.

### `CONTRADICTED` does not require supporting `ENTAILS` evidence

Nemotron treats `CONTRADICTED + one CONTRADICTS item` as a false positive. That conclusion is rejected. A claim can be contradicted by decisive contrary evidence without any supporting evidence. `CONFLICT`, not `CONTRADICTED`, is the state that requires evidence on both sides.

Decision: REJECT.

### `PARTIAL` does not have to reject every contaminated item

A partial/inconclusive evidence record may legitimately retain contaminated evidence as an observed input while refusing a strong conclusion. Blanket rejection would erase useful provenance. Strong `SUPPORTED_WITH_SCOPE` already rejects contaminated supporting evidence.

Decision: REJECT blanket prohibition; keep contamination visible and scoped.

### The pipeline is not literally mandatory for T0/T1

Some reports call the pipeline a mandatory ten-stage ritual. The text explicitly says it is a control model and that T0/T1 should not be inflated into ceremony. The cognitive-load concern is real, but the literal `mandatory` claim is not.

Decision: REJECT literal claim, FIX discoverability by putting a small hot path first and moving deep material to references.

### Add `PLAUSIBLY_INDEPENDENT`

Rejected. It adds another epistemic label without solving provenance. `UNKNOWN` plus an auditable explanation is safer than a new confidence-like state.

### Require terminal toolset for skill activation

Rejected. The policy layer remains useful when deterministic helpers are unavailable. Hard-gating the entire skill on a terminal would remove citation, intent, prompt-injection, current-state and completion controls from environments that still need them.

Decision: document degraded mode instead.

## v5.3 accepted change set

The next release should be a hardening + compression release, not another feature pile.

1. Replace the hand-rolled frontmatter acceptance decision with real YAML parsing compatible with Hermes semantics, while retaining explicit required-key/profile checks.
2. Add regression probes for the exact malformed YAML shapes reproduced by Terra/DeepSeek.
3. Validate RFC3339 timestamps for T3 current-state support and reject implausible future `observation_time` beyond a small clock-skew allowance.
4. Detect duplicate non-empty `independence_group` values among evidence items that claim verified independent support. This only catches self-declared internal inconsistency; it does not prove true independence.
5. Rename successful evidence-record output from `PASS` to `STRUCTURALLY_VALID` and update tests/docs.
6. Remove duplicated research bibliography/source lists from active `SKILL.md`. Keep canonical research identity in manifests/reference documents.
7. Align `evidence-state-model.md` vocabulary with executable schema/checker terminology.
8. Define `consequential` operationally near the risk-tier entry point.
9. Remove the local HSDB convention from the portable public skill.
10. Move the protocol-level adversarial case reference into `references/` while retaining executable tests in `tests/`.
11. Clarify README liveness validation command and Windows/Bash boundary.
12. Make legacy v3/godmode scripts explicitly non-load-bearing. Do not present historical calibration machinery as portable v5 health.
13. Preserve the explicit hard limit that Markdown, source labels and deterministic shape validation do not prove semantic truth or runtime obedience.

## Deferred work

These are not v5.3 Markdown fixes:

- real behavioral obedience benchmark across model classes;
- runtime/output gate or Hermes hook;
- provenance graph / source-origin resolution;
- live world-state adapters;
- semantic entailment verifier;
- judge-bias evaluation harness;
- native Windows execution matrix.

## Bottom line

v5.2 is a clear architectural improvement over the installed v2 in evidence-state discipline, verifier failure handling, current-state reasoning, prompt-injection awareness and testability. The audit also shows that green unit tests did not close several executable contract gaps.

v5.3 should therefore get smaller in its active instruction plane while becoming stricter at the deterministic boundaries that machines can actually check.
