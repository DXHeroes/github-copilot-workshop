# postToolUse hook: after the agent creates or edits a .md file, format it with mdformat
# (GFM tables, YAML frontmatter kept as is, ordered lists numbered consecutively).
# Formatting is deterministic and must always happen, so it is a hook, not a sentence in the instructions.
#
# Registered in formatovani-md.json (python3 on macOS/Linux, python on Windows).
# Requires: pip install -r requirements.txt. Without mdformat the hook only warns and lets the work continue.
# postToolUse is fail-open: an error here never blocks the agent.
#
# The same script formats files on request: formatovani-md.py <files or folders> (used by /formatovat-md).
#
# The hook config cannot filter by file path, so the .md filter is here.
# docs/ is never formatted: the source documents stay exactly as they are.
# Only file tools are handled; .md files written from a shell command are not formatted.
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIPPED_DIR = "docs"

# Local: create_file, replace_string_in_file, multi_replace_string_in_file, insert_edit_into_file,
# edit_notebook_file, apply_patch. Copilot: create, edit.
WRITE_TOOL = re.compile(r"create|edit|replace|insert|patch", re.I)
# filePath (Local) and path (Copilot).
PATH_KEY = re.compile(r"path$", re.I)
PATCH_HEADER = re.compile(r"^\*\*\* (?:Add|Update) File: (.+)$|^\*\*\* Move to: (.+)$", re.M)


def strings_under(value, key_pattern, key=""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from strings_under(child, key_pattern, child_key)
    elif isinstance(value, list):
        for item in value:
            yield from strings_under(item, key_pattern, key)
    elif isinstance(value, str) and key_pattern.search(key):
        yield value


def formattable(path, roots):
    """A .md file inside one of the roots and outside docs/."""
    if path.suffix.lower() != ".md" or not path.is_file():
        return False
    for root in roots:
        if path.is_relative_to(root):
            return path.relative_to(root).parts[0] != SKIPPED_DIR
    return False


def markdown_paths(event, repo_root=REPO_ROOT):
    tool = event.get("tool_name") or event.get("toolName") or ""
    if not WRITE_TOOL.search(tool):
        return []

    args = event.get("tool_input", event.get("toolArgs")) or {}
    if isinstance(args, str):
        args = json.loads(args)
    candidates = list(strings_under(args, PATH_KEY))
    for text in strings_under(args, re.compile("")):
        candidates.extend(match[0] or match[1] for match in PATCH_HEADER.findall(text))

    cwd = Path(event.get("cwd") or repo_root).resolve()
    # The working copy can differ from the hook's own repository, e.g. in a worktree session.
    roots = [cwd, Path(repo_root).resolve()]
    selected = []
    for candidate in candidates:
        path = (cwd / candidate.strip().replace("\\", "/")).resolve()
        if formattable(path, roots) and path not in selected:
            selected.append(path)
    return selected


def command_line_paths(arguments, cwd):
    selected = []
    for argument in arguments:
        path = (cwd / argument).resolve()
        for file in sorted(path.rglob("*.md")) if path.is_dir() else [path]:
            if formattable(file, [cwd]) and file not in selected:
                selected.append(file)
    return selected


def format_file(path):
    import mdformat

    original = path.read_text(encoding="utf-8")
    formatted = mdformat.text(original, options={"number": True}, extensions={"gfm", "frontmatter"})
    if formatted == original:
        return False
    path.write_text(formatted, encoding="utf-8", newline="")
    return True


def context_output(changed):
    message = (
        "Formatted with mdformat by the formatovani-md hook: " + ", ".join(changed)
        + ". Re-read these files before editing them again."
    )
    # Copilot reads additionalContext at the top level, VS Code Local reads it from hookSpecificOutput.
    return json.dumps({
        "additionalContext": message,
        "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message},
    })


def mdformat_missing():
    try:
        import mdformat  # noqa: F401
    except ImportError:
        print("mdformat is not installed: pip install -r requirements.txt", file=sys.stderr)
        return True
    return False


def run_command_line(arguments):
    cwd = Path.cwd().resolve()
    if mdformat_missing():
        return 1
    changed = [path.relative_to(cwd).as_posix() for path in command_line_paths(arguments, cwd) if format_file(path)]
    print("Formatted: " + ", ".join(changed) if changed else "Nothing to format.")
    return 0


def run_hook():
    raw = sys.stdin.buffer.read().decode("utf-8")
    paths = markdown_paths(json.loads(raw)) if raw.strip() else []
    if not paths or mdformat_missing():
        return
    changed = [str(path) for path in paths if format_file(path)]
    if changed:
        print(context_output(changed))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(run_command_line(sys.argv[1:]))
    try:
        run_hook()
    except Exception as error:  # Formatting is a convenience; a bug here must not disturb the agent.
        print(f"formatovani-md hook skipped: {error}", file=sys.stderr)
    sys.exit(0)
