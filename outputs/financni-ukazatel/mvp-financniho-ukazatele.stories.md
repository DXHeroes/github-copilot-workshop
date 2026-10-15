# User stories: MVP finančního ukazatele

- Vychází z epicu `outputs/financni-ukazatel/mvp-financniho-ukazatele.epic.md`.
- Zapracovaná rozhodnutí člověka k rozporům z epicu (sekce 10): 1 termín MVP 4 týdny od kickoffu, 2 jen základní metriky, 3 název „Finanční ukazatel“ bez slova „skóre“, 6 bez sdílení, 10 batch jednou denně.
- Rozpory 4, 5, 7, 8, 9, 11, 12 a 13 zůstávají otevřené; čísla „rozpor N“ a „otázka N“ odkazují na tabulku v sekci 10 epicu.

### US-01: Udělení granulárního souhlasu

Jako klient chci udělit samostatné souhlasy s analýzou transakcí, se zobrazením ukazatele a s notifikacemi, abych měl kontrolu nad tím, co banka s mými daty dělá.

**Akceptační kritéria:**

- Souhlas je explicitní opt-in, žádný checkbox není předškrtnutý (email-zmena-priorit.md).
- Souhlasy jsou oddělené: analýza transakcí, zobrazení ukazatele, notifikace; jeden generální souhlas nestačí (email-zmena-priorit.md).
- Bez souhlasu s analýzou transakcí se ukazatel klientovi nepočítá, protože výpočet je automatizované profilování podle GDPR čl. 22 (email-zmena-priorit.md).
- Consent flow existuje na FE i BE (email-zmena-priorit.md).
- Otevřená otázka: co klient bez souhlasu uvidí na místě ukazatele, viz otázka 28 v epicu.
- Otevřená otázka: frekvence notifikací, ke kterým se souhlas váže, viz rozpor 5 v epicu.

**Závislosti:** Žádné.

**Zdroj:** email-zmena-priorit.md

### US-02: Odvolání souhlasu

Jako klient chci kdykoliv odvolat udělený souhlas, abych mohl analýzu svých dat zastavit.

**Akceptační kritéria:**

- Každý z granulárních souhlasů jde kdykoliv odvolat (email-zmena-priorit.md).
- Po odvolání souhlasu s analýzou transakcí se klient nezařadí do dalšího výpočtu (email-zmena-priorit.md).
- Otevřená otázka: co se stane s už spočítanými výsledky v cache a jak dlouho se uchovávají, viz otázka 23 v epicu.
- Otevřená otázka: co klient po odvolání uvidí na místě ukazatele, viz otázka 28 v epicu.

**Závislosti:** US-01.

**Zdroj:** email-zmena-priorit.md

### US-03: Výpočetní jádro ze základních metrik

Jako Data Scientist chci rule-based výpočetní jádro ze základních metrik v odděleném modulu, abych ho ve fázi 2 mohl nahradit ML modelem.

**Akceptační kritéria:**

- Vstupy výpočtu jsou poměr příjmů a výdajů, zůstatek relativně k měsíčním výdajům, úvěrové zatížení (poměr splátek k příjmům) a trend (zlepšuje se / zhoršuje / stagnuje) (poznamka-architekt.md, schuzka-business.md).
- Výsledek je hodnota ukazatele, barva a textový popis (poznamka-architekt.md).
- Analýza finančního chování (pravidelnost spoření, impulzivní výdaje, finanční polštář) se nepočítá; rozhodnuto, viz rozpor 2 v epicu (schuzka-business.md, email-zmena-priorit.md).
- Jádro je oddělený modul vyměnitelný za ML model a architektura počítá s rozšířením o analýzu chování ve fázi 2 (schuzka-technicka.md, poznamka-architekt.md, schuzka-business.md).
- Výpočet bere jen settled transakce, pending transakce nejsou k dispozici (schuzka-technicka.md, poznamka-architekt.md).
- Otevřená otázka: kdo definuje váhy vstupů, viz rozpor 13 v epicu; váhy nejsou definované (poznamka-architekt.md).
- Otevřená otázka: forma výstupní škály, 0–100 nebo 3–5 úrovní, viz rozpor 4 v epicu.
- Otevřená otázka: segmentace vah podle věku, viz otázka 21 v epicu.
- Otevřená otázka: očekávaný výsledek pro nulový zůstatek a klienta s exekucí, viz otázka 27 v epicu.

