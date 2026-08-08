<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# @GitHub @Akademicki \# FORENSIC DOCUMENT-LEVEL AUDIT - ANTI-HALLUCINATION PROTOCOL v5.2

Masz do dyspozycji dokładnie dwa załączone pliki:

1. `SKILL.md`
2. `README.md`

Dotyczą projektu:

`Anti-Hallucination Protocol v5.2`

Twoim zadaniem jest przeprowadzić maksymalnie krytyczny, evidence-driven audit tej wersji jako:

1. instrukcyjnego systemu anti-hallucination dla Hermes Agent,
2. publicznie dokumentowanego projektu,
3. specyfikacji epistemicznego workflow dla agentów LLM.

Nie zakładaj, że projekt jest dobry tylko dlatego, że wygląda technicznie, jest rozbudowany, używa terminologii researchowej albo zawiera wiele zabezpieczeń.

Twoim celem jest aktywnie spróbować wykazać, że:

- część mechanizmów jest pozorna,
- reguły mogą być niespójne,
- instrukcji jest zbyt dużo,
- niektóre claims są za mocne,
- progressive disclosure jest źle wykorzystane,
- research jest używany dekoracyjnie,
- README overselluje możliwości,
- model może nie być w stanie realnie przestrzegać całego protokołu,
- v5.2 może tworzyć fałszywe poczucie epistemicznego bezpieczeństwa.

Jeżeli po takim ataku projekt nadal wygląda dobrze, dopiero wtedy uznaj jego mocne strony.

---

# FUNDAMENTAL EVIDENCE BOUNDARY

Masz tylko `SKILL.md` i `README.md`.

NIE MASZ:

- source code helperów,
- schemas,
- tests,
- fixtures,
- scripts,
- runtime hooków,
- konfiguracji Hermesa,
- pełnych references,
- repo tree,
- wyników testów.

Dlatego NIE WOLNO ci twierdzić, że:

- testy przechodzą,
- checker coś rzeczywiście egzekwuje,
- schema jest poprawna,
- helper jest fail-closed,
- liveness działa,
- dany bug jest naprawiony implementacyjnie,
- runtime enforcement istnieje,
- Hermes rzeczywiście wykonuje którykolwiek helper,
- repository integrity checker działa zgodnie z opisem.

Jeżeli `SKILL.md` lub `README.md` coś takiego twierdzą, oceń to jako:

`DOCUMENTED CLAIM - IMPLEMENTATION UNVERIFIED`

To ograniczenie jest krytyczne.

Nie uzupełniaj brakującego repo swoją wyobraźnią.

---

# WEB RESEARCH

Możesz i powinieneś użyć internetu.

Preferuj primary sources.

Dla Hermes Agent:

1. oficjalne repo `NousResearch/hermes-agent`,
2. oficjalną dokumentację Hermes,
3. aktualne source files Hermesa, jeżeli są potrzebne do sprawdzenia konkretnego claimu.

Dla research papers:

1. arXiv,
2. ACL Anthology,
3. NIST,
4. oficjalne publication pages.

Nie używaj blogspamu jako dowodu, jeśli istnieje primary source.

Dla każdego zewnętrznego claimu rozróżniaj:

`FILE CLAIM`
`WEB VERIFIED`
`WEB CONTRADICTED`
`UNVERIFIED`

---

# PHASE 1 - DOCUMENT INVENTORY

Najpierw przeczytaj oba pliki W CAŁOŚCI.

Podaj:

- liczbę linii,
- przybliżoną liczbę słów,
- strukturę sekcji,
- frontmatter `SKILL.md`,
- deklarowaną wersję,
- deklarowane przeznaczenie,
- wszystkie główne claims dotyczące możliwości systemu.

Nie zaczynaj oceny po przeczytaniu pierwszych sekcji.

---

# PHASE 2 - RECONSTRUCT THE SYSTEM

Na podstawie WYŁĄCZNIE `SKILL.md` zrekonstruuj rzeczywisty model działania protokołu.

Odpowiedz:

1. Co autorzy rozumieją przez hallucination/factual failure?
2. Jak wygląda pipeline?
3. Jak działa risk-tiering?
4. Jak klasyfikowane są evidence states?
5. Jak traktowana jest uncertainty?
6. Jak traktowane są citations?
7. Jak traktowany jest retrieval?
8. Jak traktowane są current-state claims?
9. Jak traktowana jest memory?
10. Jak traktowane są prompt injections w evidence?
11. Jak traktowana jest source lineage?
12. Jak definiowana jest independence?
13. Jak traktowane są verifier failures?
14. Jak traktowany jest model-as-judge?
15. Jak traktowane są contradictions?
16. Jak traktowane są agent trajectories?
17. Jak traktowane są completion claims typu:
`fixed`, `works`, `deployed`?
18. Jak traktowany jest blast radius błędnego claimu?
19. Jak traktowana jest błędna interpretacja intencji użytkownika?
20. Gdzie system jawnie przyznaje swoje ograniczenia?

Następnie przedstaw najkrótszy możliwy pseudomodel:

`INPUT -> ... -> OUTPUT`

---

# PHASE 3 - INTERNAL CONSISTENCY AUDIT

Szukaj sprzeczności wewnątrz `SKILL.md`.

Szczególnie:

- jedna sekcja wymaga czegoś, co inna osłabia,
- progressive disclosure vs liczba aktywnych invariants,
- risk-tiering vs obowiązkowe kroki pipeline,
- `not mandatory ceremony` vs język, który praktycznie brzmi obowiązkowo,
- strong evidence requirements vs adaptive verification budget,
- source independence vs `when feasible`,
- current-state requirements vs general source rules,
- runtime limitations vs język sugerujący enforcement,
- refusal/abstention vs operational usefulness.

Dla każdej znalezionej sprzeczności podaj:

`CLAIM A`
`CLAIM B`
`CONFLICT`
`PRACTICAL CONSEQUENCE`

Nie wymyślaj konfliktu tam, gdzie dwa rules są kompatybilne.

---

# PHASE 4 - COGNITIVE LOAD / OBEDIENCE AUDIT

To jest jeden z najważniejszych elementów.

Nie premiuj kompletności.

Spróbuj odpowiedzieć:

> Czy realny model LLM ma szansę konsekwentnie stosować ten skill w długich, narzędziowych sesjach?

Oceń:

- instruction density,
- number of simultaneous invariants,
- duplication,
- token overhead,
- lost-in-the-middle risk,
- conflicting priorities,
- number of epistemic states,
- number of classification steps,
- need for repeated context rereading,
- risk of cargo-cult verification,
- risk, że agent odtworzy terminologię bez faktycznej zmiany zachowania.

Podziel reguły na:

`CORE - agent powinien pamiętać zawsze`
`CONDITIONAL - tylko dla określonych tasków`
`REFERENCE MATERIAL`
`LIKELY OVERLOAD`

Następnie zaproponuj minimalny "hot path":

maksymalnie 5-7 zasad, które dają największą część korzyści anti-hallucination.

Nie zmieniaj jeszcze pliku. To audit.

---

