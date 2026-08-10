# Contributing to Anti-Hallucination Protocol

You do not need write access to this repository to contribute an audit, test, reproducer, documentation change or code fix.

## External human or AI agent

Start here:

```text
EXTERNAL-CONTRIBUTOR.md
```

Minimum-friction path:

```bash
gh repo clone antydizajn/anti-hallucination-protocol
cd anti-hallucination-protocol
python3 scripts/external_contributor.py start
# perform the selected [AGENT-READY] task
python3 scripts/external_contributor.py submit
```

The normal trust boundary is:

```text
public upstream
-> your fork
-> your branch
-> Pull Request
-> project CI / intake
-> maintainer or trusted-agent adjudication
```

Do not request collaborator `Write` merely to submit work.

A Pull Request is a proposal, not acceptance:

```text
PR OPEN != CHANGE ACCEPTED
STRUCTURALLY_VALID_SUBMISSION != FINDING TRUE
```

## Trusted project agents / maintainers

Use `AGENTS.md`, `AGENT-BOOTSTRAP.json` and `AUTONOMOUS-AGENT.md` for the internal scoped-credential workflow.
