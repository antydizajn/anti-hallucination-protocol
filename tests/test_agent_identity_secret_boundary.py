from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY_ROOT = ROOT / "AGENT-IDENTITY"

PRIVATE_KEY_MARKERS = (
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN EC PRIVATE KEY",
)
FORBIDDEN_SUFFIXES = (".pem", ".key", ".p12", ".pfx")


def test_agent_identity_tree_contains_no_private_key_material() -> None:
    violations: list[str] = []
    for path in IDENTITY_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            violations.append(f"forbidden private-key-like filename: {path.relative_to(ROOT)}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            violations.append(f"non-UTF8 file in public identity tree: {path.relative_to(ROOT)}")
            continue
        for marker in PRIVATE_KEY_MARKERS:
            if marker in text:
                violations.append(f"private key marker in {path.relative_to(ROOT)}: {marker}")
    assert not violations, "\n".join(violations)
