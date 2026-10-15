<!-- Vytvořeno: 2026-10-14 | Zdroj podkladů: docs/financni-ukazatel/ -->

# Epic: MVP finančního ukazatele

## 1. Popis

- Cílem je dát uživatelům v mobilní aplikaci jednoduchý přehled o jejich finančním zdraví (email-kickoff.md).
- Přehled tvoří jedno číslo na škále 0–100 doplněné vizuálními prvky a srozumitelným komentářem (email-kickoff.md); forma škály je v rozporu, viz bod 4 v sekci 10.
- Funkce má podpořit orientaci v osobních financích a motivovat k finančně zodpovědnému chování (email-kickoff.md).
- Ukazatel musí být čistě edukační a orientační a nesmí vypadat jako oficiální úvěrový rating nebo skóring (email-kickoff.md).
- Projekt spustil board, pracovní název je „Finanční ukazatel“ (email-kickoff.md).
- Název pro uživatele je „Finanční ukazatel“ bez slova „skóre“; rozhodnuto, viz bod 3 v sekci 10 (email-zmena-priorit.md).
- Termín MVP jsou 4 týdny od kickoffu; rozhodnuto, viz bod 1 v sekci 10 (email-zmena-priorit.md).
- V JIRA se používají názvy „Finanční ukazatel“, „Financial Health Score“ a „Finanční zdraví“; Legal žádá název sjednotit (email-zmena-priorit.md).
- Po executive review se kvůli AML požadavkům zkracuje termín a omezuje kapacita backendu; CTO žádá revizi scope na „core funkčnost“ (email-zmena-priorit.md).

## 2. Cílová skupina

- Podle Business Ownera všichni retail klienti s osobním účtem (schuzka-business.md).
- Sdílené účty nejsou v MVP podporované (schuzka-technicka.md, poznamka-architekt.md).
- Pro MVP jen účty v CZK, EUR účty odloženy na po MVP (schuzka-technicka.md, poznamka-architekt.md).
- Zobrazení klientům s krátkou transakční historií není rozhodnuto, viz body 11 a 12 v sekci 10 (schuzka-business.md, schuzka-technicka.md).
- Není určeno, zda se u klienta s více běžnými účty (např. osobní a podnikatelský) počítají všechny účty (ux-vyzkum.md).

## 3. Cíle / Byznysová hodnota

- Lepší orientace uživatelů v osobních financích (email-kickoff.md).
- Motivace k finančně zodpovědnému chování (email-kickoff.md).
- Přidaná hodnota podle Data Science: automatický výpočet za uživatele a jeho vizualizace (schuzka-business.md).
- Ukázat funkci na červnové boardové prezentaci jako příklad inovace (email-zmena-priorit.md).
- Business Owner očekává adopci a engagement (email-kickoff.md, schuzka-business.md).
- Business Owner chce odlišení od konkurence transparentností výpočtu (email-kickoff.md); rozsah transparentnosti je v rozporu, viz bod 7 v sekci 10.

## 4. Rozsah

### V rozsahu

