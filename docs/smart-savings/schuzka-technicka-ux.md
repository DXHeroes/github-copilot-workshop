# Záznam schůzky — Technická architektura + UX review

**Datum:** 4. 6. 2025, 10:00–11:45\
**Účastníci:** Jana P. (PM), Lucie Š. (UX), Radek F. (Data Scientist), Ondřej B. (IT analytik), Petr N. (Team Lead FE), Tomáš H. (Solution Architect), Jakub K. (BE vývojář)\
**Nepřítomen:** Martin D. (Business Owner) — omluven, je na konferenci

Jana: „Dobře, pojďme navázat na pondělní business schůzku. Dneska bychom chtěli vyřešit technickou architekturu a zároveň projít první UX návrhy od Lucie. Tomáši, můžeš začít s architekturou?“

Tomáš H.: „Jasně. Takže jsem se díval na to, jak se napojit na existující infrastrukturu. Základní architektura by byla: nový microservice — nazvěme ho savings-goal-service — který bude spravovat cíle, komunikovat s transakčním enginem pro převody, a s ML modelem pro doporučení.“

Jakub: „A ten savings-goal-service poběží kde? V Kubernetes clusteru vedle ostatních služeb?“

Tomáš H.: „Jo, standardně v K8s. REST API, PostgreSQL pro ukládání cílů a jejich stavu. Komunikace s transakčním enginem přes interní message bus.“

Ondřej: „Moment — přes message bus? Myslel jsem, že transakční engine má REST API.“

Tomáš H.: „Má, ale pro iniciaci transakcí se používá message bus. Je to asynchronní. Pošleš zprávu ‚proveď převod‘, a dostaneš callback, až je to hotové.“

Jakub: „A jak rychle ten callback přijde?“

Tomáš H.: „Záleží. Core banking systém zpracovává transakce v dávkách. Takže když pošleš request v 10 ráno, zpracuje se to typicky v nejbližším batch runu, což je… myslím, že jedou třikrát denně? Ráno, v poledne a večer. Musíme to ověřit s core banking týmem.“

Ondřej: „Takže uživatel klikne ‚převeď peníze‘ a reálně se to stane třeba až za 4 hodiny?“

Tomáš H.: „V nejhorším případě ano. Ale v UI to můžeme zobrazit jako ‚zpracovává se‘ a pak potvrdit, až to proběhne.“

Jana: „OK, tohle je důležitý bod. Na pondělní schůzce jsme se vlastně dohodli — já a Martin jsme to po schůzce řešili — že pro MVP půjdeme s modelem, kde uživatel dostane doporučení a SÁM se rozhodne, jestli převede. Žádné automatické převody. Takže ten flow bude: model vygeneruje doporučení → push notifikace uživateli → uživatel otevře appku → vidí doporučení → klikne ‚převést‘ nebo ‚ignorovat‘.“

Petr: „Počkej, takže žádné auto-spoření? Martin mluvil o automatických mikro-převodech…“

Jana: „Vím, ale po konzultaci s compliance to pro MVP neděláme. Automatické převody vyžadují SCA a celý consent flow, na to nemáme čas. Pro MVP jenom doporučení s jedním kliknutím.“

Petr: „Škoda, ale chápu. Takže z FE pohledu — jak to bude vypadat?“

Lucie: „Můžu navázat? Mám první wireframy. Takže hlavní obrazovky budou:

1. **Dashboard spoření** — přehled všech aktivních cílů, u každého progress bar, kolik zbývá, kolik dní do deadline
2. **Detail cíle** — podrobnější pohled, historie převodů na tento cíl, aktuální doporučení
3. **Nastavení nového cíle** — wizard se 3 kroky: pojmenování → cílová částka a datum → volba frekvence doporučení
4. **Doporučení k převodu** — karta, která se objeví na dashboardu a v notifikacích“

Petr: „A kolik typů cílů bude? Martin říkal, že si uživatel definuje vlastní.“

Lucie: „Ano. Uživatel napíše vlastní název, ale my mu nabídneme 8 šablon jako inspiraci — dovolená, auto, elektronika, finanční polštář, dárek, bydlení, vzdělávání, a jednu prázdnou ‚vlastní cíl‘.“

Ondřej: „Na businessu jsme říkali 5 šablon, ne 8.“

Jana: „Martin chtěl vlastní cíle. Šablony jsou jen inspirace. Kolik jich bude, to je UX rozhodnutí. Lucie, 8 je OK.“

Lucie: „Díky. Další věc — gamifikace. Mám návrh na progress bar s milníky na 25 %, 50 %, 75 % a 100 %. Při dosažení milníku animace + gratulační zpráva.“

Jana: „K tomu — na pondělní schůzce jsme gamifikaci zaparkovali s tím, že to musíme ověřit s compliance. Já jsem od té doby… No, upřímně, neměla jsem čas to řešit s právníky. Ale myslím si, že progress bar a milníky compliance problém nebudou. Badges a odměny bych ale pro MVP vynechala, to je pravděpodobnější, že narazí.“

Lucie: „Takže progress bar s milníky ano, badges ne?“

Jana: „Pro MVP ano. Pokud právníci neřeknou jinak.“

Ondřej: „To je ale dost vágní. Co když řeknou ne na celou gamifikaci?“

Jana: „Tak to vyřadíme. Ale nemyslím, že se to stane.“

Tomáš H.: „Můžu se vrátit k technice? Chtěl jsem probrat API design. Navrhuji tyhle endpointy:

