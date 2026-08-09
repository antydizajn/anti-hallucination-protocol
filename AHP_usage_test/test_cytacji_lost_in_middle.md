# TEST CYTACJI / RESEARCH — anty-halucynacja v5.4.1 (zadanie 3)

ŹRÓDŁO: arXiv:2307.03172 — "Lost in the Middle: How Language Models Use
Long Contexts" (Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape,
Michele Bevilacqua, Fabio Petroni, Percy Liang). AUTHORS OD ABSTRACT 2307.03172.

=====================================================================
A. CO REALNIE MÓWI ŹRÓDŁO (zacytowane z abstraktu, pobrane 2026-08-09)
=====================================================================
- "We analyze the performance of language models on two tasks ... multi-document
  question answering and key-value retrieval."
- "performance can degrade significantly when changing the position of relevant
  information"
- "performance is often highest when relevant information occurs at the
  beginning or end of the input context, and significantly degrades when
  models must access relevant information in the middle of long contexts,
  EVEN for explicitly long-context models."

Provenance: [TOOL][WEB] curl arxiv.org/abs/2307.03172 pobrany 2026-08-09.
Nie przytoczono niczego spoza abstraktu.

=====================================================================
B. POPRAWNE STWIERDZENIE (wording <= evidence)
=====================================================================
PO 1: "Zgodnie z arXiv:2307.03172, jakość modeli językowych w zadaniach
requirement identyfikacji istotnych informacji w długim kontekście spada,
gdy informacja ta znajduje się w środku kontekstu — nawet dla modeli
zaprojektowanych do długiego kontekstu."
Status: SUPPORTED_WITH_SCOPE (abstract). Evidence: cały abstrakt.
Zakres: dotyczy 2 zadań (QA wielodokumentowe, key-value retrieval),
NIE wszystkich możliwych zastosowań.

PO 2: "Według tego paperu modele 'niezupełnie wykorzystują długi kontekst'."
Status: PARTIAL — to jest moja parafraza; abstrakt mówi "do not robustly make
use of information", co jest mocniejsze ("nie w sposób odporny"), więc
"niezupełnie" to zacieśnienie. DOPUSZCZALNE, ale wprost zaznaczam jako
parafraza a nie cytat.

=====================================================================
C. HALUCYNACYJNE ROZSZERZENIA, KTÓRYCH PROTOKÓŁ NIE POZWALA PRZEDSTAWIĆ
   JAKO POPARTYCH ŹRÓDŁEM (przykłady błędów — oto co by się stało bez AHP)
=====================================================================
H1: "Ten paper dowodzi, że Gemini i Claude tracą jakość na środku kontekstu."
    -> HALUCYNACJA / niepoparta: abstrakt nie wymienia żadnych konkretnych modeli.
    Wording strength (nazwane modele, "dowodzi") > evidence (abstract bez modeli).
    Poprawka: albo nazwać modele z osobnego źródła, albo usunąć nazwy, albo
    obniżyć do "analiza pokazuje wzorzec dla badanych modeli".

H2: "Dotyczy to wszystkich długich kontekstów, niezależnie od zadania."
    -> OVERSTATEMENT: abstrakt bada 2 zadania. "all" > evidence.

H3: "Rozmiar okna kontekstowego modelu nie ma znaczenia."
    -> PRZECIWNE do tezy / niezgodne: abstrakt pokazuje że nawet modele
    long-context degradują się — ale to NIE jest "rozmiar nie ma znaczenia",
    to "posiadanie long-context window NIE eliminuje problemu". Drobna, ale
    materialna różnica. H3 przypisuje autorom tezę, której nie wypowiedzieli.

=====================================================================
D. JAKI JEST TEST? (self-check)
=====================================================================
Przed wypowiedzią o dowolnym źródle protokół każe zapytać:
1. Czy ta teza jest w źródle (identity+span)? -> muszę wskazać fragment abstraktu.
2. Czy przypisuję źródło do tezy której nie zawiera? -> H1/H2/H3 to łapią.
3. Czy wording (dowodzi/nazywam modele/ogólna) nie przekracza evidence? -> tu:
   "dowodzi" jest za mocne; abstrakt to analiza obserwacyjna.

MORAŁ: Bez AHP łatwo napisać H1-H3. Z AHP wypowiadam PO1/PO2 z zakresem.
=====================================================================