**Závislosti:** US-04, US-05.

**Zdroj:** poznamka-architekt.md, schuzka-technicka.md, schuzka-business.md, email-zmena-priorit.md

### US-04: Načtení transakčních dat z Account Data API

Jako backend vývojář chci načítat zůstatky a transakce z Account Data API v rámci jeho limitů, abych měl vstupy pro výpočet bez výpadků služby.

**Akceptační kritéria:**

- Služba dodržuje rate limit 200 req/min per API key, který je sdílený, ne per user (poznamka-architekt.md).
- Při odpovědi 429 služba dodrží 60s cooldown (poznamka-architekt.md).
- Historie delší než 90 dní se načítá více cally a se stránkováním po 50 záznamech (poznamka-architekt.md).
- Počítá se s odezvou v peaku 3–5 s (pondělní rána, 1. pracovní den v měsíci) (poznamka-architekt.md, email-kickoff.md).
- Načítají se jen účty v CZK (schuzka-technicka.md, poznamka-architekt.md).
- Otevřená otázka: zda se u klienta s více běžnými účty počítají všechny účty, viz otázka 20 v epicu.

**Závislosti:** Account Data API; žádost o zvýšení rate limitu, odpověď nejdříve za 3 týdny (poznamka-architekt.md).

**Zdroj:** poznamka-architekt.md, schuzka-technicka.md, email-kickoff.md

### US-05: Načtení úvěrových dat z Loan Service API

Jako backend vývojář chci načítat úvěry a splátky z Loan Service API, abych mohl spočítat úvěrové zatížení.

**Akceptační kritéria:**

- Služba volá Loan Service API přes API gateway se service accountem s elevated permissions (poznamka-architekt.md).
- Služba dodržuje rate limit 50 req/min (poznamka-architekt.md).
- Služba počítá s daty starými až 24 hodin kvůli nightly sync (poznamka-architekt.md, schuzka-technicka.md).
- Otevřená otázka: kdo požádá o service account, vyřízení trvá cca 2 týdny, viz otázka 17 v epicu.

**Závislosti:** Service account pro Loan Service API (poznamka-architekt.md).

**Zdroj:** poznamka-architekt.md, schuzka-technicka.md

### US-06: Denní dávkový přepočet do cache

Jako backend vývojář chci jednou denně přepočítat ukazatel a uložit ho do Redis cache, aby aplikace četla hotový výsledek bez čekání na zdrojová API.

**Akceptační kritéria:**

- Přepočet běží jako batch jednou denně, plánovaně 02:00–06:00; rozhodnuto, viz rozpor 10 v epicu (poznamka-architekt.md, schuzka-technicka.md).
- Výsledky se ukládají do Redis cache s TTL 24h (poznamka-architekt.md).
- Uživatel vidí stav z posledního přepočtu, real-time aktualizace po platbě kartou se nedělá; rozhodnuto, viz rozpor 10 v epicu (schuzka-technicka.md).
- Batch je rozložený tak, aby se vešel do limitu 200 req/min, s prioritou aktivních uživatelů (schuzka-technicka.md, poznamka-architekt.md).
- Kafka topic `account.balance.changed` se jako spouštěč nepoužívá (schuzka-technicka.md, poznamka-architekt.md).
- Otevřená otázka: doba retence výsledků, viz otázka 23 v epicu.

**Závislosti:** US-03, US-04, US-05.

**Zdroj:** poznamka-architekt.md, schuzka-technicka.md

### US-07: Monitoring dávkových jobů

Jako provozní tým chci vidět stav dávkových jobů, abych poznal, že přepočet nedoběhl.

**Akceptační kritéria:**

