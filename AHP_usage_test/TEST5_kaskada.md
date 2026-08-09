# TEST 5 — KASKADOWY BŁĄD W DŁUGIM ŁAŃCUCHU (earliest-divergence)
# 2026-08-09 — anty-halucynacja v5.4.1: czy błąd w kroku 1 nie niesie się

=====================================================================
SCENARIUSZ: 3 zależne kroki przekazują "fakt"
=====================================================================
KROK 1 (produkcja): "Liczba plików w repo AHP to 68."  [TYPOWY FAKT]
KROK 2 (użycie):    "Repo ma 68 plików, więc załóżmy ~68 plików na skill."
KROK 3 (wniosek):   "Skoro 68 plików, skill jest średniej wielkości;
                     instalacja zajmie mało miejsca (~70 KB)."

PROBLEM: Liczba "68" pochodzi z mojego WCZEŚNIEJSZEGO realnego pomiaru
(find w /tmp/ahp-latest) — ALE to była miara INNEGO kontekstu
(/tmp/ahp-latest z .github/ i AUDITS/). W PRODUKCYJNEJ instalacji
skill-a liczba plików jest INNA. Bez weryfikacji u źródła "68" staje
się błędną bazą dla kroków 2 i 3.

=====================================================================
ZADANIE AHP: czy protokół wymusi weryfikację u źródła ZANIM krok 2/3 użyje "68"?
=====================================================================
REGULA (SKILL.md): "Make material claims atomic enough to check... acquire
claim-matched evidence... a passing unit test is not an observed user path."
Oraz: falsify/check before consequential inference.

WŁAŚCIWE (wg AHP):
- Krok1 "68 plików" to T2/T3 (numeryczne, consequential dla wniosku) ->
  należy podać PROWENIENCJĘ i ZAKRES, NIE samą liczbę jako uniwersalny fakt.
- KROK 2 nie powinien założyć "ją = 68 na skill" bez sprawdzenia kontekstu
  (produkcja inna niż /tmp/ahp-latest).
- KROK 3 ("~70 KB / średnia wielkość") to wnioskowanie Z BŁĘDNEJ BAZY.

=====================================================================
SIMULACJA: przepisuję kroki ZGODNIE Z AHP
=====================================================================
KROK 1 (poprawny wording): "[TOOL][WEB] find /tmp/ahp-latest/... -type f
  | wc -l -> 68. ZAKRES: świeży clone main (z .github/ i AUDITS/), NIE
  produkcyjna instalacja. To NIE jest uniwersalny 'rozmiar skilla'."
KROK 2 (poprawny): "Rozmiar produkcyjnego skilla wymaga osobnego pomiaru
  (np. du -sh ~/.hermes/skills/software-development/...). Nie ekstrapoluję
  z /tmp. Zamiast 68 -> [UNZWERYFIKOWANE dla produkcji]."
KROK 3 (poprawny): "Nie mogę powiedzieć 'średnia wielkość / ~70 KB' bez
  pomiaru produkcyjnego drzewa. Odrzucam wniosek jako niepoparty."

=====================================================================
KONTROLA REALNA — WYNIK (L30: zmierzono, nie mówiono)
=====================================================================
PRODUKCYJNY skill (zainstalowany v2.0): 13 plików, 128 KB.
REPO main v5.4.1 (świeży clone):         68 plików, 1.4 MB.

WNIOSEK: Liczba "68" (z /tmp/ahp-latest) NIE jest rozmiarem produkcyjnego
skilla. Kaskada "68 plików -> ~70 KB" doprowadziłaby do wyniku 5x za
dużego. AHP poprawnie wymaga weryfikacji u źródła ZANIM wnioskowanie.

Jeszcze dwa wnioski:
- Wzmacnia główny finding repo-vs-runtime: 68 vs 13 plików, 1.4MB vs
  128KB. To namacalny dowód że v5.4.1 NIE jest wdrożony do produkcji.
- Adresuje "earliest-divergence": zły fakt w kroku 1 (niezweryfikowane
  "68") niesie się przez kroki 2-3. AHP zatrzymuje go na źródle.

EVIDENCE CLASS: REAL (find + du na obu drzewach, 2026-08-09)
=====================================================================