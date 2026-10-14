---
name: navrh-api
description: "Navrhne OpenAPI specifikaci z hotových user stories v outputs/<projekt>/ do api/<projekt>.openapi.yaml a zkontroluje ji validátorem. Postup agenta api-architekt."
argument-hint: "cesta ke stories"
---

# Návrh API

Na macOS a Linuxu spouštěj skripty přes `python3`, na Windows přes `python`.

## Postup

1. **Získej zadání** — přečti `outputs/<projekt>/<slug>.stories.md` a sekci „Otevřené otázky a rozpory“
   v epicu se stejným slugem. Do `docs/<projekt>/` se dívej jen tam, kde story cituje limit nebo omezení.

2. **Navrhni API** — do `api/<projekt>.openapi.yaml` podle [pravidel pro návrh API](../../instructions/api.instructions.md).
   Každá operace vychází z jedné story. Rozpory nerozhoduj, dotčená operace dostane `x-open-question`.

3. **Zkontroluj specifikaci** — spusť [validate_openapi.py](./scripts/validate_openapi.py) a oprav každý nález.
   Opakuj, dokud skript neskončí `OK`.

   ```sh
   python3 .github/skills/navrh-api/scripts/validate_openapi.py api/smart-savings.openapi.yaml
   ```

   Validátor hlídá jen to, že je soubor platné OpenAPI. Jestli API odpovídá stories, posuzuje člověk,
   třeba přes `/kontrola-dod`. Když skript hlásí, že chybí `openapi-spec-validator`, nic neinstaluj
   a řekni uživateli, ať spustí `pip install -r requirements.txt`.

## Kdy skill nepoužívat

- Na epic, user stories nebo jiný výstup než návrh API.
- Když by se mělo cokoli měnit v `docs/` nebo `outputs/`. Stories a epic jsou pro návrh API jen ke čtení.
