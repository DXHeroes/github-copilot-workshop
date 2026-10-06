---
description: "Projde podklady projektu jako oponent a najde rozpory, nepodložená tvrzení a chybějící informace."
argument-hint: "projekt"
agent: ask
tools: [read, search]
---

<!-- Prompt = vstupní bod. Adversarial reading: hledá, co nesedí, ne shrnutí. -->

Přečti všechny podklady v `docs/${input:projekt:smart-savings nebo financni-ukazatel}/` a hledej, co nesedí. Nic neshrnuj a nic nerozhoduj.

Vrať tabulku se sloupci: téma, tvrzení A (soubor), tvrzení B (soubor), proč je to problém, kdo by měl rozhodnout. Pod ni dva seznamy:

- tvrzení, která nemají oporu v žádném jiném podkladu,
- informace, které pro návrh chybí úplně.
