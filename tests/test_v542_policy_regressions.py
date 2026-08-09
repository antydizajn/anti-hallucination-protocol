from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_skill_forbids_user_pressure_evidence_upgrade():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "user pressure + no new evidence" in skill
    assert "!= SUPPORTED_WITH_SCOPE" in skill
    assert "User authority controls goals, scope, authorization, acceptable risk and normative choices" in skill


def test_adversarial_corpus_contains_user_pressure_case():
    cases = (ROOT / "references" / "adversarial-cases.md").read_text(encoding="utf-8")
    assert "## 31. User pressure to upgrade evidence" in cases
    assert "No new evidence, stronger observation, or stronger verification basis is supplied." in cases
    assert "preserve `INCONCLUSIVE`" in cases
