#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: bash INTERNAL-AUDITS/RUNNERS/install_frozen_ahp.sh <rep-slug>" >&2
}
[[ $# -eq 1 ]] || { usage; exit 64; }
REP="$1"
[[ "$REP" =~ ^[a-z0-9][a-z0-9_-]{0,31}$ ]] || { echo "ERROR: invalid rep-slug" >&2; exit 64; }

command -v hermes >/dev/null || { echo "ERROR: hermes not found" >&2; exit 69; }
command -v git >/dev/null || { echo "ERROR: git not found" >&2; exit 69; }
command -v tar >/dev/null || { echo "ERROR: tar not found" >&2; exit 69; }

REPO_URL="https://github.com/antydizajn/anti-hallucination-protocol.git"
LEGACY_REF="v2.0.0"
LEGACY_COMMIT_EXPECTED="b71cc9d06b58c8f12e06b77606a279f536a18959"
CURRENT_REF="94bfd13f9c4818a949775bd73c1c0d91ce6a3116"
CURRENT_COMMIT_EXPECTED="94bfd13f9c4818a949775bd73c1c0d91ce6a3116"
LEGACY_SKILL_BLOB_EXPECTED="2de9613a846771db159d041ab0e75bf92805b9a4"
CURRENT_SKILL_BLOB_EXPECTED="0860d4547a5e8e7ed27221724da0cdaaf33a1b41"

BENCH_HOME="${AHP_BENCH_HOME:-$HOME/ahp-benchmark-v01}"
CACHE="$BENCH_HOME/cache/ahp-source.git"
WORKDIR="$BENCH_HOME/work/$REP"
INTEGRITY="$WORKDIR/integrity"
A="ahpbench-${REP}-a"
B="ahpbench-${REP}-b"
C="ahpbench-${REP}-c"
mkdir -p "$BENCH_HOME/cache" "$INTEGRITY"

for p in "$A" "$B" "$C"; do
  hermes profile show "$p" >/dev/null 2>&1 || {
    echo "ERROR: missing profile $p. Run bootstrap_profiles.sh first." >&2
    exit 2
  }
done

if [[ ! -d "$CACHE" ]]; then
  git clone --bare "$REPO_URL" "$CACHE" >/dev/null
else
  git -C "$CACHE" fetch --tags --force origin >/dev/null
fi

LEGACY_COMMIT="$(git -C "$CACHE" rev-parse "${LEGACY_REF}^{commit}")"
CURRENT_COMMIT="$(git -C "$CACHE" rev-parse "${CURRENT_REF}^{commit}")"
[[ "$LEGACY_COMMIT" == "$LEGACY_COMMIT_EXPECTED" ]] || {
  echo "ERROR: v2.0.0 resolved to unexpected commit: $LEGACY_COMMIT" >&2; exit 3;
}
[[ "$CURRENT_COMMIT" == "$CURRENT_COMMIT_EXPECTED" ]] || {
  echo "ERROR: v5.4.2 anchor resolved unexpectedly: $CURRENT_COMMIT" >&2; exit 3;
}

profile_home() {
  dirname "$(hermes -p "$1" config path)"
}

A_HOME="$(profile_home "$A")"
B_HOME="$(profile_home "$B")"
C_HOME="$(profile_home "$C")"
B_DEST="$B_HOME/skills/anti-hallucination-protocol"
C_DEST="$C_HOME/skills/anti-hallucination-protocol"

# Refuse ambiguous/reused treatment state.
for d in "$B_DEST" "$C_DEST"; do
  [[ ! -e "$d" ]] || { echo "ERROR: treatment destination already exists: $d" >&2; exit 4; }
done

mkdir -p "$B_DEST" "$C_DEST"
git -C "$CACHE" archive "$LEGACY_COMMIT" | tar -x -C "$B_DEST"
git -C "$CACHE" archive "$CURRENT_COMMIT" | tar -x -C "$C_DEST"

LEGACY_SOURCE_BLOB="$(git -C "$CACHE" show "$LEGACY_COMMIT:SKILL.md" | git hash-object --stdin)"
CURRENT_SOURCE_BLOB="$(git -C "$CACHE" show "$CURRENT_COMMIT:SKILL.md" | git hash-object --stdin)"
LEGACY_INSTALLED_BLOB="$(git hash-object "$B_DEST/SKILL.md")"
CURRENT_INSTALLED_BLOB="$(git hash-object "$C_DEST/SKILL.md")"

[[ "$LEGACY_SOURCE_BLOB" == "$LEGACY_SKILL_BLOB_EXPECTED" ]] || { echo "ERROR: unexpected legacy source blob" >&2; exit 5; }
[[ "$CURRENT_SOURCE_BLOB" == "$CURRENT_SKILL_BLOB_EXPECTED" ]] || { echo "ERROR: unexpected current source blob" >&2; exit 5; }
[[ "$LEGACY_INSTALLED_BLOB" == "$LEGACY_SKILL_BLOB_EXPECTED" ]] || { echo "ERROR: legacy installed bytes differ" >&2; exit 5; }
[[ "$CURRENT_INSTALLED_BLOB" == "$CURRENT_SKILL_BLOB_EXPECTED" ]] || { echo "ERROR: current installed bytes differ" >&2; exit 5; }
cmp -s <(git -C "$CACHE" show "$LEGACY_COMMIT:SKILL.md") "$B_DEST/SKILL.md" || { echo "ERROR: legacy SKILL.md cmp failed" >&2; exit 5; }
cmp -s <(git -C "$CACHE" show "$CURRENT_COMMIT:SKILL.md") "$C_DEST/SKILL.md" || { echo "ERROR: current SKILL.md cmp failed" >&2; exit 5; }

# Discoverability is not load evidence, but it is a required precondition.
A_SKILLS="$(hermes -p "$A" skills list --source local --enabled-only 2>&1 || true)"
B_SKILLS="$(hermes -p "$B" skills list --source local --enabled-only 2>&1 || true)"
C_SKILLS="$(hermes -p "$C" skills list --source local --enabled-only 2>&1 || true)"

if grep -qi 'anti-hallucination-protocol' <<<"$A_SKILLS"; then
  echo "ERROR: CONTROL can discover anti-hallucination-protocol" >&2
  exit 6
fi
grep -qi 'anti-hallucination-protocol' <<<"$B_SKILLS" || { echo "ERROR: LEGACY AHP not discoverable" >&2; exit 6; }
grep -qi 'anti-hallucination-protocol' <<<"$C_SKILLS" || { echo "ERROR: CURRENT AHP not discoverable" >&2; exit 6; }

cat > "$INTEGRITY/ahp-identity.txt" <<EOF
rep=$REP
legacy_ref=$LEGACY_REF
legacy_commit=$LEGACY_COMMIT
legacy_source_skill_blob=$LEGACY_SOURCE_BLOB
legacy_installed_skill_blob=$LEGACY_INSTALLED_BLOB
legacy_byte_cmp=PASS
current_ref=$CURRENT_REF
current_commit=$CURRENT_COMMIT
current_source_skill_blob=$CURRENT_SOURCE_BLOB
current_installed_skill_blob=$CURRENT_INSTALLED_BLOB
current_byte_cmp=PASS
control_ahp_discoverable=NO
legacy_ahp_discoverable=YES
current_ahp_discoverable=YES
NOTE=DISCOVERABLE_IS_NOT_LOADED
EOF

printf '%s\n' "$A_SKILLS" > "$INTEGRITY/control-skills.txt"
printf '%s\n' "$B_SKILLS" > "$INTEGRITY/legacy-skills.txt"
printf '%s\n' "$C_SKILLS" > "$INTEGRITY/current-skills.txt"

echo "Frozen treatment identity verified for repetition $REP"
echo "Identity record: $INTEGRITY/ahp-identity.txt"