- POST /savings-goals — vytvoření cíle
- GET /savings-goals — seznam cílů uživatele
- GET /savings-goals/{id} — detail cíle
- PUT /savings-goals/{id} — úprava cíle
- DELETE /savings-goals/{id} — smazání cíle
- POST /savings-goals/{id}/transfer — iniciace převodu
- GET /savings-goals/{id}/recommendations — získání aktuálního doporučení“

Jakub: „A co endpoint pro historii převodů na konkrétní cíl?“

Tomáš H.: „Jo, přidáme GET /savings-goals/{id}/transfers.“

Radek: „K tomu ML modelu — pro MVP bych navrhoval jednoduchý přístup. Podíváme se na průměrný měsíční příjem, odečteme pravidelné výdaje (inkasa, nájem, pojistky), a ze zbytku navrhneme X %. To X se bude lišit podle toho, jak konzervativní chceme být.“

Jana: „A jak to X určíme?“

Radek: „Pro začátek fixní procento — řekněme 10 % z disponibilního přebytku. Časem to personalizujeme.“

Petr: „A ten model bude běžet kde? V tom savings-goal-service, nebo jako separátní služba?“

Tomáš H.: „Separátní. recommendation-engine jako další microservice. Savings-goal-service si ho zavolá přes REST, když potřebuje doporučení.“

Radek: „Jo, to dává smysl. A data o transakcích uživatele — jak se k nim dostanu?“

Tomáš H.: „Přes transaction-history-api. Ale pozor — ten endpoint má rate limit. Myslím, že 100 requestů za minutu na API key. A vrací max 90 dní historie najednou.“

Radek: „100 za minutu? To když budu generovat doporučení pro tisíce uživatelů najednou, tak to nebude stačit.“

Tomáš H.: „Budeme muset generovat v dávkách. Nebo požádat o zvýšení limitu. Ale to je na core banking týmu.“

Ondřej: „Ještě k tomu limitu 3 cílů, o kterém psal Petr v emailu…“

Petr: „Jo, to je v legacy backendu. Entita ‚spořicí plán‘ má constraint max 3 na klienta. Nikdo neví, proč tam je. Mohlo to být business rozhodnutí z roku 2018.“

Tomáš H.: „Počkej — ale my budeme mít vlastní savings-goal-service. Spořicí cíl u nás je logická entita, ne nutně spořicí plán v core bankingu. Záleží, jak to implementujeme.“

Jakub: „Ale převod peněz musí jít na reálný spořicí účet, ne?“

Tomáš H.: „Nemusí. Můžeme to řešit jako ‚earmarking‘ — peníze zůstanou na běžném účtu, ale my si interně vedeme, kolik z nich je ‚alokováno‘ na který cíl.“

Petr: „To ale Martin na schůzce nechtěl. Říkal, že peníze se musí fyzicky přesunout.“

Jana: „Martin… říkal hodně věcí. Pro MVP si myslím, že earmarking je pragmatičtější řešení. Fyzický převod můžeme přidat ve fázi 2.“

Ondřej: „Ale to kompletně mění UX! Uživatel si myslí, že šetří, ale peníze jsou pořád na běžném účtu.“

Lucie: „To je problém. Z UX pohledu musí uživatel VIDĚT, že peníze ‚odešly‘. Jinak to nemá psychologický efekt. Celý koncept stojí na tom, že peníze jsou ‚pryč‘ z běžného účtu.“

Jana: „Hm, tak co takhle — pro MVP uděláme earmarking, ale v UI to zobrazíme jako ‚uspořeno‘. A pokud nám core banking tým řekne, že zvládnou zrušit limit 3 plánů, přejdeme na fyzické převody.“

Tomáš H.: „Tak to musíme nadesignovat tak, aby ta výměna šla udělat. Earnings service abstrahujeme za interface, za kterým může být earmarking nebo reálný převod.“

Jana: „Perfektní. Ondřeji, akční body?“

Ondřej: „Takže:

- Tomáš a Jakub: návrh architektury savings-goal-service + recommendation-engine, rozhodnutí earmarking vs. fyzický převod (závisí na odpovědi core banking)
- Radek: prototyp ML modelu na historických datech, ověřit dostupnost dat přes transaction-history-api
- Petr: zjistit, jestli core banking tým může zrušit limit 3 spořicích plánů a jaký je timeline
- Lucie: finální wireframy na základě dnešní diskuze — flow ‚doporučení → převod‘, gamifikace jen progress bar + milníky
- QA: zapojit na další schůzce, až budeme mít jasnější scope
- Jana: ověřit s compliance gamifikaci a consent pro analýzu transakcí“

Jana: „Ještě jedna věc — máme vlastně definovaný, jak budeme měřit úspěch? Martine bych se ptala na KPIs, ale není tu.“

Ondřej: „Martin zmiňoval na pondělku, že chce vidět ‚adopci‘ — kolik uživatelů si cíl nastaví a kolik ho dotáhne do konce.“

Jana: „OK, doplníme příště. Díky všem.“

**Poznámka Ondřeje po schůzce (přidáno 4. 6. večer):**

Mluvil jsem s Petrem po schůzce. Říkal, že ten limit 3 spořicích plánů je v databázi core bankingu jako CHECK constraint na tabulce. Změna by vyžadovala DB migraci na produkčním core banking systému, což má change window jednou za měsíc (vždy první víkend v měsíci). Nejbližší možný termín by byl 5.–6. 7. 2025, ale request musí být podaný minimálně 3 týdny předem, tzn. do 15. 6. Pokud to nestíháme, další window je až 2.–3. 8.

Taky jsem zjistil, že transakční engine opravdu jede v batch režimu — 3× denně (6:00, 12:00, 18:00). Real-time transakce jdou jen přes platební bránu (karetní transakce), ale interní převody mezi účty jedou vždy přes batch.
