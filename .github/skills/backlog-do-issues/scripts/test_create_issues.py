import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import create_issues  # noqa: E402

STORIES = """# User stories: MVP úsporných cílů

Úvodní poznámka, která není story.

### US-01: Nastavení úsporného cíle

Jako klient chci nastavit cíl s částkou a datem, abych věděl, kolik mám spořit.

**Akceptační kritéria:**

- Cíl má název, cílovou částku a datum.
- Klient může mít nejvýš 3 aktivní cíle.

### US-02: Doporučený převod

Jako klient chci dostat doporučenou částku k převodu, abych neskončil v mínusu.
"""


class ParseTest(unittest.TestCase):
    def test_parses_ids_titles_and_bodies(self):
        stories = create_issues.parse_stories(STORIES)
        self.assertEqual([story.id for story in stories], ["US-01", "US-02"])
        self.assertEqual(stories[0].title, "Nastavení úsporného cíle")
        self.assertIn("nejvýš 3 aktivní cíle", stories[0].body)
        self.assertNotIn("US-02", stories[0].body)
        self.assertTrue(stories[1].body.startswith("Jako klient"))

    def test_text_before_first_story_is_ignored(self):
        stories = create_issues.parse_stories(STORIES)
        self.assertNotIn("Úvodní poznámka", stories[0].body)

    def test_no_stories_gives_empty_list(self):
        self.assertEqual(create_issues.parse_stories("# Nic\n\nŽádné stories."), [])

    def test_issue_title_contains_id(self):
        story = create_issues.parse_stories(STORIES)[0]
        self.assertEqual(story.issue_title, "US-01: Nastavení úsporného cíle")


class RunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "mvp.stories.md"
        self.file.write_text(STORIES, encoding="utf-8")
        self.calls = []

    def tearDown(self):
        self.tmp.cleanup()

    def fake_run(self, args):
        self.calls.append(args)

    def run_main(self, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = create_issues.main([str(self.file), *extra], run=self.fake_run)
        return code, out.getvalue()

    def test_dry_run_is_default_and_calls_nothing(self):
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(self.calls, [])
        self.assertIn("US-01: Nastavení úsporného cíle", out)
        self.assertIn("--apply", out)

    def test_apply_creates_one_issue_per_story(self):
        code, _ = self.run_main("--apply")
        self.assertEqual(code, 0)
        self.assertEqual(len(self.calls), 2)
        first = self.calls[0]
        self.assertEqual(first[:3], ["gh", "issue", "create"])
        self.assertEqual(first[first.index("--title") + 1], "US-01: Nastavení úsporného cíle")
        self.assertIn("nejvýš 3 aktivní cíle", first[first.index("--body") + 1])

    def test_label_and_repo_are_passed_to_gh(self):
        self.run_main("--apply", "--label", "smart-savings", "--repo", "DXHeroes/github-copilot-workshop")
        first = self.calls[0]
        self.assertEqual(first[first.index("--label") + 1], "smart-savings")
        self.assertEqual(first[first.index("--repo") + 1], "DXHeroes/github-copilot-workshop")

    def test_gh_failure_stops_and_exits_one(self):
        def failing_run(args):
            self.calls.append(args)
            if len(self.calls) == 2:
                raise create_issues.subprocess.CalledProcessError(1, args)

        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = create_issues.main([str(self.file), "--apply"], run=failing_run)
        self.assertEqual(code, 1)
        self.assertIn("Created: US-01", out.getvalue())
        self.assertNotIn("Created: US-02", out.getvalue())

    def test_file_without_stories_exits_one(self):
        self.file.write_text("# Prázdné\n", encoding="utf-8")
        code, _ = self.run_main("--apply")
        self.assertEqual(code, 1)
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
