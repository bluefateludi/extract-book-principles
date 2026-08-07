from __future__ import annotations

import unittest
from pathlib import Path

import yaml


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
        self.assertEqual(interface["display_name"], "Extract Book Principles")
        self.assertIn("$extract-book-principles", interface["default_prompt"])


if __name__ == "__main__":
    unittest.main()
