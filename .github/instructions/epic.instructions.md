---
description: "Pravidla pro epic: struktura, zdroje a rozpory. Použij při tvorbě nebo úpravě epicu (*.epic.md)."
applyTo: "outputs/**/*.epic.md"
---

# Pravidla pro epic

## Struktura

- Epic má přesně sekce ze [šablony](../skills/tvorba-epicu/assets/epic.template.md), ve stejném pořadí a se stejnými nadpisy. Žádné sekce navíc.
- Soubor se jmenuje `outputs/<projekt>/<slug>.epic.md` a zakládá ho skript `novy_epic.py`, nikdy model.
- V hotovém epicu nezůstane žádný zástupný text ze šablony v hranatých závorkách.

## Práce se zdroji

- Fakta pochází jen z `docs/<projekt>/` daného epicu. Podklady druhého projektu se nepoužívají.
- Za každým faktem je v závorce zdrojový soubor, např. `(schuzka-business.md)`. Odkazuje se jen na soubory, které v `docs/<projekt>/` opravdu jsou.
- Co v podkladech není, je otevřená otázka, ne předpoklad.
- Rozpor se nerozhoduje. Do tabulky v sekci „Otevřené otázky a rozpory“ patří obě varianty, každá se svým zdrojem, a role, která rozhodne.

## Styl

- Česky, věcně, v odrážkách. Jedna odrážka = jedno tvrzení.
- Čísla, termíny a limity přesně podle podkladů, nezaokrouhlovat.