- Rule-based výpočet ukazatele ze základních vstupů: poměr příjmů a výdajů, zůstatek relativně k měsíčním výdajům, úvěrové zatížení (poměr splátek k příjmům), trend (poznamka-architekt.md, schuzka-business.md); jen základní metriky, rozhodnuto, viz bod 2 v sekci 10.
- Váhy vstupů nejsou definované (poznamka-architekt.md).
- Výpočetní jádro je oddělený modul vyměnitelný za ML model ve fázi 2 (schuzka-technicka.md, poznamka-architekt.md).
- Architektura musí počítat s rozšířením o analýzu finančního chování ve fázi 2 (schuzka-business.md).
- Nová služba `financial-health-service` v Kotlinu, nasazená v K8s (schuzka-technicka.md, poznamka-architekt.md).
- Výsledky v Redis cache s TTL 24h a dávkovým přepočtem jednou denně, plánovaně 02:00–06:00 (poznamka-architekt.md); batch jednou denně, rozhodnuto, viz bod 10 v sekci 10.
- Bootstrap batch na předplnění cache před spuštěním, potřebuje min. 2 dny (schuzka-technicka.md, poznamka-architekt.md).
- Fallback při prázdné cache: placeholder „Načítáme váš ukazatel“ nebo prázdný kruh a on-demand výpočet na pozadí (schuzka-technicka.md).
- Endpoint `GET /users/{id}/financial-health` vrací hodnotu, barvu a textový popis (schuzka-technicka.md, poznamka-architekt.md).
- Endpoint `GET /users/{id}/financial-health/details` vrací rozpad faktorů (schuzka-technicka.md, poznamka-architekt.md).
- Interní endpoint `POST /financial-health/calculate` pro on-demand výpočet, není pro FE (schuzka-technicka.md, poznamka-architekt.md).
- Interní endpoint `GET /financial-health/batch/status` pro monitoring batch jobů (schuzka-technicka.md, poznamka-architekt.md).
- Veškerá validace na serveru, FE přebírá data beze změny (schuzka-technicka.md).
- Home screen: animovaný barevný kruh s hodnotou uprostřed (schuzka-technicka.md).
- Barevná pásma: zelená 70–100, oranžová 40–69, červená 0–39 (schuzka-technicka.md).
- Textace pod kruhem: „Jste na dobré cestě“, „Mírné riziko“, „Potřebuje pozornost“ (schuzka-technicka.md).
- Detail ukazatele po kliknutí: rozpad na příjmy, výdaje, zůstatek a úvěrové zatížení, u každého faktoru šipka nahoru/dolů a krátký komentář (schuzka-technicka.md).
- Onboarding při prvním zobrazení s vysvětlením, co ukazatel je a co není, včetně disclaimeru (schuzka-technicka.md).
- Granulární consent flow v aplikaci na FE i BE; zatím ho nikdo neplánoval (email-zmena-priorit.md).
- Disclaimer viditelný na hlavní obrazovce (email-zmena-priorit.md).

### Mimo rozsah

- Sdílené účty (schuzka-technicka.md, poznamka-architekt.md).
- Jiné měny než CZK (schuzka-technicka.md, poznamka-architekt.md).
- ML model, plánovaný až ve fázi 2 (schuzka-technicka.md, poznamka-architekt.md).
- Pending transakce; account-data-api vrací jen settled transakce (schuzka-technicka.md, poznamka-architekt.md).
- Napojení na payment gateway kvůli real-time autorizačním datům (schuzka-technicka.md).
- Analýza finančního chování, až ve fázi 2 (schuzka-business.md, email-zmena-priorit.md); rozhodnuto, viz bod 2 v sekci 10.
- Real-time aktualizace po každé platbě kartou (schuzka-business.md); rozhodnuto, viz bod 10 v sekci 10.
- Sdílení na sociálních sítích a s přáteli v aplikaci (email-kickoff.md, email-zmena-priorit.md); rozhodnuto, viz bod 6 v sekci 10.
- Kafka topic `account.balance.changed` architekt nedoporučuje pro kritické funkce (schuzka-technicka.md, poznamka-architekt.md).

## 5. Závislosti

- Account Data API: rate limit 200 req/min per API key, sdílený, ne per user (poznamka-architekt.md).
- Account Data API: při překročení limitu 429 a 60s cooldown (poznamka-architekt.md).
- Account Data API: průměrná odezva 800 ms, v peaku 3–5 s (pondělní rána, 1. pracovní den v měsíci) (poznamka-architekt.md, email-kickoff.md).
- Account Data API: max 90 dní historie v jednom callu, stránkování po 50 záznamech (poznamka-architekt.md).
- Žádost o zvýšení rate limitu podána, odpověď core bankingu nejdříve za 3 týdny (poznamka-architekt.md).
- Loan Service API: úvěrová data, nightly sync, data až 24 hodin stará (poznamka-architekt.md, schuzka-technicka.md).
- Loan Service API: rate limit 50 req/min (poznamka-architekt.md).
- Loan Service API je dostupné jen přes API gateway se service accountem s elevated permissions; vyřízení cca 2 týdny (poznamka-architekt.md).
- Kdo o service account požádá, není určeno (poznamka-architekt.md).
- Event `loan.payment.processed` neexistuje, Loan Service nemá event bus (poznamka-architekt.md).
- Kruhová komponenta v George není přístupná pro screen readery; kdo ji opraví, není určeno (poznamka-architekt.md, ux-vyzkum.md).
- Backend kapacita je omezená kvůli AML compliance (email-zmena-priorit.md).
- DPIA trvá minimálně 3–4 týdny a je podmínkou pro analýzu finančního chování (email-zmena-priorit.md); analýza chování je mimo MVP, viz bod 2 v sekci 10.
- Formální právní stanovisko k použití slova „skóre“ trvá 4–6 týdnů (email-zmena-priorit.md); slovo „skóre“ se nepoužije, viz bod 3 v sekci 10.
- QA připraví testovací scénáře v Gherkinu až po dodání API specifikace a výpočetních pravidel (schuzka-technicka.md).

