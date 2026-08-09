# Evidence state model

This is the conceptual contract behind consequential verification. It is not a requirement to serialize every answer into JSON.

The purpose is to prevent invisible evidence state from disappearing between retrieval, judgment and final wording.

## ClaimRecord

Useful conceptual fields:

```text
claim_id
claim
claim_type
intent_constraint
risk_tier
state
scope
observation_time
residual_unknowns
```

`claim` should be atomic enough that one evidence verdict can meaningfully apply. `intent_constraint` records which user requirement the claim/action serves. `residual_unknowns` prevents `SUPPORTED_WITH_SCOPE` from silently becoming universal truth.

## EvidenceRecord

The machine-readable schema uses these evidence fields:

```text
source
source_class
source_identity
evidence_span
retrieved_at
freshness
integrity
lineage
lineage_basis
lineage_verification
independence_group
entailment
verifier
verifier_failure_state
```

Do not invent values for fields that cannot be established. Use explicit unknown states where available and downgrade the claim when an unknown is load-bearing.

The JSON schema is a storage/shape contract. `scripts/check_evidence_record.py` adds deterministic cross-field invariants that depend on risk tier and claim type. The checker deliberately supports only the schema keywords and schema forms used by the canonical schema and refuses an unknown construct rather than silently ignoring a future constraint.

## Claim states

```text
SUPPORTED_WITH_SCOPE
PARTIAL
CONTRADICTED
CONFLICT
NOT_FOUND_WITHIN_SCOPE
INCONCLUSIVE
ERROR
UNKNOWN_SCOPE
```

Forbidden collapses include `ERROR -> NOT_FOUND`, scoped absence -> global absence, and `PARTIAL`/`INCONCLUSIVE`/`CONFLICT` -> unsupported certainty.

`NOT_FOUND_WITHIN_SCOPE` requires an explicit non-empty inspected scope. Without the search boundary, the negative claim is not structurally complete.

`PARTIAL` requires at least some supporting or partially supporting evidence. A record containing only irrelevant, unclear, or contradictory evidence should use a state that reflects that evidence rather than `PARTIAL` by label alone.

`CONTRADICTED` means decisive contrary evidence remains and no material supporting `ENTAILS` evidence survives in the submitted record. If material support and contradiction both remain unresolved, use `CONFLICT`.

## Entailment

Executable values:

```text
ENTAILS
PARTIAL
CONTRADICTS
IRRELEVANT
UNCLEAR
```

`ENTAILS` means the recorded evidence item is asserted to support the claim within its inspected scope. The deterministic checker validates the label and cross-field contract. It does not prove the semantic assertion.

## Source integrity

```text
CLEAN_OBSERVED
SUSPECT
CONTAMINATED
UNKNOWN
```

`CLEAN_OBSERVED` means no anomaly was observed in the inspected material. It is deliberately weaker than `TRUSTED`.

## Freshness

Executable values:

```text
CURRENT_ENOUGH
STALE
UNKNOWN
NOT_APPLICABLE
```

Freshness is relative to the claim. A ten-year-old specification can be current enough for a stable historical interface; a ten-minute-old market quote can be stale. Historical-only evidence should use `STALE` or `NOT_APPLICABLE` according to claim semantics rather than inventing another machine state.

## Lineage

```text
INDEPENDENT_ORIGIN
DERIVED_COPY
SHARED_ORIGIN
UNKNOWN
```

Lineage verification:

```text
VERIFIED
HEURISTIC
UNKNOWN
```

`independence_group` is a declared grouping label used to catch obvious internal contradictions such as two allegedly independent supporting records reusing the same known origin group.

It is not proof of real-world independence.

Examples of weak independence:

```text
Reuters article -> syndication copy -> search snippet
GitHub README -> blog quoting README -> LLM answer citing the blog
same model + same prompt + same evidence repeated five times
```

Stronger independence can come from materially different failure domains such as source inspection plus runtime execution, specification plus independent conformance testing, distinct primary measurements, or positive evidence plus active falsification.

