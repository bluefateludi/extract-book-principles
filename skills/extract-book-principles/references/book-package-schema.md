# Book package schema

## Contents

- [Package layout](#package-layout)
- [Metadata](#metadata)
- [Sources](#sources)
- [Principles](#principles)
- [EPUB locators](#epub-locators)
- [Narrative and generated files](#narrative-and-generated-files)
- [Evolution rules](#evolution-rules)

## Package layout

Use this MVP layout:

```text
books/<book-id>/<edition-id>/
├── metadata.yaml
├── sources.yaml
├── book-map.md
├── summary.md
├── principles.yaml
└── principles.md
```

Use lowercase kebab-case IDs. Treat `principles.yaml` as the only fact source for principle content. Generate `principles.md`; begin it with `<!-- GENERATED FROM principles.yaml; DO NOT EDIT DIRECTLY. -->`.

## Metadata

Require:

```yaml
schema_version: "0.1"
package_id: designing-your-life-zh-cn-2017-chapter-1
book_id: designing-your-life
edition_id: zh-cn-2017-epub
title: 斯坦福大学人生设计课
authors: [比尔·博内特, 戴夫·伊万斯]
language: zh-CN
publisher: 中信出版社
publication_date: "2017-12-01"
isbn: "9787508677835"
source_format: epub
scope:
  type: chapter_sample
  label: 第1章及其小节
  chapters: [1]
processing:
  status: reviewing
  extractor: extract-book-principles/0.1
  extracted_at: "2026-08-07"
  source_sha256: <64 lowercase hex characters>
```

The metadata identity fields must match the single primary book entry in `sources.yaml`. The package directory names must match `book_id` and `edition_id`. Use `human_reviewed: true` only after a person checks the registered source; principles cannot be marked `verified` or `published` without it.

Allow `source_format`: `epub`, `pdf`, `docx`, `markdown`, `txt`, `html`, `ocr-pdf`. Keep format-specific parsing details under `processing` or a source entry.

## Sources

Use one registry for book and external sources:

```yaml
schema_version: "0.1"
sources:
  - id: designing-your-life-zh-cn-2017-epub
    type: book
    role: primary
    title: 斯坦福大学人生设计课
    authors: [比尔·博内特, 戴夫·伊万斯]
    language: zh-CN
    publisher: 中信出版社
    publication_date: "2017-12-01"
    isbn: "9787508677835"
    format: epub
    sha256: <64 lowercase hex characters>
    locator_scheme: epub-block-v1
    access: private-local-input
```

Register an independent source before using `external`. Do not register project inspirations as principle evidence unless they actually supply the claim.

Keep the primary book's title, authors, language, publisher, publication date, ISBN, format, and SHA-256 synchronized with `metadata.yaml`. For EPUB, require `locator_scheme: epub-block-v1`.

## Principles

Require this shape:

```yaml
schema_version: "0.1"
package_id: designing-your-life-zh-cn-2017-chapter-1
principles:
  - id: start-from-current-reality
    title: 从真实的当前位置开始
    statement: 先了解当前处境，再决定可行动的设计方向。
    extraction_type: explicit
    source_refs:
      - source_id: designing-your-life-zh-cn-2017-epub
        chapter: 1
        section: 重力问题
        evidence_type: paraphrase
        evidence_summary: 作者把接受真实起点作为人生设计的开始。
        locator:
          format: epub
          spine_index: 8
          doc_path: OEBPS/Text/chapter4-2.xhtml
          block_start: 11
          block_end: 11
    applications:
      - 在制定改变计划前盘点现状和不可改变的约束
    boundaries:
      - 接受现实不等于放弃仍可影响的部分
    confidence: high
    review_status: reviewing
```

Enums:

- `extraction_type`: `explicit`, `inferred`, `adapted`, `external`
- `evidence_type`: `paraphrase`, `short_quote`, `synthesis`
- `confidence`: `low`, `medium`, `high`
- `review_status`: `draft`, `reviewing`, `verified`, `published`

Use at least one non-empty application and boundary. Keep IDs stable after publication. Change a statement materially by editing the same record only when its meaning remains the same; otherwise create a new ID and deprecate the old record in a future schema revision.

## EPUB locators

Bind every EPUB locator to the source file hash. Require:

- chapter number or name;
- section title;
- spine index;
- normalized archive document path;
- 1-based block start and optional inclusive block end.

Define a block as a non-empty heading, paragraph, list item, or blockquote emitted in document order by `parse_epub.py`. Do not claim stable printed pages when the EPUB does not provide them. An EPUB locator is stable only for the registered file hash.

Future locator contracts should preserve the same role while using native coordinates: printed/rendered page plus text block for PDF, OOXML part plus paragraph ID for DOCX, heading plus line/block for text formats, and page image plus OCR block coordinates for OCR PDF.

## Narrative and generated files

Write `book-map.md` as a map of processed chapters, sections, claims, and their relationship. Write `summary.md` as a scope-labeled synthesis. These two files are authored narrative content, not alternate principle databases.

Generate `principles.md` deterministically from `principles.yaml`. Include type, confidence, review status, applications, boundaries, and locators. Do not add facts available only in the generated view.

## Evolution rules

Keep `schema_version` explicit. Add backward-compatible optional fields within `0.x`; increment the version when changing required meanings. Create a new edition directory when source content or locator stability changes. Never overwrite provenance to make a new edition appear equivalent to an old one.
