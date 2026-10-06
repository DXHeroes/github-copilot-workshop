# postToolUse hook: after the agent creates or edits a .md file, format it with mdformat
# (GFM tables, YAML frontmatter kept as is, ordered lists numbered consecutively).
# Formatting is deterministic and must always happen, so it is a hook, not a sentence in the instructions.
#
# Registered in formatovani-md.json (python3 on macOS/Linux, python on Windows).
# Requires: pip install -r requirements.txt. Without mdformat the hook only warns and lets the work continue.
# postToolUse is fail-open: an error here never blocks the agent.
#
# The hook config cannot filter by file path (matcher only filters by tool name), so the .md filter is here.
# docs/ is never formatted: the source documents stay exactly as they are.
# Only file tools are handled; .md files written from a shell command are not formatted.
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIPPED_DIR = "docs"

WRITE_TOOL = re.compile(r"edit|create|write|replace|insert|patch|notebook", re.I)
PATH_KEY = re.compile(r"(?:path|paths|file|files|filename|uri|uris|target|destination)$", re.I)
PATCH_HEADER = re.compile(r"^\*\*\* (?:Add|Update) File: (.+)$|^\*\*\* Move to: (.+)$", re.M)


def parse_args(raw):
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except ValueError:
            return {}
    return raw if raw is not None else {}


def collect_strings(value, key="", only_paths=True):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from collect_strings(child, child_key, only_paths)
    elif isinstance(value, list):
        for item in value:
            yield from collect_strings(item, key, only_paths)
    elif isinstance(value, str) and (not only_paths or PATH_KEY.search(key)):
        yield value


def to_path(raw_path, cwd):
    text = raw_path.strip().strip("\"'")
    if text.startswith("file:"):
        text = unquote(urlparse(text).path)
        if re.match(r"^/[A-Za-z]:", text):
            text = text[1:]
    path = Path(text.replace("\\", "/"))
    if not path.is_absolute():
        path = Path(cwd) / path
    return Path(os.path.normpath(path))


def markdown_paths(event, repo_root=REPO_ROOT):
    tool = event.get("toolName") or event.get("tool_name") or ""
    if not WRITE_TOOL.search(tool):
        return []

    args = parse_args(event.get("toolArgs", event.get("tool_input")))
    candidates = list(collect_strings(args))
    for text in collect_strings(args, only_paths=False):
        candidates.extend(match[0] or match[1] for match in PATCH_HEADER.findall(text))

    root = Path(repo_root).resolve()
    selected = []
    for candidate in candidates:
        path = to_path(candidate, event.get("cwd") or root)
        try:
            parts = PurePosixPath(path.resolve().relative_to(root).as_posix()).parts
        except (ValueError, OSError):
            continue
        if path.suffix.lower() == ".md" and parts[0] != SKIPPED_DIR and path.is_file() and path not in selected:
            selected.append(path)
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


def main():
    raw = sys.stdin.buffer.read().decode("utf-8")
    event = json.loads(raw) if raw.strip() else {}
    paths = markdown_paths(event)
    if not paths:
        return

    try:
        import mdformat  # noqa: F401
    except ImportError:
        print("formatovani-md hook skipped: mdformat is not installed (pip install -r requirements.txt).",
              file=sys.stderr)
        return

    changed = [path.relative_to(REPO_ROOT).as_posix() for path in paths if format_file(path)]
    if changed:
        print(context_output(changed))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # Formatting is a convenience; a bug here must not disturb the agent.
        print(f"formatovani-md hook skipped: {error}", file=sys.stderr)
    sys.exit(0)
