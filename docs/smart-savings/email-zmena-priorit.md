# Emailový thread — Změna priorit + Compliance

**Od:** Tomáš K. (CTO)\
**Komu:** Jana P., Martin D.\
**Kopie:** DL-SmartSavings-Core, Eva M. (Legal)\
**Datum:** 16. 6. 2025, 8:03\
**Předmět:** Smart Savings — úprava priorit a timeline

Jano, Martine,

po včerejším executive review musím přeprioritizovat některé věci. Dostali jsme tlak ze strany regulátora na implementaci nových PSD2 požadavků (viz níže zpráva od Evy), což nám zabere kapacitu na backendu.

V praxi to znamená:

- Timeline pro Smart Savings se zkracuje — MVP musí být hotové do konce července, ne do konce Q3. Důvod: chceme to stihnout před zářijovým auditem, kde to chceme prezentovat jako příklad inovace.
- Backend kapacita bude omezenější, protože část týmu půjde na PSD2 compliance.
- Prosím zrevidujte scope a navrhněte, co je realisticky achievable v tomto kratším timeframe.

Nechci říkat „ořežte to na kost“, ale musíme být pragmatičtí. Core funkčnost spoření musí fungovat, zbytek se může dodělat v další fázi.

Ještě jedna věc — Eva dole zmiňuje, že automatické převody peněz BEZ explicitního souhlasu uživatele pro KAŽDOU jednotlivou transakci mohou být problém z pohledu PSD2. Prosím, tohle si prostudujte a na příští schůzce to chci mít vyřešené.

Tomáš

------------------------------------------------------------------------

**Přeposlal:** Tomáš K.\
**Původní odesílatel:** Eva M. (Legal & Compliance)\
**Datum původní zprávy:** 15. 6. 2025, 16:41\
**Předmět:** Regulatorní poznámky k projektu Smart Savings

Tomáši,

posílám shrnutí regulatorních bodů, které je potřeba zohlednit u projektu Smart Savings (nebo jak tomu říkáte — viděla jsem v JIRA i „Chytré spoření“ a „Auto-Save modul“, prosím sjednoťte název):

**PSD2 a automatické transakce:**

- Jakýkoliv automatický převod peněz z účtu klienta vyžaduje Strong Customer Authentication (SCA), pokud nejde o výjimku. Opakovaný převod na vlastní účet MŮŽE spadat pod výjimku pro „trusted beneficiaries“, ale POUZE pokud klient explicitně přidal svůj spořicí účet jako důvěryhodného příjemce.
- Jednorázový generální souhlas typu „souhlasím s automatickým spořením“ NESTAČÍ. Klient musí mít možnost každý jednotlivý automatický převod schválit NEBO musí existovat mechanismus standing order s jasně definovanými parametry (max. částka, frekvence).
- Alternativa: převody iniciované klientem na základě doporučení (klient klikne „ano, převeď“) — to je z regulatorního hlediska čisté.

**GDPR a analýza transakcí:**

- Pro analýzu spending patterns potřebujeme legitimní právní základ. Souhlas klienta je nejčistší cesta, ale musí být granulární — nelze to schovat do obecných podmínek.
- Pokud budeme data o transakcích zpracovávat pro účely ML modelu, musíme zajistit anonymizaci trénovacích dat. Není přípustné používat reálná klientská data pro trénink bez anonymizace.
- Retence dat: výsledky analýzy (doporučení, predikce) musí mít definovanou dobu retence. Nemůžeme je uchovávat neomezeně.

**Informační povinnost:**

- V UI musí být jasně uvedeno, že doporučení generuje AI/algoritmus, ne finanční poradce. Musíme se vyhnout tomu, aby klient měl dojem, že jde o personalizované finanční poradenství (to by vyžadovalo licenci).
- Disclaimer musí být viditelný, ne schovaný v podmínkách.

Pokud budete potřebovat detailnější analýzu k některému z bodů, dejte vědět. Ale tohle jsou hard constraints, které nelze obejít.

Eva

------------------------------------------------------------------------

**Od:** Jana P.\
**Komu:** Tomáš K.\
**Kopie:** Martin D.\
**Datum:** 16. 6. 2025, 9:28\
**Předmět:** RE: Smart Savings — úprava priorit a timeline

Tomáši,

rozumím situaci. Ale potřebuju jasno v jedné věci: když říkáš „core funkčnost spoření musí fungovat“ — myslíš tím:

a) Uživatel si nastaví cíl a RUČNĚ převádí peníze (žádná automatika)?\
b) Uživatel si nastaví cíl a dostává DOPORUČENÍ kolik převést (ale kliká sám)?\
c) Plně automatické mikro-převody (to, co jsme původně plánovali)?

Protože z toho, co píše Eva, vyplývá, že varianta c) je regulatorně komplikovaná. Varianta b) by byla výrazně jednodušší na implementaci i z compliance pohledu. Ale Martin na to asi nebude nadšený, protože chtěl „wow efekt“ s automatickým spořením.

Dej mi vědět, ať se podle toho zařídíme na pondělní schůzce.

Jana
