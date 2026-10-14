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


def copilot(tool, args):
    return {"toolName": tool, "toolArgs": json.dumps(args, ensure_ascii=False), "cwd": str(REPO_ROOT)}


def local(tool, args):
    return {"hook_event_name": "PostToolUse", "tool_name": tool, "tool_input": args, "cwd": str(REPO_ROOT)}


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
