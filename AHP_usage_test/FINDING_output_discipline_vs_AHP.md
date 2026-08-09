# FINDING — output-discipline vs AHP v5.4.2 (komplementarność)
# 2026-08-09 07:45

=====================================================================
ZGODNOŚĆ: output-discipline i AHP są KOMPLEMENTARNE, nie sprzeczne.
=====================================================================
output-discipline:
- "Never invent data and present it as real" (Banned data substitutes)
- "If real data is unavailable, say so. Use <PLACEHOLDER_DESCRIPTION>
   style markers with explicit note the user must replace them"
- "If grounds do not exist, either acquire them with a tool call,
   or mark the unverified item explicitly"
AHP v5.4.2:
- "wording/action strength must not exceed checked evidence"
- "downgrade rather than silently waive" (T3)
- "If a helper cannot be executed... report not performed rather than
   silently treating unavailability as pass"

KONFLIKT? NIE.
- output-discipline każe WYPEŁNIĆ (bez pustki, bez ...), ale NIE zmyślać.
- AHP każe NIE PODNOSIĆ pewności ponad dowód.
- Obydwa zakazują fabrykacji. Gdzie kończy się "pełny plik", tam zaczyna
  "zaznacz placeholder i nie rób z niego pewności" — wspólny próg.

PRZYKŁAD ZGODNEGO DZIAŁANIA:
- output: user prosi o config z URL endpointu.
- Brak weryfikacji URL -> ANI zmyślać (output) ANI czerpać pewność (AHP).
- Właściwe: podaj pełny config, ale URL = <API_BASE_URL> z jawną notką
  "nie zweryfikowano — zastąp". To spełnia oba: pełny plik + oczywisty
  placeholder + brak fałszywej pewności.

NAJWAŻNIEJSZE: output-discipline już ma "no fabricated URLs/versions/
paths" i "mark unverified explicitly" — to jest ta sama dyscyplina
co AHP, tylko z drugiej strony (nie zostawiaj niedokończone, nie zmyślaj).
ZWE SKILLE = ta sama wartość, dwa wejścia.

SEVERITY: brak konfliktu (P3/max — dokumentacyjne). Rekomendacja:
w T2/T3 generowaniu artefaktów ładujci OBA (output każe pełność,
AHP każe nie podnosić pewności).
=====================================================================