# Evidence state model

This is a conceptual contract for consequential verification. It is not a requirement to serialize every answer into JSON.

The purpose is to prevent invisible state from disappearing between retrieval, judgment and final wording.

## ClaimRecord

Minimum conceptual fields:

```text
claim_id
claim_text
claim_type
intent_constraint
risk_tier
volatility
current_state_required
verification_state
residual_unknowns
```

### Notes

- `claim_text` should be atomic enough that one evidence verdict can meaningfully apply.
- `intent_constraint` records which user requirement this claim/action serves. A factually correct claim can still be irrelevant or violate the requested scope.
- `current_state_required` distinguishes timeless/historical claims from claims that need fresh observation.
- `residual_unknowns` prevents `SUPPORTED within scope` from silently becoming `universally true`.

## EvidenceRecord

For complicated T2 or consequential T3 work, an auditable evidence item can need:

```text
source_uri_or_pointer
source_class
source_identity
source_version_or_date
retrieved_at
freshness_status
authority_basis
integrity_status
lineage_or_origin
lineage_basis
lineage_verification
independence_group
evidence_span
entailment_status
contradiction_status
scope
verifier_kind
verifier_provenance
verifier_status
notes
```

Do not invent values for fields that cannot be established. Use `UNKNOWN` explicitly and downgrade the verdict when an unknown is load-bearing.

The JSON schema is intentionally a storage/shape contract. `scripts/check_evidence_record.py` adds cross-field invariants that depend on risk tier and claim type.

## Strong T3 contract

A strong T3 `SUPPORTED_WITH_SCOPE` verdict must not be earned by labels alone.

For supporting evidence, v5.2 requires an auditable source identity, evidence span, retrieval time, verifier provenance and a clean observed verifier state. `source_class=unknown` cannot earn a strong T3 verdict.

If an item is labelled `INDEPENDENT_ORIGIN`, that label alone is not evidence. A strong T3 verdict requires:

```text
lineage = INDEPENDENT_ORIGIN
lineage_verification = VERIFIED
lineage_basis = non-empty auditable basis
```

The deterministic checker can verify that these fields are present and internally consistent. It cannot prove that the asserted provenance is true. That remains an external evidence problem.

For T3 `current_state`, a strong verdict additionally requires:

```text
observation_time = explicit observation time
freshness = CURRENT_ENOUGH
```

A stale or unknown freshness state cannot be promoted to current truth merely because another field says `SUPPORTED_WITH_SCOPE`.

## Evidence states

### Entailment

```text
SUPPORTS
CONTRADICTS
PARTIAL
IRRELEVANT
INCONCLUSIVE
NOT_CHECKED
```

### Source integrity

```text
CLEAN_OBSERVED
SUSPECT
CONTAMINATED
UNKNOWN
```

`CLEAN_OBSERVED` means no anomaly was observed in the inspected material. It is deliberately weaker than `TRUSTED`.

### Freshness

```text
CURRENT_ENOUGH
STALE_FOR_CLAIM
HISTORICAL_ONLY
UNKNOWN
NOT_APPLICABLE
```

Freshness is relative to the claim. A ten-year-old specification can be current; a ten-minute-old stock price can be stale.

### Verifier execution

```text
PASS
FAIL
ERROR
PARTIAL
UNKNOWN_SCOPE
```

A verifier `PASS` describes the verifier's contract, not global truth.

## Independence groups

`independence_group` exists to prevent fake source multiplicity.

Examples:

```text
Reuters article -> syndication copy on site A -> snippet on site B
```

All three may belong to one underlying origin group if B/A merely reproduce Reuters.

```text
GitHub README -> blog post quoting README -> LLM answer citing blog
```

These do not constitute three independent confirmations.

Strong independence can come from materially different failure domains, for example:

- source code inspection + executable runtime observation,
- official specification + independent conformance test,
- two primary measurements by separate systems,
- positive evidence + active falsification via a different mechanism.

Independence remains a provenance judgment. `VERIFIED` means there is an auditable basis for that judgment, not that a string field has magically made two sources independent.

## Source classes

Useful coarse classes:

```text
LIVE_SYSTEM
SOURCE_CODE
OFFICIAL_DOCS
PRIMARY_RESEARCH
PRIMARY_DATA
SECONDARY_REPORTING
USER_PROVIDED
MEMORY
LOG
SEARCH_SNIPPET
LLM_GENERATED
OTHER
```

No class is automatically true. The class influences what claims it can reasonably support.

## Claim-state aggregation

A claim may be `SUPPORTED_WITH_SCOPE` only when all load-bearing requirements are satisfied within a declared scope.

A conservative aggregation sketch:

```text
if any decisive evidence CONTRADICTS and conflict is unresolved:
    claim = CONFLICT
elif verifier execution ERROR/PARTIAL prevents required coverage:
    claim = INCONCLUSIVE or UNKNOWN_SCOPE
elif required current-state evidence is STALE/UNKNOWN:
    claim = INCONCLUSIVE
elif evidence is topically relevant but entailment is PARTIAL:
    claim = PARTIAL
elif sufficient evidence SUPPORTS, coverage is adequate, and no unresolved contradiction remains:
    claim = SUPPORTED_WITH_SCOPE
else:
    claim = INCONCLUSIVE
```

Do not add numerical confidence unless there is a calibrated basis for it.

## Intent state

Fact checking is not enough. Record whether the output/action satisfies the user's actual request:

```text
ALIGNED
PARTIAL
MISINTERPRETED
OUT_OF_SCOPE
AMBIGUOUS
```

A response can be `factually supported + intent misinterpreted` and should still be considered a failed answer.

This is motivated by FAITHQA / intent hallucination research:
https://aclanthology.org/2025.acl-long.349/

## Trajectory state

For multi-step agents, a later correct-looking action can descend from an earlier bad premise. For consequential loops, track the earliest known divergence class:

```text
PLANNING
RETRIEVAL
REASONING
HUMAN_INTERACTION
TOOL_USE
UNKNOWN
```

This taxonomy is informed by AgentHallu (arXiv:2601.06818):
https://arxiv.org/abs/2601.06818

The protocol does not claim perfect step attribution. The purpose is to force the agent to inspect upstream dependencies rather than patch only the final sentence.

## Why not require all fields always?

Because that would make the skill unusable.

Use the full state model for T3 or complicated T2 claims. For low-risk claims, keep only fields needed to prevent the likely failure. This selective use is a **HEURISTIC** consistent with the adaptive verification budget.
