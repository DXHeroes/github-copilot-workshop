# UX Research — Automatické spoření: co uživatelé skutečně chtějí

**Autor:** Lucie Š. (UX Research)\
**Datum:** 10. 6. 2025\
**Metoda:** Hloubkové rozhovory, 12 respondentů (6 žen, 6 mužů, věk 24–42, všichni aktivní uživatelé George)\
**Pozn.:** Výzkum proběhl PŘED zahájením projektu Smart Savings, jako součást širšího výzkumu spoření. Některé otázky jsme doplnili ad hoc, když jsme se dozvěděli o projektu.

------------------------------------------------------------------------

## Klíčová zjištění

### 1. Automatické převody vyvolávají nedůvěru

**8 z 12 respondentů** odmítlo koncept automatických mikro-převodů. Nejčastější reakce:

> „Nechci, aby mi aplikace sama přesouvala peníze. Co když zrovna potřebuju zaplatit něco nečekaného?“ (R3, žena, 31)
>
> „Automatické spoření jsem měl u [konkurenční banka]. Jednou mi to strhlo peníze den před splátkou hypotéky a dostal jsem se do debetu. Od té doby tomu nevěřím.“ (R7, muž, 38)
>
> „Doporučení, kolik si dát stranou, to by bylo fajn. Ale ať mi to neberou automaticky.“ (R11, žena, 27)

Pouze 2 respondenti byli otevřeni plné automatice. Zbylí 2 řekli „možná, pokud by to šlo kdykoliv vypnout“.

**Implikace:** Business předpoklad, že uživatelé chtějí „automatické mikro-převody“, neodpovídá datům. Model „doporučení + jedno kliknutí k převodu“ je výrazně preferovanější.

### 2. Uživatelé chtějí jednoduchost, ne gamifikaci

Na přímou otázku „Co by vás motivovalo šetřit víc?“ odpovědi byly:

| Motivátor                                                  | Počet zmínění |
|------------------------------------------------------------|---------------|
| Vidět, jak se blížím k cíli (progress bar)                 | 10            |
| Konkrétní vizualizace „za 3 měsíce budeš mít na dovolenou“ | 8             |
| Možnost nastavit si vlastní cíl                            | 7             |
| Přehled, kam peníze odchází                                | 6             |
| Odměny, badges, body                                       | 2             |
| Soutěžení s přáteli                                        | 1             |

**Implikace:** Gamifikace typu badges/odměny není priorita. Progress bar a vizualizace zbývající doby jsou silnější motivátory. Sociální funkce „spoří s přáteli“ nemá prakticky žádnou poptávku.

### 3. Frekvence a timing doporučení

- 7 respondentů preferuje doporučení **po výplatě** (ne fixně jednou týdně)
- 3 preferují doporučení **na konci měsíce** („když vidím, kolik mi zbylo“)
- 2 je to jedno

> „Nechci, aby mi appka psala v pondělí ráno, ať si dám stranou peníze. To je otravné. Ale po výplatě, kdy mám přehled, to dává smysl.“ (R5, muž, 34)

**Implikace:** Default frekvence „jednou týdně“ (jak navrhoval business owner) neodpovídá preferencím. Optimální by bylo doporučení vázané na příjem na účet.

### 4. Pojmenování a kategorie cílů

- Všech 12 respondentů chce vlastní pojmenování cílů
- Předdefinované šablony vnímají jako „inspiraci“, ne jako omezení
- 4 respondenti zmínili, že by chtěli k cíli přidat obrázek/ikonu (vizuální motivace)

### 5. Zrušení cíle a flexibilita

- 9 respondentů se ptalo: „A co když cíl zruším? Vrátí se mi peníze?“
- 6 respondentů zmínilo, že potřebují možnost „přestat šetřit na měsíc“ (pauza), ne nutně zrušit cíl
- 3 respondenti zmínili, že by chtěli změnit cílovou částku za běhu

> „Život se mění. V lednu chci šetřit na dovolenou, v březnu se mi rozbije auto a potřebuju peníze zpátky. Nesmí to být jako termíňák.“ (R9, žena, 36)

**Implikace:** Funkce „pauza“ a „zrušení s vrácením“ jsou pro uživatele kritické. Bez nich hrozí, že cíl nenastaví, protože se bojí, že k penězům nebudou mít přístup.

### 6. Edge cases z rozhovorů

**Sdílené účty:** 3 respondenti (páry) zmínili, že mají společný účet s partnerem. Ptali se, jestli mohou oba nastavit cíle na stejný účet a jestli se to nebude „bít“.

**Více účtů:** 2 respondenti mají u nás více běžných účtů (osobní + podnikatelský). Chtěli by vybrat, ze kterého účtu se spoří.

**Nedostatečný zůstatek:** Všech 12 se ptalo, co se stane, když na účtu nebude dost peněz. Očekávají, že systém jednoduše doporučení nepošle, ne že pošle doporučení na 0 Kč.

### 7. Přístupnost

Jeden respondent (R4, muž, 29) používá screen reader. Zmínil, že progress bary v George jsou aktuálně nepřístupné — screen reader je ignoruje. Pokud budeme stavět na stejné komponentě, musíme to opravit.

------------------------------------------------------------------------

## Doporučení pro design

1. **Preferovat model „doporučení + akce“** před automatickými převody

2. **Progress bar a vizualizace** jsou hlavní motivátory, ne badges
3. **Doporučení vázat na příjem** (detekce příchozí platby), ne na fixní den
4. **Umožnit pauzu a zrušení** cíle s jasnou komunikací, co se stane s penězi
5. **Řešit sdílené účty** minimálně upozorněním, že cíl nastavuje jeden z držitelů
6. **Opravit přístupnost** progress barů před launchem
