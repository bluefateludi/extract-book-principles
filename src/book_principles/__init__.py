"""Lightweight tools for building and checking book-principle packages."""

from __future__ import annotations

from typing import Any


__all__ = ["inspect_epub", "render_principles", "validate"]
__version__ = "0.1.0"


def __getattr__(name: str) -> Any:
    if name == "inspect_epub":
        from book_principles.epub import inspect_epub

        return inspect_epub
    if name in {"render_principles", "validate"}:
        from book_principles.package import render_principles, validate

        return {"render_principles": render_principles, "validate": validate}[name]
    raise AttributeError(name)
