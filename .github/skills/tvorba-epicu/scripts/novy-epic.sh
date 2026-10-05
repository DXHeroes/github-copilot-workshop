#!/usr/bin/env bash
# Založí nový epic z šablony: novy-epic.sh <projekt> "Název epicu"
set -euo pipefail

pouziti='Použití: novy-epic.sh <projekt> "Název epicu"'
projekt="${1:?$pouziti}"
nazev="${2:?$pouziti}"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
sablona="$(cd "$(dirname "${BASH_SOURCE[0]}")/../assets" && pwd)/epic.template.md"
podklady="$repo_root/docs/$projekt"
cilova_slozka="$repo_root/outputs/$projekt"

if [[ ! "$projekt" =~ ^[a-z0-9-]+$ ]] || [ ! -d "$podklady" ]; then
  echo "Neznámý projekt: $projekt. Dostupné projekty:" >&2
  ls -1 "$repo_root/docs" >&2
  exit 1
fi

slug="$(printf '%s' "$nazev" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -e 'y/áčďéěíňóřšťúůýž/acdeeinorstuuyz/' \
        -e 's/[^a-z0-9]\{1,\}/-/g' -e 's/^-//' -e 's/-$//')"

cil="$cilova_slozka/$slug.epic.md"

[ -f "$sablona" ] || { echo "Chybí šablona: $sablona" >&2; exit 1; }
[ -e "$cil" ] && { echo "Soubor už existuje: $cil" >&2; exit 1; }

mkdir -p "$cilova_slozka"
{
  echo "<!-- Vytvořeno: $(date +%Y-%m-%d) | Zdroj podkladů: docs/$projekt/ -->"
  sed "1s|.*|# Epic: $nazev|" "$sablona"
} > "$cil"

echo "$cil"
