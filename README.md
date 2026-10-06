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
  řešení nad Smart Savings. Když tě zajímá jedna vrstva, otevři rovnou její soubor
  z tabulky níže.

## 🧱 AI artefakty v tomto repu

| Artefakt        | Soubor                                              | K čemu je                              |
| --------------- | --------------------------------------------------- | -------------------------------------- |
| agent instrukce | `.github/copilot-instructions.md`                   | vždy platný kontext projektu           |
| instructions    | `.github/instructions/epic.instructions.md`         | pravidla pro soubory `*.epic.md`       |
| instructions    | `.github/instructions/user-stories.instructions.md` | formát `*.stories.md`                  |
| instructions    | `.github/instructions/api.instructions.md`          | konvence pro návrh API v `api/`        |
| prompt          | `.github/prompts/novy-epic.prompt.md`               | vstupní bod `/novy-epic`               |
| prompt          | `.github/prompts/rozpory.prompt.md`                 | `/rozpory`: oponentní čtení podkladů   |
| prompt          | `.github/prompts/user-stories.prompt.md`            | `/user-stories` z hotového epicu       |
| agent           | `.github/agents/analytik.agent.md`                  | koordinátor: role, flow, kontrolní bod |
| subagent        | `.github/agents/rozbor-podkladu.agent.md`           | přečte podklady ve vlastním kontextu   |
| subagent        | `.github/agents/recenzent.agent.md`                 | zkontroluje epic proti DoD, jen čte    |
| skill           | `.github/skills/tvorba-epicu/`                      | postup nad jedním typem artefaktu      |
| script          | `.../tvorba-epicu/scripts/novy-epic.sh`             | deterministický krok místo modelu      |
| script          | `.../tvorba-epicu/scripts/validate_epic.py`         | kontrola struktury epicu               |
| template        | `.../tvorba-epicu/assets/epic.template.md`          | struktura výstupu                      |
| skill           | `.github/skills/backlog-do-issues/`                 | `/backlog-do-issues`: skript místo MCP |
| hook            | `.github/hooks/ochrana-docs.json` (+ `.py`)         | zamítne zápis do `docs/`               |
| hook            | `.github/hooks/formatovani-md.json` (+ `.py`)       | po zápisu `.md` soubor zformátuje      |

## 🧭 Kterou vrstvu použít

```mermaid
graph TD
    Start((úkol)) --> Q1
    Start -->|a navíc| Q4
    Q1{Má to platit<br/>v každé konverzaci?} -->|ano| I[copilot-instructions.md]
    Q1 -->|jen pro určité soubory| PI[*.instructions.md<br/>s applyTo]
    Q1 -->|ne| Q2{Spouští to<br/>člověk na požádání?}
    Q2 -->|ano| P[prompt file]
    Q2 -->|ne, model si to<br/>vybere sám| Q3{Je to postup nad<br/>jedním typem výstupu?}
    Q3 -->|ano| S[skill<br/>+ skript na deterministické kroky]
    Q3 -->|ne, je to role<br/>s vlastními nástroji| A[custom agent]
    Q4{Musí to platit<br/>bez výjimky?} -->|ano| H[hook]
```

| Vrstva       | Náklad                               | Přínos                                          |
| ------------ | ------------------------------------ | ----------------------------------------------- |
| instructions | pár řádků, ale žerou kontext vždycky | konvence, které nemusíš opakovat v promptu      |
| prompt       | jeden soubor                         | ověřený prompt používá celý tým                 |
| skill        | `SKILL.md` + skripty a šablony       | opakovatelný postup, bez MCP serveru            |
| agent        | role, hranice, výběr nástrojů        | delegace s jasným místem, kde rozhoduje člověk  |
| hook         | skript a jeho údržba                 | kontrola, která nezávisí na tom, co model udělá |

## 🗂️ Struktura repa

- `docs/<projekt>/` — chaotické podklady k projektu a `dod-sablona.md` (zdroj pravdy)
- `outputs/<projekt>/` — vygenerované výstupy
- `.github/` — vlastní AI framework nad Copilotem

## ▶️ Spuštění ukázky

1. Nainstaluj formátovač pro hook: `pip install -r requirements.txt` (Python 3.10+).
2. Otevři repo ve VS Code jako důvěryhodnou složku (Workspace Trust), jinak se hooky nespustí.
3. V chatu zvol prostředí **Local**. Prompt files a subagenti v ukázce běží v něm.
4. Spusť `/novy-epic` s projektem `smart-savings`.

Testy skriptů a hooků (na Windows `python` místo `python3`):

```sh
python3 .github/skills/tvorba-epicu/scripts/test_validate_epic.py
python3 .github/skills/backlog-do-issues/scripts/test_create_issues.py
python3 .github/hooks/test_hooks.py
```

## ▶️ Jak s tím pracovat

1. Otevři jeden artefakt a nahraď TODO vlastním obsahem.
2. Zkus ho v chatu (např. `/novy-epic`) nad `docs/financni-ukazatel/` a podívej se, co se změnilo.
3. Přidej další artefakt tam, kde ti něco chybí.
4. Když nevíš, jak dál, podívej se, jak stejnou vrstvu řeší branch `ukazka`.

## 🔍 Na co se u toho dívat

- Co patří do **instructions** a co už do **skillu**?
- Proč zakládá soubor **skript** a ne model?
- Co by se stalo, kdyby **template** neexistoval?
- Proč má **agent** delegovat na skill místo vlastního postupu?
- Proč kontrolu zápisu do `docs/` řeší **hook**, a ne věta v instrukcích?

```mermaid
graph LR
    Prompt[/novy-epic<br/>prompt/] --> Agent[agent<br/>analytik]
    Agent --> Skill[skill<br/>tvorba-epicu]
    Skill --> Script[script<br/>novy-epic.sh]
    Tmpl[template<br/>epic.template.md] --> Script
    Docs[docs/*/<br/>chaotické podklady] --> Skill
    Script --> Epic[outputs/*/<br/>*.epic.md]
    Instr[instructions<br/>epic.instructions.md] -.pravidla.-> Epic
    Hook[hook<br/>ochrana-docs] -.chrání.-> Docs

    style Docs fill:#FFE4B5
    style Epic fill:#90EE90
```
