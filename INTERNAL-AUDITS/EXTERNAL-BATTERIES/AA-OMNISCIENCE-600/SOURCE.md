# AA-Omniscience-600 external battery

## Purpose

External diagnostic battery for AHP behavioral evaluation.

This benchmark is not part of the native QUICK-5 or DEEP-60 batteries. It is an independent factual calibration battery.

## Source

Dataset:

`ArtificialAnalysis/AA-Omniscience-Public`

Pinned revision:

`4a8ffc87c4650054825fb767fe0da4a4fc97ff32`

Expected public release artifact:

`AA-Omniscience_dataset_public.csv`

License:

Apache-2.0 (according to dataset metadata).

## Boundary

This is a PUBLIC benchmark.

Therefore:

```
PUBLIC DATASET != HELD-OUT DATASET
```

Do not use public AA-Omniscience results as uncontaminated evidence of generalization.

## Identity requirements

Every execution must record:

- source repository
- pinned revision
- downloaded artifact SHA256
- row count
- schema hash
- evaluator version
- model/provider identity
- runtime conditions

The dataset name alone is not a sufficient identity.

## AHP interpretation boundary

A result may show changes in:

- factual calibration
- abstention behavior
- incorrect guessing

It cannot alone prove:

- universal hallucination reduction
- tool-use reliability
- evidence lineage correctness
- current-state verification behavior

Those require dedicated AHP batteries.
