# Založí nový epic ze šablony: novy_epic.py <projekt> "Název epicu"
#
# Vytvoří outputs/<projekt>/<slug>.epic.md a vypíše jeho cestu. Existující epic nepřepíše.
# Exit kódy: 0 = založeno, 1 = chyba vstupu, 2 = chybí argumenty.
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
TEMPLATE_PATH = SCRIPT_DIR.parent / "assets" / "epic.template.md"
USAGE = 'Použití: novy_epic.py <projekt> "Název epicu"'


def slug(title):
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")


def main(argv, repo_root=REPO_ROOT, template_path=TEMPLATE_PATH):
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 2
    project, title = argv

    docs = repo_root / "docs"
    if not re.fullmatch(r"[a-z0-9-]+", project) or not (docs / project).is_dir():
        projects = sorted(path.name for path in docs.iterdir() if path.is_dir())
        print(f"Neznámý projekt: {project}. Dostupné projekty: {', '.join(projects)}", file=sys.stderr)
        return 1

    name = slug(title)
    if not name:
        print(f"Z názvu „{title}“ nejde udělat název souboru. Použij písmena nebo číslice.", file=sys.stderr)
        return 1

    epic = repo_root / "outputs" / project / f"{name}.epic.md"
    if epic.exists():
        print(f"Soubor už existuje: {epic}", file=sys.stderr)
        return 1

    template = template_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header = f"<!-- Vytvořeno: {date.today().isoformat()} | Zdroj podkladů: docs/{project}/ -->\n"
    epic.parent.mkdir(parents=True, exist_ok=True)
    epic.write_text(header + f"# Epic: {title}\n" + "".join(template[1:]), encoding="utf-8")
    print(epic)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