- Interní endpoint `GET /financial-health/batch/status` vrací stav batch jobů (schuzka-technicka.md, poznamka-architekt.md).
- Endpoint není dostupný pro FE mobilní aplikace (schuzka-technicka.md).
- Otevřená otázka: kdo bude průběžně monitorovat přesnost výpočtu, viz otázka 19 v epicu.

**Závislosti:** US-06.

**Zdroj:** schuzka-technicka.md, poznamka-architekt.md

### US-08: Bootstrap cache před spuštěním

Jako produktový tým chci před spuštěním předplnit cache, aby klienti po nasazení neviděli místo ukazatele jen placeholder.

**Akceptační kritéria:**

- Bootstrap batch naplní cache před zpřístupněním funkce klientům (schuzka-technicka.md, poznamka-architekt.md).
- Harmonogram počítá s minimálně 2 dny na bootstrap (schuzka-technicka.md, poznamka-architekt.md).
- Bootstrap dodržuje stejné limity zdrojových API jako denní batch (poznamka-architekt.md).

**Závislosti:** US-06.

**Zdroj:** schuzka-technicka.md, poznamka-architekt.md

### US-09: API pro základní údaje ukazatele

Jako FE vývojář chci endpoint s hodnotou, barvou a textem ukazatele, abych ho mohl zobrazit bez vlastní logiky.

**Akceptační kritéria:**

- `GET /users/{id}/financial-health` vrací hodnotu, barvu a textový popis (schuzka-technicka.md, poznamka-architekt.md).
- Data se čtou z Redis cache (schuzka-technicka.md, poznamka-architekt.md).
- Veškerá validace je na serveru, FE data přebírá beze změny (schuzka-technicka.md).
- Otevřená otázka: forma hodnoty, 0–100 nebo 3–5 úrovní, viz rozpor 4 v epicu.

**Závislosti:** US-06.

**Zdroj:** schuzka-technicka.md, poznamka-architekt.md

### US-10: API pro rozpad faktorů

Jako FE vývojář chci endpoint s rozpadem faktorů, abych mohl zobrazit detail ukazatele.

**Akceptační kritéria:**

- `GET /users/{id}/financial-health/details` vrací rozpad faktorů (schuzka-technicka.md, poznamka-architekt.md).
- Rozpad obsahuje faktory příjmy, výdaje, zůstatek a úvěrové zatížení, u každého směr změny a krátký komentář (schuzka-technicka.md).
- Veškerá validace je na serveru (schuzka-technicka.md).
- Otevřená otázka: zda vracet i váhy a vzorec, nebo jen faktory a jejich obecný vliv, viz rozpor 7 v epicu.

**Závislosti:** US-06.

**Zdroj:** schuzka-technicka.md, poznamka-architekt.md

### US-11: Fallback při prázdné cache

Jako klient chci při chybějícím výsledku vidět, že se ukazatel načítá, abych nečekal na prázdnou obrazovku.

**Akceptační kritéria:**

- Při prázdné cache (po deployi, výpadku Redis, nový uživatel) se zobrazí placeholder „Načítáme váš ukazatel“ nebo prázdný kruh (schuzka-technicka.md).
- Na pozadí se spustí on-demand výpočet přes interní `POST /financial-health/calculate`, který není pro FE (schuzka-technicka.md, poznamka-architekt.md).
- Zobrazení home screenu nečeká na on-demand výpočet, ten může v peaku trvat až 5 s (schuzka-technicka.md).

**Závislosti:** US-03, US-09.

**Zdroj:** schuzka-technicka.md, poznamka-architekt.md

### US-12: Finanční ukazatel na home screenu

Jako klient chci na home screenu vidět Finanční ukazatel jako barevný kruh, abych se rychle zorientoval ve svých financích.

**Akceptační kritéria:**