# PHASE 5 - PROGRESSIVE DISCLOSURE

Zweryfikuj aktualne zasady Hermes Agent dotyczące skills i progressive disclosure.

Następnie oceń, czy `SKILL.md` wykorzystuje ten mechanizm dobrze.

Pytania:

1. Czy główny `SKILL.md` zawiera tylko rzeczy, które agent faktycznie powinien mieć aktywne?
2. Czy część materiału powinna zostać przeniesiona do references?
3. Czy lista supporting artifacts jest sensowna?
4. Czy model wie, kiedy załadować konkretny reference?
5. Czy zbyt wiele reguł nadal siedzi bezpośrednio w main skill?
6. Czy research bibliography powinna znajdować się w głównym prompt context?
7. Czy obecna struktura zwiększa czy zmniejsza obedience?

Oznacz większe sekcje:

`KEEP IN SKILL`
`MOVE TO REFERENCE`
`CONDENSE`
`REMOVE`

---

# PHASE 6 - EPISTEMIC SECURITY AUDIT

Oceń, czy projekt rzeczywiście atakuje nowoczesne failure modes.

Sprawdź osobno:

- citation identity failure,
- citation entailment failure,
- stale evidence,
- source duplication,
- correlated agents,
- model-as-judge bias,
- verifier failure,
- retrieval poisoning,
- indirect prompt injection,
- memory poisoning,
- current-state drift,
- error -> empty collapse,
- partial search -> exhaustive claim,
- entity collision,
- semantic mismatch,
- tool success != user success,
- agent-loop progress mirage,
- stale bug reports,
- already-completed work,
- intent hallucination,
- past-action denial after context compaction.

Dla każdego:

`COVERED WELL`
`PARTIAL`
`WEAK`
`MISSING`

i podaj exact section evidence.

---

# PHASE 7 - ATTACK THE "INDEPENDENCE" MODEL

To jest szczególnie ważne.

Projekt twierdzi, że:

- wiele URL-i nie oznacza wielu źródeł,
- wiele agentów nie oznacza niezależnych verifierów,
- independence powinna oznaczać różne failure domains.

Oceń krytycznie:

1. Czy ta definicja jest epistemicznie sensowna?
2. Czy agent LLM jest w stanie realnie oceniać source lineage?
3. Skąd agent ma wiedzieć, że dwa źródła są faktycznie niezależne?
4. Czy projekt wystarczająco rozróżnia:
    - known independent,
    - plausibly independent,
    - unknown lineage?
5. Czy istnieje ryzyko, że model po prostu nazwie coś `independent`?

Szukaj tu pseudo-rigor.

---

# PHASE 8 - CURRENT-STATE / TEMPORAL AUDIT

Sprawdź szczególnie mocno obsługę claims takich jak:

- "service działa teraz",
- "ten model obecnie istnieje",
- "repo jest aktualnie maintained",
- "API obecnie obsługuje X",
- "ta konfiguracja jest aktywna",
- "ta cena jest aktualna",
- "ten komponent jest live".

Oceń:

- observation time,
- freshness,
- live-state requirement,
- stale memory handling,
- source supersession,
- documentation vs runtime state.

Czy `SKILL.md` realnie utrudnia zamianę:

`was true`
na
`is true now`?

---

# PHASE 9 - PROMPT-INJECTION AUDIT

Porównaj podejście opisane w skillu z aktualnymi najlepszymi praktykami i badaniami dotyczącymi:

- indirect prompt injection,
- agent hijacking,
- retrieved-content poisoning,
- RAG poisoning.

Odpowiedz uczciwie:

1. Co sam prompt może poprawić?
2. Czego prompt nie może zabezpieczyć?
3. Czy `SKILL.md` jasno mówi o tej granicy?
4. Czy gdziekolwiek overselluje prompt-level protection jako security boundary?
5. Czy runtime controls, least privilege, sandboxing i authorization są odpowiednio rozdzielone od prompt policy?

---

# PHASE 10 - RESEARCH AUDIT

Znajdź wszystkie research claims i źródła wymienione w `SKILL.md` i README.

Dla najważniejszych sprawdź w primary source:

- poprawność tytułu,
- poprawność ID,
- czy paper faktycznie istnieje,
- czy przypisywany mu finding jest zgodny z publikacją,
- czy projekt nie ekstrapoluje wyniku poza zakres paperu.

Szczególnie sprawdź wszystkie papers użyte do uzasadnienia:

- factuality,
- intent hallucination,
- prompt injection,
- retrieval poisoning,
- source conflict,
- self-preference judge bias,
- agent trajectory hallucination,
- long-context problems,
- stale memory / freshness,
- progress mirage.

Nie trzeba przepisywać całych paperów.

Interesuje mnie:

`SOURCE`
`WHAT THE FILE CLAIMS`
`WHAT THE SOURCE ACTUALLY SUPPORTS`
`VERDICT`

Szukaj citation laundering.

---

# PHASE 11 - HERMES COMPATIBILITY

Zweryfikuj przy pomocy AKTUALNEJ oficjalnej dokumentacji / repo Hermes Agent:

- format skill frontmatter,
- discovery,
- supported supporting directories,
- progressive disclosure,
- sposób ładowania skills,
- czy references/scripts są automatycznie wykonywane,
- czy runtime Hermesa rzeczywiście zapewnia mechanizmy sugerowane w dokumentacji.

Nie zgaduj.

Jeżeli `SKILL.md` lub README używa terminology/tool names, których aktualny Hermes nie posiada, wskaż to.

Oddziel:

`COMPATIBLE DOCUMENT STRUCTURE`

od:

`ACTUAL RUNTIME ENFORCEMENT`

---

# PHASE 12 - README AUDIT

Teraz oceń README jako publiczny README GitHub projektu.

Nie oceniaj tylko treści technicznej.

Oceń:

## First screen

Czy w pierwszych sekundach wiadomo:

- co to jest,
- dla kogo,
- jaki problem rozwiązuje,
- dlaczego różni się od zwykłego "fact check prompt"?

## Credibility

Czy README:

- overselluje,
- używa buzzwordów,
- brzmi research-washed,
- twierdzi więcej niż może wykazać,
- odpowiednio eksponuje limitations?

## Information architecture

Czy kolejność sekcji jest właściwa?

## Human writing

Szukaj AI slopu:

- artificial rule-of-three,
- generycznych transitions,
- nadmiaru symetrycznych list,
- corporate copy,
- pustych abstrakcyjnych nominalizacji,
- repetitive "It does X / It does Y",
- marketingowego nadęcia.

## README length

Czy jest:

`TOO SHORT`
`ABOUT RIGHT`
`TOO LONG`

i dlaczego?

## Trust

Czy po przeczytaniu README techniczna osoba bardziej ufa projektowi, czy ma wrażenie epistemic theatre?

---

# PHASE 13 - CLAIM AUDIT OF README

Dla każdego mocnego publicznego claimu oznacz:

`SUPPORTED BY SKILL`
`SUPPORTED BY WEB`
`IMPLEMENTATION UNVERIFIED`
`OVERSTATED`
`MISLEADING`

