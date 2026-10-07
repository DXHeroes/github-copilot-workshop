import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parent
REPO_ROOT = HOOKS_DIR.parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), HOOKS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_hook(name, payload):
    data = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return subprocess.run([sys.executable, str(HOOKS_DIR / f"{name}.py")], input=data, capture_output=True,
                          cwd=REPO_ROOT)


def copilot(tool, args):
    return {"toolName": tool, "toolArgs": json.dumps(args, ensure_ascii=False), "cwd": str(REPO_ROOT)}


def local(tool, args):
    return {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": args, "cwd": str(REPO_ROOT)}


class OchranaDocsTest(unittest.TestCase):
    denied = {
        "copilot edit": copilot("edit", {"path": "docs/smart-savings/email-kickoff.md"}),
        "absolute path": copilot("edit", {"path": str(REPO_ROOT / "docs" / "a.md")}),
        "path traversal": copilot("edit", {"path": "outputs/../docs/a.md"}),
        "windows backslashes": copilot("edit", {"path": "docs\\smart-savings\\a.md"}),
        "czech file name": copilot("create", {"path": "docs/žluťoučký.md"}),
        "local replace": local("replace_string_in_file", {"filePath": str(REPO_ROOT / "docs" / "a.md")}),
        "local new directory": local("create_directory", {"dirPath": "docs/new"}),
        "one of many files": local("multi_replace_string_in_file",
                                   {"replacements": [{"filePath": "outputs/a.md"}, {"filePath": "docs/b.md"}]}),
        "apply patch": local("apply_patch", {"input": "*** Begin Patch\n*** Update File: docs/a.md\n*** End Patch"}),
        "shell redirect": copilot("bash", {"command": "echo x > docs/a.md"}),
        "shell sed -i": copilot("bash", {"command": "sed -i '' s/a/b/ docs/a.md"}),
        "shell rm": copilot("bash", {"command": "rm -rf ./docs/"}),
        "powershell": copilot("powershell", {"command": "Set-Content -Path docs\\a.md -Value x"}),
        "local terminal git mv": local("run_in_terminal", {"command": "git mv docs/a.md docs/b.md"}),
        "local task command": local("create_and_run_task",
                                    {"task": {"label": "x", "type": "shell", "command": "rm docs/a.md"}}),
        "local task args": local("create_and_run_task",
                                 {"task": {"label": "x", "type": "shell", "command": "rm", "args": ["docs/a.md"]}}),
        "python one-liner": copilot("bash", {"command": "python3 -c \"open('docs/a.md', 'w').write('x')\""}),
        "node one-liner": local("run_in_terminal",
                                {"command": "node -e \"require('fs').writeFileSync('docs/a.md', 'x')\""}),
    }
    allowed = {
        "write to outputs": copilot("create", {"path": "outputs/smart-savings/x.epic.md", "file_text": "docs/a.md"}),
        "read docs": copilot("view", {"path": "docs/smart-savings/a.md"}),
        "local read docs": local("read_file", {"filePath": str(REPO_ROOT / "docs" / "a.md")}),
        "similar directory name": copilot("edit", {"path": "docs-old/a.md"}),
        "nested docs directory": copilot("edit", {"path": "outputs/docs/a.md"}),
        "patch to outputs": local("apply_patch", {"input": "*** Add File: outputs/a.md\n+see docs/a.md"}),
        "shell read": copilot("bash", {"command": "cat docs/smart-savings/*.md | wc -w"}),
        "shell stderr redirect": copilot("bash", {"command": "grep -rn PSD2 docs/ 2>/dev/null"}),
        "shell grep -e": copilot("bash", {"command": "grep -e PSD2 docs/smart-savings/a.md"}),
        "local task without docs": local("create_and_run_task", {"task": {"label": "x", "command": "npm test"}}),
    }

    def test_denied(self):
        for name, payload in self.denied.items():
            with self.subTest(name):
                result = run_hook("ochrana-docs", payload)
                self.assertEqual(result.returncode, 2)
                self.assertIn(b"docs/", result.stderr)

    def test_deny_reason_reaches_the_copilot_agent(self):
        # Copilot merges stdout JSON with the exit 2 deny and shows permissionDecisionReason to the agent.
        result = run_hook("ochrana-docs", copilot("edit", {"path": "docs/a.md"}))
        output = json.loads(result.stdout)
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("docs/", output["permissionDecisionReason"])

    def test_repo_opened_through_a_symlink_is_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            link = Path(tmp) / "repo-link"
            link.symlink_to(REPO_ROOT, target_is_directory=True)
            payload = local("create_file", {"filePath": str(link / "docs" / "a.md")}) | {"cwd": str(link)}
            self.assertEqual(run_hook("ochrana-docs", payload).returncode, 2)

    def test_docs_of_another_working_copy_are_protected(self):
        # A worktree session works in a different folder than the one the hook script lives in.
        with tempfile.TemporaryDirectory() as tmp:
            payload = copilot("create", {"path": "docs/a.md"}) | {"cwd": tmp}
            self.assertEqual(run_hook("ochrana-docs", payload).returncode, 2)

    def test_allowed(self):
        for name, payload in self.allowed.items():
            with self.subTest(name):
                self.assertEqual(run_hook("ochrana-docs", payload).returncode, 0)

    def test_bad_input_lets_the_call_through(self):
        for name, payload in {"empty": b"", "not json": b"not json"}.items():
            with self.subTest(name):
                self.assertEqual(run_hook("ochrana-docs", payload).returncode, 0)


class FormatovaniMdPathsTest(unittest.TestCase):
    def setUp(self):
        self.hook = load("formatovani-md")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / "outputs").mkdir()
        (self.root / "docs").mkdir()
        for name in ("outputs/a.md", "outputs/b.txt", "docs/c.md"):
            (self.root / name).write_text("x\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def paths(self, payload):
        return [path.relative_to(self.root).as_posix() for path in self.hook.markdown_paths(payload, self.root)]

    def test_written_markdown_file_is_selected(self):
        self.assertEqual(self.paths(copilot("edit", {"path": "outputs/a.md"}) | {"cwd": str(self.root)}),
                         ["outputs/a.md"])

    def test_local_payload_is_selected(self):
        payload = local("create_file", {"filePath": str(self.root / "outputs" / "a.md")})
        self.assertEqual(self.paths(payload), ["outputs/a.md"])

    def test_other_file_types_are_ignored(self):
        self.assertEqual(self.paths(copilot("edit", {"path": "outputs/b.txt"}) | {"cwd": str(self.root)}), [])

    def test_read_tools_are_ignored(self):
        self.assertEqual(self.paths(copilot("view", {"path": "outputs/a.md"}) | {"cwd": str(self.root)}), [])

    def test_docs_are_never_formatted(self):
        self.assertEqual(self.paths(copilot("edit", {"path": "docs/c.md"}) | {"cwd": str(self.root)}), [])

    def test_missing_and_outside_files_are_ignored(self):
        for path in ("outputs/missing.md", "/etc/hosts.md"):
            with self.subTest(path):
                self.assertEqual(self.paths(copilot("edit", {"path": path}) | {"cwd": str(self.root)}), [])

    def test_file_in_another_working_copy_is_selected(self):
        # A worktree session works in a different folder than the one the hook script lives in.
        payload = copilot("edit", {"path": "outputs/a.md"}) | {"cwd": str(self.root)}
        paths = self.hook.markdown_paths(payload, Path(self.tmp.name) / "elsewhere")
        self.assertEqual([path.relative_to(self.root).as_posix() for path in paths], ["outputs/a.md"])

    def test_docs_of_another_working_copy_are_never_formatted(self):
        payload = copilot("edit", {"path": "docs/c.md"}) | {"cwd": str(self.root)}
        self.assertEqual(self.hook.markdown_paths(payload, Path(self.tmp.name) / "elsewhere"), [])


@unittest.skipUnless(importlib.util.find_spec("mdformat"), "mdformat is not installed (pip install -r requirements.txt)")
class FormatovaniMdFormatTest(unittest.TestCase):
    def setUp(self):
        self.hook = load("formatovani-md")
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "a.md"

    def tearDown(self):
        self.tmp.cleanup()

    def test_messy_table_is_aligned_and_reported(self):
        self.file.write_text("# T\n|a|b|\n|-|-|\n|1|22|\n", encoding="utf-8")
        self.assertTrue(self.hook.format_file(self.file))
        self.assertIn("| a   | b   |", self.file.read_text(encoding="utf-8"))

    def test_formatted_file_is_left_alone(self):
        self.file.write_text("# T\n\nText s „uvozovkami“.\\\nDruhý řádek.\n", encoding="utf-8")
        before = self.file.read_bytes()
        self.assertFalse(self.hook.format_file(self.file))
        self.assertEqual(self.file.read_bytes(), before)

    def test_frontmatter_survives(self):
        text = "---\ndescription: \"Analytik\"\ntools: [read, search]\n---\n\n# Analytik\n"
        self.file.write_text(text, encoding="utf-8")
        self.hook.format_file(self.file)
        self.assertEqual(self.file.read_text(encoding="utf-8"), text)

    def test_ordered_lists_keep_consecutive_numbers(self):
        self.file.write_text("# T\n\n1. a\n2. b\n3. c\n", encoding="utf-8")
        self.hook.format_file(self.file)
        self.assertIn("2. b\n3. c", self.file.read_text(encoding="utf-8"))

    def test_command_line_formats_given_folder_but_not_docs(self):
        # The formatovat-md prompt runs the same script with paths instead of a hook payload.
        root = Path(self.tmp.name)
        (root / "outputs").mkdir()
        (root / "docs").mkdir()
        messy = "# T\n|a|b|\n|-|-|\n|1|22|\n"
        for name in ("outputs/a.md", "docs/b.md"):
            (root / name).write_text(messy, encoding="utf-8")

        result = subprocess.run([sys.executable, str(HOOKS_DIR / "formatovani-md.py"), "."], capture_output=True,
                                cwd=root, text=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("outputs/a.md", result.stdout)
        self.assertNotIn("docs/b.md", result.stdout)
        self.assertIn("| a   | b   |", (root / "outputs" / "a.md").read_text(encoding="utf-8"))
        self.assertEqual((root / "docs" / "b.md").read_text(encoding="utf-8"), messy)

    def test_output_tells_the_model_to_reread_in_both_shapes(self):
        output = json.loads(self.hook.context_output(["outputs/a.md"]))
        self.assertIn("outputs/a.md", output["additionalContext"])
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertEqual(output["hookSpecificOutput"]["additionalContext"], output["additionalContext"])


if __name__ == "__main__":
    unittest.main()
