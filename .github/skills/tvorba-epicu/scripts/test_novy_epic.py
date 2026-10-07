import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import novy_epic  # noqa: E402

TEMPLATE_PATH = SCRIPT_DIR.parent / "assets" / "epic.template.md"


class SlugTest(unittest.TestCase):
    def test_czech_title_becomes_ascii_slug(self):
        self.assertEqual(novy_epic.slug("MVP úsporných cílů"), "mvp-uspornych-cilu")

    def test_czech_capitals_lose_diacritics_too(self):
        self.assertEqual(novy_epic.slug("ŘÍZENÍ Účtů"), "rizeni-uctu")

    def test_punctuation_collapses_to_single_dashes(self):
        self.assertEqual(novy_epic.slug("  Fáze 2: notifikace & limity!  "), "faze-2-notifikace-limity")


class MainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs" / "smart-savings").mkdir(parents=True)
        (self.root / "docs" / "financni-ukazatel").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = novy_epic.main(list(argv), repo_root=self.root, template_path=TEMPLATE_PATH)
        return code, out.getvalue(), err.getvalue()

    def test_creates_epic_from_template_and_prints_its_path(self):
        code, out, _ = self.run_main("smart-savings", "MVP úsporných cílů")

        epic = self.root / "outputs" / "smart-savings" / "mvp-uspornych-cilu.epic.md"
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), str(epic))
        lines = epic.read_text(encoding="utf-8").splitlines()
        self.assertRegex(lines[0], r"^<!-- Vytvořeno: \d{4}-\d{2}-\d{2} \| Zdroj podkladů: docs/smart-savings/ -->$")
        self.assertEqual(lines[1], "# Epic: MVP úsporných cílů")
        self.assertEqual(lines[2:], TEMPLATE_PATH.read_text(encoding="utf-8").splitlines()[1:])

    def test_unknown_project_lists_available_projects(self):
        code, _, err = self.run_main("neexistuje", "MVP")
        self.assertEqual(code, 1)
        self.assertIn("financni-ukazatel", err)
        self.assertIn("smart-savings", err)
        self.assertFalse((self.root / "outputs").exists())

    def test_project_must_be_a_plain_folder_name(self):
        code, _, _ = self.run_main("../docs/smart-savings", "MVP")
        self.assertEqual(code, 1)

    def test_existing_epic_is_not_overwritten(self):
        self.run_main("smart-savings", "MVP")
        epic = self.root / "outputs" / "smart-savings" / "mvp.epic.md"
        epic.write_text("rozpracováno", encoding="utf-8")

        code, _, err = self.run_main("smart-savings", "MVP")

        self.assertEqual(code, 1)
        self.assertIn("už existuje", err)
        self.assertEqual(epic.read_text(encoding="utf-8"), "rozpracováno")

    def test_missing_arguments_print_usage(self):
        code, _, err = self.run_main("smart-savings")
        self.assertEqual(code, 2)
        self.assertIn("Použití", err)

    def test_title_without_letters_is_rejected(self):
        code, _, _ = self.run_main("smart-savings", "!!!")
        self.assertEqual(code, 1)
        self.assertFalse((self.root / "outputs").exists())


class LocaleTest(unittest.TestCase):
    def test_runs_with_c_locale(self):
        # The former bash script failed with LC_ALL=C on the Czech characters in the title.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "smart-savings").mkdir(parents=True)
            code = (
                "import sys, novy_epic; from pathlib import Path; "
                f"sys.exit(novy_epic.main(sys.argv[1:], repo_root=Path({str(root)!r})))"
            )
            result = subprocess.run(
                [sys.executable, "-c", code, "smart-savings", "Řízení účtů"],
                cwd=SCRIPT_DIR, capture_output=True, env=os.environ | {"LC_ALL": "C", "LANG": "C"},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "outputs" / "smart-savings" / "rizeni-uctu.epic.md").is_file())


if __name__ == "__main__":
    unittest.main()
