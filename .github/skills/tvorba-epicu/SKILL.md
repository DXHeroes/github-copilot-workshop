---
name: tvorba-epicu
description: "TODO: co skill dělá a kdy se má načíst. Popis je jediné, podle čeho se skill vybírá."
argument-hint: "projekt a název epicu"
---

# Tvorba epicu

<!-- Skill = postup nad jedním typem artefaktu. Deterministické kroky patří do skriptu. -->

Na macOS a Linuxu spouštěj skripty přes `python3`, na Windows přes `python`.

## Postup

1. **Založ soubor** — spusť [novy_epic.py](./scripts/novy_epic.py) s projektem
   (název složky v `docs/`) a názvem epicu. Skript zkopíruje [šablonu](./assets/epic.template.md)
   do `outputs/<projekt>/<slug>.epic.md`.

   ```sh
   python3 .github/skills/tvorba-epicu/scripts/novy_epic.py financni-ukazatel "MVP finančního ukazatele"
   ```

2. TODO: co má agent udělat s podklady v `docs/`

3. TODO: jak vyplnit sekce šablony

4. TODO: jak zkontrolovat výsledek

## Kdy skill nepoužívat

- TODO
