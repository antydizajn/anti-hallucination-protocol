# Hermes Human Runbook

## 0. Prepare workspace

Use a neutral directory. Do not run benchmark from inside a repository containing:

```text
AGENTS.md
.hermes.md
CLAUDE.md
.cursorrules
```

Example:

```bash
mkdir -p ~/ahp-benchmark/work
cd ~/ahp-benchmark/work
```

## 1. Record Hermes version

Before every run:

```bash
hermes --version
git rev-parse HEAD
```

Record the actual Hermes source commit. Never assume a remembered SHA is current.

## 2. Create isolated profiles

Create separate profiles:

```bash
hermes profile create ahp-control
hermes profile create ahp-v200
hermes profile create ahp-v542
```

Verify:

```bash
hermes profile list
hermes profile show ahp-control
hermes profile show ahp-v200
hermes profile show ahp-v542
```

Profiles isolate Hermes state but are not filesystem sandboxes.

## 3. Install frozen AHP versions

Clone AHP separately:

```bash
git clone https://github.com/antydizajn/anti-hallucination-protocol.git
cd anti-hallucination-protocol
```

For legacy:

```bash
git checkout v2.0.0
```

For current:

```bash
git checkout 94bfd13f9c4818a949775bd73c1c0d91ce6a3116
```

Record:

```bash
git rev-parse HEAD
```

## 4. Configure identical runtime

For all three profiles keep identical:

- model;
- provider;
- tool permissions;
- environment;
- sampling parameters;
- timeout configuration.

Disable external memory providers unless the benchmark case explicitly tests them.

Check:

```bash
hermes memory status
```

## 5. Load AHP only in treatment conditions

Do not claim installation equals loading.

Confirm the loaded skill:

```bash
hermes skills list
```

Use explicit preload only for B/C runs:

```bash
hermes --profile ahp-v200 chat --skills anti-hallucination-protocol

hermes --profile ahp-v542 chat --skills anti-hallucination-protocol
```

CONTROL does not load AHP.

## 6. Execute cases

Use identical prompts from:

```text
INTERNAL-AUDITS/BATTERIES/QUICK-5
INTERNAL-AUDITS/BATTERIES/DEEP-60
```

Do not modify prompts after seeing results.

## 7. Archive evidence

Save:

```text
run-manifest.json
transcript.md
tool-trace.json
human-score.md
result.json
```

Include hashes for artifacts.

## 8. Never claim beyond evidence

Valid:

```text
AHP reduced metric X in this tested configuration.
```

Invalid:

```text
AHP solved hallucinations.
```

The benchmark measures behavior. It does not certify universal model reliability.
