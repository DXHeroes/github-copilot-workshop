# Záznam schůzky — Business requirements Smart Savings

**Datum:** 2. 6. 2025, 14:00–15:20\
**Účastníci:** Jana P. (PM), Martin D. (Business Owner), Lucie Š. (UX), Radek F. (Data Scientist), Ondřej B. (IT analytik), Karolína N. (QA)\
**Zapisovatel:** Ondřej B. (pozn.: zápis dělaný za běhu, některé části nemusí být doslovné)

------------------------------------------------------------------------

Jana: „Tak, díky že jste dorazili. Cíl dnešní schůzky — projít základní business požadavky na Smart Savings a odejít s jasnou představou, co vlastně děláme. Martin, chceš začít?“

Martin: „Jasně. Takže základní myšlenka — chceme, aby si lidi v appce nastavili spořicí plán, řekli kolik chtějí našetřit a do kdy, a my jim s tím budeme pomoáhat. Ideálně automaticky.“

Jana: „Počkej, ještě než se dostaneme k detailům — měli bychom definovat, jaký problém vlastně řešíme. Máme data o tom, kolik uživatelů aktuálně spoří?“

Martin: „Máme. Z posledního průzkumu vyplývá, že 65 % našich klientů říká, že by chtěli víc šetřit, ale nemají disciplínu. Jenom 12 % aktivně používá spořicí účet. Zbytek má peníze na běžném účtu a utrácí všechno.“

Radek: „To je zajímavé. Máme ty data segmentovaná podle věku? Protože u mladších uživatelů bych čekal jiný pattern než u starších.“

Martin: „Nemám to tady, ale můžu to dodat. Nicméně cílová skupina jsou primárně 25–40 let, digitálně aktivní, používají mobilní banking minimálně 3x týdně.“

Ondřej: „OK, a jakou funkčnost přesně chceme v MVP? Protože z Janina emailu jsem pochopil, že 5 kategorií cílů, ale ty říkáš, Martine, že uživatel si má definovat vlastní?“

Martin: „Vlastní. Jednoznačně. Těch 5 kategorií z boardové prezentace bylo jenom jako příklad. Uživatel musí mít svobodu. Chci, aby si mohl napsat ‚Nový iPhone‘, ‚Dovolená Řecko‘, cokoliv.“

Jana: „OK, ale to zvyšuje složitost na FE i BE. Když máme předdefinované kategorie, je to jednodušší pro UI, pro reporting, pro model…“

Martin: „Vím. Ale bez toho to nebude mít adopci. Uživatelé nesnáší, když jim dictujete, na co mají šetřit.“

Lucie: „Souhlasím s Martinem. Z UX pohledu — přednastavené šablony jako inspirace ano, ale musí být možnost custom cíle. Jinak to lidi odradí.“

Jana: „Fajn, zapíšeme to jako požadavek. Tak pojďme dál — jak vlastně to spoření bude fungovat? Martin, ty jsi v emailu zmiňoval automatické mikro-převody.“

Martin: „Jo, přesně. Představ si to takhle — uživatel nastaví cíl, třeba ‚Dovolená, 30 000 Kč, do prosince‘. Appka se podívá na jeho příjmy a výdaje, a navrhne: ‚Tento týden můžeš bezpečně převést 500 Kč.‘ A když uživatel souhlasí, převede se to automaticky.“

Radek: „Takže model by měl predikovat ‚safe amount to save‘? Na základě čeho? Historických transakcí?“

Martin: „Ano, historické transakce, pravidelné příjmy, nadcházející předpokládané výdaje…“

Radek: „To je poměrně komplexní. Pro začátek bychom mohli jít s jednodušším přístupem — podívat se na průměrný zůstatek za posledních X měsíců a navrhnout procento z přebytku. Nemusíme hned predikovat budoucí výdaje.“

Jana: „Souhlasím. Pro MVP jednodušší model, iterujeme.“

Martin: „Ale nesmí to být hloupé. Nesmí to navrhnout, ať si převede peníze den před tím, než mu přijde inkaso za hypotéku.“

Radek: „No to je právě ten problém. Abychom tohle zachytili, musíme znát pravidelné platby. A to je vlastně ta složitější verze.“

Jana: „OK, tohle rozhodneme na technické schůzce. Teď pojďme k dalšímu bodu — gamifikace. Martin, ty jsi to zmiňoval v emailu.“

Martin: „Ano, trvám na tom. Musíme tam mít gamifikaci. Progress bar je samozřejmost, ale chci i milníky, badges, třeba ‚Ušetřil jsi prvních 1 000 Kč!‘ nebo ‚10 převodů za sebou!‘ Motivace je klíčová.“

