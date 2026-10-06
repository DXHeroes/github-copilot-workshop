# Deterministic structural check of an epic: validate_epic.py outputs/<project>/<slug>.epic.md [...]
#
# Checks only what a script can decide without judgement:
#   - every "## " section of the template is present,
#   - no template placeholder is left over,
#   - every table has at least one row,
#   - the epic cites sources and every cited .md file exists in docs/<project>/.
# Whether the content is right is the reviewer's job, not this script's.
#
# Exit codes: 0 = valid, 1 = findings, 2 = usage error.
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
TEMPLATE_PATH = SCRIPT_DIR.parent / "assets" / "epic.template.md"

PLACEHOLDER = re.compile(r"\[(?! \]|x\])[^\]\n]+\](?!\()")
SOURCE_REF = re.compile(r"(?<![\w.-])([\w-]+\.md)\b")
TABLE_SEPARATOR = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$")


def section_headings(markdown):
    return [line.strip() for line in markdown.splitlines() if line.startswith("## ")]


def placeholders(markdown):
    return set(PLACEHOLDER.findall(markdown))


def tables_without_rows(markdown):
    lines = markdown.splitlines()
    empty = []
    for index, line in enumerate(lines):
        if TABLE_SEPARATOR.match(line.strip()):
            header = lines[index - 1].strip() if index > 0 else ""
            following = lines[index + 1].strip() if index + 1 < len(lines) else ""
            if not following.startswith("|"):
                empty.append(header)
    return empty


def validate(epic, template, sources):
    findings = []

    present = set(section_headings(epic))
    for heading in section_headings(template):
        if heading not in present:
            findings.append(f"Missing section: {heading}")

    for placeholder in sorted(placeholders(template)):
        if placeholder in epic:
            findings.append(f"Template placeholder left in the epic: {placeholder}")

    for header in tables_without_rows(epic):
        findings.append(f"Table has no rows: {header}")

    cited = set(SOURCE_REF.findall(epic))
    if not cited:
        findings.append("The epic cites no source file from docs/<project>/.")
    for name in sorted(cited - set(sources)):
        findings.append(f"Cited source does not exist in docs/<project>/: {name}")

    return findings


def project_of(epic_path, repo_root):
    try:
        parts = epic_path.resolve().relative_to(repo_root.resolve()).parts
    except ValueError:
        return None
    if len(parts) >= 3 and parts[0] == "outputs":
        return parts[1]
    return None


def main(argv, repo_root=REPO_ROOT, template_path=TEMPLATE_PATH):
    if not argv:
        print("Usage: validate_epic.py outputs/<project>/<slug>.epic.md [...]", file=sys.stderr)
        return 2

    template = template_path.read_text(encoding="utf-8")
    status = 0
    for argument in argv:
        epic_path = Path(argument)
        project = project_of(epic_path, repo_root)
        docs_dir = repo_root / "docs" / (project or "")
        if project is None or not docs_dir.is_dir() or not epic_path.is_file():
            print(f"{argument}: expected an existing file in outputs/<project>/ with a matching docs/<project>/.",
                  file=sys.stderr)
            return 2

        sources = {path.name for path in docs_dir.glob("*.md")}
        findings = validate(epic_path.read_text(encoding="utf-8"), template, sources)
        if findings:
            status = 1
            print(f"{argument}: {len(findings)} finding(s)")
            for finding in findings:
                print(f"  - {finding}")
        else:
            print(f"{argument}: OK")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
