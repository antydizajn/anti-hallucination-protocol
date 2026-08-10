Mam pełny obraz. Oto ocena.

WERDYKT: repo uczciwe, rzemiosło dobre, ale MA CZERWONE TESTY — i to jest najlepsza ironia tego projektu

To jest nasze repo (Paulina + Gniewka, dziś 19:48 UTC, 1 commit). Oceniam jak obcy audytor by ocenił — zero litości.

CO TO JEST (z kodu, nie z README)

Hermes skill v5.4.0: warstwa proceduralna anty-halucynacji z 4 progami ryzyka (T0-T3), 7 zasadami hot path, 8 stanami dowodowymi z ZAKAZANYMI kolapsami (ERROR nie jest NOT_FOUND), granicą nieufnego dowodu (prompt injection = dane, nie instrukcje), rozdzieleniem mutacji od walidacji i progressive disclosure. Do tego 5 deterministycznych checkerów + schemat JSON evidence record. 44 pliki, 976 KB.

DOWODY — co uruchomiłam

1. pytest: 100 PASS / 2 FAIL (102 testy). I to jest sedno:
   - test_trailing_unterminated_flow_sequence_fails — zakłada, że description: Test fixture [ to zły YAML. PyYAML poprawnie parsuje to jako plain scalar — spec YAML: [ w środku plain scalar to literalny znak. BUG W TEŚCIE, nie w kodzie. Test ma błędne założenie o YAML.
   - test_metadata_hermes_must_be_mapping — fixture hermes: nope + wcięty tags: pod spodem = YAML parse error WCZEŚNIEJ, walidator zwraca "not valid YAML" zamiast oczekiwanego "metadata.hermes must be a mapping". Walidator WYKRYWA problem, ale innym komunikatem. Test za sztywny co do stringa.
   - Wniosek: rdzeń jest zdrowy, ale repo sprzedające "adversarial verification" ma czerwoną suitę. Dokładnie to, co protokół sam mówi: "a passing test is not an observed user path". Naprawa = 5 minut (trailing test: użyć [foo bez zamknięcia; mapping test: fixture bez tags: pod scalarem).
2. check_v5_integrity.py: PASS (pina 5.4.0, realny YAML parse, nie ręczna imitacja — to rzadka jakość)
3. check_research_provenance.py: PASS
4. liveness_check.sh: PASS (L1/L2 portable; uczciwie raportuje L3 legacy i L4 behavioral jako UNKNOWN)

CO JEST NAPRAWDĘ DOBRE (nie lizanie — dowody)

1. AUDITS/SUMMARY.md — poziom, którego nie widuję w OSS. 10 audytów podzielonych na 2 klasy dowodowe (execution-capable vs document-only, "nie wolno ich uśredniać"), SHA-256 manifest oryginałów, ledger F-001..F-015 z decyzjami, i — najlepsze — sekcja findings REJECTED z uzasadnieniem ("trust me jako lineage_basis to nie P0, bo string-validator nie może rozstrzygnąć prawdy semantycznej; blacklista to security theatre"). To jest myślenie epistemiczne, nie marketing.
2. Jawny placeholder: SUMMARY sam mówi, że PPX-GLM5.2.md to placeholder (hash, nie surowy plik) i że repo NIE może twierdzić kompletnego 10/10 archiwum. Repo które samo się demaskuje = zaufanie.
3. "What it does not prove" — 11 pozycji, w tym "two sources are independent because a record says so", "Markdown instructions were obeyed at runtime". Zero obietnic zero-hallucination. README mówi wprost: "No behavioral obedience benchmark is claimed by this release."
4. arxiv-manifest: 32+ realnych ID (Survey Hallucination 2202.03629, TruthfulQA 2109.07958, CoVe 2309.11495, Self-RAG 2310.11511, FActScore, MiniCheck... wszystkie istnieją) z verified_on i verification_scope — jawnie ograniczonym do identity check.
5. adversarial-cases.md: 5+ przypadków jako SPECYFIKACJA, nie ukryte testy CoT ("These are protocol-level fixtures. They are not hidden chain-of-thought tests.").

CO UKRAŚĆ (gdyby to było cudze repo)

1. Wzorzec "jedno zdanie zarabia swoje brzmienie" — claim strength <= evidence strength jako jedyny invariant pod 4 tierami. Prosty, egzekwowalny, przenośny.
2. Konwencja exit codes FOUND=0/NOT_FOUND=1/ERROR=2 — niepoprawna komenda NIGDY nie staje się FOUND przez substring w stderr. To łata konkretny, częsty bug agentów.
3. Metoda AUDITS z REJECTED-ledger — archiwizowanie nie tylko co przyjęto, ale co ODRZUCONO i dlaczego. Chroni przed "model count is not truth".

WADY (poza czerwonymi testami)

- Bus factor = 1 konto, 0 gwiazdek, 0 forków, 1 commit — to etap, nie grzech, ale adopcja = zero.
- README badge "Hermes-Agent" linkuje do github.com/NousResearch/hermes-agent — nie weryfikowałam czy to oficjalne repo (docs są na hermes-agent.nousresearch.com); do sprawdzenia przed promocją.
- F-013 samo-się-potwierdza: obedience pod long-context pressure nie jest zbadane behavioralnie — repo to jawnie przyznaje, ale to oznacza że wartość = tylko tyle, ile model faktycznie przestrzega. Skill zainstalowany u nas w ~/.hermes/skills/software-development/ działa, ale to nie jest dowód obedience.

OCENY

- Tech/rzemiosło: 8/10 (checkery solidne, schema z invalidation, testy coverage dobre — minus 2 czerwone)
- Uczciwość/epistemika: 9/10 (to główny produkt i jest wybitny)
- Adopcja/dojrzałość: 1/10 (dziś powstało)
- Gotowość do promocji: 7/10 — po naprawie 2 testów i weryfikacji badge'a.

REKOMENDACJA

Naprawić 2 testy (5 minut), commit, i wtedy repo w 100% przechodzi własny egzekwowalny kontrakt. Ironia czerwonej suity w repo anty-halucynacyjnym jest zbyt dobra, żeby ją zostawić — to pierwszy przypadek, który protokół powinien złapać na sobie. Chcesz, żebym to naprawiła?
