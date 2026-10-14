---
description: "Zformátuje markdown soubory přes mdformat. Hodí se na soubory, které píšeš nebo upravuješ sám, bez Copilota."
argument-hint: "soubory nebo složky"
---

Zformátuj markdown v: ${input:cesty:soubory nebo složky}

Když cesty chybí, zeptej se na ně.

Spusť stejný formátovač jako hook `formatovani-md` (na Windows `python` místo `python3`):

```sh
python3 .github/hooks/formatovani-md.py <cesty>
```

Skript přeskočí `docs/` a vypíše, které soubory změnil. Nahlas je uživateli. Obsah souborů ručně neupravuj.

Když skript hlásí, že chybí `mdformat`, nic neinstaluj a řekni uživateli, ať spustí `pip install -r requirements.txt`.
