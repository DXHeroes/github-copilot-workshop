# Emailový thread — Kickoff: Smart Savings

**Od:** Jana P. (PM)\
**Komu:** DL-SmartSavings-Core\
**Datum:** 2. 6. 2025, 9:14\
**Předmět:** Kickoff Smart Savings — shrnutí a další kroky

Ahoj všichni,

jak jsme si říkali na boardu minulý týden (viz přiložená prezentace — Tomáš K. ji sdílel ve složce na SharePointu, kdo nemá přístup, napište Katce), spouštíme nový projekt Smart Savings.

Cíl: dát uživatelům v mobilní aplikaci možnost nastavit si úsporné cíle a nechat appku, aby jim pomáhala šetřit. Představte si to jako kombinaci „automatického spoření“ a chytrých doporučení — appka by analyzovala příjmy a výdaje uživatele a podle toho navrhovala (a volitelně automaticky prováděla) mikro-převody na spořicí účet.

Základní parametry z boardu:

- MVP do konce Q3
- 5 přednastavených kategorií cílů (dovolená, elektronika, finanční polštář, auto, vzdělávání)
- Integrace s existujícím transakčním enginem
- AI model pro predikci „bezpečné“ částky k převodu (aby uživatel neskončil v mínusu)

Potřebuju od vás:

- Data Science: odhad, jaká data budeme potřebovat a jestli máme dost historických transakcí na natrénování modelu
- Backend: první pohled na to, jak se napojit na transakční engine a spořicí účty
- UX: návrh, jak to celé ukázat uživateli — onboarding, nastavení cíle, průběh spoření
- QA: připravit si představu o testovacích scénářích

Schůzku plánuju na pondělí 2. 6. odpoledne, pozvánka přijde dneska.

Díky, Jana

P.S. Ještě jedna věc, na kterou Tomáš na boardu hodně tlačil — musíme zajistit, že systém NIKDY nepřevede peníze, pokud by zůstatek na běžném účtu klesl pod 5 000 Kč (nebo individuálně nastavený limit). Tohle je absolutní podmínka, bez toho nespustíme. Prosím mějte to v hlavě od začátku.

------------------------------------------------------------------------

**Od:** Martin D. (Business Owner)\
**Komu:** Jana P.\
**Kopie:** DL-SmartSavings-Core\
**Datum:** 2. 6. 2025, 11:47\
**Předmět:** RE: Kickoff Smart Savings — shrnutí a další kroky

Jani,

díky za shrnutí. Pár věcí bych doplnil/upravil z business pohledu:

1) Těch 5 kategorií je málo. Z průzkumů víme, že uživatelé chtějí hlavně flexibilitu — ať si sami pojmenují cíl a nastaví částku. Klidně můžeme mít přednastavené šablony jako inspiraci, ale uživatel musí mít možnost vytvořit vlastní cíl s vlastním názvem a cílovou částkou. Tohle je pro nás klíčové, jinak to nebude mít dostatečnou adopci.

2) K tomu AI modelu — musíme to pojmout ambiciózněji. Nechceme jen „bezpečnou částku“. Chceme, aby model uživateli aktivně doporučoval, kolik by měl šetřit na základě jeho spending patterns. Třeba: „Tento měsíc jste utratil o 2 000 Kč míň za restaurace, chcete tu částku přesunout na cíl Dovolená?“ Tohle je to, co nás odliší od konkurence.

3) Gamifikace! Musíme tam mít nějaké odměny, badges, progress bary, milníky. Uživatel potřebuje motivaci. Bez gamifikace to bude jen další nudný spořicí nástroj, kterého se lidi za měsíc přestanou používat.

4) Ještě důležitá věc — musíme promyslet propojení s investičními produkty. Když uživatel naspoří cílovou částku, mohli bychom mu nabídnout, ať peníze investuje místo toho, aby ležely na spořáku. Ale to je možná fáze 2.

Jinak souhlasím s timeline, Q3 je realistické, pokud nezačneme přidávat scope.

Martin

------------------------------------------------------------------------

**Přeposlal:** Martin D.\
**Původní odesílatel:** Petr N. (Team Lead, FE)\
**Datum původní zprávy:** 2. 6. 2025, 10:22

> Martine, k tomu savings goalu — v George máme aktuálně omezení na max 3 aktivní „spořicí plány“ na jednoho uživatele (je to hardcoded v legacy backendu, nikdo neví proč). Jestli chceme víc, bude to vyžadovat změnu na core banking straně, a to je minimálně 4–6 týdnů jen na analýzu. Dej vědět, jestli to máme začít řešit hned, nebo jestli pro MVP stačí 3 cíle.
>
> A ještě — kluci z BE říkali, že transakční engine aktuálně nepodporuje „earmarking“ peněz na sub-účtech. Takže buď budeme muset použít reálné převody na separátní spořicí účet, nebo to nějak simulovat na UI úrovni. Obojí má svoje problémy.
