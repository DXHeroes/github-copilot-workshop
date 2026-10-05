# Definition of Done — Šablona pro validaci výstupů

## 1. Analýza požadavků (BRD)

- [ ] Dokument má jasně definovaný cíl projektu (co a proč)
- [ ] Funkční požadavky jsou formulovány konkrétně a ověřitelně (ne vágně)
- [ ] Nefunkční požadavky jsou uvedeny (výkon, bezpečnost, regulace, přístupnost)
- [ ] Rozpory mezi zdroji jsou explicitně identifikovány a popsány
- [ ] U každého rozporu je uvedeno, jak by měl být vyřešen (otevřená otázka / eskalace / rozhodnutí)
- [ ] Chybějící informace jsou identifikovány jako otevřené body s navrženým krokem k dořešení
- [ ] Předpoklady jsou explicitně uvedeny a označeny jako neověřené, pokud nebyly potvrzeny
- [ ] Omezení (technická, regulatorní, časová) jsou uvedena
- [ ] Scope je jasně ohraničen — co je IN a co je OUT pro MVP

## 2. Epic

- [ ] Epic má jednoznačný název vystihující business hodnotu
- [ ] Je popsán business kontext (proč tento epic existuje)
- [ ] Cílová skupina je definována
- [ ] Měřitelná kritéria úspěchu (KPIs) jsou uvedena
- [ ] Scope epicu je ohraničen — co zahrnuje a co ne
- [ ] Rizika a otevřené otázky jsou popsány
- [ ] Regulatorní a compliance požadavky relevantní pro epic jsou zmíněny

## 3. User Stories

- [ ] Každá story sleduje formát „Jako [role] chci [akce], abych [hodnota]“
- [ ] Každá story je nezávislá (lze implementovat a dodat samostatně)
- [ ] Každá story je testovatelná (lze jednoznačně ověřit, jestli je splněna)
- [ ] Každá story má akceptační kritéria (min. 2)
- [ ] Granularita je přiměřená — story je realizovatelná v jednom sprintu
- [ ] Error states a edge cases jsou pokryty vlastními stories nebo akceptačními kritérii
- [ ] Stories pokrývají i nefunkční požadavky (bezpečnost, přístupnost, výkon) tam, kde je to relevantní
- [ ] Závislosti mezi stories jsou identifikovány

## 4. Diagramy

- [ ] Všichni relevantní aktéři/systémy jsou zakresleni (včetně externích systémů a boundary)
- [ ] Happy path je kompletní od začátku do konce
- [ ] Alternativní flow (minimálně 1) je zakreslena
- [ ] Error handling flow je zakreslena (co se stane, když něco selže)
- [ ] Asynchronní operace jsou správně znázorněny (pokud existují)
- [ ] Diagram je konzistentní s popsanou architekturou

## 5. Slovník pojmů

- [ ] Obsahuje všechny klíčové doménové pojmy z podkladů
- [ ] Každý pojem má jednoznačnou definici (1–2 věty)
- [ ] Anglické a české varianty jsou propojeny (pokud se v podkladech používají obě)
- [ ] Technické zkratky jsou rozepsány
- [ ] Pojmy, které se v podkladech používají nekonzistentně, jsou identifikovány s poznámkou o sjednocení
- [ ] Slovník pokrývá business i technickou terminologii (nikoliv však standardní technické pojmy jako HTTP metody, status codes, atd.)

## 6. Testovací scénáře (Gherkin)

- [ ] Scénáře jsou ve formátu Given-When-Then
- [ ] Každý scénář testuje jednu konkrétní věc
- [ ] Happy path je pokryt pro každou klíčovou funkci
- [ ] Negativní scénáře jsou pokryty (neplatný vstup, nedostatečná historie, chybějící nebo odvolaný souhlas)
- [ ] Edge cases z podkladů jsou pokryty (sdílené účty, více účtů, nulový zůstatek, klient s exekucí)
- [ ] Scénáře zohledňují technická omezení (denní batch a cache, cold start, rate limity, až 24 h stará úvěrová data)
- [ ] Scénáře pokrývají i chybové stavy systému (API nedostupné, timeout, nevalidní data)

## 7. API specifikace

- [ ] Endpointy používají správné HTTP metody (GET pro čtení, POST pro vytvoření, PUT/PATCH pro úpravu, DELETE pro smazání)
- [ ] URL cesty jsou konzistentní a sledují REST konvence
- [ ] Request a response formáty jsou definovány (alespoň schematicky)
- [ ] Autentizace a autorizace jsou popsány
- [ ] Chybové kódy jsou definovány pro hlavní error states (400, 401, 403, 404, 409, 429, 500)
- [ ] Rate limity jsou zdokumentovány (pokud existují)
- [ ] Asynchronní operace jsou správně popsány (jak klient zjistí výsledek)
- [ ] Stránkování je řešeno u endpointů vracejících seznamy
- [ ] Verzování API je definováno

## 8. User dokumentace

- [ ] Dokumentace je psaná z pohledu uživatele, ne vývojáře
- [ ] Jazyk je srozumitelný pro netechnického čtenáře
- [ ] Hlavní use cases jsou pokryty krok za krokem
- [ ] Chybové stavy jsou popsány z pohledu uživatele (co uvidí, co má dělat)
- [ ] Obsahuje informaci o tom, že ukazatel počítá algoritmus a nejde o úvěrové hodnocení (regulatory disclaimer)
- [ ] FAQ sekce pokrývá nejčastější otázky identifikované v podkladech
- [ ] Dokumentace popisuje, jak ukazatel skrýt, odvolat souhlas a požádat o lidský přezkum
