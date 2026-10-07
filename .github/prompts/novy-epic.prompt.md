---
description: "Spustí analytika, který z podkladů projektu připraví epic a předloží otevřené rozpory."
argument-hint: "téma epicu"
agent: analytik
---

<!-- Prompt = vstupní bod. Předá kontext a zadání, doménová logika sem nepatří. -->

Vytvoř epic na téma: ${input:tema:téma epicu}

Projekt: ${input:projekt:název složky v docs/}

Postupuj podle svého operating flow. Než budeš pokračovat user stories, ukaž mi otevřené rozpory a počkej na moje rozhodnutí.
