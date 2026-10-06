---
description: "Spustí analytika, který z podkladů projektu připraví epic a nechá ho zkontrolovat."
argument-hint: "téma epicu"
agent: analytik
---

<!-- Prompt = vstupní bod. Předá kontext a zadání, doménová logika sem nepatří. -->

Vytvoř epic na téma: ${input:tema:např. MVP úsporných cílů}

Projekt: ${input:projekt:smart-savings nebo financni-ukazatel}

Postupuj podle svého operating flow. Než budeš pokračovat user stories, ukaž mi nálezy recenzenta a otevřené rozpory a počkej na moje rozhodnutí.
