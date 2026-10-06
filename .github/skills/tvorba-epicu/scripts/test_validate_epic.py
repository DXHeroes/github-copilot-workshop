import contextlib
import io
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_epic  # noqa: E402

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "assets" / "epic.template.md"
TEMPLATE = TEMPLATE_PATH.read_text(encoding="utf-8")
SOURCES = {"email-kickoff.md", "schuzka-business.md"}


def filled_epic():
    """The real template with every placeholder replaced by a sourced value."""
    return re.sub(r"\[(?! \])[^\]\n]+\]", "Hodnota (email-kickoff.md)", TEMPLATE)


class ValidateTest(unittest.TestCase):
    def test_filled_template_passes(self):
        self.assertEqual(validate_epic.validate(filled_epic(), TEMPLATE, SOURCES), [])

    def test_missing_section_is_reported(self):
        epic = filled_epic().replace("## 8. Rizika", "## Rizika a jejich zmírnění")
        findings = validate_epic.validate(epic, TEMPLATE, SOURCES)
        self.assertTrue(any("## 8. Rizika" in finding for finding in findings), findings)

    def test_leftover_placeholder_is_reported(self):
        epic = filled_epic() + "\n- [Cíl 1]\n"
        findings = validate_epic.validate(epic, TEMPLATE, SOURCES)
        self.assertTrue(any("[Cíl 1]" in finding for finding in findings), findings)

    def test_checkbox_is_not_a_placeholder(self):
        self.assertIn("- [ ] ", filled_epic())
        self.assertEqual(validate_epic.validate(filled_epic(), TEMPLATE, SOURCES), [])

    def test_table_without_rows_is_reported(self):
        epic = re.sub(r"(\| ---[^\n]*\n)(\|[^\n]*\n)+", r"\1", filled_epic())
        findings = validate_epic.validate(epic, TEMPLATE, SOURCES)
        self.assertTrue(any("table" in finding.lower() for finding in findings), findings)

    def test_unknown_source_is_reported(self):
        epic = filled_epic() + "\n- Tvrzení (zapis-z-porady.md)\n"
        findings = validate_epic.validate(epic, TEMPLATE, SOURCES)
        self.assertTrue(any("zapis-z-porady.md" in finding for finding in findings), findings)

    def test_epic_without_sources_is_reported(self):
        epic = filled_epic().replace("(email-kickoff.md)", "")
        findings = validate_epic.validate(epic, TEMPLATE, SOURCES)
        self.assertTrue(any("source" in finding.lower() for finding in findings), findings)

    def test_epic_file_names_are_not_sources(self):
        epic = filled_epic() + "\nNavazuje na mvp-smart-savings.epic.md.\n"
        self.assertEqual(validate_epic.validate(epic, TEMPLATE, SOURCES), [])

    def test_docs_path_reference_is_accepted(self):
        epic = filled_epic() + "\n- Tvrzení (docs/smart-savings/schuzka-business.md)\n"
        self.assertEqual(validate_epic.validate(epic, TEMPLATE, SOURCES), [])


class MainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        docs = self.root / "docs" / "smart-savings"
        docs.mkdir(parents=True)
        for name in SOURCES:
            (docs / name).write_text("x", encoding="utf-8")
        self.outputs = self.root / "outputs" / "smart-savings"
        self.outputs.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, epic_text):
        epic = self.outputs / "mvp.epic.md"
        epic.write_text(epic_text, encoding="utf-8")
        return self.quiet_main(epic)

    def quiet_main(self, epic):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return validate_epic.main([str(epic)], repo_root=self.root, template_path=TEMPLATE_PATH)

    def test_valid_epic_exits_zero(self):
        self.assertEqual(self.run_main(filled_epic()), 0)

    def test_invalid_epic_exits_one(self):
        self.assertEqual(self.run_main(TEMPLATE), 1)

    def test_epic_outside_outputs_project_exits_two(self):
        stray = self.root / "mvp.epic.md"
        stray.write_text(filled_epic(), encoding="utf-8")
        self.assertEqual(self.quiet_main(stray), 2)


if __name__ == "__main__":
    unittest.main()
