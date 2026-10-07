---
description: "Z hotového epicu vytvoří user stories podle pravidel pro user stories."
argument-hint: "cesta k epicu"
agent: analytik
---

<!-- Prompt = vstupní bod. Formát stories je v user-stories.instructions.md, ne tady. -->

Z epicu `${input:epic:cesta k epicu v outputs/}` vytvoř user stories do souboru se stejným slugem a příponou `.stories.md` vedle něj.
Když cesta chybí nebo epic neexistuje, zeptej se na ni.

Jedna story na každou položku ze sekce „Uživatelské příběhy“ v epicu. Kde epic uvádí otevřený rozpor, story ho nerozhoduje, jen na něj odkáže.
