#!/usr/bin/env python3
"""Stable Skill entry point for self-contained EPUB inspection."""

from __future__ import annotations

from epub_inspector import inspect_epub, main


__all__ = ["inspect_epub", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
