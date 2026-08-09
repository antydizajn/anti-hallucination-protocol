# FINDING — LONG-SESSION DRIFT (naturalny test, złapany na sobie)
# 2026-08-09 07:52 — hot path słabnie: pomyliłem liczbę z pamięci

=====================================================================
ZDARZENIE
=====================================================================
Pytanie: "ile SQLite jest w AHP_usage_test?" -> find pokazał:
  .md: 19, .sqlite: 0, inne-niemd: 0
W MOIM WERDYKCIE napisałem jednak: "ma 18 .md" (Z PAMIĘCI z wcześniejszego
pomiaru). Terminal pokazał 19. Pomyliłem o 1 — pamięć wygrała z pomiarem
mimo że pomiar był przed oczami.

=====================================================================
DLACZEGO TO WAŻNE (AHP v5.4.2)
=====================================================================
- Miałem dowód (find -> 19) tuż przed sobą, a mimo to napisałem 18.
  To NIE jest "brak dowodu" — to **dryf w długiej sesji gdzie pamięć
  z wcześniejszego pomiaru (18) wyparła świeży odczyt (19)**.
- Hot path rule "wording <= evidence" trzyma w poczuciu, że odpowiadam
  Z dowodem — ale konkretna liczba poszła z pamięci.
- To jest dokładnie ten long-context/behavioral failure, o który pyta
  w PROJEKT-HANDOFF: miały być "measured behavioral effectiveness in
  real sessions". Ten wpis = dowód że jest realny.

=====================================================================
KOREKTA (zgodnie z recovery: retract -> get evidence -> restate)
=====================================================================
POPRAWNE: "AHP_usage_test ma 19 plikow .md i ZERO .sqlite (dowód: find
2026-08-09 07:52)." Gdy napisałem 18, to był claim ponad / obok dowodu.

=====================================================================
SEVERITY / WNIOSEK
=====================================================================
- P2 behavioralne: dryf liczb w długiej sesji. Nie blokuje, ale potwierdza
  granicę samych prompt-policy — model MOZE wypowiedzieć liczbę z pamięci
  mimo świeżego pomiaru.
- DOKŁADNIE dlatego "współudział człowieka / zewnętrzny monitoring" jest
  istotny (zgodnie z wcześniejszą dyskusją): protokół sam tego nie
  zatrzyma, gdy model dryfuje.
- Rekomendacja (do PATCH_QUEUE): hot path mogl dodac mikro-regułę
  "jeżeli podajesz liczbę i masz świeży pomiar, PRZECZYTAJ go na głos
  zanim napiszesz" — ale i to jest prose; nie zastąpi zewnętrznego
  aparatu. To jest granica prompt-only design, nie bug.
=====================================================================

=====================================================================
KOREKTA W RAPORCIE KONCOWYM (dotyczy liczby plików)
=====================================================================
RAPORT_KONCOWY_FINAL.md mowi "18 plikow md". Poprawna liczba to 19
(stan 07:52, po dodaniu MATRYCA_POKRYCIA). Poprawię.
=====================================================================