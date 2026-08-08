# Anti-Hallucination Protocol v5

**An epistemic control plane for AI agents that refuse to cosplay certainty.**

Anti-Hallucination Protocol is a research-grounded Hermes Agent skill for controlling how claims move from model prediction to user-visible fact or consequential action.

It does not promise impossible "zero hallucinations". Instead, it attacks the actual failure chain:

`INTENT -> CLAIM -> EVIDENCE -> RETRIEVAL -> SOURCE -> ENTAILMENT -> VERIFIER -> DECISION -> ACTION`

The protocol adds explicit controls for claim decomposition, evidence scope, source freshness, source lineage, contradictory evidence, verifier failure, untrusted retrieved content, prompt injection, agent-loop error propagation, current-state verification, and honest completion semantics.

## Why this exists

Because:

- a real citation can support the wrong sentence,
- five agents can repeat the same bad premise,
- official documentation can be stale,
- retrieval can be poisoned,
- a verifier can return a confident false positive,
- a passing unit test can miss the real user path,
- memory can preserve yesterday's truth as today's fiction,
- and "the model sounded confident" is not an epistemic method.

## The rule

> **No vibes-only verification. No oracle cosplay. Evidence or abstain.**

## What is inside

- operational `SKILL.md`
- verified research provenance
- evidence-state model
- source-lineage and contradiction controls
- untrusted-evidence boundary
- deterministic verification helpers
- semantic evidence-record validator
- structural integrity checker
- adversarial attack corpus

The protocol deliberately distinguishes deterministic checks from semantic judgment. A Python script can prove that an exit code was non-zero. It cannot magically prove that a paragraph entails a scientific claim.

## Authors

Created by **[Paulina Janowska](https://github.com/antydizajn/)** and **[Gniewisława AI](https://gniewka.antydizajn.pl)**.

**Proudly witchcrafted in Poznań, Poland ♥**

*Built with skepticism, adversarial spite, and an unreasonable allergy to confident bullshit.*

## Philosophy

**Truth over fluency.**  
**Mechanism over ritual.**  
**Falsification over self-congratulation.**  
**Scope over fake certainty.**  
**Evidence over vibes.**

If a verifier can be wrong, verify the verifier.

If the evidence cannot carry the claim, downgrade the claim.

If the world is mutable, check the world.

If the answer is still unknown, say so.

---

MIT licensed. Built for Hermes Agent, but most of the epistemic model is intentionally tool- and model-agnostic.
