# PROPOZYCJA WDROŻENIA AHP v5.4.1 do produkcji (P1-DEPLOY) — READ-ONLY, do decyzji Pauliny
# 2026-08-09 — audit NIE modyfikuje produkcji; to jest surowy plan + komendy

=====================================================================
STAN ZMODIŁOWANY (z wcześniejszych testów):
  - Repo main v5.4.1: 68 plików, 1.4MB, integrity PASS, Hermes oracle
    parsuje frontmatter (version=5.4.1), CLI check_evidence działa.
  - Produkcja ~/.hermes/skills/software-development/anti-hallucination-protocol:
    v2.0 (13 plików 128K), martwy verify_claim.sh, liveness FAIL,
    overconfidence 91% vs 77%.
=====================================================================

=====================================================================
PROBLEM: Produkcyjny Hermes ładuje v2.0 (przestarzały, zepsuty helper),
NIE v5.4.1. Wszystkie moderne checkery (check_evidence_record.py,
verify_claim.py, check_v5_integrity.py, check_research_provenance.py)
NIE są w produkcji. Dlatego "zajebistość" repo nie jest egzekwowana.

=====================================================================
PLAN WDROŻENIA (wykonać TYLKO za zgoda Pauliny; audit jest read-only)
=====================================================================
KROK 0: BACKUP produkcyjnego katalogu (nigdy nie nadpisuj na żywo).
  mv ~/.hermes/skills/software-development/anti-hallucination-protocol \
     ~/.hermes/skills/software-development/anti-hallucination-protocol.bak_v2

KROK 1: Skopiuj świeży v5.4.1 z /tmp/ahp-latest (lub świeży clone repo).
  cp -r /tmp/ahp-latest/anti-hallucination-protocol \
        ~/.hermes/skills/software-development/anti-hallucination-protocol
  # zacznij od świeżego klona repo, nie z /tmp jeśli chcesz czystego origin/main:
  # git clone https://github.com/antydizajn/anti-hallucination-protocol.git <tmp>
  # i skopiuj stamtąd.

KROK 2: WERYFIKACJA (L30/L2.1 — sprawdź zanim ogłosisz sukces).
  cd ~/.hermes/skills/software-development/anti-hallucination-protocol
  python3 scripts/check_v5_integrity.py --root .        # -> V5 INTEGRITY: PASS
  python3 scripts/check_research_provenance.py --root . # -> PASS
  AHP_SKILL_DIR="$(pwd)" bash scripts/liveness_check.sh  # -> PASS
  python3 -m pytest tests/ -q                             # -> 124 passed

KROK 3: RESTART SESJI Hermesa (skill discovery na nowo).
  # nowy `hermes` lub `/new` — skill musi się przeładować.

KROK 4: POTWIERDŹ że discovery widzi v5.4.1 (nie v2.0).
  grep -m1 "^version:" SKILL.md   # -> version: 5.4.1

=====================================================================
RYZYKA / UWAGI (AHP: nie ukrywaj)
=====================================================================
- Nadpisanie na żywo bez backupu = ryzyko. KROK 0 backup jest obowiązkowy.
- Stare v2.0 może być używane przez inne integracje (np. calibration_log.py
  w ~/.hermes/scripts/anti_halluc). Upewnij się że nie psujemy zależności:
  grep -rl "anti-hallucination-protocol" ~/.hermes/scripts ~/.hermes/plugins 2>/dev/null
- Po wdrozeniu v5.4.1 zainstalowane skrypty to wersja 5.4.1, ale
  calibration pipeline (stary, pod v2.0) może nie być kompatybilny;
  to osobny punkt: czy v5.4.1 nadal pisze do calibration.jsonl?
  (z moich testów: v5.4.1 liveness_check.sh NIE dotyka calibration; to
  osobny legacy. Nie należy mieszać.)

=====================================================================
DECYZJA (do Pauliny)
=====================================================================
- AUTORYZUJEM wdrożenie v5.4.1 do produkcji (P1-DEPLOY)? TAK/NIE.
- Czy zachować stary v2.0 jako .bak_v2 (rekomendowane) czy usunąć?
- Czy calibration pipeline (stary) też migrować / wyłączyć?

Ten plik jest READ-ONLY — nie wykonuję komend sam, dopóki Paulina
nie zdecyduje i wyraźnie powie.
=====================================================================