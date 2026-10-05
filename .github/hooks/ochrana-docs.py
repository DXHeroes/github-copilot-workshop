# preToolUse hook: the agent must not write to docs/, the source documents are the source of truth.
# A hook is a deterministic check outside the model. What must always hold does not belong only in instructions.
#
# Registered in ochrana-docs.json (python3 on macOS/Linux, python on Windows).
# Note: preToolUse is fail-closed. If python is missing, the agent cannot run any tool.
#
# Payloads differ by harness: Copilot sends `toolName` + `toolArgs` (often a JSON string),
# VS Code Local sends `tool_name` + `tool_input`. Tool names differ too, so tools are classified
# by name patterns instead of an exact list.
# File tools are checked reliably by their path arguments. Shell commands are best effort:
# a command that changes directory first (cd docs && ...) is not detected.
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse

PROTECTED_DIR = "docs"
REPO_ROOT = Path(__file__).resolve().parents[2]

WRITE_TOOL = re.compile(r"edit|create|write|replace|insert|patch|delete|remove|rename|move|notebook", re.I)
SHELL_TOOL = re.compile(r"bash|powershell|shell|terminal|command|execute", re.I)
PATH_KEY = re.compile(r"path|file|uri|dir|target|dest|source", re.I)
PATCH_HEADER = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$", re.M)

DOCS_IN_COMMAND = re.compile(r"(?<![\w.-])(?:\./)?" + PROTECTED_DIR + r"[/\\]")
SHELL_WRITE = re.compile(
    r">{1,2}\s*[\"']?(?:\./)?" + PROTECTED_DIR + r"[/\\]"
    r"|\b(?:rm|mv|cp|tee|touch|truncate|unlink|rmdir|mkdir|del|erase|ren|move|copy)\b"
    r"|\bsed\s+(?:-\w*\s+)*-i|\bperl\s+(?:-\w*\s+)*-\w*i"
    r"|\bgit\s+(?:rm|mv|checkout|restore)\b"
    r"|\b(?:Set|Add|Clear)-Content\b|\bOut-File\b|\b(?:Remove|Move|Copy|Rename|New)-Item\b",
    re.I,
)

REASON = (
    f"Writing to {PROTECTED_DIR}/ is blocked by the ochrana-docs hook: the source documents are read-only. "
    "Write results to outputs/<project>/ instead and record contradictions there."
)


def parse_args(raw):
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except ValueError:
            return {"command": raw}
    return raw if raw is not None else {}


def collect_paths(value, key=""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from collect_paths(child, child_key)
    elif isinstance(value, list):
        for item in value:
            yield from collect_paths(item, key)
    elif isinstance(value, str) and PATH_KEY.search(key):
        yield value


def collect_command_text(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from collect_command_text(child)
    elif isinstance(value, list):
        for item in value:
            yield from collect_command_text(item)
    elif isinstance(value, str):
        yield value


def is_protected(raw_path, cwd):
    text = raw_path.strip().strip("\"'")
    if text.startswith("file:"):
        text = unquote(urlparse(text).path)
        if re.match(r"^/[A-Za-z]:", text):
            text = text[1:]
    text = text.replace("\\", "/")

    path = Path(text)
    if not path.is_absolute():
        path = Path(cwd) / path
    try:
        relative = Path(os.path.normpath(path)).relative_to(REPO_ROOT)
    except ValueError:
        return False
    parts = PurePosixPath(relative.as_posix()).parts
    return len(parts) > 0 and parts[0] == PROTECTED_DIR


def blocked(event):
    tool = event.get("toolName") or event.get("tool_name") or ""
    args = parse_args(event.get("toolArgs", event.get("tool_input")))
    cwd = event.get("cwd") or str(REPO_ROOT)

    if WRITE_TOOL.search(tool):
        paths = list(collect_paths(args))
        for text in collect_command_text(args):
            paths.extend(match[0] or match[1] for match in PATCH_HEADER.findall(text))
        return any(is_protected(path, cwd) for path in paths)

    if SHELL_TOOL.search(tool):
        command = "\n".join(collect_command_text(args))
        return bool(DOCS_IN_COMMAND.search(command) and SHELL_WRITE.search(command))

    return False


def main():
    raw = sys.stdin.buffer.read().decode("utf-8")
    event = json.loads(raw) if raw.strip() else {}
    if blocked(event):
        print(REASON, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # A bug in the hook must not block every tool call.
        print(f"ochrana-docs hook skipped: {error}", file=sys.stderr)
    sys.exit(0)
