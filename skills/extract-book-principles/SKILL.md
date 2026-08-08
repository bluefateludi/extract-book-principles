---
name: extract-book-principles
description: Help users absorb a book's essence by reading the available source, distilling its argument and core principles, preserving honest source boundaries, and turning the result into memorable and practical guidance. Use when a user supplies or points to a book and asks to read, digest, summarize, explain, extract lessons or mental models, apply it to a goal, or create a durable book-essence.md. Work with any book format the current environment can access; use available PDF, document, terminal, OCR, or other tools rather than requiring a bundled parser.
---

# Extract Book Principles

Create one durable, reader-first `book-essence.md` that makes a book understandable, memorable, and usable. Keep file handling subordinate to comprehension.

## Set the scope

1. Identify the exact book, edition, language, source format, and requested scope.
2. Infer the desired depth. Use a concise pass for a quick explanation, a whole-book pass by default, or a goal-focused pass when the user supplies a concrete problem.
3. State material gaps whenever the source is partial, unreadable, abridged, or not the edition claimed.
4. Ask a question only when a missing choice would materially change the result.

## Read with available tools

Use the environment's suitable PDF, document, archive, terminal, browser, vision, or OCR capabilities. Choose the method from the actual source; do not require a particular parser, language runtime, or conversion pipeline.

- Inspect the book's structure before synthesizing it.
- Read the full requested scope. For long books, work section by section, retain compact notes, then reconcile them against the whole argument.
- Preserve useful native locations such as chapter, section, page, paragraph, or e-book location when available. Do not invent precision.
- If reliable access is impossible, explain the limit and offer a narrower result based only on material actually available.

## Protect the source

- Treat copyrighted books and full-text derivatives as private inputs. Never copy them into the Skill, a public repository, or the deliverable.
- Do not move, rename, modify, or delete the user's source unless explicitly requested.
- Prefer paraphrase. Include only necessary short quotations, attribute them, and never reproduce enough text to substitute for the book.
- Distinguish the author's claims from AI inference, adaptation, outside knowledge, and the user's own interpretation.

## Extract the essence

1. Express the central problem, the author's answer, and the argument path.
2. Build a compact thought map showing how the major ideas support, constrain, or lead to one another.
3. Surface the few highlights a reader should notice before presenting detail.
4. Select the smallest set of non-overlapping principles that explains most of the book. Do not turn every chapter heading into a principle.
5. For each principle, explain the claim, why it matters, its source location, and its most important boundary or failure mode.
6. Convert the ideas into low-risk, observable practices. Tailor them to the user's goal without presenting the adaptation as the author's words.
7. Write a few "AI memory sentences": compact recall cues that preserve the book's causal logic, not slogans detached from context.

## Create the deliverable

Read [references/book-essence-template.md](references/book-essence-template.md) before writing. Create a single `book-essence.md` by default when the user asks for a saved artifact; otherwise use the same structure in the response. Put it in the user-specified destination or a sensible workspace location and report the path.

Keep technical details out of the main reading experience. Include parsing, OCR, hashes, conversion notes, or machine-oriented locators only when the user requests an audit trail or when a limitation depends on them.

## Check quality

Read [references/quality-checklist.md](references/quality-checklist.md) and complete the checks before delivery. Keep AI-only work labeled as unverified where exact source claims have not been manually checked. Never imply whole-book coverage from a table of contents, excerpt, summary, or selected chapters.
