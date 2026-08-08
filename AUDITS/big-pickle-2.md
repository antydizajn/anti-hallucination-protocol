Mam komplet danych. Oto raport.


================================================================================
FORENSIC REGRESSION AUDIT v5.2 + NOVEL FAILURE HUNT
CURRENT (2.0.0) vs CANDIDATE (5.2.0) — ANTI-HALLUCINATION PROTOCOL
================================================================================


1. EXECUTIVE VERDICT

YES - CLEAR UPGRADE

INSTALL v5.2 NOW: NO (czekam na osobne polecenie — HARD STOP zachowany)
CONFIDENCE: 88%

Próba obalenia nie powiodła się na głównych frontach: R1 (T3 current-state) zablokowany 14/15, R3 (liveness) naprawiony we wszystkich realnych przypadkach, R4 (frontmatter) zablokowany 13/13, R5 (provenance v4 + gap-map) egzekwowany. Znalazłam 2 realne drifty (independence_group nieegzekwowany; SKILL.md v5 section nie walidowany) i 5 nowych luk niższej wagi — żadna nie jest P0. v5.2 jest realnie lepszy i sam siebie broni testami, których v5.1 nie miał.

2. TARGET VERIFICATION

VERIFIED — CANDIDATE = v5.2.0 (frontmatter linia 4: version: 5.2.0, SKILL.md nagłówek "v5.2"). CURRENT = v2.0.0. Oba canonical, ZERO symlinków.
VERIFIED — CANDIDATE: 31 plików, 256 KB. 19 nowych/zmienionych od v5.1 (16:44 → 17:38): SKILL.md 28,566→30,113; README 9,175→11,193; evidence-record.schema.json 2,622→3,157; evidence-state-model.md 5,184→6,578; v5-gap-map.md 11,217→11,365; check_evidence_record.py 7,933→9,591; check_research_provenance.py 5,911→8,343; check_v5_integrity.py 6,959→8,035; liveness_check.sh 3,278; +NOWE: v5-research-manifest.json (3,902, 24 sources), test_liveness.py (1,673). verify_claim.py 12,016 (bez zmian od v5.1).
VERIFIED — testy: 82 fns (było 59): test_verify_claim 17, test_evidence_record 25, test_v5_integrity 18, test_research_provenance 19, test_liveness 3.

3. TEST EXECUTION


COMMAND: python3 -m pytest tests/ -v   (izolowana kopia /tmp/ahp-test3.VPoHW3)
WORKING DIRECTORY: /tmp/ahp-test3.VPoHW3/skill
EXIT CODE: 0
PASSED: 82
FAILED: 0
SKIPPED: 0
WARNINGS: 0
DURATION: 10.05s

COMMAND: python3 scripts/check_v5_integrity.py --root .        -> V5 INTEGRITY: PASS, exit 0
COMMAND: python3 scripts/check_research_provenance.py --root . -> RESEARCH PROVENANCE: PASS, exit 0
COMMAND: AHP_SKILL_DIR=<copy> bash scripts/liveness_check.sh   -> end liveness check: PASS (portable L1/L2), exit 0


4. KNOWN-REGRESSION MATRIX

ID: R1
Previous failure: T3 current-state false strong
v5.2 result: 14/15 ataków zablokowanych (brak source_identity/retrieved_at/observation_time/span/verifier → FAIL; freshness UNKNOWN/STALE/N/A →
  FAIL; verifier UNKNOWN/SUSPECT → FAIL; source_class=unknown → FAIL; 2 weak items → FAIL). Wyjątek: R1-14 garbage strings ("a"/"b"/"c") → PASS
Evidence: 15 probe'ów, sekcja 6
Status: FIXED (R1-14 = świadomy limit non-empty, nie semantyka — dokumentowany w Hard limits)
Column 6:
────────────────────────────────────────
ID: R2
Previous failure: self-declared independence
v5.2 result: Machine-validity FIXED: INDEP+UNKNOWN/HEURISTIC/brak-basis/pusty-basis/ws-basis → FAIL; checker wymaga INDEPENDENT_ORIGIN +
  lineage_verification=VERIFIED + non-empty lineage_basis + source_class!=unknown. Semantic truth: "trust me" basis → PASS (słusznie — zadeklarowane
  w Hard limits). NOWE: independence_group nieegzekwowany (2 items ta sama grupa → PASS)