Szczególnie sprawdź claims dotyczące:

- deterministic checks,
- false-positive prevention,
- fail-closed behavior,
- research provenance,
- Hermes compatibility,
- tests,
- runtime limitations.

Pamiętaj:

dostałeś tylko `README.md` i `SKILL.md`.

Jeśli README mówi, że skrypt coś robi, możesz ocenić tylko:

`document claims implementation does X`.

Nie możesz potwierdzić implementation behavior bez source code.

---

# PHASE 14 - OVERENGINEERING ATTACK

Spróbuj udowodnić, że v5.2 jest przekombinowane.

Dla każdego głównego mechanizmu oceń:

1. Czy odpowiada realnemu failure mode?
2. Czy LLM może praktycznie stosować regułę?
3. Czy mechanizm wnosi coś ponad prostszy rule?
4. Czy duplikuje inne sekcje?
5. Czy koszt token/context/attention jest proporcjonalny?
6. Czy zwiększa czy zmniejsza prawdopodobieństwo obedience?
7. Czy tworzy epistemic theatre?

Oznacz:

`ESSENTIAL`
`VALUABLE`
`QUESTIONABLE`
`OVERENGINEERED`

---

# PHASE 15 - WHAT IS ACTUALLY NOVEL?

Nie zakładaj, że projekt jest innowacyjny.

Rozdziel:

1. dobrze znane factuality best practices,
2. znane RAG / citation controls,
3. znane prompt-injection principles,
4. znane agentic safety controls,
5. lokalne engineering heuristics,
6. faktycznie interesującą integrację znanych mechanizmów.

Odpowiedz:

> Czy Anti-Hallucination Protocol v5.2 wnosi realnie interesującą architekturę, czy przede wszystkim agreguje istniejące dobre praktyki w jeden skill?

Obie odpowiedzi są dopuszczalne.

---

# PHASE 16 - COMPARE AGAINST A MUCH SIMPLER ALTERNATIVE

Zaprojektuj mentalnie prosty 8-rule anti-hallucination skill.

Następnie porównaj:

`SIMPLE 8-RULE VERSION`
vs
`AHP v5.2`

pod względem:

- coverage,
- obedience,
- token cost,
- maintainability,
- false certainty,
- agentic usefulness,
- high-risk reliability.

Czy złożoność v5.2 faktycznie się zwraca?

---

# PHASE 17 - SCORING

Daj oceny 0-10:

| Dimension | Score |
| :-- | --: |
| Epistemic rigor |  |
| Hallucination prevention design |  |
| Citation discipline |  |
| Retrieval robustness |  |
| Current-state reasoning |  |
| Memory safety |  |
| Prompt-injection awareness |  |
| Source-lineage reasoning |  |
| Verifier skepticism |  |
| Agentic workflow safety |  |
| Intent preservation |  |
| Recovery / blast radius |  |
| Progressive disclosure |  |
| Context efficiency |  |
| Instruction obedience probability |  |
| Hermes compatibility |  |
| Research grounding |  |
| Internal consistency |  |
| Maintainability |  |
| README quality |  |
| Public credibility |  |
| Production-readiness as DOCUMENTED DESIGN |  |

Następnie:

`OVERALL DESIGN SCORE`

oraz osobno:

`DOCUMENTATION SCORE`

Nie przyznawaj:

`IMPLEMENTATION SCORE`

bo nie dostałeś implementacji.

---

# PHASE 18 - FINAL VERDICT

Wybierz jedno:

`EXCELLENT DESIGN - IMPLEMENTATION STILL UNVERIFIED`

`STRONG DESIGN - NEEDS DOCUMENT/SCOPE FIXES`

`PROMISING BUT OVERENGINEERED`

`MIXED`

`MOSTLY EPISTEMIC THEATRE`

`FUNDAMENTALLY FLAWED`

Następnie odpowiedz:

1. Czy `SKILL.md` jest faktycznie dobrym main skill dla Hermes?
2. Czy jest za długi?
3. Co powinno zostać w main skill?
4. Co przenieść do references?
5. Czy README nadaje się już publicznie?
6. Jakie claims README należy osłabić?
7. Jaki jest największy realny atut v5.2?
8. Jaki jest największy realny problem v5.2?
9. Czy architektura prawdopodobnie poprawi zachowanie mocnego agenta?
10. Czy prawdopodobnie pogorszy zachowanie słabszego agenta przez instruction overload?

---

# REQUIRED FINAL OUTPUT

## 1. EXECUTIVE VERDICT

## 2. WHAT YOU ACTUALLY INSPECTED

## 3. SYSTEM RECONSTRUCTION

## 4. STRONGEST PARTS

## 5. WEAKEST PARTS

## 6. INTERNAL CONTRADICTIONS

## 7. COGNITIVE LOAD / OBEDIENCE

## 8. PROGRESSIVE DISCLOSURE

## 9. EPISTEMIC SECURITY COVERAGE

## 10. CURRENT-STATE HANDLING

## 11. SOURCE LINEAGE / INDEPENDENCE

## 12. PROMPT-INJECTION BOUNDARY

## 13. RESEARCH VERIFICATION

## 14. HERMES COMPATIBILITY

## 15. README FORENSIC AUDIT

## 16. OVERENGINEERING AUDIT

## 17. SIMPLE 8-RULE BASELINE vs v5.2

## 18. WHAT IS ACTUALLY NOVEL

## 19. SCORECARD

## 20. P0 / P1 / P2 / P3 DOCUMENT-LEVEL FINDINGS

## 21. FINAL VERDICT

## 22. EXACT RECOMMENDED CHANGES

---

# EVIDENCE STANDARD

Każde istotne stwierdzenie oznacz:

`FILE-VERIFIED`
`WEB-VERIFIED`
`INFERENCE`
`HEURISTIC`
`UNVERIFIED`

Jeżeli coś wynika z `SKILL.md`, podaj sekcję.

Jeżeli coś zweryfikowałeś online, podaj primary source.

Jeżeli czegoś nie możesz sprawdzić z tych dwóch plików:

powiedz to.

Najważniejsza zasada całego audytu:

`DOCUMENTED CONTROL != IMPLEMENTED CONTROL != RUNTIME ENFORCEMENT`

Nie mieszaj tych trzech poziomów.

# POSTAWA

Zero sycophancy.

Nie chwal projektu za samą ambicję.

Nie karz projektu za uczciwie opisane ograniczenia.

Nie wymyślaj bugów implementacyjnych bez implementacji.

Nie zakładaj, że więcej procedur oznacza mniej halucynacji.

Szukaj punktu, w którym epistemic rigor zaczyna zmieniać się w epistemic theatre.

Jeżeli ten punkt nie został przekroczony, również powiedz to jasno.

I have enough primary-source verification. Writing the full forensic audit from the two files plus web-checked Hermes and research sources.

***

## 1. EXECUTIVE VERDICT

**Verdict: `PROMISING BUT OVERENGINEERED`** - with honest limits and real epistemic insight, undermined by instruction density that likely reduces obedience.

