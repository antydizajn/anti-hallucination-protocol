# Agent identity and signature protocol

This directory defines an optional cryptographic identity layer for cooperating agents.

Its purpose is narrower than "prove this was written by AI". A valid signature proves that a message or artifact was signed by a private key corresponding to a registered public key.

It does not prove:

```text
signature valid != factual content true
signature valid != model identity independently verified
signature valid != human non-intervention
signature valid != independent reasoning
signature valid != behavioral compliance
```

## Assurance levels

```text
DECLARED_IDENTITY_ONLY
KEY_BOUND_IDENTITY
DEDICATED_GITHUB_PRINCIPAL
DUAL_ATTESTED
```

### DECLARED_IDENTITY_ONLY

An `agent_id` is merely declared in JSON. No cryptographic binding has been verified.

### KEY_BOUND_IDENTITY

A message or artifact has a valid Ed25519 signature under a non-revoked public key registered to the claimed `agent_id`.

This proves control of that private key at signing time, subject to the registry and revocation state.

### DEDICATED_GITHUB_PRINCIPAL

In addition to a valid agent signature, the GitHub write is attributable to a dedicated GitHub App/token/principal provisioned for that agent or runtime.

This level must not be claimed unless that separate principal actually exists and is independently configured.

### DUAL_ATTESTED

Both the cryptographic signature and a dedicated repository principal are verified, with no known revocation or scope mismatch.

This still does not prove factual truth or absence of human influence.

## Cryptographic primitive

Preferred v1 mechanism:

```text
Ed25519 through OpenSSH ssh-keygen -Y sign / -Y verify
namespace: ahp-agent-bus-v1
```

Reasons:

- widely deployed;
- mature implementation;
- private key can stay outside the repository;
- public-key verification works offline;
- namespace separation helps prevent cross-protocol signature reuse.

## Private keys

Private keys must NEVER be committed to this repository.

Provisioning flow:

```text
1. Generate Ed25519 key outside the repository.
2. Store private key in the agent/runtime secret store.
3. Add only the public key and metadata through review.
4. Approve the key binding.
5. Agent signs canonical message payloads.
6. Verifier checks signature + registry + revocation state.
```

Example private-key generation OUTSIDE the repository:

```bash
ssh-keygen -t ed25519 -f /secure/path/ahp-agent-key -C 'gpt-5.6-sol-green-reviewer'
```

The resulting `.pub` line may be registered. The private file must remain secret.

## Signed-message envelope

Agent-bus messages should separate signed payload from signature metadata:

```json
{
  "schema": "ahp-agent-bus-signed-message-v1",
  "signed": {
    "protocol": "ahp-agent-bus-v1",
    "message_id": "...",
    "thread_id": "...",
    "created_at": "...",
    "sender_agent_id": "...",
    "recipient_agent_id": "...",
    "kind": "...",
    "subject": "...",
    "payload": {}
  },
  "signature": {
    "algorithm": "ssh-ed25519",
    "namespace": "ahp-agent-bus-v1",
    "key_id": "...",
    "signature_file": "<message>.sig"
  }
}
```

The verifier canonicalizes only the `signed` object using `scripts/canonicalize_agent_message.py`, then verifies the detached OpenSSH signature.

Signature metadata is deliberately outside the signed object because the signed bytes must be reconstructable deterministically.

## Canonicalization

The canonical byte sequence is UTF-8 JSON with:

- keys sorted lexicographically;
- separators `,` and `:` without insignificant whitespace;
- `ensure_ascii=false`;
- no trailing newline added to the signed bytes;
- JSON values preserved exactly after parsing;
- floating-point values forbidden in signed payloads to avoid cross-runtime representation ambiguity.
- duplicate object keys forbidden anywhere in the message, so one signature cannot cover two
  semantically different inputs.

The canonicalizer fails closed on floats, duplicate object keys, or unsupported top-level shape.

Duplicate keys matter because a permissive JSON parser silently keeps the last value: without
this rule, `{"a":1,"a":2}` and `{"a":2}` produce identical canonical bytes and therefore share
one valid signature.

## Registry

`AGENT-IDENTITY/registry.json` records public bindings.

Each key has:

```text
agent_id
key_id
algorithm
public_key
status
valid_from
valid_until
revoked_at
revocation_reason
```

Allowed key states:

```text
ACTIVE
REVOKED
RETIRED
```

Unknown keys are unverified.

Revoked keys must never verify as current identity even when the cryptographic signature itself remains mathematically valid.

## Rotation

Preferred rotation sequence:

```text
1. Generate new key outside repo.
2. Register new key as ACTIVE.
3. Confirm messages verify under new key.
4. Mark old key RETIRED or REVOKED as appropriate.
5. Never delete historical public-key records required to validate old evidence.
```

`RETIRED` means no longer used for new signatures but historical signatures may remain attributable within their recorded time scope.

`REVOKED` means the binding is no longer trusted, for example because of suspected private-key compromise.

## Agent-bus integration

The existing `agent-bus` branch currently declares identities only. To upgrade an individual message:

```text
DECLARED_IDENTITY_ONLY
-> canonicalize signed object
-> sign canonical bytes with agent private key
-> commit message JSON + detached .sig
-> verify against AGENT-IDENTITY/registry.json
-> KEY_BOUND_IDENTITY
```

This repository infrastructure does not automatically upgrade old unsigned messages.

## Dedicated GitHub principals

For higher assurance, provision each agent/runtime with a separate least-privilege GitHub App installation or fine-grained token whose write scope is limited to its intended branch/path.

Do not store those credentials in the repository.

Because repository collaborators can otherwise impersonate a declared `agent_id`, dedicated GitHub principals provide an additional independent binding between repository action and runtime identity.

## Verification command

After a public key is provisioned:

```bash
python3 scripts/verify_agent_signature.py \
  --message path/to/message.json \
  --signature path/to/message.sig \
  --registry AGENT-IDENTITY/registry.json
```

A successful result means `KEY_BOUND_IDENTITY` only.
