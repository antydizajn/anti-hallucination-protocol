# AHP Behavioral Benchmark v0.1 Design

## Objective

Measure whether loading AHP changes observable Hermes Agent behavior.

The benchmark does not attempt to prove consciousness, intelligence improvement, or universal factuality improvement. It measures defined behaviors under controlled prompts.

## Experimental conditions

| Condition | Description |
|---|---|
| A CONTROL | Hermes baseline without AHP loaded |
| B LEGACY | Hermes + AHP v2.0.0 |
| C CURRENT | Hermes + AHP v5.4.2 |

## Control variables

Record before every run:

- Hermes repository and commit SHA;
- AHP ref/SHA;
- model and provider;
- temperature/sampling settings where available;
- tools enabled;
- tool availability;
- operating system;
- profile name and HERMES_HOME;
- external memory provider status;
- CWD and discovered context files;
- session ID;
- date/time.

## Freshness requirements

Every case starts from a fresh session.

The runner must not:

- reuse previous chat history;
- reuse previous memory writes;
- preload unrelated skills;
- use contaminated project context.

## Case families

### QUICK-5 smoke battery

Five representative cases:

1. User pressure does not upgrade evidence.
2. Current-state claim requires fresh verification.
3. Tool failure cannot become success.
4. Patch exists but deployment is unknown.
5. Prompt injection inside retrieved evidence.

### DEEP-60 expansion

60 cases distributed across:

- evidence state transitions;
- contradiction handling;
- stale memory conflicts;
- source independence;
- tool failure;
- completion claims;
- prompt injection;
- long context placement;
- compaction/restart;
- user pressure;
- citations/provenance;
- runtime state claims.

## Metrics

Primary metrics:

- false support rate;
- false certainty rate;
- evidence downgrade correctness;
- conflict preservation rate;
- fresh verification rate;
- tool error preservation rate;
- completion overclaim rate;
- prompt injection resistance rate.

Secondary metrics:

- response latency;
- token usage;
- tool calls;
- human rating.

## Evidence model

Results are stored as:

```text
raw transcript
raw tool trace
run manifest
case score
human evaluation
aggregate report
```

No aggregate score is valid without denominators.

## Interpretation rules

Allowed:

```text
In this benchmark configuration C outperformed A on metric X.
```

Not allowed:

```text
AHP makes models truthful.
```

The second statement exceeds the evidence scope.
