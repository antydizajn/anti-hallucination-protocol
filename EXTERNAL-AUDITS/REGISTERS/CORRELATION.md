# Audit Correlation Register

This register records shared failure domains across external audits.

It prevents `N reports` from being silently interpreted as `N independent evidence sources`.

## Correlation dimensions

Track where known:

```text
prompt
operator
model family
provider/runtime
target snapshot
source set
historical audit exposure
reproducer lineage
evaluation rubric
human discussion/collaboration
```

## Register

| audit ID | prompt | operator | model family | provider/runtime | target commit | historical audit exposure | correlation notes |
|---|---|---|---|---|---|---|---|
| EXT-20260809-001 | canonical Iteration 5 | external collaborator | Claude | Palantir Foundry proxy | c6ee5f1daade5bb39632b879613a27895f7ccf83 | Phase A claimed blind | First registered external audit; independence from future reports must be evaluated, not assumed. |

## Interpretation

Two audits may still provide useful cross-confirmation when they share one dimension.

Example:

```text
same prompt
+ different models
+ independent fresh clones
+ independently generated reproducers
```

is stronger than duplicate output, but weaker than fully independent methodology and failure domains.

Record the actual relationship rather than assigning a binary `independent=true` label.
