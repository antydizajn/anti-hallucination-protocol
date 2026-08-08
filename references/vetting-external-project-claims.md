# Vetting external project, launch, and marketing claims

Use this workflow when evaluating a repository pitch, launch post, README claim,
benchmark brag, or product announcement. The governing rule is symmetric:
third-party marketing copy is an unverified claim until checked against primary
artifacts.

The goal is not reflexive cynicism. It is calibrated attribution: what is
verified, what is unsupported by the inspected evidence, what is estimated rather
than measured, and what remains unknown.

## 1. Resolve the exact artifact first

Before evaluating claims, prove that you are inspecting the intended repository,
release, benchmark run, paper, or dataset.

Record where practical:

- repository owner/name,
- branch/tag/commit or release,
- artifact path,
- timestamp or run identifier,
- access limitations.

Do not treat an endpoint error as a universal semantic. For example, an HTTP 404
can mean different things depending on service and authentication state. Phrase the
result as "the requested resource was not accessible at this endpoint under the
current access context" until the service's documented semantics justify a stronger
claim.

If querying GitHub owner metadata, inspect the owner type first. A repository owner
may be an organization or a user; do not blindly call an organization-specific
endpoint for every owner.

## 2. Establish that there is a substantive project

Inspect primary repository metadata and the tree itself. Useful questions:

- Is there executable/library code, or mainly a README and assets?
- Are there tests?
- Are benchmark/evaluation artifacts present?
- Is there a license?
- Is the project archived?
- Is development recent relative to the claim being evaluated?
- Is the implementation concentrated in one contributor or distributed across a
  team?

Contributor concentration is a maintenance-risk signal, not proof of project
quality or fraud.

## 3. Trace every consequential number to a primary artifact

For benchmark or performance claims, locate the files that contain the underlying
results:

- `examples/`
- `bench*/`
- `eval*/`
- result JSON/CSV files,
- generated reports,
- experiment logs,
- reproducibility scripts.

For each advertised number, record one of these states:

- `MATCHED` - the inspected primary artifact contains the same measured value.
- `DERIVED` - the number can be reproduced from values in the artifact.
- `ESTIMATED` - the artifact labels it as an estimate/model/projection.
- `NOT_SUPPORTED_HERE` - the inspected artifact does not support the number.
- `CONTRADICTED` - the inspected artifact supports a materially different value.
- `UNKNOWN` - evidence is incomplete or inaccessible.

Do **not** jump from `NOT_SUPPORTED_HERE` to "invented". The number may come from
another run, another artifact, an unpublished experiment, or a derivation you have
not yet located. Call fabrication only when there is evidence of fabrication.

## 4. Separate measured from estimated

This is a high-value check because launch copy often promotes the most impressive
number while the underlying artifact distinguishes direct measurement from a
cost/performance estimate.

Search for both:

- directly observed fields,
- estimated/projected fields,
- confidence intervals or ranges,
- sample counts,
- excluded/failed runs.

Report them side by side rather than collapsing them into one headline number.

## 5. Read the code behind the headline verb

Strong verbs imply strong mechanisms. If the pitch says the system:

- proves,
- guarantees,
- verifies,
- exploits,
- autonomously resolves,
- formally checks,

inspect the implementation that performs the decisive step.

Examples of mismatches worth surfacing:

- "proves exploitability" but final acceptance is a single LLM classification,
- "sandboxed" but execution is an ordinary local subprocess,
- "autonomous" but a human must approve every decisive transition,
- "verified" but the verifier checks only string presence rather than behavior.

Describe the mechanism precisely. Do not convert an implementation mismatch into a
claim of deception unless intent is independently established.

## 6. Surface material omissions

A technically real result can still be marketed selectively. Look for omitted:

- wall-clock time,
- compute/token/API cost,
- model/provider dependency,
- hardware dependency,
- failed or inconclusive cases,
- unverified findings,
- excluded datasets,
- retry counts,
- manual intervention,
- non-default configuration.

The correct statement is usually "the launch copy omits X, which materially changes
how the result should be interpreted", not "they hid X" unless concealment is
actually established.

## 7. Verify scope, not just numbers

A benchmark result has a domain. Ask:

- Which dataset/version?
- Which model/version?
- Which commit?
- How many samples?
- What selection criteria?
- What baseline configuration?
- Was the result reproduced independently?

A valid result on one narrow benchmark does not automatically support a broad claim
about general performance.

## 8. Credit honesty when present

Evidence-based vetting is not a dunking exercise. Positive epistemic signals matter:

- raw result files are shipped,
- methodology is reproducible,
- estimates are labeled as estimates,
- failures are reported,
- competitors are marked `N/A` rather than assigned invented values,
- limitations are explicit.

Calibrated criticism is more useful than reflexive suspicion.

## 9. Verdict format

A good final verdict separates:

### Verified
Claims directly supported by inspected primary artifacts.

### Oversold or scope-inflated
Claims whose wording is stronger or broader than the implementation/evidence.

### Unsupported by inspected evidence
Claims not established by the artifacts you actually checked. Do not call them
false unless contradicted.

### Material omissions
Costs, dependencies, failures, scope limits, or partial results missing from the
headline presentation.

### Unknown
Anything you could not verify because access, artifact completeness, or scope was
insufficient.

## 10. Worked lesson: measured vs estimated

A prior audit found a launch claim using a "200+" style headline while the primary
result artifact contained a much smaller directly reported invocation count and a
separate estimated range near the marketed number. The durable lesson is not the
specific project or values. It is the method:

1. find the measured field,
2. find the estimate field,
3. identify which one marketing repeated,
4. label the distinction explicitly.

Likewise, a strong verb such as "proves" must be traced to the actual decision
mechanism. If the decisive step is probabilistic model judgment, report that rather
than inheriting the marketing verb.

## 11. Stylometry is secondary evidence

Do not let an AI-writing detector, especially one calibrated on another language or
text genre, dominate a repository audit. Bullet lists, technical prose, and launch
copy can trigger rhythm/style heuristics for reasons unrelated to authorship.

Treat stylometry as orientational at most. Repository artifacts, code paths, result
files, and reproducibility evidence carry the load-bearing verdict.
