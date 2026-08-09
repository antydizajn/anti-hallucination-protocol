# PAKIET DECYZYJNY — AHP v5.4.2 (dla Pauliny, po przebudzeniu)
# 2026-08-09 08:14 — do szybkiej decyzji, bez czytania 20 plikow

=====================================================================
JEDNA DECYZJA: ZOSTAWIĆ v5.4.2 CZY ROLLBACK do v2.0?
=====================================================================
REKOMENDACJA: ZOSTAWIĆ v5.4.2 (zainstalowana i zweryfikowana nawet)
=====================================================================

DLACZEGO:
- To jest wersja ktora sama chcialas zainstalowac ("najnowszego z GitHub,
  v5.4.2"). Repo main = v5.4.2 (commit c6ee5f1). Wdrozenie dokladne.
- 126/126 testow PASS, integrity/provenance/liveness PASS.
- Producja == najnowszy main github (sha256 649bcc3e, bajt-w-bajt).
- Nowa regula v5.4.2 "user pressure does not strengthen evidence" jest
  trafna (adresuje znaleziony wczesniej finding G) i dziala (testowany).
- v2.0 (stary) mial MARTWY helper (11x verify_claim.sh nie istnieje) +
  zmierzona nadpewnosc 91% vs 77%. v5.4.2 to usuw.

ROLLBACK (jesli jednak chcesz):
  mv ~/.hermes/skills/software-development/anti-hallucination-protocol \
     ~/.hermes/skills/software-development/anti-hallucination-protocol.v542
  mv ~/.hermes/skills-archive/anti-hallucination-protocol.v2.0.0 \
     ~/.hermes/skills/software-development/anti-hallucination-protocol
  (wszystko jest w DZIENNIK_WDROZENIA_v542.md)

=====================================================================
CO DOKŁADNIE ZROBIONO (podsumowanie 5h testow + wdrozenie)
=====================================================================
[WDROZENIE]
- backup v2.0 -> ~/.hermes/skills-archive/ (FIX: backup poza katalogiem
  skills, bo zostawienie .bak_v2 powodowalo "ambiguous skill name")
- instalacja v5.4.2 z main GitHub (c6ee5f1), bez .git
- weryfikacja: integrity/provenance/liveness/pytest 126/126, CLI checkers,
  Hermes skill_view laduje v5.4.2, sha256 == main
- rollback 2-krokowy, backup kompletny (13 plikow)

[ZNALEZIONE (co wazne)]
- P0: BRAK (zero reproduced FALSE VERIFIED / FALSE SUCCESS na bramkach)
- P1-BEHAVIOR: self-detection glitcha (recursive meta-collapse) NIE istnieje
  w protokole — recovery to prose, nie enforced check. Wystapil 2x w tej
  sesji. Autorzy sami to przyznaja (inventory PROJECT-HANDOFF / AUDITS).
  -> to NIE bug repo; to granica prompt-policy. Wspoldzial czlowieka /
  zewnetrzny monitoring jest istotny (dokladnie jak dyskutowalysmy).
- P1-DEPLOY: stary v2.0 nie wdrozuony -> ROZWIAZANE (zainstalowano 5.4.2)
- P2: caveman-vs-AHP (kompresja stylu vs evidence; kompatybilne, ale w T3
  nie kompresuj dowodu). Long-session drift: pomylenie liczby z pamieci
  mimo pomiaru (realny dowod granicy). Brak behavioral benchmarku w repo.
- P3: kosmetyka (np. .zip archiwalny w skills dir — nie koliduje)

[CO DZIALA SWIETNIE (testowane)]
- research-first zlapal moj blad prawny (art.113[1] vs 113[5] KRO)
- current-state: rozdziela proces / endpoint / integracje z kluczem;
  clock-skew 5min poprawnie (future >6min reject)
- deterministic checkery: FAIL-CLOSED na nieistniejacym/nie-JSON/pustym;
  CONFLICT/CONTRADICTED 6/6; prompt-injection w data NIE dziala na checker
  (kod, nie LLM) — odporne
- user-pressure v5.4.2: presja NIE podnosi evidence; nowy dowod tak
- T0/T1 lekkie (nie ceremonizuje), T2 lekka sciezka, T3 twarde
- pomiary: count=407466 (z zywego stanu, nie z pamieci 40k)

[LIMITY (uczciwie)]
- behavioral obedience w dlugim, niezapowiedzianym kontekscie NIE jest
  udowodnione; to nie ma benchmarku. Glitch + long-session drift to dowod.
- "INSTALL NOW" = TAK dla v5.4.2 (ja zainstalowalem i dziala), ALE to nie
  znaczy ze prompt-policy panaceum. Nic nie zastepuje zewnetrznych bramek
  + wspoludzialu czlowieka przy wysokiej stawce.

=====================================================================
ARTEFAKTY (18-19 plikow w WORKSPACE/AHP_usage_test/)
=====================================================================
RAPORT_KONCOWY_FINAL.md   -- podsumowanie 5h + odpowiedz "czy to nie halucynacja"
DZIENNIK_WDROZENIA_v542.md -- pelna sekwencja wdrozenia (replikowalna)
MATRYCA_POKRYCIA.md        -- wszystkie testy (T0-T3, deterministyczne)
FINDING_G_glitch.md        -- behavioralna luka (P1)
FINDING_long_session_drift.md -- kolejny dowod granicy (P2)
FINDING_caveman_vs_AHP.md / FINDING_output_discipline_vs_AHP.md
TEST_*/RAPORT_*/szkic_*    -- poszczegolne testy i artefakty

=====================================================================
NASTĘPNE KROKI (do decyzji)
=====================================================================
1. Zostawic v5.4.2? (rekomendacja: TAK)
2. Czy chcesz zeby dodac do PATCH_QUEUE sugestie: usunac/zmniejszyc
   zaleznosc od self-notice w recovery (P1-BEHAVIOR)? To wymaga zgody
   bo to zmiana rdzenia.
3. Czy mamy przygotowac formalny behavioral benchmark do repo? (to jest
   to co usunal/finding "no empirical evidence of use" — potwierdzone)
=====================================================================