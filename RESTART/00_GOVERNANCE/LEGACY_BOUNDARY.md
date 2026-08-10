# Legacy and Development Evidence Boundary

## Status

Normative governance artifact for AHP-RESTART-1.

## 1. Old repository state

The pre-restart AHP architecture is forensic evidence only unless a component is separately re-admitted as neutral infrastructure.

The following do NOT count as behavioral efficacy evidence:

- old green regression suites;
- structural integrity checks;
- liveness/install checks;
- old AHP behavioral prompts;
- old self-authored adversarial batteries;
- old attack-class reference material;
- old efficacy expectations;
- prior treatment-specific scoring thresholds.

The old project may establish narrow structural or mechanism facts about itself. It does not establish that loading AHP improves real model behavior.

## 2. Existing benchmark-research-v1 material

Everything under:

```text
BENCHMARK-RESEARCH-V1/
```

is classified by default as:

```text
D0 = MEASUREMENT DEVELOPMENT
```

because its benchmark names, constructs, source notes, scoring ideas and methodology have already been exposed to the intervention-design process.

It may be reused for:

- landscape discovery;
- source triage;
- benchmark metadata;
- adapter design;
- measurement debugging;
- grader validation;
- scoring research;
- contamination analysis;
- statistical planning.

It may NOT be re-labeled as sealed confirmatory evidence for an intervention whose design was informed by it.

## 3. Exposed attack material

Any attack scenario, failure class, prompt, expected response, benchmark item, rubric boundary or grader behavior already inspected by the project is development-exposed.

Allowed roles:

```text
DEVELOPMENT
THREAT_MODEL
HARNESS_TEST
ENGINEERING_REGRESSION
```

Forbidden role:

```text
SEALED_UNSEEN_CONFIRMATORY
```

Renaming or paraphrasing exposed material does not restore blindness.

## 4. Salvage rule

Default rule:

> KEEP MEASUREMENT PLUMBING. DO NOT KEEP BEHAVIORAL THEORY BY DEFAULT.

Potentially salvageable after fresh review:

- hashing primitives;
- manifest validation;
- deterministic serialization;
- generic schema validation;
- generic filesystem/path checks;
- tri-state runtime distinctions such as FOUND / NOT_FOUND / ERROR;
- generic provenance fields;
- neutral CI mechanics;
- neutral fixture/test harness helpers.

Not neutral by default:

- AHP behavioral states;
- risk tiers;
- evidence hierarchy;
- old hot path;
- old policy prompt;
- old behavioral decision tree;
- old attack ontology;
- old efficacy scorer;
- old treatment fixtures.

## 5. Revalidation requirement

No old implementation file enters the active restart simply because it is convenient.

Every salvaged component must receive a salvage record containing:

```text
source_path
source_hash
classification
reason_for_reuse
old_semantics_found
old_semantics_removed
execution_capabilities
fresh_spec
fresh_tests
negative_tests
mutation_or_failure_injection
reviewer
decision
new_hash
```

Required neutrality questions:

1. Would the component still make sense in a completely unrelated evidence-evaluation project?
2. Does it work after the old AHP behavioral architecture is removed?
3. Are its new tests derived from the restart measurement contract rather than old behavioral expectations?
4. Does deliberate corruption cause the new test suite to fail?

Failure on these questions keeps the component forensic-only.

## 6. Import boundary

Before intervention admission:

```text
runtime/product code MUST NOT import from development benchmark/research trees
```

Research code must not become treatment code indirectly through generated artifacts or imports.

## 7. Claim boundary

The restart must preserve:

```text
STRUCTURAL EVIDENCE != BEHAVIORAL EFFICACY
MECHANISM TEST != EFFECTIVENESS TEST
DEVELOPMENT BENCHMARK != SEALED CONFIRMATION
```

No amount of old structural green tests changes this boundary.
