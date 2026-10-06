---
name: tvorba-epicu
description: "TODO: co skill dělá a kdy se má načíst. Popis je jediné, podle čeho se skill vybírá."
argument-hint: "projekt a název epicu"
---

# Tvorba epicu

<!-- Skill = postup nad jedním typem artefaktu. Deterministické kroky patří do skriptu. -->

## Postup

1. **Založ soubor** — spusť [novy-epic.sh](./scripts/novy-epic.sh) s projektem
   (název složky v `docs/`) a názvem epicu. Skript zkopíruje [šablonu](./assets/epic.template.md)
   do `outputs/<projekt>/<slug>.epic.md`.

   ```sh
   .github/skills/tvorba-epicu/scripts/novy-epic.sh financni-ukazatel "MVP finančního ukazatele"
   ```

2. TODO: co má agent udělat s podklady v `docs/`

3. TODO: jak vyplnit sekce šablony

4. TODO: jak zkontrolovat výsledek

## Kdy skill nepoužívat

- TODO