v5.2 is a serious design document, not pure theatre. The core invariant (`claim strength ≤ evidence strength`), forbidden state collapses, independence-as-failure-domains, completion semantics, and explicit “policy ≠ enforcement” boundary are genuinely good. But as a **main Hermes skill** it is far too dense: ~30k characters of always-on procedure when Hermes peer skills aim for **8-14k** and advise splitting past **20k**. `FILE-VERIFIED` · `WEB-VERIFIED`

You only have two documents. Every script/schema/test claim is **`DOCUMENTED CLAIM - IMPLEMENTATION UNVERIFIED`**.

***

## 2. WHAT YOU ACTUALLY INSPECTED

| Artifact | Size (given) | Approx. scale | Status |
| :-- | --: | :-- | :-- |
| `SKILL.md` | 30,107 chars | ~5,000-5,500 words; ~550-700 lines | Read in full `FILE-VERIFIED` |
| `README.md` | 11,036 chars | ~1,600-1,900 words; ~250-350 lines | Read in full `FILE-VERIFIED` |

**Not inspected:** scripts, schemas, tests, fixtures, Hermes hooks, repo tree, runtime behavior. `FILE-VERIFIED`

**Web checked:** Hermes Skills System + Working with Skills docs; skill-authoring size guidance; arXiv/ACL/NIST for major research IDs. `WEB-VERIFIED`

***

## 3. SYSTEM RECONSTRUCTION

### Frontmatter / purpose `FILE-VERIFIED`

- **name:** `anti-hallucination-protocol`
- **version:** `5.2.0`
- **author:** Paulina Janowska & Gniewisława AI
- **license:** MIT
- **platforms:** linux, macos, windows
- **category:** software-development
- **Purpose:** control how *consequential* claims earn stronger wording/action; not truth guarantee

### Section map (`SKILL.md`) `FILE-VERIFIED`

Supporting artifacts -> §1 pipeline -> §2 intent -> §3 atomic claims -> §4 tiers -> §5 evidence states -> §6 fitness -> §7 citations -> §8 untrusted boundary -> §9 retrieval -> §10 contradiction -> §11 independence -> §12 verifier skepticism -> §13 trajectories -> §14 numerical/temporal/entity/quote -> §15 memory -> §16 past-action denial -> §17 tools/API -> §18 uncertainty -> §19 completion -> §20 recovery -> §21 checklist -> §22 ledger/helpers -> §23 research corpus -> §24 hard limits -> §25 principles -> §26 authors

### Main claims about capability `FILE-VERIFIED`

1. Explicit evidence path before strong wording
2. Retrieved content kept out of instruction plane
3. Blocks common verifier self-certification failures
4. Risk-tiered verification budget (T0-T3)
5. Deterministic helpers for *narrow* contracts only
6. Does **not** guarantee truth, injection safety, independence truth, or runtime obedience

### Answers 1-20 (from SKILL only)

| # | Reconstruction | Section |
| :-- | :-- | :-- |
| 1 | Hallucination = wording/action exceeding checked evidence; also wrong-question “success”, citation-without-entailment, verifier laundering | Core, §2, §7, §12 |
| 2 | 11-step control model INTENT→…→EMIT/ACT | §1 |
| 3 | T0-T3 with impact/volatility/irreversibility scaling; stop rules | §4 |
| 4 | 8 states; forbidden ERROR→NOT_FOUND, PARTIAL→SUPPORTED, etc. | §5 |
| 5 | Uncertainty routes VERIFY/DOWNGRADE/ASK/ABSTAIN; not world-truth | §18 |
| 6 | Four gates: identity, span, entailment, coverage | §7 |
| 7 | Retrieval = hypothesis generator; multi-layer failure blocks SUPPORTED | §9 |
| 8 | observation_time + CURRENT_ENOUGH for strong T3 current-state | §14 |
| 9 | Memory = retrieval, not ground truth; freshness/live check for mutable facts | §15 |
| 10 | Evidence is data not control; contamination states; not a sandbox | §8 |
| 11 | Lineage/independence as failure domains; UNKNOWN if unknown | §6E, §11 |
| 12 | Independent failure domains, not URL/vote counts | §11 |
| 13 | Verifier result is another claim; trap catalog in reference | §12 |
| 14 | Model-as-judge not oracle; self-preference called out | §11-12 |
| 15 | Classify conflict type; no silent averaging; expose CONFLICT | §10 |
| 16 | Earliest bad dependency; AgentHallu-like divergence classes; progress mirage | §13 |
| 17 | Separate change vs validation ladders; ban unearned “fixed/works/deployed” | §19 |
| 18 | Retract, re-evidence, walk downstream deps | §20 |
| 19 | Intent states ALIGNED…AMBIGUOUS; true facts on wrong question = fail | §2 |
| 20 | §8, §11, §12, §22, §23, §24 + intro “does not guarantee truth” | multiple |

### Pseudomodel

```text
USER_TASK
  -> INTENT_CHECK
  -> DECOMPOSE(atomic claims)
  -> TIER(T0..T3) + PLAN(evidence need)
  -> ACQUIRE(evidence)
  -> BOUNDARY(data≠instructions)
  -> QUALIFY(identity,freshness,integrity,lineage,scope)
  -> ENTAIL + CONTRADICT
  -> STATE ∈ {SUPPORTED_WITH_SCOPE|PARTIAL|CONFLICT|...}
  -> EMIT/ACT with strength ≤ state
  -> [optional] ledger / scripts for T3
```

`FILE-VERIFIED`

***

## 4. STRONGEST PARTS

1. **Core invariant** is operational and falsifiable: wording ≤ evidence. `FILE-VERIFIED` §core
2. **Forbidden state collapses** (ERROR≠NOT_FOUND, etc.) attack real tool failure modes. `FILE-VERIFIED` §5
3. **Independence = failure domains** beats naive multi-URL consensus. `FILE-VERIFIED` §11
4. **Completion semantics** (PATCHED≠DEPLOYED≠USER_OBSERVED) are excellent for coding agents. `FILE-VERIFIED` §19
5. **Honest hard limits** (§24 + “Policy is not runtime enforcement”) reduce epistemic theatre risk. `FILE-VERIFIED`
6. **Intent as verification target** matches intent-hallucination research. `FILE-VERIFIED` §2 · `WEB-VERIFIED` FAITHQA/ACL
7. **Progress mirage / external success signals** match 2026 agent-loop work. `FILE-VERIFIED` §13 · `WEB-VERIFIED` arXiv:2607.25152

***

## 5. WEAKEST PARTS

1. **Main skill length vs Hermes progressive disclosure norms** (~30k chars vs 8-14k peer target; split past 20k). `FILE-VERIFIED` · `WEB-VERIFIED`
2. **§23 research bibliography in hot path** - dozens of papers burn attention without changing next-token behavior. `FILE-VERIFIED`
3. **Independence still partly performative at inference time** - LLM can still *label* `INDEPENDENT_ORIGIN`. Document admits checker can’t prove provenance; agent still must judge lineage. `FILE-VERIFIED` §11
4. **“not mandatory ceremony” vs dense mandatory-sounding machinery** - cognitive double bind. `FILE-VERIFIED` §1 vs §§5-22
5. **Supporting artifact list is a second catalog** (12 refs + 5 scripts + tests) before any procedure. `FILE-VERIFIED`
6. **All enforcement claims implementation-unverified** from this audit boundary. `FILE-VERIFIED`
7. **HSDB/HyperspaceDB local note** (§15) is installation-specific noise in a portable skill. `FILE-VERIFIED`

