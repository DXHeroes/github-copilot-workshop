---
description: "Z hotového epicu vytvoří user stories ve formátu, který umí převést skill backlog-do-issues."
argument-hint: "cesta k epicu"
agent: agent
tools: [read, search, edit]
---

<!-- Prompt = vstupní bod. Formát stories je v user-stories.instructions.md, ne tady. -->

Z epicu `${input:epic:outputs/smart-savings/mvp-uspornych-cilu.epic.md}` vytvoř user stories do souboru se stejným slugem a příponou `.stories.md` vedle něj.

Jedna story na každou položku ze sekce „Uživatelské příběhy“ v epicu. Kde epic uvádí otevřený rozpor, story ho nerozhoduje, jen na něj odkáže.