## 6. Regulatorní a compliance požadavky

- Ukazatel musí být edukační a orientační a nesmí vypadat jako úvěrový rating nebo skóring (email-kickoff.md).
- Slovo „skóre“ v UI a komunikaci může být vykládáno jako úvěrový skóring regulovaný ČNB; Legal doporučuje neutrální termín „ukazatel“, „přehled“ nebo „index“ (email-zmena-priorit.md).
- Použití slova „skóre“ vyžaduje formální právní stanovisko, odhad 4–6 týdnů (email-zmena-priorit.md).
- Výpočet z transakčních dat je automatizované profilování podle GDPR čl. 22 (email-zmena-priorit.md).
- Vyžaduje se explicitní opt-in souhlas, ne předškrtnutý checkbox (email-zmena-priorit.md).
- Souhlas musí jít kdykoliv odvolat (email-zmena-priorit.md).
- Klient má právo na vysvětlení logiky výpočtu a na lidský přezkum (email-zmena-priorit.md).
- Souhlas musí být granulární: analýza transakcí, zobrazení ukazatele, notifikace; generální souhlas nestačí (email-zmena-priorit.md).
- Analýza finančního chování je plnohodnotné profilování a vyžaduje DPIA; bez dokončené DPIA ji nelze spustit (email-zmena-priorit.md).
- Legal doporučuje vysvětlit faktory a jejich obecný vliv, ne konkrétní váhy a vzorec, kvůli riziku gamingu (email-zmena-priorit.md).
- Sdílení finančních údajů mimo zabezpečený kanál banky Legal nedoporučuje implementovat (email-zmena-priorit.md).
- UI musí jasně uvádět, že ukazatel generuje algoritmus, ne finanční poradce, aby nešlo o poradenství vyžadující licenci MiFID (email-zmena-priorit.md).
- Disclaimer musí být viditelný na hlavní obrazovce, ne schovaný v podmínkách (email-zmena-priorit.md).
- Legal označuje uvedené body za hard constraints (email-zmena-priorit.md).
- Pro ML model ve fázi 2 nelze použít produkční data bez anonymizace (poznamka-architekt.md).
- Doba retence výsledků analýzy musí být definovaná, zatím není (poznamka-architekt.md).

## 7. Uživatelské příběhy

- [ ] US-01 Udělení granulárního souhlasu
- [ ] US-02 Odvolání souhlasu
- [ ] US-03 Výpočetní jádro ze základních metrik
- [ ] US-04 Načtení transakčních dat z Account Data API
- [ ] US-05 Načtení úvěrových dat z Loan Service API
- [ ] US-06 Denní dávkový přepočet do cache
- [ ] US-07 Monitoring dávkových jobů
- [ ] US-08 Bootstrap cache před spuštěním
- [ ] US-09 API pro základní údaje ukazatele
- [ ] US-10 API pro rozpad faktorů
- [ ] US-11 Fallback při prázdné cache
- [ ] US-12 Finanční ukazatel na home screenu
- [ ] US-13 Disclaimer na home screenu
- [ ] US-14 Detail ukazatele s rozpadem faktorů
- [ ] US-15 Onboarding při prvním zobrazení
- [ ] US-16 Přístupnost kruhové komponenty
- [ ] US-17 Klient s krátkou transakční historií
- [ ] US-18 Nepodporované účty
- [ ] US-19 Neúplná data ze zdrojových API
- [ ] US-20 Žádost o lidský přezkum

