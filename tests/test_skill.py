from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from test_cli import write_minimal_epub


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "extract-book-principles"
DISCOVERY_ENTRY = ROOT / ".agents" / "skills" / "extract-book-principles"


class SkillContractTests(unittest.TestCase):
    def test_repository_discovery_entry_resolves_to_skill(self) -> None:
        self.assertTrue(DISCOVERY_ENTRY.is_symlink())
        self.assertEqual(DISCOVERY_ENTRY.resolve(), SKILL.resolve())

    def test_skill_frontmatter_and_sidebar_metadata(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        _, frontmatter, _ = text.split("---", 2)
        metadata = yaml.safe_load(frontmatter)
        self.assertEqual(metadata["name"], "extract-book-principles")
        self.assertTrue(metadata["description"])

        interface = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))["interface"]
        self.assertEqual(interface["display_name"], "Absorb Book Essence")
        self.assertIn("book", interface["short_description"].lower())
        self.assertIn("essence", interface["default_prompt"].lower())
        self.assertIn("$extract-book-principles", interface["default_prompt"])

    def test_standalone_skill_inspects_all_epub_chapters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            standalone = temporary / "extract-book-principles"
            shutil.copytree(SKILL, standalone)
            epub = temporary / "fixture.epub"
            output = temporary / "inspection.json"
            write_minimal_epub(epub)

            result = subprocess.run(
                [
                    sys.executable,
                    str(standalone / "scripts" / "parse_epub.py"),
                    str(epub),
                    "--all-chapters",
                    "--output",
                    str(output),
                ],
                cwd=temporary,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            inspection = json.loads(output.read_text(encoding="utf-8"))
            self.assertTrue(inspection["coverage"]["complete"])
            self.assertEqual(inspection["coverage"]["processed_chapters"], 2)


if __name__ == "__main__":
    unittest.main()
