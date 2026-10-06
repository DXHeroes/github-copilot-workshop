# ⭐️ GitHub Copilot workshop — demo repo

Ukázka, jak si postavit vlastní „AI framework" nad GitHub Copilotem. Celé demo řeší
**jeden use case: vytvoření epicu z chaotických podkladů**.

Podklady v `docs/` popisují dva fiktivní bankovní projekty. Pocházejí od různých lidí
(PM, business owner, architekt, legal, UX) a **úmyslně si odporují** — cvičení je o tom
rozpory najít a zapsat, ne o tom je rozhodnout.

| Projekt           | Podklady                  | K čemu je                                   |
| ----------------- | ------------------------- | ------------------------------------------- |
| Smart Savings     | `docs/smart-savings/`     | hotová ukázka v branchi `ukazka`            |
| Finanční ukazatel | `docs/financni-ukazatel/` | cvičení — postav si framework sám na `main` |

## 🌿 Branche

- **`main`** — AI artefakty jsou záměrně **prázdné kostry s TODO**. Hotový je jen skript `novy-epic.sh`
  a hook `ochrana-docs`, který chrání `docs/` před zápisem. Tady začínáš.
- **[`ukazka`](https://github.com/DXHeroes/github-copilot-workshop/tree/ukazka)** — kompletní
  řešení nad Smart Savings. Když tě zajímá jedna vrstva, otevři rovnou její složku
  v `.github/` podle tabulky níže.

## 🧱 AI artefakty v tomto repu

| Artefakt           | Kde                                      | Proč                                                                         |
| ------------------ | ---------------------------------------- | ---------------------------------------------------------------------------- |
| instrukce projektu | `.github/copilot-instructions.md`        | kontext, který platí v každé konverzaci                                      |
| instruction files  | `.github/instructions/*.instructions.md` | pravidla jen pro určité soubory (`applyTo`), jinde nezabírají kontext        |
| prompt files       | `.github/prompts/*.prompt.md`            | vstupní bod workflow, spouští ho člověk přes `/název`                        |
| custom agenti      | `.github/agents/*.agent.md`              | role s vlastními nástroji a hranicemi, subagent šetří kontext hlavního chatu |
| skills             | `.github/skills/<název>/`                | opakovatelný postup nad jedním typem výstupu                                 |
| skripty a šablony  | složky `scripts/` a `assets/` ve skillu  | deterministické kroky, které nedělá model                                    |
| hooks              | `.github/hooks/*.json`                   | kontrola, která platí vždycky, ať model udělá cokoli                         |

## 🗂️ Struktura repa

- `docs/<projekt>/` — chaotické podklady k projektu a `dod-sablona.md` (zdroj pravdy)
- `outputs/<projekt>/` — vygenerované výstupy: epic a user stories
- `api/` — návrh API k projektu (OpenAPI)
- `.github/` — vlastní AI framework nad Copilotem

## ▶️ Spuštění ukázky

1. Nainstaluj formátovač pro hook: `pip install -r requirements.txt` (Python 3.10+).
2. Otevři repo ve VS Code jako důvěryhodnou složku (Workspace Trust), jinak se hooky nespustí.
3. Spusť `/novy-epic` s projektem `smart-savings`.
4. Celý cyklus od podkladů po návrh API: v chatu zvol agenta `projektak` a napiš mu projekt a téma.

Skripty a hooky mají testy, které můžeš spustit i ručně (na Windows `python` místo `python3`):

```sh
python3 .github/skills/tvorba-epicu/scripts/test_validate_epic.py
python3 .github/skills/backlog-do-issues/scripts/test_create_issues.py
python3 .github/hooks/test_hooks.py
```