## 8. Rizika

| Riziko                                                                                                                                       | Dopad                 | Pravděpodobnost                                           | Zmírnění                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Batch pro 500k uživatelů trvá při limitu 200 req/min ~42 hodin (poznamka-architekt.md, schuzka-technicka.md)                                 | Neurčeno v podkladech | Vysoká, plyne z aktuálního limitu (poznamka-architekt.md) | Vyšší limit, nebo rozložení batche přes den s prioritou aktivních uživatelů (poznamka-architekt.md, schuzka-technicka.md) |
| Cold start: po nasazení nemá cache 100 % uživatelů (schuzka-technicka.md)                                                                    | Neurčeno v podkladech | Vysoká (schuzka-technicka.md)                             | Bootstrap batch, min. 2 dny (schuzka-technicka.md, poznamka-architekt.md)                                                 |
| On-demand výpočet při prázdné cache čeká až 5 s na account-data-api (schuzka-technicka.md)                                                   | Neurčeno v podkladech | Neurčeno v podkladech                                     | Placeholder a výpočet na pozadí (schuzka-technicka.md)                                                                    |
| Render home screenu na starších zařízeních (cca 30 % uživatelů) vzroste z 2,8 s přes 3,5 s, nad SLA (email-kickoff.md, schuzka-technicka.md) | Neurčeno v podkladech | Neurčeno v podkladech                                     | Performance analýza home screenu (schuzka-technicka.md)                                                                   |
| Loan data až 24 h stará, ukazatel nemusí odpovídat realitě a může podkopat důvěru (poznamka-architekt.md)                                    | Neurčeno v podkladech | Neurčeno v podkladech                                     | Neuvedeno v podkladech                                                                                                    |
| Chybějící pending transakce zkreslí výpočet (schuzka-technicka.md)                                                                           | Neurčeno v podkladech | Neurčeno v podkladech                                     | Architekt to bere jako přijaté omezení (schuzka-technicka.md)                                                             |
| Protichůdné signály vůči internímu loan scoringu s jinými váhami (schuzka-technicka.md, poznamka-architekt.md)                               | Neurčeno v podkladech | Neurčeno v podkladech                                     | Komunikace, že ukazatel není credit scoring, alespoň disclaimerem (poznamka-architekt.md, schuzka-technicka.md)           |
| Uživatelé se bojí vlivu ukazatele na úvěr nebo hypotéku, 4 z 12 respondentů (ux-vyzkum.md)                                                   | Neurčeno v podkladech | Neurčeno v podkladech                                     | Jasný a opakovaný disclaimer, že ukazatel neovlivňuje bankovní rozhodnutí (ux-vyzkum.md)                                  |
| Marketing chystá kampaň „Vaše finanční skóre“ a o zákazu slova „skóre“ neví (poznamka-architekt.md)                                          | Neurčeno v podkladech | Neurčeno v podkladech                                     | Urgentně vyřešit naming (poznamka-architekt.md, email-zmena-priorit.md); název rozhodnut, viz bod 3 v sekci 10            |
| Riziko licence ČNB při vnímání jako credit scoring (email-zmena-priorit.md)                                                                  | Neurčeno v podkladech | Neurčeno v podkladech                                     | Nepoužívat slovo „skóre“, nebo právní stanovisko (email-zmena-priorit.md); rozhodnuto nepoužívat, viz bod 3 v sekci 10    |
| Consent flow nikdo neplánoval, práce na FE i BE (email-zmena-priorit.md)                                                                     | Neurčeno v podkladech | Neurčeno v podkladech                                     | Neuvedeno v podkladech                                                                                                    |
| Zkrácený termín a omezená BE kapacita kvůli AML (email-zmena-priorit.md)                                                                     | Neurčeno v podkladech | Neurčeno v podkladech                                     | Revize scope podle CTO (email-zmena-priorit.md); rozhodnuto jen základní metriky, viz bod 2 v sekci 10                    |
| Nepřístupná kruhová komponenta pro screen readery (ux-vyzkum.md, poznamka-architekt.md)                                                      | Neurčeno v podkladech | Neurčeno v podkladech                                     | Opravit přístupnost před launchem (ux-vyzkum.md)                                                                          |
| Ukazatel může být „nespravedlivý“ v nákladných měsících (sezónnost) (ux-vyzkum.md)                                                           | Neurčeno v podkladech | Neurčeno v podkladech                                     | Messaging pro sezónní výkyvy (ux-vyzkum.md)                                                                               |
| Fallback při neúplných datech z API (timeout, partial response) není definovaný (poznamka-architekt.md)                                      | Neurčeno v podkladech | Neurčeno v podkladech                                     | Neuvedeno v podkladech                                                                                                    |