***

## 6. INTERNAL CONTRADICTIONS

### C1 - Ceremony vs obligation

- **CLAIM A:** “control model, not mandatory ceremony”; T0/T1 must not become ten-step ritual. §1
- **CLAIM B:** 26 sections, 8 evidence states, 6 fitness questions, 4 citation gates, dual checklists, ledger, contamination states, change/validation ladders.
- **CONFLICT:** Soft optionality buried under hard taxonomy.
- **PRACTICAL CONSEQUENCE:** Models cargo-cult labels instead of selective verification. `FILE-VERIFIED` · `HEURISTIC`

### C2 - Progressive disclosure vs always-on bulk

- **CLAIM A:** “Load these only when the task needs them” for references.
- **CLAIM B:** Full research corpus + almost all control theory sits *in* SKILL.md.
- **CONFLICT:** Disclosure works for *files*, not for *content already in Level-1 body*.
- **PRACTICAL CONSEQUENCE:** Paying Level-1 cost of a knowledge base. `FILE-VERIFIED` · `WEB-VERIFIED`

### C3 - Strong T3 requirements vs “when feasible”

- **CLAIM A:** T3 needs direct evidence + falsification + independent check when feasible. §4
- **CLAIM B:** Strong T3 machine-readable verdicts need auditable lineage_basis + VERIFIED. §11, §14
- **CONFLICT:** Mild if read carefully; sharp in practice - “when feasible” vs schema-hard requirements.
- **PRACTICAL CONSEQUENCE:** Either skip T3 discipline or fake ledger fields. `FILE-VERIFIED` · `INFERENCE`

### C4 - Policy honesty vs helper marketing surface

- **CLAIM A:** Markdown is not a gate; PASS is scoped.
- **CLAIM B:** Language of “fail-closed”, “deterministic state-invariant checker”, “enforces…” (README + artifact blurbs).
- **CONFLICT:** Tone oscillates between humility and enforcement theatre.
- **PRACTICAL CONSEQUENCE:** Readers over-trust docs; agents may treat PASS as global truth despite disclaimers. `FILE-VERIFIED`

### C5 - Abstain vs usefulness (tension, not pure contradiction)

- **CLAIM A:** Abstain rather than launder uncertainty. §25
- **CLAIM B:** Agent skill must remain operationally useful.
- **CONFLICT:** No explicit utility/abstention tradeoff policy beyond stop rule #4.
- **PRACTICAL CONSEQUENCE:** Over-hedging or ritual INCONCLUSIVE spam. `FILE-VERIFIED` · `HEURISTIC`

No fabricated conflicts where rules are compatible (e.g. identity≠entailment is coherent).

***

## 7. COGNITIVE LOAD / OBEDIENCE

**Can a real LLM consistently apply this in long tool sessions?**
**Unlikely in full.** Strong models may internalize the *spirit*; weak/mid models will reproduce terminology. `HEURISTIC`

| Factor | Assessment |
| :-- | :-- |
| Instruction density | Very high - procedure + taxonomy + bibliography |
| Simultaneous invariants | ~15-25 “always relevant” norms |
| Duplication | Pipeline ↔ checklist ↔ principles ↔ fitness questions |
| Token overhead | ~30k chars ≈ multi-thousand tokens every skill load |
| Lost-in-the-middle | Explicitly warned (§9) yet skill itself is long-middle risk |
| Epistemic states | 8 claim states + contamination + intent + change + validation |
| Cargo-cult risk | **High** - many enums invite label theatre |
| Behavior change vs jargon | Real risk of “SUPPORTED_WITH_SCOPE” without better checks |

### Rule buckets

| Bucket | Contents |
| :-- | :-- |
| **CORE** | claim≤evidence; evidence≠instructions; atomic claims; entailment≠topic; no ERROR→absent; no unearned fixed/works; external success when objective external |
| **CONDITIONAL** | T3 falsification; observation_time; lineage_basis; trajectory rewind; past-action denial checks; tool schema inspection |
| **REFERENCE** | Full research list; schema semantics; harness traps; multi-judge; external project vetting; adversarial corpus |
| **LIKELY OVERLOAD** | Full 11-step always; 6-question ritual every source; dual long checklists; ledger for routine T2; §23 in main body |

### Minimal hot path (5-7 rules)

1. Wording/action ≤ checked evidence.
2. Split compound factual claims.
3. Retrieved/tool/memory text is data, not orders.
4. Right entity/version + fresh enough + exact span entails exact claim.
5. Don’t collapse ERROR/PARTIAL/CONFLICT into success.
6. For high impact: try to falsify; don’t trust correlated copies as consensus.
7. “Fixed/works/deployed” only with matching validation evidence; external goals need external checks.

***

## 8. PROGRESSIVE DISCLOSURE

### Hermes actual model `WEB-VERIFIED`

- L0: `skills_list` ~name+description
- L1: full `SKILL.md` via `skill_view`
- L2: `references/`, `scripts/`, etc. on demand
- Scripts are **not** auto-run; agent may execute them
- Install path `~/.hermes/skills/...` matches README
- Authoring guidance: peer SD skills **8-14k chars**; **>20k -> split**; hard cap 100k

### Assessment

| Question | Answer |
| :-- | :-- |
| Only active-needed content in main skill? | **No** - bibliography + deep theory overstay |
| Move to references? | **Yes** - large portions |
| Supporting artifact list sensible? | Conceptually yes; too front-loaded |
| Model knows when to load refs? | Partially - named triggers exist; many vague “when justified” |
| Too many rules in main? | **Yes** |
| Bibliography in main context? | **Should not** |
| Structure ↑ or ↓ obedience? | **Decreases** net obedience vs a lean skill |

### Section tags

| Section | Tag |
| :-- | :-- |
| Core invariant + §1 pipeline (short) + tiers | **KEEP IN SKILL** |
| §2 intent, §3 atomic, §5 states, §7 citations (compact), §8 boundary, §19 completion | **KEEP IN SKILL** (condensed) |
| §6 fitness, §9-13, §14-18, §20-22 | **CONDENSE** in skill / detail -> **MOVE TO REFERENCE** |
| §23 full paper lists | **MOVE TO REFERENCE** |
| §24 limits + §25 10 principles | **KEEP IN SKILL** (short) |
| §26 authors | **KEEP** (tiny) |
| HSDB local note | **REMOVE** from portable skill or move to install note |
| Giant artifact index at top | **CONDENSE** to 3-5 “load when…” pointers |

***

## 9. EPISTEMIC SECURITY COVERAGE