Evidence: 10 probe'ów
Status: PARTIALLY_FIXED (kontrakt maszynowy OK; drift independence_group — patrz F1)
Column 6:
────────────────────────────────────────
ID: R3
Previous failure: liveness FAIL → exit 0
v5.2 result: Wszystkie realne failure → exit 1: brak SKILL.md/verify_claim.py/integrity-checker, python3 shim exit-1, uszkodzony frontmatter,
  wielokrotne failure → exit 1, "end liveness check: FAIL" w stdout. Legacy calibration missing/stale → INFO, exit 0 (poprawne)
Evidence: 9 probe'ów (w tym czyste pomiary bez pipe)
Status: FIXED
Column 6:
────────────────────────────────────────
ID: R4
Previous failure: malformed frontmatter
v5.2 result: 13/13 zablokowanych: desc [/{, unclosed quote, brak otwarcia/zamknięcia ---, duplicate key, malformed nested, body-version-mask,
  v4.0.0/v6.0.0/v5.2/v5.2.0-beta → FAIL. Flow mapping akceptowany (spójnie z Hermes CSafeLoader). Block scalar \
Evidence: → FAIL (false-negative bezpieczny)
Status: 15 probe'ów
Column 6: FIXED
────────────────────────────────────────
ID: R5
Previous failure: v5 provenance gap
v5.2 result: 2606.01435 POPRAWIONY ("Reliable Post-Retrieval Assembly..." spójny w gap-map + manifest). v4 markdown entries: wrong title/ID/URL →
  FAIL. gap-map vs manifest: extra/missing/duplicate → FAIL. NOWE: SKILL.md "Key v5 additions" (plain text) NIE walidowany vs manifest — wrong
  title/ID w SKILL.md v5 section → PASS
Evidence: 11 probe'ów
Status: PARTIALLY_FIXED (patrz F2)
Column 6:

5. NEW ADVERSARIAL FINDINGS


ID: F1 (N1/R2-7)
SEVERITY: P1
CLAIM: independence_group istnieje w spec (evidence-state-model.md:46) i w schema
	   (evidence-record.schema.json:65), ale ZERO wystąpień w jakimkolwiek checkerze.
	   Dwa evidence items z TYM SAMYM independence_group="G1" (czyli świadomie
	   oznaczonymi jako jedna grupa źródeł) przechodzą T3 SUPPORTED_WITH_SCOPE.
MINIMAL REPRODUCER:
  {"claim_type":"research","risk_tier":"T3","state":"SUPPORTED_WITH_SCOPE",
   "evidence":[ev(source=A, group="G1"), ev(source=B, group="G1")]}
  (oba ev: lineage=INDEPENDENT_ORIGIN, lineage_verification=VERIFIED, basis non-empty)
COMMAND: python3 scripts/check_evidence_record.py <record>
EXPECTED: FAIL (grupa ta sama = brak niezależności = T3 kontrakt złamany)
ACTUAL: EVIDENCE RECORD: PASS, exit 0
WHY IT MATTERS: SKILL.md sekcja 11 mówi "lineage=INDEPENDENT_ORIGIN is not enough"
	   i wymaga niezależności jako "materially different ways of being wrong" —
	   a checker akceptuje dwa źródła w tej samej grupie jako niezależne.
	   To jest deterministycznie wykrywalne (porównanie group), nie zaimplementowane.



ID: F2 (R5-10/R5-11)
SEVERITY: P1
CLAIM: SKILL.md linia 680 twierdzi "The offline provenance checker validates
	   repository-internal identity consistency across both the v4 corpus and the
	   v5 source list" — ale checker waliduje TYLKO v4 markdown entries
	   (SKILL_ENTRY_RE) i gap-map vs manifest. Sekcja "### Key v5 additions"
	   w SKILL.md (19 plain-text bullets) jest poza kontraktem.
MINIMAL REPRODUCER: zmiana "AgentDojo - arXiv:2406.13352" -> "AgentDojo FAKE - arXiv:2406.13352"
	   w SKILL.md sekcja v5 additions
COMMAND: python3 scripts/check_research_provenance.py --root .
EXPECTED: FAIL (wg deklaracji SKILL.md linia 680)
ACTUAL: RESEARCH PROVENANCE: PASS, exit 0
WHY IT MATTERS: dokumentacja obiecuje spójność v5 source list, implementacja jej
	   nie sprawdza — false documentation claim (nie false verified, ale drift
	   spec vs implementation).



ID: F3 (N8)
SEVERITY: P2
CLAIM: observation_time="2099-01-01T00:00:00Z" (przyszłość) przechodzi T3 current_state
	   SUPPORTED_WITH_SCOPE. Schema: observation_time = {"type":["string","null"]}
	   — bez format ISO8601, bez walidacji "nie w przyszłości".
MINIMAL REPRODUCER: jak w N8 (BASE + claim_type=current_state, obs_time 2099)
COMMAND: python3 scripts/check_evidence_record.py <record>
EXPECTED: FAIL lub przynajmniej ERROR (format date-time)
ACTUAL: PASS, exit 0
WHY IT MATTERS: current_state z obserwacją z przyszłości to nonsens semantyczny,
	   deterministycznie wykrywalny (parse + compare z now), nie zaimplementowany.



ID: F4 (N14)
SEVERITY: P2
CLAIM: liveness_check.sh nie uruchamia testów — liveness PASS (exit 0) nawet gdy
	   tests/ są zepsute (test_verify_claim.py z assert False). L1/L2 sprawdzają
	   pliki + integrity, nie testy.
MINIMAL REPRODUCER: podmiana tests/test_verify_claim.py na test_boom() -> assert False
COMMAND: AHP_SKILL_DIR=<copy> bash scripts/liveness_check.sh
EXPECTED: (debatable) FAIL gdy test suite broken
ACTUAL: exit 0, PASS
WHY IT MATTERS: L1/L2 to contract "present and runnable", nie "correct".
	   Jest to częściowo zamierzone (L4 uczciwie UNKNOWN), ale testy są
	   deterministyczne i tanie — liveness mógłby je wołać (--check only).
	   P2, nie P1: liveness nigdy nie obiecywał weryfikacji testów.



ID: F5 (N7 + R1-14 + N13)
SEVERITY: P3
CLAIM: T2 strong akceptuje evidence bez evidence_span/retrieved_at/verifier
	   (świadoma asymetria T2/T3); garbage strings ("a","b","c") przechodzą
	   jako non-empty; evidence z dead pointer (source_identity=/nonexistent)
	   przechodzi PASS.
COMMAND: jak w probes
EXPECTED: dokumentowane granice (T2 = "direct claim-matched evidence",
	   non-empty != meaningful, pointer liveness = external problem)
ACTUAL: PASS — zgodnie z deklarowanym kontraktem
WHY IT MATTERS: świadome ograniczenia warstwy, nie bugi. Zapisane dla pełności.


6. FALSE-POSITIVE LEDGER


NO REPRODUCED FALSE POSITIVES (P0-class) FOUND

Jedyny "PASS mimo wątpliwości" w warstwie deterministycznej to F1 (independence_group) — sklasyfikowany jako P1, bo checker MÓGŁBY to wykryć deterministycznie. R1-14/R2-6 ("trust me" basis, garbage strings) to świadome granice semantic layer, jawnie zadeklarowane w SKILL.md sekcja 24 ("a supplied lineage_basis is factually correct without external inspection") — nie są false positives, są documented limits.

7. SPEC / SCHEMA / IMPLEMENTATION MATRIX

Concept: Entailment values
State model (spec): SUPPORTS, CONTRADICTS, PARTIAL, IRRELEVANT, INCONCLUSIVE, NOT_CHECKED (evidence-state-model.md:90-97)
Schema: ENTAILS, PARTIAL, CONTRADICTS, IRRELEVANT, UNCLEAR (schema:66)
Checker: ENTAILS / CONTRADICTS
Consistent?: DRIFT — spec: SUPPORTS/INCONCLUSIVE/NOT_CHECKED; schema: ENTAILS/UNCLEAR. Ktoś piszący wg spec z SUPPORTS dostanie schema FAIL. P2
Column 6:
────────────────────────────────────────
Concept: Freshness
State model (spec): CURRENT_ENOUGH, STALE_FOR_CLAIM, HISTORICAL_ONLY, UNKNOWN, NOT_APPLICABLE (spec:113-118)
Schema: CURRENT_ENOUGH, STALE, UNKNOWN, NOT_APPLICABLE (schema:60)
Checker: CURRENT_ENOUGH wymagane dla T3 current
Consistent?: DRIFT — spec: STALE_FOR_CLAIM/HISTORICAL_ONLY; schema: STALE. P2
Column 6:
────────────────────────────────────────
Concept: Integrity
State model (spec): CLEAN_OBSERVED, SUSPECT, CONTAMINATED, UNKNOWN
Schema: SAME
Checker: SAME
Consistent?: SPÓJNE
Column 6:
────────────────────────────────────────
Concept: Lineage
State model (spec): INDEPENDENT_ORIGIN, DERIVED_COPY, SHARED_ORIGIN, UNKNOWN (+lineage_basis/verification)
Schema: SAME + lineage_basis, lineage_verification, independence_group
Checker: lineage_basis+verification egzekwowane dla T3; independence_group NIE
Consistent?: DRIFT — F1. P1
Column 6:
────────────────────────────────────────
Concept: Verifier state
State model (spec): PASS, FAIL, ERROR, PARTIAL, UNKNOWN_SCOPE (spec:124-130)
Schema: NONE_OBSERVED, SUSPECT, FAILED, UNKNOWN (schema:68)
Checker: NONE_OBSERVED wymagane dla T3
Consistent?: DRIFT — inny koncept nazwany inaczej (execution result vs failure state). P3
Column 6:
────────────────────────────────────────
Concept: Risk tiers
State model (spec): T0-T3
Schema: T0-T3
Checker: T0-T3
Consistent?: SPÓJNE
Column 6:
────────────────────────────────────────
Concept: Claim types
State model (spec): nie wymienione w spec
Schema: 13 enumów
Checker: claim_type=current_state ma specjalne reguły
Consistent?: CZĘŚCIOWO — spec nie definiuje listy
Column 6:
────────────────────────────────────────
Concept: observation_time
State model (spec): wymagane dla T3 current_state
Schema: string\
Checker: null, bez formatu
Consistent?: non-empty tylko
Column 6: CZĘŚCIOWO — F3 (brak formatu/przyszłości). P2
────────────────────────────────────────
Concept: Scope
State model (spec): SUPPORTED wymaga scope
Schema: string\
Checker: null
Consistent?: non-empty wymagane
Column 6: SPÓJNE

8. CROSS-COMPONENT FAILURES

1. integrity PASS + provenance FAIL: możliwe (integrity sprawdza czy v5-research-manifest.json ISTNIEJE, provenance czy zawartość spójna). Nie jest to bug — różne kontrakty, prawidłowo rozdzielone. DETERMINISTICALLY DETECTABLE, działa jak trzeba.
2. liveness PASS + broken tests: F4. liveness nie woła pytest. SEMANTICALLY/OPERATIONALLY detectable, nie zaimplementowane. P2.
3. evidence record PASS + dead pointer: N13. Checker nie może wiedzieć czy source_identity (URL/DOI/path) żyje. NOT SOLVABLE AT THIS LAYER (external observation needed).
4. SKILL.md v5 drift + provenance PASS: F2. SKILL.md obiecuje walidację której nie ma. DETERMINISTICALLY DETECTABLE (regex na plain-text bullets), nie zaimplementowane. P1.
5. verify_claim FOUND vs evidence record: verify_claim.py jest "narrow" (substring), check_evidence_record wymaga entailment=ENTAILS — FOUND z verify_claim nie gwarantuje ENTAILS. Poprawne rozdzielenie, oba dokumentują scope.
6. T3 strong + verifier o słabszym kontrakcie: verify_claim.py file-contains daje FOUND dla substring — ale evidence record wymaga TYLKO verifier provenance string, nie sprawdza siły verifiera. Semantic gap, nie deterministycznie rozwiązywalny bez registry verifier strength. P3.

9. TEST-SUITE BLIND SPOTS

Czego 82 testy NIE atakują (zweryfikowane przez moje 45+ probes):
1. independence_group duplikaty (F1) — zero testów na grupach;
2. future observation_time (F3) — zero testów formatu/przyszłości;
3. SKILL.md v5 plain-text drift (F2) — testy atakują tylko gap-map ↔ manifest, nie SKILL.md v5 section;
4. liveness z broken test suite (F4) — test_liveness.py sprawdza brak plików, nie zepsute testy;
5. flow mapping / block scalar w frontmatter — test_v5_integrity nie ma case'ów flow/block;
6. T2 minimal provenance (świadoma luka, ale nietestowana jako wymaganie);
7. stdout/stderr merge w command-output (N10 działa, ale bez testu dokumentującego);
8. unicode path w file-contains (N12 działa, ale nietestowane);
9. symlink w file-contains/file-line (tylko file-exists --kind symlink);
10. duplicate evidence items w jednym rekordzie (dwa identyczne ev) — brak testu;
11. observation_time < retrieved_at (N15: obs 2020, retrieved 2026 → PASS — czy to OK? dla current_state obs_time 6 lat przed retrieved_at to red flag, nietestowane);
12. ENTAILS + IRRELEVANT w jednym rekordzie (schema dozwala, checker nie sprawdza spójności);
13. claim_type=legal/security bez specyficznych invariants (N3/N4 — legal T3 przechodzi bez niczego extra poza ogólnym T3);
14. version 5.9.9 w frontmatter (VERSION_RE akceptuje dowolną 5.x.y — integrity PASS dla 5.9.9; zamierzone? README mówi "version: 5.1.0 string in the body does not count" — ale 5.9.9 w frontmatter NIE jest odrzucany. P3);
15. redundant evidence (entails + entails z tym samym źródłem, różne URL — R2-10 → PASS; semantic, ale MÓGŁBY być wykrywany po normalized source_identity).

10. WHAT CURRENT (2.0.0) STILL DOES BETTER

1. Inline worked examples: A ma 5 przykładów w głównym pliku (Kira, Messenger, PATCH_QUEUE, OKO, SEC-AF); B ma 2 (atomic claims, denial) i deleguje resztę do refs. Dla modelu pod presją inline examples to złoto. (Jedyna realna przewaga ergonomiczna.)
2. Prostota frontmatter: A prostszy (choć martwy dla Hermesa), B poprawny. B wygrywa compat, A wygrywa nic poza czytelnością.
3. Żywy cron: A ma daily_self_audit.sh wpięty w cron 1b4a422f7443 (9:00 codziennie) wołający liveness — B ma liveness ale SKILL.md B nie referencjonuje crona. Po migracji cron nadal działa (woła ten sam skrypt), ale nikt nie udokumentował tej zależności w B.

11. WHAT v5.2 DOES BETTER

Wszystko z poprzednich audytów PLUS: fail-closed schema validator (additionalProperties=false, enumy egzekwowane), T3 current-state reguły (observation_time + CURRENT_ENOUGH), lineage_verification+basis contract, liveness z poprawnymi exit codes + test_liveness.py, v5-research-manifest.json z 24 sources, integrity checker z fail-closed frontmatter parserem (13/13 malformed odrzuconych), 82 testy z regression probes z zewnętrznych audytów, README 11KB z "What it does not prove" + "One rule worth stealing: if the verifier can be wrong, verify the verifier".

12. OVERENGINEERING / COGNITIVE LOAD

MEASURED: SKILL.md 30,113 B / 727 linii / 26 sekcji. Było 28,566 B w v5.1 (+5.4%). Sekcje 23 (research provenance, 32+24 sources) i 26 (authors) to największe bloki nieoperacyjne. Hot path (sekcje 1-22) ~24KB.
INFERRED: v5.2 dodaje 2 koncepty (lineage_verification, independence_group) i 1 plik (v5-research-manifest) do już gęstego modelu. Sekcja 11 dostała akapit o lineage_basis — dobry, konkretny.
HEURISTIC: przy 26 sekcjach ryzyko lost-in-the-middle rośnie, ale struktura (pipeline 0-10 + tiers + stany) jest liniowa i spójna. Z 82 testów i integrity checkerem system ma zewnętrzną kotwicę — coś czego A nie ma.
UNVERIFIED: obedience przy 26 sekcjach w realnej sesji — wymaga behavioral benchmarku (liveness L4 uczciwie to deklaruje).
VERDICT: NIE jest przekombinowany. Jedyny kandydat do SIMPLIFY: sekcja 23 "Key v5 additions" (19 bullets plain text) — albo przenieść do refs, albo walidować (F2).

13. ARCHITECTURAL LIMITS

Wymagają plugin/hook/runtime gate, NIE kolejnego Markdownu:
1. Prompt injection w obrazach/audio (sekcja 8 tylko tekst).
2. Behavioral enforcement (czy LLM faktycznie stosuje protokół) — liveness L4 UNKNOWN, wymaga Hermes hook/benchmark.
3. Live world-state verification (czy source_identity żyje, czy observation_time jest prawdziwe) — external observation.
4. Memory poisoning detection (sekcja 15 mówi, nie wykrywa).
5. Semantic entailment (checker nie udowodni, że proza wynika z evidence) — zadeklarowane w każdym docstringu.
6. Verifier-of-verifier jako CI (testy istnieją, ale nikt ich nie odpala cronem).

14. SCORECARD

Wagi ZADEKLAROWANE przed obliczeniem (zgodnie z briefem; najwyższe: FP-resistance 3, verifier robustness 3, hallucination prevention 3, spec/code consistency 3, deterministic enforcement 3):

| Dimension (waga)                 | CURRENT | v5.2 |
|----------------------------------|---------|------|
| Epistemic rigor (2)              | 5       | 9    |
| Hallucination prevention (3)     | 6       | 9    |
| False-positive resistance (3)    | 4       | 9    |
| Citation discipline (2)          | 7       | 9    |
| Retrieval robustness (1)         | 3       | 8    |
| Source-lineage handling (2)      | 3       | 7    |
| Current-state verification (2)   | 4       | 8    |
| Tool/verifier robustness (3)     | 3       | 9    |
| Prompt-injection resilience (2)  | 1       | 9    |
| Memory safety (1)                | 3       | 8    |
| Agentic workflow safety (2)      | 5       | 9    |
| Deterministic enforcement (3)    | 3       | 8    |
| Test quality (2)                 | 1       | 8    |
| Spec/schema/code consistency (3) | 4       | 6    |
| Progressive disclosure (1)       | 4       | 9    |
| Context efficiency (2)           | 3       | 8    |
| Maintainability (1)              | 6       | 8    |
| Hermes compatibility (2)         | 5       | 9    |
| Research provenance (1)          | 3       | 7    |
| Production readiness (2)         | 3       | 7    |

CURRENT: (52+63+43+72+31+32+42+33+12+31+52+33+12+43+41+32+61+52+31+32) = 10+18+12+14+3+6+8+9+2+3+10+9+2+12+4+6+6+10+3+6 = 153 / 40 = 3.83
v5.2: (92+93+93+92+81+72+82+93+92+81+92+83+82+63+91+82+81+92+71+72) = 18+27+27+18+8+14+16+27+18+8+18+24+16+18+9+16+8+18+7+14 = 309 / 40 = 7.73

Największa przewaga CURRENT: worked examples inline + żywy cron na sh-scriptach.
Największa przewaga v5.2: fail-closed enforcement (schema validator + T3 reguły + liveness exit codes) + 82 testów z regression probes.
Największa wada CURRENT: enforcement martwy (liveness zawsze FAIL na arxiv, calibration 1577h, Brier 0.293 ≈ chance), zero testów.
Największa wada v5.2: spec/schema drift (F2: SKILL.md v5 section nie walidowany; F1: independence_group martwy) + brak runtime benchmarku.

15. P0 / P1 / P2 / P3

P0: NONE.
P1:
- F1: independence_group w spec+schema, nieegzekwowany — 2 items ta sama grupa = PASS (checker MÓGŁBY wymagać: dla T3 strong, wspierające items z INDEPENDENT_ORIGIN muszą mieć różne independence_group albo jawnie UNKNOWN).
- F2: SKILL.md "Key v5 additions" nie walidowany vs manifest — SKILL.md:680 obiecuje coś czego checker nie robi (rozszerzyć SKILL_ENTRY_RE o plain-text bullets albo dopisać "only gap-map is validated").
P2:
- F3: observation_time bez formatu/przyszłości — dodać format date-time + <= now (z tolerancją na timezone).
- F4: liveness nie woła testów — dodać opcjonalny --run-tests albo L2.5.
- Spec/schema entailment drift (SUPPORTS vs ENTAILS, STALE_FOR_CLAIM vs STALE) — ujednolicić enumy w evidence-state-model.md.
- Sekcja 23: przenieść v5 additions do refs albo walidować.
- Cron: udokumentować w B zależność liveness/daily_self_audit/cron 1b4a422f7443.
P3:
- version 5.9.9 akceptowany przez VERSION_RE (zamierzone luźne dopasowanie? udokumentować).
- Verifier strength registry (verify_claim FOUND ≠ ENTAILS).
- Duplicate evidence items / normalized source dedup.
- Verifier state naming drift (PASS/FAIL vs NONE_OBSERVED/FAILED).
- Inline examples (Kira, OKO) przywrócić do SKILL.md.

16. FINAL YES / NO


KNOWN P0 REMAINING: 0
NEW P0: 0
KNOWN P1 REMAINING: 0 (z poprzedniego audytu — obie naprawione i potwierdzone reproducerem)
NEW P1: 2 (F1 independence_group, F2 SKILL.md v5 drift)
ALL PREVIOUS REPRODUCERS CLOSED: TAK (R1, R3, R4 w 100%; R2, R5 w warstwie maszynowej)
TEST SUITE: 82/82 PASS (izolowana kopia), integrity PASS, provenance PASS, liveness PASS
NOVEL PROBES: 45+ wykonanych (15xR1, 10xR2, 9xR3, 15xR4, 11xR5, 15xN), 2 nowe P1 znalezione
READY FOR INSTALLATION: TAK PO FIXACH P1 (F1+F2) — lub TAK Z ŚWIADOMOŚCIĄ, że F1/F2
						 to drifty dokumentacyjno-kontraktowe, nie false-verified w runtime


Czy v5.2 jest realnie lepsze od CURRENT? TAK — CLEAR UPGRADE (7.73 vs 3.83). Czy zamienić? TAK, po F1/F2 — ale NIE WYKONUJĘ żadnej zmiany bez Twojego osobnego polecenia. Oba drzewa nietknięte (jedyna modyfikacja: izolowana kopia testowa /tmp/ahp-test3.VPoHW3 — do skasowania na Twój sygnał).

17. EVIDENCE / COMMAND LOG

- PHASE 0: readlink (0 symlinków), frontmatter v5.2.0, find 31 plików, stat mtimes — VERIFIED
- PHASE 1: pytest 82 passed/0 failed/10.05s/exit 0 na /tmp/ahp-test3.VPoHW3; check_v5_integrity PASS exit 0; check_research_provenance PASS exit 0; liveness PASS exit 0 — VERIFIED
- R1 (15 probes): 14 FAIL + R1-14 garbage PASS — REPRODUCED
- R2 (10 probes): 1-5 FAIL, 6-10 PASS — REPRODUCED
- R3 (9 probes, czyste pomiary): 1-3/5/6/8 exit 1, 4 (stub) exit 0 (limit), 7 exit 0 (INFO OK) — REPRODUCED
- R4 (15 probes): 13/13 FAIL + R4-13b baseline PASS + R4-14 flow PASS + R4-15 block FAIL — REPRODUCED
- R5 (11 probes): R5-7/8/9 FAIL (v4), R5-10/11 PASS (v5 plain — F2), extra/missing gap FAIL — REPRODUCED
- N1-N15: 8 evidence-record + 4 verify_claim + 3 cross-component — REPRODUCED (F1 z N1)
- grep independence_group w scripts/: 0 wystąpień — VERIFIED (F1)
- grep SKILL_ENTRY_RE/v5 w check_research_provenance: tylko markdown format — VERIFIED (F2)
- Hermes skill_utils.py:174-219: CSafeLoader + fallback simple parsing — VERIFIED (R4 compat)
- VERSION_RE ^5\.\d+\.\d+$: 5.1.0/5.9.9/5.0.0 → integrity PASS — REPRODUCED (P3)

Zatrzymuję się. HARD STOP respektowany: zero zmian w CURRENT, zero instalacji CANDIDATE, zero commitów, zero poprawek.