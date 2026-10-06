# Create GitHub issues from a user stories file: create_issues.py outputs/<project>/<slug>.stories.md [--apply]
#
# A script instead of an MCP server: it calls the gh CLI the user is already logged in with.
# Dry run is the default and only prints what would be created. Nothing is created without --apply.
#
# Expected story format (see .github/instructions/user-stories.instructions.md):
#   ### US-01: Title
#   body until the next "### US-" heading
import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

STORY_HEADING = re.compile(r"^### (US-\d+): (.+?)\s*$", re.M)


@dataclass
class Story:
    id: str
    title: str
    body: str

    @property
    def issue_title(self):
        return f"{self.id}: {self.title}"


def parse_stories(markdown):
    matches = list(STORY_HEADING.finditer(markdown))
    stories = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[match.end():end].strip()
        stories.append(Story(id=match.group(1), title=match.group(2), body=body))
    return stories


def gh_command(story, label=None, repo=None):
    command = ["gh", "issue", "create", "--title", story.issue_title, "--body", story.body]
    if label:
        command += ["--label", label]
    if repo:
        command += ["--repo", repo]
    return command


def run_gh(command):
    subprocess.run(command, check=True)


def main(argv, run=run_gh):
    parser = argparse.ArgumentParser(description="Create GitHub issues from a user stories file.")
    parser.add_argument("stories_file", type=Path)
    parser.add_argument("--apply", action="store_true", help="really create the issues (default is a dry run)")
    parser.add_argument("--label", help="label to add to every issue; it must already exist in the repository")
    parser.add_argument("--repo", help="OWNER/REPO, defaults to the repository of the current directory")
    args = parser.parse_args(argv)

    stories = parse_stories(args.stories_file.read_text(encoding="utf-8"))
    if not stories:
        print(f"No stories found in {args.stories_file}. Expected headings like '### US-01: Title'.",
              file=sys.stderr)
        return 1

    if not args.apply:
        print(f"Dry run: {len(stories)} issue(s) would be created:")
        for story in stories:
            print(f"  - {story.issue_title}")
        print("Nothing was created. Run again with --apply after the user confirms the list.")
        return 0

    if run is run_gh and shutil.which("gh") is None:
        print("The gh CLI is not installed or not on PATH.", file=sys.stderr)
        return 1

    for story in stories:
        try:
            run(gh_command(story, args.label, args.repo))
        except subprocess.CalledProcessError as error:
            print(f"gh failed for {story.issue_title} (exit {error.returncode}). Stopped; stories above were created.",
                  file=sys.stderr)
            return 1
        print(f"Created: {story.issue_title}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
