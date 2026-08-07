from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PACKAGE = ROOT / "books" / "designing-your-life" / "zh-cn-2017-epub"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Exercise the installed public module entry point outside the checkout."""
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, "-m", "book_principles", *args],
        cwd=tempfile.gettempdir(),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def write_minimal_epub(path: Path) -> None:
    """Create a complete, deterministic EPUB fixture using the standard library."""
    container = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
    package = """<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" unique-identifier="book-id"
 xmlns="http://www.idpf.org/2007/opf"
 xmlns:dc="http://purl.org/dc/elements/1.1/">
  <metadata>
    <dc:identifier id="book-id">urn:isbn:9780000000001</dc:identifier>
    <dc:title>Runtime Fixture Book</dc:title>
    <dc:creator>Fixture Author</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Fixture Press</dc:publisher>
    <dc:date>2026-01-02</dc:date>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="chapter-1" href="chapter-1.xhtml" media-type="application/xhtml+xml"/>
    <item id="chapter-2" href="chapter-2.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="chapter-1"/>
    <itemref idref="chapter-2"/>
  </spine>
</package>
"""
    nav = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head><title>Contents</title></head>
  <body><nav epub:type="toc"><ol>
    <li><a href="chapter-1.xhtml">Chapter 1 Beginning</a></li>
    <li><a href="chapter-2.xhtml">Chapter 2 Next</a></li>
  </ol></nav></body>
</html>
"""
    chapter_1 = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"><body>
  <h1>Beginning</h1>
  <p>The first stable paragraph.</p>
  <p>The second stable paragraph.</p>
</body></html>
"""
    chapter_2 = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"><body>
  <h1>Next</h1><p>This chapter must not appear in chapter one.</p>
</body></html>
"""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        archive.writestr("META-INF/container.xml", container)
        archive.writestr("EPUB/package.opf", package)
        archive.writestr("EPUB/nav.xhtml", nav)
        archive.writestr("EPUB/chapter-1.xhtml", chapter_1)
        archive.writestr("EPUB/chapter-2.xhtml", chapter_2)


class CliTests(unittest.TestCase):
    def test_module_and_console_help_identify_the_entry_point(self) -> None:
        module = run_cli("--help")
        self.assertEqual(module.returncode, 0, module.stdout + module.stderr)
        self.assertTrue(module.stdout.startswith("usage: python -m book_principles"))

        executable = Path(sys.executable).parent / "book-principles"
        self.assertTrue(executable.is_file(), "installed console script is unavailable")
        console = subprocess.run(
            [str(executable), "--help"],
            cwd=tempfile.gettempdir(),
            env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(console.returncode, 0, console.stdout + console.stderr)
        self.assertTrue(console.stdout.startswith("usage: book-principles"))

    def test_inspect_writes_metadata_and_selected_chapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            epub = temporary / "fixture.epub"
            output = temporary / "inspection.json"
            write_minimal_epub(epub)

            result = run_cli("inspect", str(epub), "--chapter", "1", "--output", str(output))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(output.is_file(), "inspect did not create --output")
            inspection = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(inspection["metadata"]["titles"], ["Runtime Fixture Book"])
            self.assertEqual(inspection["metadata"]["creators"], ["Fixture Author"])
            self.assertEqual(inspection["metadata"]["identifiers"], ["urn:isbn:9780000000001"])
            self.assertEqual(inspection["chapter"]["title"], "Chapter 1 Beginning")
            documents = inspection["chapter"]["documents"]
            self.assertEqual(
                [document["doc_path"] for document in documents],
                ["EPUB/chapter-1.xhtml"],
            )
            self.assertEqual(documents[0]["spine_index"], 1)
            self.assertEqual(
                [block["text"] for block in documents[0]["blocks"]],
                ["Beginning", "The first stable paragraph.", "The second stable paragraph."],
            )

    def test_render_then_validate_generated_view(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "designing-your-life" / "zh-cn-2017-epub"
            shutil.copytree(SAMPLE_PACKAGE, package)
            (package / "principles.md").unlink()

            rendered = run_cli("render", str(package))

            self.assertEqual(rendered.returncode, 0, rendered.stdout + rendered.stderr)
            generated = package / "principles.md"
            self.assertTrue(generated.is_file())
            self.assertIn("GENERATED FROM principles.yaml", generated.read_text(encoding="utf-8"))

            validated = run_cli("validate", str(package), "--check-generated")
            self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
            self.assertIn("OK:", validated.stdout)


if __name__ == "__main__":
    unittest.main()
