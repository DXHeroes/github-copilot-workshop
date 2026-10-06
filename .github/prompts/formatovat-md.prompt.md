---
description: "Zformátuje markdown soubory přes mdformat. Hodí se na soubory, které píšeš nebo upravuješ sám, bez Copilota."
argument-hint: "soubory nebo složky"
agent: agent
tools: [execute]
---

<!-- Prompt = vstupní bod. Stejný formátovač jako hook formatovani-md, jen ho spouští člověk. -->

Zformátuj markdown v: ${input:cesty:soubory nebo složky, např. outputs/smart-savings/}

1. Zjisti, které soubory se změní. Na Windows použij `python` místo `python3`.

   ```sh
   python3 -m mdformat --check --number --exclude "docs/**" <cesty>
   ```

2. Zformátuj je stejným příkazem bez `--check`.

3. Nahlas, které soubory se změnily. Obsah souborů ručně neupravuj.

Když `mdformat` chybí, nic neinstaluj a řekni uživateli, ať spustí `pip install -r requirements.txt`.
