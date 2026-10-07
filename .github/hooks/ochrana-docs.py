# preToolUse hook: the agent must not write to docs/, the source documents are the source of truth.
# A hook is a deterministic check outside the model. What must always hold does not belong only in instructions.
#
# Registered in ochrana-docs.json (python3 on macOS/Linux, python on Windows). It runs in both VS Code harnesses:
# - Local sends `tool_name` + `tool_input` and blocks only on exit 2. If python is missing or the hook
#   crashes, Local shows a warning and the tool runs anyway.
# - Copilot sends `toolName` + `toolArgs` (a JSON string) and denies on any non-zero exit or crash.
#   If python is missing there, the agent cannot run any tool.
#
# File tools are checked by their path arguments. Commands (terminal, tasks) are best effort:
# a command that changes directory first (cd docs && ...) is not detected, and copying out of docs/
# is blocked too, because the agent has no reason to copy the source documents.
import json
import re
import sys
from pathlib import Path

PROTECTED_DIR = "docs"
REPO_ROOT = Path(__file__).resolve().parents[2]

# Local: create_file, replace_string_in_file, multi_replace_string_in_file, insert_edit_into_file,
# edit_notebook_file, apply_patch, create_directory. Copilot: create, edit.
WRITE_TOOL = re.compile(r"create|edit|replace|insert|patch", re.I)
# filePath, dirPath (Local) and path (Copilot). Content keys such as content or file_text are not paths.
PATH_KEY = re.compile(r"path$", re.I)
# Commands of run_in_terminal, bash, powershell and create_and_run_task (command + args).
COMMAND_KEY = re.compile(r"^(?:command|args)$", re.I)
PATCH_HEADER = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$", re.M)

DOCS_IN_COMMAND = re.compile(r"(?<![\w.-])(?:\./)?" + PROTECTED_DIR + r"[/\\]")
SHELL_WRITE = re.compile(
    r">{1,2}\s*[\"']?(?:\./)?" + PROTECTED_DIR + r"[/\\]"
    r"|\b(?:rm|mv|cp|tee|touch|truncate|unlink|rmdir|mkdir|del|erase|ren|move|copy)\b"
    r"|\bsed\s+(?:-\w*\s+)*-i|\bperl\s+(?:-\w*\s+)*-\w*i"
    r"|\b(?:python[\d.]*|py|node|ruby|perl)\s+(?:-\w+\s+)*-[ce]\b"
    r"|\bgit\s+(?:rm|mv|checkout|restore)\b"
    r"|\b(?:Set|Add|Clear)-Content\b|\bOut-File\b|\b(?:Remove|Move|Copy|Rename|New)-Item\b",
    re.I,
)

REASON = (
    f"Writing to {PROTECTED_DIR}/ is blocked by the ochrana-docs hook: the source documents are read-only. "
    "Write results to outputs/<project>/ instead and record contradictions there."
)


def strings_under(value, key_pattern, key=""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from strings_under(child, key_pattern, child_key)
    elif isinstance(value, list):
        for item in value:
            yield from strings_under(item, key_pattern, key)
    elif isinstance(value, str) and key_pattern.search(key):
        yield value


def is_protected(raw_path, cwd):
    path = Path(raw_path.strip().strip("\"'").replace("\\", "/"))
    path = (cwd / path).resolve()
    # The working copy can differ from the hook's own repository, e.g. in a worktree session.
    for root in {REPO_ROOT, cwd}:
        if path.is_relative_to(root):
            parts = path.relative_to(root).parts
            if parts and parts[0] == PROTECTED_DIR:
                return True
    return False


def blocked(event):
    tool = event.get("tool_name") or event.get("toolName") or ""
    args = event.get("tool_input", event.get("toolArgs")) or {}
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except ValueError:
            args = {"command": args}
    cwd = Path(event.get("cwd") or REPO_ROOT).resolve()

    if WRITE_TOOL.search(tool):
        paths = list(strings_under(args, PATH_KEY))
        for text in strings_under(args, re.compile("")):
            paths.extend(match[0] or match[1] for match in PATCH_HEADER.findall(text))
        if any(is_protected(path, cwd) for path in paths):
            return True

    command = "\n".join(strings_under(args, COMMAND_KEY))
    return bool(DOCS_IN_COMMAND.search(command) and SHELL_WRITE.search(command))


def main():
    raw = sys.stdin.buffer.read().decode("utf-8")
    if raw.strip() and blocked(json.loads(raw)):
        # Local shows stderr; Copilot passes permissionDecisionReason from stdout to the agent.
        print(json.dumps({"permissionDecision": "deny", "permissionDecisionReason": REASON}))
        print(REASON, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # A bug in the hook must not block every tool call.
        print(f"ochrana-docs hook skipped: {error}", file=sys.stderr)
    sys.exit(0)