- Home screen zobrazuje animovaný barevný kruh s hodnotou uprostřed (schuzka-technicka.md).
- Barevná pásma: zelená 70–100, oranžová 40–69, červená 0–39 (schuzka-technicka.md).
- Pod kruhem je textace „Jste na dobré cestě“, „Mírné riziko“ nebo „Potřebuje pozornost“ (schuzka-technicka.md).
- Funkce se v UI jmenuje „Finanční ukazatel“ a slovo „skóre“ se nikde nepoužívá; rozhodnuto, viz rozpor 3 v epicu (email-zmena-priorit.md).
- Na home screenu není žádná možnost sdílení ukazatele; rozhodnuto, viz rozpor 6 v epicu (email-zmena-priorit.md, ux-vyzkum.md).
- Kliknutí na kruh otevře detail ukazatele (schuzka-technicka.md).
- Render home screenu nepřekročí SLA; dnes 2,8 s na starších zařízeních, s komponentou hrozí přes 3,5 s (email-kickoff.md, schuzka-technicka.md).
- Otevřená otázka: forma škály, 0–100 nebo 3–5 úrovní / semafor, viz rozpor 4 v epicu.
- Otevřená otázka: tón textací, upřímný nebo vždy motivační, viz rozpor 8 v epicu.
- Otevřená otázka: zda jde ukazatel z home screenu skrýt, viz rozpor 9 v epicu.
- Otevřená otázka: hodnota SLA pro render, viz otázka 25 v epicu, a řešení performance od začátku nebo workaroundem, viz otázka 15 v epicu.

**Závislosti:** US-09, US-11, US-13, US-16.

**Zdroj:** schuzka-technicka.md, email-kickoff.md, email-zmena-priorit.md, ux-vyzkum.md

### US-13: Disclaimer na home screenu

Jako klient chci přímo u ukazatele vidět, že jde o orientační výstup algoritmu, abych ho nezaměnil za úvěrové hodnocení banky.

**Akceptační kritéria:**

- Disclaimer je viditelný na hlavní obrazovce, ne schovaný v podmínkách (email-zmena-priorit.md).
- Disclaimer uvádí, že ukazatel generuje algoritmus, ne finanční poradce (email-zmena-priorit.md).
- Disclaimer uvádí, že ukazatel je edukační a orientační a není úvěrový rating ani skóring (email-kickoff.md, poznamka-architekt.md).
- Disclaimer uvádí, že ukazatel nemá vliv na žádné bankovní rozhodnutí (ux-vyzkum.md).
- Otevřená otázka: finální texty disclaimeru, viz otázka 24 v epicu.

**Závislosti:** Texty od UX (schuzka-technicka.md).

**Zdroj:** email-zmena-priorit.md, email-kickoff.md, poznamka-architekt.md, ux-vyzkum.md

### US-14: Detail ukazatele s rozpadem faktorů

Jako klient chci po kliknutí na ukazatel vidět, co ho ovlivňuje, abych věděl, co můžu zlepšit.

**Akceptační kritéria:**

- Detail zobrazuje rozpad na příjmy, výdaje, zůstatek a úvěrové zatížení (schuzka-technicka.md).
- U každého faktoru je šipka nahoru/dolů a krátký komentář (schuzka-technicka.md).
- Detail vysvětluje logiku výpočtu v rozsahu, který splní právo na vysvětlení podle GDPR (email-zmena-priorit.md).
- Detail neobsahuje faktory analýzy finančního chování; rozhodnuto, viz rozpor 2 v epicu (email-zmena-priorit.md).
- Otevřená otázka: zda zobrazit kompletní vzorec a váhy, nebo jen faktory a jejich obecný vliv, viz rozpor 7 v epicu.
- Otevřená otázka: tón komentářů u faktorů, viz rozpor 8 v epicu.

**Závislosti:** US-10.

**Zdroj:** schuzka-technicka.md, email-zmena-priorit.md

### US-15: Onboarding při prvním zobrazení

Jako klient chci při prvním zobrazení vysvětlení, co ukazatel je a co není, abych mu správně rozuměl.

**Akceptační kritéria:**

- Onboarding se zobrazí při prvním zobrazení ukazatele (schuzka-technicka.md).
- Onboarding vysvětluje, co ukazatel je a co není, včetně disclaimeru (schuzka-technicka.md).
- Onboarding uvádí, že ukazatel nemá vliv na úvěr ani hypotéku (ux-vyzkum.md).
- Otevřená otázka: finální texty onboardingu, viz otázka 24 v epicu.

