---
name: extract-book-principles
description: Help users absorb a book's essence by turning it into a concise mental model, traceable core principles, memorable takeaways, and practical next actions. Use when a user attaches or points to a book and asks to read it, extract its essence, summarize core ideas, identify mental models or lessons, apply the book to a goal, or build a reusable book knowledge package. Support EPUB with bundled deterministic inspection and preserve honest source boundaries for other formats when a suitable parser is available.
---

# Absorb Book Essence

Help the user understand, remember, and apply a book. Treat the knowledge package as the reliable internal representation, not the default user experience.

## Choose the experience

Infer the mode from the request. Do not ask a setup question when the book and intent are already clear.

- Use **quick essence** for requests such as “三分钟讲懂” or “这本书讲了什么”.
- Use **deep absorption** by default when the user asks to absorb, digest, or extract a book's essence.
- Use **goal-focused** when the user supplies a problem, role, project, or life goal; select and adapt only the relevant ideas.
- Use **knowledge package** when the user asks to archive, publish, compare, validate, or reuse the result with AI.

## Read the contracts

Before extracting, read [references/book-package-schema.md](references/book-package-schema.md) for provenance and [references/quality-rubric.md](references/quality-rubric.md) for claim quality. Apply these contracts internally even when delivering only a conversational digest.

## Inspect the source

1. Identify the exact file, edition, format, language, and requested scope without modifying the source.
2. Keep copyrighted books and full-text extracts in ignored private locations. Never copy a private source into the Skill or knowledge package.
3. For EPUB, run `scripts/parse_epub.py` to inspect metadata, TOC, spine, and selected chapters. Bind locators to the registered file hash.
4. For PDF, DOCX, Markdown, TXT, HTML, or OCR PDF, use a suitable parser available in the environment. Preserve native page, section, paragraph, or OCR coordinates when possible. If reliable parsing is unavailable, explain the limitation instead of inventing support.
5. Inspect the whole structure before selecting chapters. State omitted front matter, appendices, or unreadable sections.

For EPUB in an installed project checkout:

```bash
python -m book_principles inspect private/inputs/book.epub --output private/epub-map.json
python -m book_principles inspect private/inputs/book.epub --chapter 1 --output private/chapter-1.json
```

For a source checkout without installation, use `scripts/parse_epub.py`.

## Extract in layers

1. Map the book's central problem, answer, argument path, and chapter roles.
2. Read the selected scope chapter by chapter. Track recurring claims, contrasts, mechanisms, exercises, and qualifications.
3. Select the smallest set of principles that explains most of the book. Merge duplicates and avoid turning every chapter heading into a principle.
4. Classify each principle honestly:
   - `explicit`: the author states the rule or recommendation directly.
   - `inferred`: the principle synthesizes multiple passages.
   - `adapted`: the application extends the source; label the extension as Codex's adaptation.
   - `external`: the claim comes from a separately registered non-book source.
5. Give every principle a concise statement, why it matters, an application, a misuse boundary, confidence, and source evidence.
6. Prefer paraphrases. Use a short quote only when exact wording is necessary, and never reproduce long passages or a chapter substitute.

## Deliver the essence

Lead with reader value, not files, schemas, or processing details. Adapt depth to the request while preserving this order:

1. **一句话精华** — the book's central idea in one sentence.
2. **三分钟掌握** — the problem, proposed answer, and reasoning chain in a compact explanation.
3. **核心原则** — usually 7–15 non-overlapping principles. For each, explain what it means, why it works, how to use it, and where it stops applying.
4. **把书用起来** — three to seven concrete actions or experiments, tailored to the user's goal when one is known.
5. **记住这些就够了** — a compact recall list or mental model.
6. **范围与可信度** — identify the edition and scope, distinguish author claims from inference or adaptation, and disclose gaps.

Do not dump YAML or raw parser output into the response. Cite human-readable chapters or sections near important claims; provide technical locators only when the user requests audit details or when creating files.

## Personalize without distorting

- When the user gives a goal, select relevant principles before generating advice.
- Separate “the author argues” from “applied to your situation, a useful experiment is”.
- Turn advice into low-risk, observable actions rather than generic motivation.
- Preserve meaningful counterexamples and failure conditions.
- Ask at most one follow-up question after delivering initial value when personalization would materially improve the next pass.

## Build a reusable package when needed

Create `books/<book-id>/<edition-id>/` only when the user requests files, the workspace already maintains book packages, or future comparison and reuse matter.

1. Register the edition and hash in `metadata.yaml` and `sources.yaml`.
2. Write `book-map.md` and `summary.md` as authored reading views.
3. Store principles only in `principles.yaml`; generate `principles.md` from it.
4. Keep AI-created work at `draft` or `reviewing`. Use `verified` only after a human checks the registered source.
5. Validate, render, and check generated-file freshness:

```bash
python -m book_principles render books/<book-id>/<edition-id>
python -m book_principles validate books/<book-id>/<edition-id> --check-generated
```

Without installation, use `scripts/validate_book_package.py` with `--render` or `--check-generated`.

## Review before delivery

- Ensure the digest reflects the processed scope rather than the title or table of contents alone.
- Resolve important claims to the exact edition and stable source location.
- Remove repetition, decorative quotations, unsupported certainty, and generic advice.
- Make the result useful to a reader who will not open the YAML files.
- Keep private books and derived full-text extracts outside version control.