Lucie: „Z UX výzkumů víme, že gamifikace funguje u finančních aplikací, ale musíme být opatrní. Nesmí to vypadat infantilně — jsme banka, ne Duolingo.“

Martin: „Jasně, ale to je záležitost designu, ne konceptu. Prostě to udělejme elegantně.“

Jana: „A co z compliance pohledu? Nemůže nám někdo vyčíst, že ‚manipulujeme‘ uživatele, aby šetřili víc, než je pro ně rozumné?“

Martin: „To je absurdní. Pomáháme jim šetřit. To přece nemůže být problém.“

Jana: „No, nevím. Radši bych to ověřila s právníky. Ale OK, gamifikaci zatím zapíšeme jako požadavek s tím, že ji musíme validovat s compliance.“

Ondřej: „Ještě mě napadá — Martin, ty jsi zmiňoval propojení s investicemi. Je to v scope MVP?“

Martin: „Nene, to je fáze 2. Pro MVP to úplně vynechte. Ale mějte to v hlavě, ať to pak půjde snadno doplnit.“

Ondřej: „Rozumím. A co notifikace? Jak budeme uživateli dávat vědět, že má doporučení k převodu?“

Martin: „Push notifikace v appce. Jednou týdně shrnutí, jak se mu daří se spořením, a když má doporučení k převodu.“

Lucie: „Jednou týdně? To je moc málo. Nebo moc. Záleží na uživateli. Měli bychom dát možnost si frekvenci nastavit.“

Martin: „OK, nastavitelná frekvence. Ale default jednou týdně.“

Jana: „Dobře, pojďme k dalšímu tématu. Martin, ty jsi mi včera volal s nápadem na sociální funkci. Chceš to představit?“

Martin: „Aha jo! Takže nápad je tenhle — ‚Spoří s přáteli‘. Uživatel může vytvořit sdílený cíl, třeba ‚Společná dovolená‘ a pozvat přátele, kteří taky spoří na stejný cíl. Viděli by vzájemný progress, mohli by se motivovat…“

Lucie: „To je zajímavý koncept, ale implementačně to je obrovské. Sdílení dat mezi uživateli, notifikace, správa přístupů…“

Ondřej: „A privacy? Chceme, aby uživatelé viděli, kolik jiní spoří?“

Martin: „No, jen progress v procentech, ne absolutní čísla.“

Jana: „Martine, tohle je hezký nápad, ale to je na celý samostatný projekt. Doporučuju tohle úplně vyřadit ze scope. I z fáze 2.“

Martin: „No ale… alespoň bychom to mohli mít jako ‚budoucí feature‘ v roadmapě.“

Jana: „Roadmapa ano. Ale neřešíme teď. Vraťme se k MVP.“

Martin: „Fajn. Ale chtěl bych, aby architektura počítala s tím, že to jednou budeme mít.“

Jana: „To je rozumné, zapíšeme. Ondřeji, akční body?“

Ondřej: „Moment, ještě jsem chtěl — budeme v MVP podporovat jenom korunové účty, nebo i eurové?“

Jana: „Jen korunové pro MVP.“

Martin: „A jen osobní účty, ne firemní.“

Ondřej: „Jasné. A ještě — kolik cílů může mít uživatel najednou? Petr z FE psal, že v George je limit 3 spořicí plány.“

Jana: „Hmm, to budeme muset ověřit na technické schůzce. Jestli je to backend omezení, tak to asi pro MVP neobejdeme.“

Martin: „Cože? 3 cíle? To je málo. Kdo má jen 3 věci, na které šetří?“

Jana: „No tak to eskalujeme, ale nemůžu slíbit, že to pro MVP vyřešíme. Pojďme to parkovat.“

Martin: „Dobře, ale zapište to jako riziko.“

Ondřej: „OK, mám to. Takže shrnu akční body:

- Data Science: návrh modelu pro predikci bezpečné částky (Radek)
- UX: návrh user flow — nastavení cíle, doporučení k převodu, gamifikace (Lucie)
- IT analýza: ověřit limit 3 cílů v legacy backendu, připravit seznam API, které budeme potřebovat (Ondřej)
- QA: začít přemýšlet o test scénářích (Karolína)
- PM: validovat gamifikaci s compliance (Jana)“

Jana: „Perfektní. Technická schůzka je ve středu, tam probereme architekturu. Díky všem.“

[pozn. zapisovatele: Po formálním ukončení schůzky ještě probíhala neformální diskuze mezi Janou a Martinem. Jana říkala, že podle ní by mělo MVP fungovat tak, že uživatel dostane jen DOPORUČENÍ a sám se rozhodne, jestli převede, žádné automatické převody. Martin s tím nesouhlasil, ale Jana argumentovala regulací. Nevím, jestli se na něčem dohodli.]
