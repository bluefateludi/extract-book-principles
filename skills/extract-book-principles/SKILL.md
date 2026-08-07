---
name: extract-book-principles
description: Extract traceable, actionable principles from books into a versioned knowledge package with one YAML fact source and generated human-readable views. Use when Codex needs to inspect an EPUB, map a book or chapter, summarize it without reproducing long copyrighted passages, distinguish explicit, inferred, adapted, and external claims, create stable source locators, validate a book package, or prepare future PDF, DOCX, Markdown, TXT, HTML, or OCR-PDF ingestion.
---

# Extract Book Principles

Build a knowledge package for both humans and AI. Keep `principles.yaml` as the only fact source for principles; generate `principles.md` from it.

## Read the contracts

Read [references/book-package-schema.md](references/book-package-schema.md) before creating or changing a package. Read [references/quality-rubric.md](references/quality-rubric.md) before extracting principles and during final review.

## Route the input

1. Detect the source format without modifying the original.
2. For EPUB, use `scripts/parse_epub.py`; treat its document path, spine index, and block number as stable within the registered file hash.
3. For PDF, DOCX, Markdown, TXT, HTML, or OCR PDF, stop before extraction unless a suitable parser is available. Preserve the same normalized output concepts: metadata, ordered sections, text blocks, and format-specific locators. Record `source_format` as `pdf`, `docx`, `markdown`, `txt`, `html`, or `ocr-pdf`.
4. For OCR PDF, preserve page image number, OCR engine/version, and text-block coordinates or IDs. Never present OCR text as exact evidence without checking it.

Do not add unsupported format code merely to satisfy routing. Add a parser only when a real input requires it.

## Register provenance

Maintain three distinct layers:

1. Record method and implementation influences in project documentation, never as proof of a book principle.
2. Register the exact book edition and input hash in `metadata.yaml` and `sources.yaml`.
3. Give every principle one or more source references with a format-specific stable locator.

Keep copyrighted source files in an ignored private input directory. Do not copy long passages into committed artifacts. Prefer a concise evidence summary; use only a necessary short quote when exact wording matters.

## Parse an EPUB

Run:

```bash
python scripts/parse_epub.py /private/path/book.epub --output /private/path/epub-map.json
python scripts/parse_epub.py /private/path/book.epub --chapter 1 --output /private/path/chapter-1.json
```

Inspect metadata, TOC, and spine before selecting scope. Treat numbered chapter selection as the chapter heading plus following subsections up to the next numbered chapter. Verify ambiguous TOCs manually.

## Build the package

Create `books/<book-id>/<edition-id>/` with the files required by the schema.

1. Fix the scope and version. Use a new edition ID when pagination, document paths, or content changes.
2. Write `metadata.yaml` and `sources.yaml` before analysis.
3. Write `book-map.md` as the structure and argument path for the processed scope.
4. Write `summary.md` as a concise synthesis, not a replacement copy of the source.
5. Write candidate principles only in `principles.yaml`.
6. Label each principle:
   - `explicit`: the source states the rule or recommendation directly.
   - `inferred`: synthesize a recurring claim from multiple passages.
   - `adapted`: turn source material into a new application; do not attribute the extension verbatim to the author.
   - `external`: derive from a separately registered non-book source.
7. Add stable ID, statement, applications, boundaries, confidence, review status, and evidence locators.
8. Keep AI-created work at `draft` or `reviewing`; use `verified` only after a human checks the registered source.

## Validate and generate views

Run validation, generation, then a stale-output check:

```bash
python scripts/validate_book_package.py books/<book-id>/<edition-id> --render
python scripts/validate_book_package.py books/<book-id>/<edition-id> --check-generated
```

Fix every error. Review the generated Markdown for clarity, provenance labels, and boundaries. Never edit `principles.md` directly.

Also run the Skill Creator validator after changing this skill:

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/extract-book-principles
```

## Review before delivery

Confirm all of the following:

- Preserve one fact source and two reading views.
- Resolve every source reference to a registered source and exact edition.
- Use EPUB chapter, section, spine/document path, and block location when page numbers are unstable.
- Avoid unsupported certainty and mark inference or adaptation honestly.
- State scope gaps and incomplete chapters.
- Keep private books and derived full-text extracts outside version control.
