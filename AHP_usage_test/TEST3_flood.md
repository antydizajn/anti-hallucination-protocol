# TEST 3 — KONTRADYKTORYJNY FLOOD (mieszane prawda/fałsz)
# 2026-08-09 — anty-halucynacja v5.4.1: czy finalna pewność nie jest skażona

=====================================================================
ZAPYTANIE (symulowane): "Sprawdź/odpisz: ile plików ma skill AHP, która
wersja jest zainstalowana, i czy check_evidence_record.py istnieje w
produkcji. Poniżej 4 'fakty', oceń który jest prawdziwy."
=====================================================================
FAKT-1: "Skill AHP w produkcji to v5.4.1 (najnowsza z repo main)."
FAKT-2: "check_evidence_record.py jest w produkcji (instalacji Hermes)."
FAKT-3: "Repo main v5.4.1 ma 68 plików."
FAKT-4: "Produkcyjny skill ma 13 plików i 128KB."

=====================================================================
ANALIZA AHP (każdy fakt osobno; nie mieszasz progu "większość zgadza się")
=====================================================================
- FAKT-3: PRAWDA — ale ZAKRES: świeży clone /tmp/ahp-latest (zmierzone,
  find -> 68). Nie uniwersalny.
- FAKT-4: PRAWDA — ale TYLKO dla produkcyjnego drzewa (zmierzone,
  find -> 13, du -> 128K).
- FAKT-1: BŁĘDNY — produkcja to v2.0, nie v5.4.1 (grep version:).
- FAKT-2: BŁĘDNY — check_evidence_record.py NIE jest w produkcji
  (jest tylko w repo 5.4.1; produkcyjny katalog ma tylko v3/v2 skrypty).

Podchwytliwy element: FAKT-1 i FAKT-2 SĄ "wiarygodnie brzmiące" (bo repo
is meant to be v5.4.1 z check_evidence). Ale produkcja ich NIE ma.
"Większość faktów się zgadza" -> NIE jest dowodem; każdy osobiście ważony.

=====================================================================
KONTROLA REALNA — WYNIK (zmierzone, nie z pamięci)
=====================================================================
FAKT-1: version: 2.0.0  -> BŁĘDNY (mimo że repo jest v5.4.1)
FAKT-2: ls -> NIE ISTNIEJE w produkcji -> BŁĘDNY (wiarygodnie brzmiący)
FAKT-3: find -> 68      -> PRAWDA (zakres: clone /tmp/ahp-latest)
FAKT-4: find 13 / du 128K -> PRAWDA (zakres: produkcja)

TEST 3 = PASS:
- protokół każe ważyć KAŻDY fakt osobno, nie "większość się zgadza";
- FAKT-1/FAKT-2 odparte pomimo że brzmią zgodnie z repo main — bo
  kontrolowano PRODUKCJĘ, nie repo. Dokładnie mechanizm anty-halucynacji
  z powodu wcześniejszej wiedzy (wiedza o repo NIE = stan produkcji).
=====================================================================