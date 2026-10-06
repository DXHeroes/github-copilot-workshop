---
name: tvorba-epicu
description: "Založí epic skriptem ze šablony, vyplní ho z podkladů v docs/<projekt>/ a zkontroluje ho validátorem. Použij, když má vzniknout nebo se upravit epic (*.epic.md)."
argument-hint: "projekt a název epicu"
---

# Tvorba epicu

<!-- Skill = postup nad jedním typem artefaktu. Deterministické kroky patří do skriptu. -->

Na macOS a Linuxu spouštěj skripty přes `python3`, na Windows přes `python`.

## Postup

1. **Založ soubor** — spusť [novy-epic.sh](./scripts/novy-epic.sh) s projektem
   (název složky v `docs/`) a názvem epicu. Skript zkopíruje [šablonu](./assets/epic.template.md)
   do `outputs/<projekt>/<slug>.epic.md`.

   ```sh
   .github/skills/tvorba-epicu/scripts/novy-epic.sh smart-savings "MVP úsporných cílů"
   ```

2. **Získej fakta** — přečti všechny soubory v `docs/<projekt>/` kromě `dod-sablona.md`.
   Podklady jiného projektu nečti.

3. **Vyplň sekce** — každou sekci šablony podle [pravidel pro epic](../../instructions/epic.instructions.md).
   Rozpory jdou do tabulky v sekci „Otevřené otázky a rozpory“, nerozhoduj je.

4. **Zkontroluj strukturu** — spusť [validate_epic.py](./scripts/validate_epic.py) a oprav každý nález.
   Opakuj, dokud skript neskončí `OK`.

   ```sh
   python3 .github/skills/tvorba-epicu/scripts/validate_epic.py outputs/smart-savings/mvp-uspornych-cilu.epic.md
   ```

   Validátor hlídá jen strukturu: sekce, zbylé zástupné texty, prázdné tabulky a existenci citovaných
   zdrojů. Jestli je obsah správně, posuzuje člověk, třeba přes `/kontrola-dod`.

## Kdy skill nepoužívat

- Na user stories, návrh API nebo jiný výstup než epic.
- Když by se mělo cokoli měnit v `docs/`. Podklady jsou jen ke čtení.
