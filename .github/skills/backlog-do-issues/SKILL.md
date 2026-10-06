---
name: backlog-do-issues
description: "Založí GitHub issues z user stories v outputs/<projekt>/*.stories.md přes gh CLI. Nejdřív vždy jen ukáže, co by založil."
argument-hint: "cesta k souboru se stories"
disable-model-invocation: true
---

# Backlog do issues

<!-- Skill + skript místo MCP serveru: stačí gh CLI, žádná infrastruktura. Spouští ho jen člověk přes /backlog-do-issues. -->

Na macOS a Linuxu spouštěj skript přes `python3`, na Windows přes `python`. Potřebuje přihlášené `gh` (`gh auth status`).

## Postup

1. **Zkus nanečisto** — spusť [create_issues.py](./scripts/create_issues.py) bez `--apply`.
   Skript nic nezaloží, jen vypíše seznam issues.

   ```sh
   python3 .github/skills/backlog-do-issues/scripts/create_issues.py outputs/smart-savings/mvp-uspornych-cilu.stories.md
   ```

2. **Ukaž seznam uživateli** a počkej na výslovné potvrzení. Bez něj dál nepokračuj.

3. **Založ issues** — stejný příkaz s `--apply`. Volitelně `--label <label>` (label už musí
   v repozitáři existovat) a `--repo OWNER/REPO`.

4. **Nahlas výsledek** — co vzniklo. Když skript skončí chybou, řekni, které issues už vznikly,
   a nespouštěj ho znovu celý, jinak vzniknou duplicity.

## Kdy skill nepoužívat

- Když stories ještě neprošly kontrolou člověka.
- Když soubor nemá nadpisy `### US-01: Název` podle [pravidel pro user stories](../../instructions/user-stories.instructions.md).
