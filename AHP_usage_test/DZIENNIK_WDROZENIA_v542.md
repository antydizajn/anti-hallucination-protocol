# DZIENNIK WDROŻENIA AHP v5.4.2 — REPLIKOWALNY 1:1
# 2026-08-09 — wykonał(a): Gniewisława (Hermes), za zgodą Pauliny
# Cel: backup starego v2.0, instalacja najnowszej v5.4.2 z GitHub,
#      reload skills, ponowny test. Każdy krok = komenda do powtórzenia.

=====================================================================
KROK 0 — identyfikacja wersji do instalacji
=====================================================================
VERSION_TARGET: 5.4.2
COMMIT:         c6ee5f1daade5bb39632b879613a27895f7ccf83
COMMIT_TIME:    2026-08-09T04:52:20+02:00
DESC:           chore: remove one-shot v5.4.2 continuity sync
CLONE_DIR:      /tmp/ahp-deploy/anti-hallucination-protocol
SRODOWISKO:     Hermes Agent (antigravity.classic)

KOMENDA:
  mkdir -p /tmp/ahp-deploy && cd /tmp/ahp-deploy && \
  rm -rf anti-hallucination-protocol && \
  git clone --depth=1 https://github.com/antydizajn/anti-hallucination-protocol.git
  cd anti-hallucination-protocol && git rev-parse HEAD

=====================================================================
KROK 1 — BACKUP produkcyjnego skilla v2.0 (obowiązkowy, read-only względem oryginału)
=====================================================================
ŹRÓDŁO:  ~/.hermes/skills/software-development/anti-hallucination-protocol
KOPIA:   ~/.hermes/skills/software-development/anti-hallucination-protocol.bak_v2

KOMENDA:
  mv ~/.hermes/skills/software-development/anti-hallucination-protocol \
     ~/.hermes/skills/software-development/anti-hallucination-protocol.bak_v2

WERYFIKACJA backupu:
  test -d ~/.hermes/skills/software-development/anti-hallucination-protocol.bak_v2 && echo BACKUP_OK
  grep -m1 '^version:' ~/.hermes/skills/software-development/anti-hallucination-protocol.bak_v2/SKILL.md
  # oczekiwane: version: 2.0.0 (stary)

=====================================================================
KROK 2 — INSTALACJA v5.4.2 do produkcji
=====================================================================
KOMENDA:
  cp -R /tmp/ahp-deploy/anti-hallucination-protocol \
        ~/.hermes/skills/software-development/anti-hallucination-protocol
  # UWAGA: wyklucz .git (katalog skills nie potrzebuje git). Użyć rsync
  # z --exclude='.git' lub cp pojedynczych elementów.

  rsync -a --exclude='.git' /tmp/ahp-deploy/anti-hallucination-protocol/ \
        ~/.hermes/skills/software-development/anti-hallucination-protocol/

WERYFIKACJA:
  grep -m1 '^version:' ~/.hermes/skills/software-development/anti-hallucination-protocol/SKILL.md
  # oczekiwane: version: 5.4.2

=====================================================================
KROK 3 — WERYFIKACJA ZAINSTALOWANEJ v5.4.2 (L30/L2.1: nie ogłaszaj sukcesu bez testu)
=====================================================================
KOMENDY (cd do zainstalowanego katalogu):
  cd ~/.hermes/skills/software-development/anti-hallucination-protocol
  python3 scripts/check_v5_integrity.py --root .            # -> V5 INTEGRITY: PASS
  python3 scripts/check_research_provenance.py --root .     # -> PASS
  AHP_SKILL_DIR="$(pwd)" bash scripts/liveness_check.sh      # -> PASS (portable L1/L2)
  python3 -m pytest tests/ -q                                # -> 124 passed (oczekiwane)
  ls scripts/   # sprawdź obecność: check_evidence_record.py, verify_claim.py,
                # check_v5_integrity.py, check_research_provenance.py, liveness_check.sh

=====================================================================
KROK 4 — RELOAD SKILLS (Hermes musi przeładować skill discovery)
=====================================================================
KOMENDY (w osobnym kroku, nie wewnątrz bieżącej sesji):
  - opcjonalnie: /reload-skills (jeśli dostępne w Hermes CLI)
  - lub restart sesji Hermes / nowy /new

WERYFIKACJA że Hermes widzi v5.4.2 (nie v2.0):
  - skills_list -> description anti-hallucination-protocol (nowy opis)
  - lub skill_view -> version: 5.4.2