| Failure mode | Rating | Evidence |
| :-- | :-- | :-- |
| Citation identity failure | **COVERED WELL** | §7 gate 1 |
| Citation entailment failure | **COVERED WELL** | §7 gates 2-3 |
| Stale evidence | **COVERED WELL** | §6C, §14 |
| Source duplication | **COVERED WELL** | §11 |
| Correlated agents | **COVERED WELL** | §11 + multi-judge ref |
| Model-as-judge bias | **COVERED WELL** | §12 |
| Verifier failure | **COVERED WELL** | §12 |
| Retrieval poisoning | **PARTIAL** | integrity/contamination; no operational detect beyond suspicion |
| Indirect prompt injection | **PARTIAL** | strong policy language; admits not sandbox |
| Memory poisoning | **PARTIAL** | §15 treats staleness more than adversarial memory |
| Current-state drift | **COVERED WELL** | §14 |
| Error -> empty collapse | **COVERED WELL** | §5 |
| Partial search -> exhaustive claim | **COVERED WELL** | §12, stop rules |
| Entity collision | **COVERED WELL** | §14 Entity |
| Semantic mismatch | **COVERED WELL** | entailment/scope |
| Tool success ≠ user success | **COVERED WELL** | §13, §19 |
| Agent-loop progress mirage | **COVERED WELL** | §13 |
| Stale bug reports | **PARTIAL** | deferred to reference (not in main beyond pointer) |
| Already-completed work | **PARTIAL** | same |
| Intent hallucination | **COVERED WELL** | §2 |
| Past-action denial after compaction | **COVERED WELL** | §16 |

Overall: **broad and modern** failure-mode map. Weakest are *security* modes that need runtime, not prose.

***

## 10. CURRENT-STATE HANDLING

**Does it hinder was-true -> is-true-now?** **Yes, on paper - for strong T3.** `FILE-VERIFIED` §14

- observation_time required for strong T3 current_state
- supporting items must be CURRENT_ENOUGH
- missing freshness -> downgrade
- memory explicitly not current truth §15
- docs can be stale called out in §1

**Gaps:**

- Weaker for casual T1/T2 “API supports X” without forcing live check
- “Newest ≠ correct” is right but easy to under-apply
- No simple default: “mutable public state -> prefer live probe” as one CORE line

**Rating:** strong design intent; obedience-dependent. `HEURISTIC`

***

## 11. SOURCE LINEAGE / INDEPENDENCE

| Question | Critical answer |
| :-- | :-- |
| Epistemically sensible? | **Yes** - failure domains > vote counting `FILE-VERIFIED` |
| Can LLM assess lineage well? | **Poorly in general** - syndication/press-copy hard `HEURISTIC` |
| How know independence? | Often can’t; must say UNKNOWN - doc says this `FILE-VERIFIED` |
| known / plausible / unknown split? | **Partial** - UNKNOWN + lineage_basis; not a clean 3-way enum in main skill |
| Pseudo-rigor risk? | **Yes** - naming `INDEPENDENT_ORIGIN` is cheap; checker only checks field presence `FILE-VERIFIED` §11 |

**Pseudo-rigor point:** requiring `lineage_basis` is good documentation hygiene; it is **not** independence. The skill mostly admits this - good - but still invites ledger cosplay. `INFERENCE`

***

## 12. PROMPT-INJECTION BOUNDARY

Compared with AgentDojo / IterInject / NIST agent-hijacking work: prompt defenses are necessary and **insufficient**. `WEB-VERIFIED`

| Q | Answer |
| :-- | :-- |
| What can prompt improve? | Reduce *instruction-following* of retrieved jailbreaks; keep “data vs control” framing |
| What can’t it secure? | Tool authz, sandbox escape, privileged side effects, determined adaptive IPI |
| Does SKILL state the boundary? | **Yes** - §8, §24, README limits `FILE-VERIFIED` |
| Oversell as security boundary? | **Mostly no** in SKILL; README table “what it catches” can still read stronger than “policy only” |
| Runtime separated? | **Yes, explicitly** |

**Not epistemic theatre here** - one of the more honest sections. Residual risk: users may still treat the skill as a security control because it *talks about* injection. `HEURISTIC`

***

## 13. RESEARCH VERIFICATION

### Representative checks

| SOURCE | FILE CLAIMS | ACTUAL SUPPORT | VERDICT |
| :-- | :-- | :-- | :-- |
| arXiv:2109.07958 TruthfulQA | Factuality corpus | Exists; measures imitation of falsehoods | **OK** `WEB-VERIFIED` |
| arXiv:2305.14251 FActScore | Atomic factuality | Exists; atomic fact precision | **OK** |
| arXiv:2309.11495 CoVe | Chain-of-verification | Exists | **OK** |
| ACL 2025.acl-long.349 Intent Hallucination | Intent as failure mode | Exists; FAITHQA; omit/misinterpret constraints | **OK - well used** `WEB-VERIFIED` |
| ACL 2025.acl-long.1587 FactBench | Dynamic factuality bench | Exists | **OK** |
| ACL 2025.acl-long.71 HALoGEN | Hallucination taxonomy/eval | Exists (“Fantastic LLM Hallucinations…”) | **OK** |
| arXiv:2406.13352 AgentDojo | Agentic prompt injection | Exists; tools over untrusted data | **OK** |
| arXiv:2605.24659 IterInject | IPI iterative attacks | Exists | **OK identity** |
| arXiv:2606.10525 Automated PI in agents | Agentic automated PI | Exists (Debenedetti/Tramèr et al.) | **OK** |
| arXiv:2601.06818 AgentHallu | Trajectory hallucination attribution | Exists; Planning/Retrieval/Reasoning/Human/Tool-Use - **matches §13 classes** | **OK - tight mapping** `WEB-VERIFIED` |
| arXiv:2607.25152 Progress mirage | Agent loops stagnation-as-progress | Exists; external grounding required | **OK - tight mapping** |
| arXiv:2506.08500 DRAGged into Conflicts | Source conflict | Exists | **OK** |
| arXiv:2505.06579 POISONCRAFT | RAG poisoning | Exists | **OK identity** |
| arXiv:2603.25164 PIDP-Attack | PI + DB poison | Exists | **OK identity** |
| arXiv:2604.22891 Self-preference judges | Judge bias | Exists | **OK** |
| arXiv:2307.03172 Lost in the Middle | Long-context | Exists | **OK** |
| arXiv:2510.22967 MAD-Fact | Multi-agent debate factuality | Exists | **OK identity** |
| NIST AI RMF GenAI Profile | Risk framing | NIST publication exists | **OK link-level** |
| NIST agent-hijacking blog Jan 2025 | Agent hijacking evals | Exists; AgentDojo-based | **OK** `WEB-VERIFIED` |
| arXiv:2606.01435 | “Reliable Post-Retrieval Assembly…” | arXiv title surface: **“Don't Ask the LLM to Track Freshness…”**; Semantic Scholar also shows assembly-oriented title | **TITLE DRIFT / IDENTITY FRICTION** `WEB-VERIFIED` |
| Hermes docs URL | Skill/progressive disclosure | Real docs match claimed model | **OK** `WEB-VERIFIED` |

### Research-use judgment