A `VERIFIED` lineage judgment means there is an auditable external basis for the judgment. The checker can require that a basis and group are recorded. It cannot establish that the provenance claim itself is true.

For strong T3 records, the checker also rejects the obvious internal contradiction of reusing the exact same declared `source` or `source_identity` under multiple allegedly independent groups. Different source strings and different group strings still do not prove external independence.

## Verifier failure state

Executable values:

```text
NONE_OBSERVED
SUSPECT
FAILED
UNKNOWN
```

This field is **not** the same concept as a verifier command's process outcome. A verifier may exit successfully while its evidentiary relevance remains suspect. Conversely, a verifier execution can fail and be recorded as `FAILED`.

A helper's own `PASS`, `FOUND`, `NOT_FOUND`, `ERROR`, or exit code describes that helper's contract. Do not copy those labels blindly into `verifier_failure_state`.

## Strong T3 contract

A strong T3 `SUPPORTED_WITH_SCOPE` verdict must not be earned by labels alone.

For every supporting `ENTAILS` item, the checker requires:

- known `source_class`;
- non-empty `source_identity`;
- non-empty `evidence_span`;
- RFC3339-profile `retrieved_at` with timezone;
- `integrity=CLEAN_OBSERVED`;
- non-empty verifier provenance;
- `verifier_failure_state=NONE_OBSERVED`.

At least one supporting item must additionally declare:

```text
lineage = INDEPENDENT_ORIGIN
lineage_verification = VERIFIED
lineage_basis = non-empty auditable basis
independence_group = non-empty origin/failure-domain group
```

If multiple supporting items claim verified independence, the deterministic checker rejects duplicate non-empty `independence_group` labels and duplicate declared source/source-identity reuse across those groups. These are internal consistency checks. Distinct strings still do not prove external independence.

For T3 `current_state`, a strong verdict additionally requires:

```text
observation_time = RFC3339-profile timestamp with timezone, not materially in the future
freshness = CURRENT_ENOUGH
```

Supporting `retrieved_at` timestamps must use the same accepted profile and not be materially in the future. Python-specific ISO variants such as a space instead of `T` are not accepted. The local deterministic parser intentionally implements the documented profile, not every rare RFC3339 edge such as leap-second semantics.

A stale or unknown freshness state cannot be promoted to current truth merely because the top-level state says `SUPPORTED_WITH_SCOPE`.

## Claim-state aggregation

A conservative sketch:

```text
if required verification fails:
    claim = ERROR or INCONCLUSIVE
elif supporting and contradicting evidence remain unresolved:
    claim = CONFLICT
elif decisive evidence contradicts and no material support survives:
    claim = CONTRADICTED
elif required current-state evidence is stale/unknown:
    claim = INCONCLUSIVE
elif evidence only partially supports the claim:
    claim = PARTIAL
elif sufficient evidence entails the claim within an explicit scope and no unresolved contradiction remains:
    claim = SUPPORTED_WITH_SCOPE
else:
    claim = INCONCLUSIVE
```

Do not add numerical confidence unless there is a calibrated basis for it.

## Intent state

When useful:

```text
ALIGNED
PARTIAL
MISINTERPRETED
OUT_OF_SCOPE
AMBIGUOUS
```

A response can be factually supported and still fail because it answered the wrong request.

## Trajectory state

For consequential multi-step agents, useful earliest-divergence classes are:

```text
PLANNING
RETRIEVAL
REASONING
HUMAN_INTERACTION
TOOL_USE
UNKNOWN
```

The purpose is not perfect step attribution. It is to force inspection of upstream dependencies before patching only the final sentence.

## Why not require every field always?

Because that would make the protocol unusable.

Use the full record for T3 or complicated T2 work. For lower-risk claims, keep only the state needed to prevent the likely failure. This is an adaptive verification heuristic, not a claim that missing fields are universally safe.
