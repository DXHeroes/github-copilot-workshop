# Analytická dokumentace

Repo slouží k přípravě analytických výstupů (epic, user stories, návrh API) z podkladů k projektům.

## Struktura

- `docs/<projekt>/` — podklady jednoho projektu: emaily, zápisy ze schůzek, poznámky, výzkum
  a `dod-sablona.md` s Definition of Done. Pocházejí od různých lidí a můžou si odporovat.
  Každá podsložka `docs/` je jeden projekt.
- `outputs/<projekt>/` — vygenerované výstupy: epic a user stories.
- `api/` — návrh API k projektu, `api/<projekt>.openapi.yaml`.

## Pravidla práce

- **Pracuj vždy jen s jedním projektem.** Když není jasné s kterým, zeptej se.
- **Zdroj pravdy je `docs/<projekt>/`.** Nic si nedomýšlej. Co v podkladech není, je otevřená otázka.
  Podklady jiného projektu nepoužívej.
- **Rozpory se nerozhodují, rozpory se zapisují.** Uveď obě varianty, zdroje a vlastníka rozhodnutí.
- **Struktura výstupu se bere ze šablony**, nikdy se nevymýšlí ad hoc.
- Výstupy jsou česky, věcně, v odrážkách.
- Za faktem ve výstupu vždy odkaz na zdrojový soubor v `docs/<projekt>/`.