**Závislosti:** US-01, US-13.

**Zdroj:** schuzka-technicka.md, ux-vyzkum.md

### US-16: Přístupnost kruhové komponenty

Jako klient se screen readerem chci, aby mi čtečka přečetla hodnotu a stav ukazatele, abych funkci mohl používat.

**Akceptační kritéria:**

- Screen reader kruhovou komponentu nepřeskočí a přečte její hodnotu (ux-vyzkum.md, poznamka-architekt.md).
- Přístupnost je opravená před launchem (ux-vyzkum.md).
- Otevřená otázka: kdo komponentu opraví, viz otázka 18 v epicu.

**Závislosti:** Kruhová komponenta v George (poznamka-architekt.md).

**Zdroj:** ux-vyzkum.md, poznamka-architekt.md

### US-17: Klient s krátkou transakční historií

Jako klient s krátkou historií účtu chci vědět, proč vidím jiný nebo žádný ukazatel, abych nebyl zmatený.

**Akceptační kritéria:**

- Služba pozná klienta pod hranicí minimální délky historie (schuzka-business.md, schuzka-technicka.md).
- Otevřená otázka: zda takovému klientovi zobrazit omezenou verzi ze zůstatku a příjmů s disclaimerem, nebo nic, viz rozpor 11 v epicu.
- Otevřená otázka: minimální délka historie, 3 měsíce (ideálně 6), nebo 6 měsíců, viz rozpor 12 v epicu.

**Závislosti:** US-03; varianty připraví Data Scientist a UX (schuzka-technicka.md).

**Zdroj:** schuzka-business.md, schuzka-technicka.md, poznamka-architekt.md

### US-18: Nepodporované účty

Jako klient se sdíleným nebo eurovým účtem chci, aby se ukazatel nepočítal z nepodporovaných dat, abych nedostal zavádějící výsledek.

**Akceptační kritéria:**

- Sdílené účty se do výpočtu nezahrnují (schuzka-technicka.md, poznamka-architekt.md).
- Účty v jiné měně než CZK se do výpočtu nezahrnují (schuzka-technicka.md, poznamka-architekt.md).
- Otevřená otázka: co klient se sdíleným účtem uvidí a jak řešit spoluvlastníky, viz otázka 20 v epicu.
- Otevřená otázka: zda se u klienta s více běžnými účty počítají všechny, viz otázka 20 v epicu.

**Závislosti:** US-04.

**Zdroj:** schuzka-technicka.md, poznamka-architekt.md, ux-vyzkum.md

### US-19: Neúplná data ze zdrojových API

Jako klient chci, aby se mi při výpadku zdrojových dat nezobrazil chybný ukazatel, abych mohl výsledku věřit.

**Akceptační kritéria:**

- Při odpovědi 429 z Account Data API služba dodrží 60s cooldown (poznamka-architekt.md).
- Výpočet nepočítá s pending transakcemi, account-data-api vrací jen settled; jde o přijaté omezení (schuzka-technicka.md).
- Otevřená otázka: fallback strategie pro neúplná data (timeout, partial response) není definovaná, viz otázka 16 v epicu.

**Závislosti:** US-04, US-05, US-07.

**Zdroj:** poznamka-architekt.md, schuzka-technicka.md

### US-20: Žádost o lidský přezkum

Jako klient chci požádat o lidský přezkum výpočtu, abych mohl uplatnit své právo podle GDPR.

**Akceptační kritéria:**

- Klient má k dispozici možnost požádat o lidský přezkum výpočtu (email-zmena-priorit.md).
- Přezkum se týká výpočtu ukazatele, který je automatizované profilování podle GDPR čl. 22 (email-zmena-priorit.md).
- Otevřená otázka: kanál, proces a odpovědná role pro lidský přezkum, viz otázka 26 v epicu.

**Závislosti:** US-01.

**Zdroj:** email-zmena-priorit.md