## 9. Metriky úspěchu

- Metriky úspěchu ani cílové hodnoty v podkladech nejsou definované; jde o otevřenou otázku, viz bod 22 v sekci 10.
- Podklady zmiňují bez cílové hodnoty adopci a engagement (email-kickoff.md, schuzka-business.md).
- Render home screenu nesmí překročit SLA; hodnota SLA v podkladech není uvedená (email-kickoff.md).
- Odezva API z Redis cache pod 100 ms je odhad architekta, ne schválená metrika (schuzka-technicka.md).

## 10. Otevřené otázky a rozpory

| #   | Téma                                                               | Varianta A (zdroj)                                                                                                                                 | Varianta B (zdroj)                                                                                                                                                               | Kdo rozhodne                                                                                                                                                               |
| --- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Termín MVP — ROZHODNUTO: varianta B                                | MVP do 6 týdnů, tj. polovina června; Business Owner to považuje za realistické (email-kickoff.md)                                                  | MVP do 4 týdnů od kickoffu kvůli červnovému boardu a AML (email-zmena-priorit.md)                                                                                                | Rozhodnuto 14. 10. 2026 (zadání člověka, ne podklady): varianta B, 4 týdny od kickoffu; vlastník CTO (Tomáš K.)                                                            |
| 2   | Rozsah výpočtu, „core funkčnost“ — ROZHODNUTO: varianta B          | Zahrnout analýzu finančního chování: pravidelnost spoření, impulzivní výdaje, finanční polštář (email-kickoff.md, schuzka-business.md)             | Pro MVP jen základní metriky, chování ve fázi 2; chování vyžaduje DPIA 3–4 týdny (schuzka-business.md, email-zmena-priorit.md)                                                   | Rozhodnuto 14. 10. 2026 (zadání člověka, ne podklady): varianta B, jen základní metriky, analýza chování ve fázi 2; vlastník CTO (Tomáš K.) s Business Ownerem (Martin D.) |
| 3   | Název „skóre“ — ROZHODNUTO: varianta B                             | „Vaše finanční skóre“, podle Business Ownera po dohodě s CMO definitivní, marketing chystá kampaň (schuzka-business.md, poznamka-architekt.md)     | Slovo „skóre“ nepoužívat, použít „ukazatel“, „přehled“ nebo „index“; jinak právní stanovisko 4–6 týdnů (email-zmena-priorit.md)                                                  | Rozhodnuto 14. 10. 2026 (zadání člověka, ne podklady): varianta B, „Finanční ukazatel“ bez slova „skóre“; vlastník Legal & Compliance (Eva M.) s Business Ownerem a CMO    |
| 4   | Forma škály                                                        | Škála 0–100 s granularitou (email-kickoff.md, schuzka-business.md)                                                                                 | 3–5 úrovní nebo semafor, 8 z 12 respondentů mělo se škálou 0–100 problém (ux-vyzkum.md); škála 0–100 a barvy můžou být vnímány jako hodnocení (email-zmena-priorit.md)           | Business Owner (Martin D.); PM určila 0–100 jako výchozí do ověření UX (schuzka-business.md)                                                                               |
| 5   | Frekvence notifikací                                               | Denní push s aktuální hodnotou a změnou oproti včerejšku (email-kickoff.md, schuzka-business.md)                                                   | Max. jednou týdně podle PM (schuzka-business.md); událostně při výrazné změně, denně nechce nikdo z respondentů (ux-vyzkum.md)                                                   | Business Owner (Martin D.) s PM (Jana P.)                                                                                                                                  |
| 6   | Sociální sdílení — ROZHODNUTO: varianta B                          | Umožnit sdílení na sociální sítě a s přáteli v aplikaci, marketing na tom pracuje (email-kickoff.md, schuzka-business.md)                          | Neimplementovat: Legal ho označuje za výrazně problematické (email-zmena-priorit.md), 10 z 12 respondentů by nesdílelo nikdy (ux-vyzkum.md)                                      | Rozhodnuto 14. 10. 2026 (zadání člověka, ne podklady): varianta B, bez sdílení; vlastník Business Owner (Martin D.) s Legal & Compliance (Eva M.)                          |
| 7   | Transparentnost výpočtu                                            | Kompletní vzorec a váhy faktorů (email-kickoff.md)                                                                                                 | Jen faktory a jejich obecný vliv, bez vah a vzorce (email-zmena-priorit.md, ux-vyzkum.md)                                                                                        | Business Owner (Martin D.) s Legal & Compliance (Eva M.)                                                                                                                   |
| 8   | Tón messagingu                                                     | Upřímně sdělit i špatný stav (schuzka-business.md)                                                                                                 | Vždy motivační, nikdy negativní, jak se dohodlo na boardu (email-kickoff.md, schuzka-business.md); výzkum ukazuje podporu obou přístupů a nejvíc konkrétních tipů (ux-vyzkum.md) | Business Owner (Martin D.) s PM (Jana P.); UX navrhuje A/B test (schuzka-business.md)                                                                                      |
| 9   | Viditelnost na home screenu                                        | Vždy viditelné na home screenu, ne v menu (schuzka-business.md)                                                                                    | Možnost ukazatel z home screenu skrýt (ux-vyzkum.md)                                                                                                                             | Business Owner (Martin D.)                                                                                                                                                 |
| 10  | Aktualizace ukazatele — ROZHODNUTO: varianta B                     | Real-time po každé platbě kartou (schuzka-business.md)                                                                                             | Batch jednou denně, uživatel vidí včerejší stav (schuzka-technicka.md, poznamka-architekt.md)                                                                                    | Rozhodnuto 14. 10. 2026 (zadání člověka, ne podklady): varianta B, batch jednou denně; vlastník Business Owner (Martin D.) se Solution Architectem (Tomáš H.)              |
| 11  | Klienti s krátkou historií                                         | Zobrazit všem retail klientům (schuzka-business.md); omezená verze ze zůstatku a příjmů s disclaimerem (schuzka-business.md, schuzka-technicka.md) | Raději nezobrazit nic než nepřesné číslo (schuzka-technicka.md)                                                                                                                  | PM (Jana P.) s Business Ownerem; varianty připraví Data Scientist a UX (schuzka-technicka.md)                                                                              |
| 12  | Minimální délka historie                                           | Min. 3 měsíce, ideálně 6 (schuzka-business.md)                                                                                                     | Min. 6 měsíců (schuzka-technicka.md, poznamka-architekt.md)                                                                                                                      | Data Scientist (Radek F.)                                                                                                                                                  |
| 13  | Kdo definuje váhy výpočtu                                          | Business (schuzka-technicka.md, poznamka-architekt.md)                                                                                             | Data Science, případně společně (schuzka-technicka.md, poznamka-architekt.md)                                                                                                    | Business Owner (Martin D.), čeká se na něj (poznamka-architekt.md)                                                                                                         |
| 14  | Otevřená otázka: sjednocení interního názvu projektu               | Finanční ukazatel / Financial Health Score / Finanční zdraví (email-zmena-priorit.md)                                                              | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech; požadavek vznesla Legal (email-zmena-priorit.md)                                                                                                   |
| 15  | Otevřená otázka: real-time výpočet vs. performance home screenu    | Řešit performance a cachování od začátku (email-kickoff.md)                                                                                        | Pro MVP workaround (email-kickoff.md)                                                                                                                                            | Business Owner (Martin D.); Team Lead FE se ptá jeho (email-kickoff.md)                                                                                                    |
| 16  | Otevřená otázka: fallback při neúplných datech z API               | Strategie není definovaná (poznamka-architekt.md)                                                                                                  | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 17  | Otevřená otázka: kdo požádá o service account pro loan-service-api | Neřešeno (poznamka-architekt.md)                                                                                                                   | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 18  | Otevřená otázka: kdo opraví přístupnost kruhové komponenty         | Není určeno (poznamka-architekt.md)                                                                                                                | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 19  | Otevřená otázka: monitoring přesnosti modelu                       | DS tým nemá kapacitu na průběžný monitoring (poznamka-architekt.md)                                                                                | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 20  | Otevřená otázka: více účtů a joint owners                          | Nejasné, zda se počítají všechny účty klienta (ux-vyzkum.md) a jak řešit spoluvlastníky (poznamka-architekt.md)                                    | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 21  | Otevřená otázka: segmentace vah podle věku                         | Data Scientist zmiňoval jiné vzorce u mladších a starších klientů, segmentace chybí (poznamka-architekt.md)                                        | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 22  | Otevřená otázka: metriky úspěchu                                   | Cílové metriky a hodnoty nejsou definované (email-kickoff.md, schuzka-business.md)                                                                 | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 23  | Otevřená otázka: doba retence výsledků analýzy                     | Zatím nespecifikováno (poznamka-architekt.md)                                                                                                      | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 24  | Otevřená otázka: konkrétní texty disclaimeru a onboardingu         | Připravuje UX, finální texty nejsou (schuzka-technicka.md)                                                                                         | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 25  | Otevřená otázka: hodnota SLA pro render home screenu               | Podklady uvádějí jen, že 3,5 s je nad SLA (email-kickoff.md)                                                                                       | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 26  | Otevřená otázka: proces lidského přezkumu                          | Klient má právo na lidský přezkum, kanál a proces nejsou popsané (email-zmena-priorit.md)                                                          | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 27  | Otevřená otázka: výsledek pro nulový zůstatek a klienta s exekucí  | QA je uvádí jako edge cases, očekávané chování není popsané (schuzka-technicka.md)                                                                 | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |
| 28  | Otevřená otázka: co vidí klient bez souhlasu nebo po jeho odvolání | Souhlas je opt-in a odvolatelný, zobrazení bez souhlasu není popsané (email-zmena-priorit.md)                                                      | Neuvedeno v podkladech                                                                                                                                                           | Neuvedeno v podkladech                                                                                                                                                     |

