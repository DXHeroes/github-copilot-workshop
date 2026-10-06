---
description: "Zkontroluje hotový výstup (epic, user stories nebo návrh API) proti DoD projektu a vrátí nesplněné body. Nic neopravuje."
argument-hint: "cesta k výstupu"
agent: ask
tools: [read, search]
---

<!-- Prompt = vstupní bod. Kontrolu spouští člověk, když je výstup hotový, ne agent po každém kroku. -->

Zkontroluj `${input:soubor:outputs/smart-savings/mvp-uspornych-cilu.epic.md}` proti `docs/<projekt>/dod-sablona.md`.
Projekt je složka z cesty k souboru: `outputs/<projekt>/…` nebo `api/<projekt>.openapi.yaml`.

Podle typu souboru vezmi jen jednu sekci DoD:

- `*.epic.md` → „2. Epic“
- `*.stories.md` → „3. User Stories“
- `api/*.openapi.yaml` → „7. API specifikace“

Vrať tabulku se sloupci: bod DoD, splněno (ano / ne / částečně), důkaz (sekce nebo řádek výstupu).
U nesplněného bodu uveď, jestli informace chybí už v podkladech (pak je to otevřená otázka), nebo jen ve výstupu.
Nic neopravuj.