- **Not pure decoration:** several v5 items map to concrete controls (intent, trajectories, progress mirage, conflicts, judge bias). `INFERENCE`
- **Partly decorative:** dumping 32 v4 + ~18 v5 citations into the main skill does not make the agent more factual; it signals erudition. `HEURISTIC`
- **Citation laundering risk:** low on identity for sampled IDs; moderate on **over-claiming that research “grounds” runtime reliability** - skill mostly avoids this, README slightly less so.
- **Gap:** full claim-to-finding fidelity for every paper needs `references/*` (not provided). Residual: **`UNVERIFIED` at interpretation depth**.

***

## 14. HERMES COMPATIBILITY

| Aspect | Status |
| :-- | :-- |
| YAML frontmatter shape | **COMPATIBLE** (name, description, version, author, license, platforms, metadata.hermes) `WEB-VERIFIED` |
| `platforms: windows` | Supported in Hermes platform table `WEB-VERIFIED` |
| Category path `software-development/` | Matches README + Hermes layout `FILE-VERIFIED` · `WEB-VERIFIED` |
| Progressive disclosure terminology | **Correct** `WEB-VERIFIED` |
| `skill_view` / slash load | Documented correctly at high level `WEB-VERIFIED` |
| references/scripts structure | **COMPATIBLE DOCUMENT STRUCTURE** `WEB-VERIFIED` |
| Scripts auto-enforced? | **No** - agent-invoked helpers only -> **NOT ACTUAL RUNTIME ENFORCEMENT** `WEB-VERIFIED` · `FILE-VERIFIED` (skill admits) |
| Size vs house style | **Structurally valid, stylistically non-compliant** (~30k ≫ 8-14k aim) `WEB-VERIFIED` |
| Description length | Under 1024; starts “Use for” not “Use when” - minor style drift `FILE-VERIFIED` · `WEB-VERIFIED` |
| Invented Hermes tools? | No exotic non-Hermes runtime APIs claimed in skill body `FILE-VERIFIED` |

**Split:**
`COMPATIBLE DOCUMENT STRUCTURE` ≠ `ACTUAL RUNTIME ENFORCEMENT`.

***

## 15. README FORENSIC AUDIT

### First screen

**Good:** name, tagline (“Make the agent earn the sentence”), Hermes badge, problem framing in one breath. Differentiates from dumb “fact check” via failure list. `FILE-VERIFIED`

### Credibility

- Strengths: early limits section; PASS ≠ truth; green tests ≠ obedience.
- Weaknesses: “What it catches” table reads like **behavioral guarantees**; “30 attack cases + executable regression tests” is **IMPLEMENTATION UNVERIFIED** here; research list can feel research-washed even with disclaimer.

### Information architecture

Reasonable: problem -> catches -> how -> evidence -> deterministic checks -> install -> run -> research -> limits -> map. Limits could be **higher**.

### Human writing

Better than generic AI slop; still some polish patterns (parallel failure bullets, symmetrical tables, slogan cadence). “Proudly witchcrafted” is human/brand, not corporate empty. Mild rule-of-three rhythm in places.

### Length

**ABOUT RIGHT** for a serious public skill README (~11k chars). Not a novel; not a stub.

### Trust (technical reader)

**Mixed-positive:** limitations save it from pure theatre; helper section still risks “we have scripts so we’re safe.” After README alone: cautious respect, not full trust - correct stance without code.

### Claim audit (README)

| Claim | Tag |
| :-- | :-- |
| Procedural layer for non-theatrical failures | **SUPPORTED BY SKILL** |
| claim strength ≤ evidence strength | **SUPPORTED BY SKILL** |
| Separates identity/entailment/lineage/etc. | **SUPPORTED BY SKILL** |
| Deterministic narrow helpers behavior | **IMPLEMENTATION UNVERIFIED** (documented behavior only) |
| fail-closed liveness | **IMPLEMENTATION UNVERIFIED** / doc claim |
| 30 adversarial cases + pytest suite | **IMPLEMENTATION UNVERIFIED** |
| False-positive prevention (stderr substring) | **IMPLEMENTATION UNVERIFIED** (plausible design) |
| Research provenance offline checker | **IMPLEMENTATION UNVERIFIED** |
| Hermes progressive disclosure install | **SUPPORTED BY WEB** + **SUPPORTED BY SKILL** |
| “Research is evidence for design… protocol can still be wrong” | Honest - good |
| “What it catches” as assured catching | **OVERSTATED** if read as runtime efficacy |
| Markdown obeyed at runtime? Explicitly denied | Good - not overstated |

***

## 16. OVERENGINEERING AUDIT

| Mechanism | Real FM? | LLM-applicable? | Beyond simple rule? | Dup? | Cost OK? | Obedience | Theatre? | Tag |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Core invariant | Y | Y | Foundation | N | Y | ↑ | N | **ESSENTIAL** |
| T0-T3 tiers | Y | Y | Y | Low | Y | ↑ if simple | N | **ESSENTIAL** |
| Atomic claims | Y | Y | Y | Low | Y | ↑ | N | **ESSENTIAL** |
| Evidence states + forbidden collapses | Y | Medium | Y | Med | Mostly | ↑ | Low | **VALUABLE** |
| 11-step pipeline | Y | Weak full | Partial | High w/ checklist | N full | ↓ if forced | Med | **QUESTIONABLE** as always-on |
| 6 fitness questions | Y | Partial | Expand entailment | Med | Borderline | ↓ if every source | Med | **VALUABLE** condensed |
| 4 citation gates | Y | Y | Y | Low | Y | ↑ | N | **ESSENTIAL** |
| Untrusted boundary | Y | Partial | Y | Low | Y | ↑ | N | **ESSENTIAL** |
| Independence/failure domains | Y | Weak | Y | Low | Theory heavy | Mixed | **Risk** | **VALUABLE** w/ UNKNOWN default |
| Verifier skepticism | Y | Medium | Y | Low | Y | ↑ | N | **VALUABLE** |
| Trajectory / progress mirage | Y | Medium | Y | Low | Y | ↑ agentic | N | **VALUABLE** |
| Completion ladders | Y | Y | Y | Low | Y | ↑ | N | **ESSENTIAL** |
| Full evidence ledger + JSON schema | Y niche | Weak | Narrow | High | N routine | ↓ | **Yes if always** | **OVERENGINEERED** for main path |
| Research corpus in skill | Design only | N | N runtime | High | N | ↓ | **Yes** | **OVERENGINEERED** in L1 |
| 5 helper scripts narrative | Eng. hygiene | N/A doc | Maybe | - | - | - | If oversold | **VALUABLE** if real; **UNVERIFIED** |
| Dual long checklists | Y | Cargo-cult | Low | High | N | ↓ | Med | **QUESTIONABLE** |

**Epistemic theatre threshold:** approached at full ledger + independence labels + bibliography-as-proof; **not fully crossed** because limits sections repeatedly puncture the balloon. `HEURISTIC`

***

## 17. SIMPLE 8-RULE BASELINE vs v5.2

