# TEST 2 (long-session) + TEST 4 (deployment) — wyniki
# 2026-08-09

=====================================================================
TEST 2: LONG-SESSION STRESS — czy hot path przetrwa środek kontekstu
=====================================================================
Metoda: zdeponowano marker start z regułą kluczową (proces vs endpoint vs
integracja), wykonano 3 kroki realnej pracy (sprawdzanie arXiv, deployment
oracle, CLI check_evidence_record), potem wrócono i sprawdzono zastosowanie.

WYNIK: PASS.
- Fakt kluczowy przetrwał (nie odczytano go z pliku, ale zastosowano
  dyscyplinę na świeżym twierdzeniu).
- NIE padło "serwer DZIAŁA" na podstawie samego pgrep; wykonano realny
  check /health -> 200 i rozdzielono 3 poziomy.
UWAGA UCZCIWOŚCI: test był z JAWNYM markerem (wiedziałem że to test),
więc jest słabszy niż zapowiedziany fake. Prawdziwą granicę pokazał
GLITCH (test 1) — bez markera.

=====================================================================
TEST 4: DEPLOYMENT — czy v5.4.1 da się zainstalować jako działający skill
=====================================================================
Metoda (izolacja, produkcja NIETKNIĘTA):
(a) skopiowano fresh main do tymcz. katalogu skill;
(b) python3 scripts/check_v5_integrity.py --root <katalog> -> PASS;
(c) przez venv Hermesa (py3.11) skill_utils.parse_frontmatter(SKILL.md)
    -> name=anti-hallucination-protocol, version=5.4.1, platforms=[...].

WYNIK: PASS (deployment REALNIE możliwy).
- wszystkie 5 checkers obecnych w kopii (check_evidence_record.py,
  check_research_provenance.py, check_v5_integrity.py, verify_claim.py,
  liveness_check.sh);
- Hermes oracle poprawnie parsuje frontmatter v5.4.1.

KLUCZOWE ROZRÓŻNIENIE:
- Repo main v5.4.1 da się ZAINSTALOWAĆ (tu dowód).
- Produkcyjny skill to dalej v2.0 (liveness FAIL, martwy verify_claim.sh).
- Problem NIE w tym że v5.4.1 nie da się wdrożyć; w tym że NIKT go nie
  wdrożył do ~/.hermes/skills/... (produkcja). To P1-DEPLOY.

=====================================================================
CZYSTKOWY FINDING (test 2/spot-check): własny błąd typowania ID
=====================================================================
Przy live spot-check pomylił_prefiks roku: sprawdziłem 2605.05057
(ScriptHOI) zamiast manifestowego 2505.05057 (API Hallucination).
To był FALSE POSITIVE z mojej strony — manifest jest poprawny.
Lekcja: przed zgłoszeniem title-drift zweryfikuj DOKŁADNY ID z manifestu
(transpozycja cyfr to klasyczny self-induced bug w długiej sesji).
=====================================================================