## 11. Poznámky a další informace

- Dopad a pravděpodobnost rizik v sekci 8 podklady většinou nehodnotí, proto jsou uvedeny jako neurčené.
- Rozhodnutí k rozporům 1, 2, 3, 6 a 10 dodal člověk 14. 10. 2026 v zadání; v podkladech v docs/financni-ukazatel/ zapsaná nejsou.
- CTO chce mít regulatorní body kolem automatizovaného profilování vyřešené do příští schůzky (email-zmena-priorit.md).
- Pro ML model ve fázi 2 chybí ETL pipeline na anonymizaci, odhad 4–6 týdnů jen na pipeline (poznamka-architekt.md).
- Edge cases pro QA: minimální historie, nulový zůstatek, klient s exekucí, sdílený účet (schuzka-technicka.md).
- UX výzkum: 12 respondentů, věk 24–42, všichni aktivní uživatelé George (ux-vyzkum.md).
- Respondenti nejvíc oceňují konkrétní akční tipy, 9 z 12 (ux-vyzkum.md).
- Poznámka architekta má status „draft, nekompletní“ (poznamka-architekt.md).
- Zápis z business schůzky dělaný za běhu, nemusí být doslovný; požadavek na real-time a „definitivní“ název zazněl až neformálně po schůzce (schuzka-business.md).
