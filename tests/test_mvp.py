from __future__ import annotations

import hashlib
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "extract-book-principles"
PACKAGE = ROOT / "books" / "designing-your-life" / "zh-cn-2017-epub"


def load_parser_module():
    path = SKILL / "scripts" / "parse_epub.py"
    spec = importlib.util.spec_from_file_location("parse_epub", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MvpTests(unittest.TestCase):
    def test_package_and_generated_view_validate(self) -> None:
        command = [
            sys.executable,
            str(SKILL / "scripts" / "validate_book_package.py"),
            str(PACKAGE),
            "--check-generated",
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_private_epub_locators_resolve_when_available(self) -> None:
        inputs = list((ROOT / "private" / "inputs").glob("*.epub"))
        if not inputs:
            self.skipTest("private EPUB is intentionally absent")
        self.assertEqual(len(inputs), 1, "expected exactly one private MVP EPUB")
        epub = inputs[0]
        parser = load_parser_module()
        parsed = parser.inspect_epub(epub, "1")
        documents = {doc["doc_path"]: doc for doc in parsed["chapter"]["documents"]}
        principles = yaml.safe_load((PACKAGE / "principles.yaml").read_text(encoding="utf-8"))
        metadata = yaml.safe_load((PACKAGE / "metadata.yaml").read_text(encoding="utf-8"))
        digest = hashlib.sha256(epub.read_bytes()).hexdigest()
        self.assertEqual(metadata["processing"]["source_sha256"], digest)
        self.assertEqual(parsed["metadata"]["identifiers"][-1], metadata["isbn"])
        for principle in principles["principles"]:
            for ref in principle["source_refs"]:
                locator = ref["locator"]
                document = documents.get(locator["doc_path"])
                self.assertIsNotNone(document, f"missing document for {principle['id']}")
                self.assertEqual(document["spine_index"], locator["spine_index"])
                self.assertGreaterEqual(locator["block_start"], 1)
                self.assertLessEqual(locator.get("block_end", locator["block_start"]), len(document["blocks"]))

    def test_validator_rejects_an_unknown_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package"
            shutil.copytree(PACKAGE, package)
            principles_path = package / "principles.yaml"
            principles = yaml.safe_load(principles_path.read_text(encoding="utf-8"))
            principles["principles"][0]["source_refs"][0]["source_id"] = "missing-source"
            principles_path.write_text(yaml.safe_dump(principles, allow_unicode=True, sort_keys=False), encoding="utf-8")
            command = [sys.executable, str(SKILL / "scripts" / "validate_book_package.py"), str(package)]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown source_id", result.stdout)


if __name__ == "__main__":
    unittest.main()
