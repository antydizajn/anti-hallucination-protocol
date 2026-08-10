# AA-Omniscience-600 Manifest

```yaml
battery: AA-OMNISCIENCE-600
classification:
  - EXTERNAL
  - PUBLIC
  - NOT_HELD_OUT
source:
  repository: ArtificialAnalysis/AA-Omniscience-Public
  revision: 4a8ffc87c4650054825fb767fe0da4a4fc97ff32
  artifact: AA-Omniscience_dataset_public.csv
conditions:
  - CONTROL
  - LEGACY
  - CURRENT
ahp:
  legacy: v2.0.0
  current: v5.4.2
  current_commit: 94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

Dataset identity must be resolved at runtime.

No result is valid without:

- artifact SHA256;
- schema hash;
- model identity;
- runtime conditions;
- evaluator version.
