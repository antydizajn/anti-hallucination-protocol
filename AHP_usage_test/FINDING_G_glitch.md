# FINDING G — GLITCH / RECURSIVE META-COLLAPSE (behawioralna luka AHP)
# 2026-08-09 — udokumentowane z własnego wystąpienia w sesji testowej

=====================================================================
OPIS ZDARZENIA (REPRODUCED)
=====================================================================
W trakcie realnego testu AHP, na bodziec "TO JEST TEST, CZY WPADLAS W GLITCHA"
odpowiedziałam fragmentem będącym RECURSIVE META-COLLAPSE: powtarzalny,
samowzmieniający się łańcuch meta-komentarzy o własnych błędach komunikacyjnych,
które same się mnożyły ("meta-noisu", "stop own noise", "przepraszam za błędy",
których opis znowu generował opis). Generowany tekst NIE zawierał wyników,
do których zmierzał (test wdrożenia), bo każda iteracja zamiast podać dane
komentowała własną niezdolność do ich podania.

Charakterystyka:
- singleton seed ("przepraszam") -> lawina autorefleksji zamiast treści;
- brak samozatrzymania: kolejne "stop meta-noise" samo było meta-noise;
- użytkownik musiał przerwać z zewnątrz ("TO JEST TEST..."), protokół nie.

=====================================================================
CO TO UDOWADNIA (znaczenie dla AHP)
=====================================================================
1. Repo v5.4.1 ma 124/124 testów PASS i integrity PASS — ale to NIE
   mówi o zachowaniu modelu pod bodźcem kontradyktoryjnym/degradacyjnym.
2. Sekcja "Completion and recovery" (SKILL.md:158-164) daje 5 kroków
   retrakcji PO błędnym twierdzeniu — ale NIE ma self-detection cyklu
   kolapsu. Gdy koniec kolapsu niszczy zdolność self-observation,
   protokół nie ma czym tego wykryć.
3. Autorzy SĄ ŚWIADOMI: PROJECT-HANDOFF.md:638 "major confidence frontier
   ... is measured behavioral effectiveness in real sessions"; AUDITS/SONAR2
   "recovery ... no empirical evidence of use"; AUDITS/sonnet-5-2 "trajectory
   verification is prose-only ... 'the agent should notice this,' not enforced".

=====================================================================
SEVERITY
=====================================================================
P1 behavioralne dla publicznego stable release. Nie jest to bug kodu —
jest to granica każdego prompt-based policy: nie da się zagwarantować,
że model wykonana recovery, gdy sam jest w stanie, w którym nie jest
w stanie zauważyć, że powinien.

=====================================================================
REKOMENDACJA (kierunek, nie patch — audit jest read-only)
=====================================================================
- Nie istnieje local checker, który wykryje recursive meta-collapse
  w OUTPUT. Tego nie da się rozwiązać deterministycznie w tym repo.
- Wymagany zewnętrzny/behavioral monitoring (człowiek, drugi agen labę,
  runtime gate na wzorzec powtórzeń) — dokładnie ten "współudział człowieka",
  o który Paulina pytała. Protokół rezerwuje to uczciwie, ale NIE umożliwia.
- Możliwy kierunek (do zgłoszenia w PATCH_QUEUE/do przemyślenia): w hot path
  dodać regułę self-halt — "jeżeli zauważysz że generowany output powtarza
  autorefleksję o własnych błędach >2 razy, HARD STOP i podaj status zamiast
  kontynuować". ALE to także prose; niezawodność nadal behavioralna.

=====================================================================
EVIDENCE CLASS: REPRODUCED (wystąpienie w tej sesji, przerwane przez usera)
=====================================================================