**Simple 8-rule skill (mental design):**
(1) claim≤evidence (2) decompose (3) evidence≠orders (4) identity+entailment (5) freshness for “now” (6) no state collapse (7) high-stakes: falsify + don’t trust clones (8) fixed/works only with matching checks; external goal -> external signal.

| Dimension | Simple 8 | AHP v5.2 |
| :-- | :-- | :-- |
| Coverage | ~60-70% of value | Broader edge cases |
| Obedience | **Higher** | **Lower** |
| Token cost | Low | High |
| Maintainability | High | Low-medium |
| False certainty | Lower ceremony -> less fake rigor; more silent misses | More fake rigor risk; fewer silent category misses *if obeyed* |
| Agentic usefulness | High | High *if* selectively applied |
| High-risk reliability | Good baseline | Better **conditional** depth |

**Does complexity pay?**
**Marginally, and only if bulk moves to references and CORE stays tiny.** As a single L1 blob, complexity likely **does not** pay. `HEURISTIC`

***

## 18. WHAT IS ACTUALLY NOVEL?

| Layer | Content |
| :-- | :-- |
| Known factuality | Atomic claims, entailment, abstention, CoVe-like checks |
| Known RAG/citation | Identity vs support, conflict handling |
| Known PI principles | Data/control separation |
| Known agentic safety | Tool≠user success, external metrics |
| Local engineering heuristics | Completion ladders, ERROR vs NOT_FOUND, past-action denial, stop rules |
| Interesting integration | **Unified risk-tiered control model** binding intent + states + independence-as-failure-domains + completion ontology + verifier-as-claim for Hermes skills |

**Answer:** Primarily a **high-quality aggregation and operationalization** of known practices, with a few sharp local formulations (completion semantics, forbidden collapses, independence wording). Not a new scientific paradigm. That is still useful engineering if delivered at obedient size.

***

## 19. SCORECARD

| Dimension | Score |
| :-- | --: |
| Epistemic rigor | 8.5 |
| Hallucination prevention design | 8.0 |
| Citation discipline | 8.5 |
| Retrieval robustness | 7.0 |
| Current-state reasoning | 8.0 |
| Memory safety | 7.0 |
| Prompt-injection awareness | 7.5 |
| Source-lineage reasoning | 7.0 |
| Verifier skepticism | 8.5 |
| Agentic workflow safety | 8.5 |
| Intent preservation | 8.5 |
| Recovery / blast radius | 7.5 |
| Progressive disclosure | 4.0 |
| Context efficiency | 3.5 |
| Instruction obedience probability | 4.0 |
| Hermes compatibility | 7.0 |
| Research grounding | 7.5 |
| Internal consistency | 6.5 |
| Maintainability | 5.0 |
| README quality | 7.5 |
| Public credibility | 7.0 |
| Production-readiness as DOCUMENTED DESIGN | 6.5 |

**OVERALL DESIGN SCORE: 7.0 / 10**
**DOCUMENTATION SCORE: 7.2 / 10**
*(No implementation score - boundary respected.)*

***

## 20. P0 / P1 / P2 / P3 DOCUMENT-LEVEL FINDINGS

### P0

1. Main `SKILL.md` far exceeds Hermes progressive-disclosure budget; obedience risk dominates design quality.
2. Audit boundary: all “scripts/tests enforce X” remain **IMPLEMENTATION UNVERIFIED** - README must not be read as proven runtime safety.

### P1

3. Move §23 bibliography + deep theory out of L1.
4. Resolve ceremony vs optionality: one short “when to go deep” gate at top.
5. Independence: default **UNKNOWN lineage**; forbid strong independence language without human-auditable basis (not just non-empty string).
6. README “What it catches” -> “What it is designed to catch (policy-level)”.

### P2

7. Condense fitness/citation/trajectory into CORE bullets; details -> references with explicit load triggers.
8. Remove or isolate HSDB local convention from portable skill.
9. Fix/verify arXiv:2606.01435 title identity in manifest.
10. Description style: align with Hermes “Use when…” house preference.

### P3

11. Reduce slogan density in README; keep one tagline.
12. Artifact index -> top 5 “load when” only.
13. Add one-line mutable-state default: live probe preferred.

***

## 21. FINAL VERDICT

# `PROMISING BUT OVERENGINEERED`

1. **Good main Hermes skill as-is?** **No** - too long for L1 obedience.
2. **Too long?** **Yes.**
3. **Keep in main:** core invariant, tiers, atomic claims, state collapses, data≠instructions, citation entailment, completion wording, hard limits, 7-line hot path.
4. **Move to references:** research corpus, schema/ledger, harness traps, multi-judge, vetting workflows, long checklists, gap maps.
5. **README public-ready?** **Almost** - after claim softening.
6. **Weaken:** catching guarantees, any implication tests prove LLM compliance, fail-closed as global property.
7. **Biggest real asset:** integrated agentic epistemology (intent + states + verifier-skepticism + completion ladders + external success).
8. **Biggest real problem:** instruction overload -> cargo-cult epistemic theatre at runtime.
9. **Strong agent improved?** **Probably yes** if it treats skill as selective policy.
10. **Weak agent worsened?** **Probably yes** - more tokens, more fake structure, less actual checking.

**Theatre threshold:** approached in density and independence labeling; **not fully crossed** thanks to repeated non-guarantee language. Ambition is not the problem; **packaging for a finite attention budget is.**

***

## 22. EXACT RECOMMENDED CHANGES

1. **Rewrite L1 `SKILL.md` target: 8-14k chars** (hard preference), never >20k without split.
2. **Top structure:**
   - When to use
   - Core invariant
   - 7-rule hot path
   - T0-T3 one table
   - Forbidden collapses
   - Completion wording
   - Hard limits
   - “Load reference X when Y” index (≤8 bullets)
3. **Delete from L1:** full v4/v5 paper lists; long dual checklists; HSDB note; schema field lectures.
4. **References:** `hot-path.md` optional; keep research in `research-foundations.md` only.
5. **Independence policy line:** “If you cannot name a different failure domain, write UNKNOWN - never INDEPENDENT_ORIGIN.”
6. **README:** rename catches table; badge “adversarial” -> link as *spec corpus*; keep limits above fold.
7. **Every helper claim:** “documented contract; not semantic truth; not proof of agent obedience.”
8. **Do not add more enums** until obedience measured; if anything, delete states before adding.
9. **After code is auditable:** separate IMPLEMENTATION audit - this document audit must not be reused as proof scripts work.
10. **Success metric for v5.3:** fewer tokens in L1, same CORE failures covered, higher checklist adherence in messy multi-tool sessions - not more papers.

***

### Evidence standard reminder

- Document structure, claims, contradictions: **`FILE-VERIFIED`**
- Hermes loading/size/docs and paper identities: **`WEB-VERIFIED`** where cited
- Obedience/theatre judgments: **`HEURISTIC`**
- Script/schema/test behavior: **`UNVERIFIED` / DOCUMENTED CLAIM - IMPLEMENTATION UNVERIFIED`**

**`DOCUMENTED CONTROL ≠ IMPLEMENTED CONTROL ≠ RUNTIME ENFORCEMENT`**
