from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from book_principles.package import validate


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PACKAGE = ROOT / "books" / "designing-your-life" / "zh-cn-2017-epub"


class KnowledgePackageContractTests(unittest.TestCase):
    def copy_package(self, directory: str) -> Path:
        root = Path(directory) / "designing-your-life"
        package = root / "zh-cn-2017-epub"
        shutil.copytree(SAMPLE_PACKAGE, package)
        return package

    def test_sample_package_satisfies_cross_file_contracts(self) -> None:
        errors, _, _ = validate(SAMPLE_PACKAGE)
        self.assertEqual(errors, [])

    def test_rejects_schema_and_hash_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.copy_package(directory)
            sources_path = package / "sources.yaml"
            sources = yaml.safe_load(sources_path.read_text(encoding="utf-8"))
            sources["schema_version"] = "9.9"
            sources["sources"][0]["sha256"] = "0" * 64
            sources_path.write_text(
                yaml.safe_dump(sources, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )

            errors, _, _ = validate(package)

            self.assertTrue(any("unsupported schema_version" in error for error in errors))
            self.assertTrue(any("source_sha256 does not match" in error for error in errors))

    def test_rejects_directory_identity_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = self.copy_package(directory)
            metadata_path = package / "metadata.yaml"
            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
            metadata["book_id"] = "different-book"
            metadata_path.write_text(
                yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )

            errors, _, _ = validate(package)

            self.assertIn("metadata.yaml: book_id does not match package directory", errors)


if __name__ == "__main__":
    unittest.main()