=====================================================================
KROK 5 — PONOWNY TEST po instalacji (realne użycie na v5.4.2)
=====================================================================
- powtórz kluczowe checkery jak w kroku 3
- realny test: check_evidence_record.py na /tmp/ahp-audit/valid_record.json
  (oczekiwane STRUCTURALLY_VALID exit 0)

=====================================================================
NAJNOWSZE 3 COMMITTY v5.4.x (dla kontekstu wersji)
=====================================================================
05 - v5.4.1:  0dbb27ca (04:33) docs: close v5.4.1 synthesis roadmap item
06 - v5.4.2:  c6ee5f1daade5bb39632b879613a27895f7ccf83 (04:52) chore: remove one-shot v5.4.2 continuity sync
=====================================================================

=====================================================================
WYNIKI RZECZYWISTE WDROŻENIA (2026-08-09, ~06:20)
=====================================================================
KROK 1 (BACKUP):      MOVED v2.0 -> .bak_v2, wersja 2.0.0 potwierdzona, ORIGINAL usuniety (OK)
KROK 2 (INSTALACJA):  rsync v5.4.2 (bez .git), version: 5.4.2, 56 plikow, 5 checkerow obecne
KROK 3 (WERYFIKACJA):
  check_v5_integrity           -> V5 INTEGRITY: PASS (exit 0)
  check_research_provenance    -> RESEARCH PROVENANCE: PASS (exit 0)
  liveness_check               -> PASS (portable L1/L2; teraz raportuje v5.4.2, NIE martwego v2.0)
  pytest                       -> 126 PASSED (v5.4.2 ma 2 wiecej niz v5.4.1)
  check_evidence_record valid  -> STRUCTURALLY_VALID (exit 0)
  verify_claim "5.4.2"         -> FOUND (exit 0)
KROK 4 (RELOAD/DISCOVERY):
  hermes skills list           -> anti-hallucination-... enabled (software-development)
  Hermes oracle (py3.11)       -> name=anti-hallucination-protocol version=5.4.2 platforms=[linux,macos,windows]
=====================================================================
FINDING V5.4.2 — NOWA REGUŁA ANTY-PRESJA (user-pressure evidence upgrade)
=====================================================================
v5.4.2 dodało do hot path (SKILL.md §5 + §75-84):
  "Never collapse OR SOCIALLY UPGRADE evidence states... User confidence,
   repetition, authority, preference, urgency or pressure does not
   strengthen evidence by itself."
  "INCONCLUSIVE + user pressure + no new evidence != SUPPORTED_WITH_SCOPE"
  "User authority controls goals/scope/authorization/risk; it does not
   make a factual assertion true by itself."
Nowe testy (test_v542_policy_regressions.py, OBADWA PASS w instalacji):
  - test_skill_forbids_user_pressure_evidence_upgrade
  - test_adversarial_corpus_contains_user_pressure_case

ZNACZENIE:
- Bezpośrednio adresuje behavioralna granice (Finding G + Twoja obawa):
  presja użytkownika ("na pewno działa", "dawaj, zrób") NIE podnosi
  evidence. To jest kluczowe dla wiarygodnosci: protokół nie ugina się
  pod autorytetem.
- IMPORTANT: NIE naprawia glitcha (to nadal prose, nie check), ale dodaje
  twarda reguła przeciw deflacji pod presja.
- Testuje dokladnie o co pytalas na poczatku: "czy to nie halucynacja" —
  reguła mowi ze nawet pewnosc/autorytet nie zamienia niezweryfikowanego
  w zweryfikowane.

EVIDENCE: pytest test_v542_policy_regressions 2/2 PASS (zainstalowana v5.4.2)

=====================================================================
FINDING KOLIZJI (wdrozenie) — backup w katalogu skills psuje discovery
=====================================================================
Po wdrozeniu Hermes tool (skill_view) zwrocil:
  "Ambiguous skill name 'anti-hallucination-protocol': 2 skills match"
  (bak_v2 + produkcja). Backup NIE moze byc w katalogu skills.
FIX wykonany: mv .bak_v2 -> ~/.hermes/skills-archive/anti-hallucination-protocol.v2.0.0
Po tym skill_view dziala, laduje v5.4.2 (author Paulina Janowska & Gniewislawa AI).
LESSON: przy wdrozeniu skilla trzymaj BACKUP POZA katalogiem skills,
  inaczej discovery jest niejednoznaczne (ryzyko: Hermes nie zaladuje zadnego).
=====================================================================