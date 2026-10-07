---
description: "Formát user stories. Použij při tvorbě nebo úpravě souboru s user stories (*.stories.md)."
applyTo: "outputs/**/*.stories.md"
---

# Pravidla pro user stories

## Struktura

- Soubor se jmenuje `outputs/<projekt>/<slug>.stories.md`, stejný slug jako epic, ze kterého vychází.
- Každá story začíná nadpisem `### US-01: Název` s číslem ve tvaru `US-` a dvou a víc číslic. Čísla odpovídají seznamu v epicu.
- Pod nadpisem je věta „Jako [role] chci [akce], abych [hodnota].“, pak **Akceptační kritéria:** (alespoň 2 odrážky), **Závislosti:** a **Zdroj:**.

## Obsah

- Story je nezávislá, testovatelná a zvládnutelná v jednom sprintu. Větší story se rozdělí.
- Chybové stavy a edge cases z podkladů mají vlastní story, nebo akceptační kritérium.
- Zdroj je soubor z `docs/<projekt>/`. Story bez zdroje nevzniká.
- Kde podklady o story nerozhodly, patří do akceptačních kritérií „Otevřená otázka:“ s odkazem na rozpor v epicu.
