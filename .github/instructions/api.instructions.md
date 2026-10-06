---
description: "Konvence pro návrh API (OpenAPI). Použij při tvorbě nebo úpravě souborů v api/."
applyTo: "api/**"
---

# Pravidla pro návrh API

<!-- Instructions vázané na cestu: platí jen pro soubory v api/, jinde nezabírají kontext. -->

## Formát

- OpenAPI 3.1 v YAML, jeden soubor na projekt: `api/<projekt>.openapi.yaml`.
- Cesty jsou v množném čísle a kebab-case, s verzí na začátku: `/v1/savings-goals/{goalId}`.
- Každá operace má `operationId`, `summary` česky a `x-user-story` s ID story, ze které vychází.

## Chování

- HTTP metody podle významu: GET čte, POST zakládá, PATCH mění, DELETE ruší.
- Chybové odpovědi 400, 401, 403, 404, 409, 429 a 500 sdílí jedno schéma `Error`.
- Limity z podkladů (rate limity, počty, částky) jsou ve schématu nebo v popisu operace, včetně zdroje z `docs/<projekt>/`.
- Asynchronní operace vrací `202 Accepted` a odkaz na zdroj se stavem. Seznamy jsou stránkované.
- Identita klienta se bere z tokenu, ne z cesty ani z těla požadavku.

## Co nevymýšlet

- Co podklady nerozhodly, se nenavrhuje. Operace nebo pole dostane `x-open-question` s popisem rozporu a odkazem na epic.
