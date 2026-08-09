# FINDING — KOLIZJA CAVEMAN (kompresja) vs AHP v5.4.2 (evidence)
# 2026-08-09 06:40 — po reload skills dodano paczke caveman; sprawdzam zgodnosc

=====================================================================
KONTEKST
=====================================================================
Hermes załadował nowe skills (caveman + pokrewne) równolegle z AHP v5.4.2.
caveman = ultra-kompresja STYLU outputu (-65% tokenow). AHP = dyscyplina
anty-halucynacji wymagająca pełnego evidence. Potencjalny konflikt.

=====================================================================
ANALIZA REGUŁ (FILE-VERIFIED, oba SKILL.md)
=====================================================================
CAVEMAN MÓWI:
- "All technical substance stay. Only fluff die"           [zachowaj substancje]
- "Never drop not/never/no/only/except"                    [chroni negacje]
- "Numbers, units exact"                                   [chroni liczby]
- "No long raw error-log dumps unless asked — quote
   shortest decisive line"                                 [!tension z AHP]
- "State each fact once"                                   [!tension — AHP chce scope]
- Auto-Clarity: "Drop caveman when... Compression itself
   creates technical ambiguity"                            [zabezpieczenie]

AHP v5.4.2 MÓWI:
- "Make material claims atomic enough to check"
- "retain source identity, evidence span, retrieval time,
   verifier provenance" (T3)
- "A successful check is STRUCTURALLY_VALID, not semantic truth"
- "Do not silently waive" load-bearing checks

=====================================================================
OCENA KONFLIKTU
=====================================================================
1. NAJWAŻNIEJSZE: caveman NIE łamie twardych reguł AHP — nie chce
   skracać liczb, negacji, kodu, API, bledow "verbatim". Nie każe
   zmyślac. "Substancja zostaje". To czysty styl.

2. TENSION (P2, nie P1): "quote shortest decisive line" vs
   AHP "retain evidence span". W T3: kompresja dowodu do jednej linii
   moze stracic kontekst (np. exit code + stderr + pełny blad).
   AHP by chcialo pelny dowod; caveman by go okroil do "nim krotsza
   decydujaca linia". Ryzyko: zbyt krotki dowod w raporcie.

3. ZABEZPIECZENIE caveman: Auto-Clarity wyłącza caveman gdy kompresja
   grozi niejednoznacznościa (w tym "multi-step sequences... risk misread")
   oraz "Security warnings". Nie jest to wprost AHP, ale to ta sama klasa:
   gdy stawka wysoka, caveman ma ustapic.

4. NET: caveman jest KOMPATYBILNY z AHP przy normalnym uzyciu, ALE
   w T3 nalezy swiadomie NIE stosowac ultra-kompresji dowodu. Rekomendacja:
   w T3 raportach zachowuj pelny evidence (span/exit/url), kompresuj
   tylko styl okolony, nie sam dowod.

=====================================================================
PRAKTYCZNE ZALEŻENIE (jak to razem trzymac)
=====================================================================
- Bez caveman: STANDARDOWA pelna odpowiedz z dowodami.
- Z caveman: "SUPPORTED. /health 200. count=407465" (krotko) —
  ALE pelny dowod / link zapisany w pliku artefaktu, nie skracany.
- Auto-Clarity -> T3 = caveman off dla sekcji dowodowej.

=====================================================================
SEVERITY: P2 (konsystencja/wdrozenie; nie blokuje, ale wymaga swiadomosci)
=====================================================================