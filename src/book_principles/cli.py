"""Command-line interface for the book_principles toolkit."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from book_principles.epub import inspect_epub


def _inspect(args: argparse.Namespace) -> int:
    try:
        result = inspect_epub(args.epub, args.chapter)
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, ET.ParseError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


def _validation_errors(package: Path, check_generated: bool) -> tuple[list[str], dict | None, dict | None]:
    from book_principles.package import render_principles, validate

    errors, metadata, principles = validate(package)
    if not errors and check_generated and metadata and principles:
        generated = package / "principles.md"
        expected = render_principles(principles, metadata)
        if not generated.is_file() or generated.read_text(encoding="utf-8") != expected:
            errors.append("principles.md is missing or stale; run the render command")
    return errors, metadata, principles


def _print_validation_result(package: Path, errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {package}")
    return 0


def _validate(args: argparse.Namespace) -> int:
    errors, _, _ = _validation_errors(args.package, args.check_generated)
    return _print_validation_result(args.package, errors)


def _render(args: argparse.Namespace) -> int:
    from book_principles.package import render_principles

    errors, metadata, principles = _validation_errors(args.package, False)
    if errors or metadata is None or principles is None:
        return _print_validation_result(args.package, errors)
    output = args.output or args.package / "principles.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_principles(principles, metadata), encoding="utf-8")
    print(f"OK: {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m book_principles", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    inspect_parser = commands.add_parser("inspect", help="inspect an EPUB")
    inspect_parser.add_argument("epub", type=Path)
    inspect_parser.add_argument("--chapter", help="TOC title substring or numbered chapter")
    inspect_parser.add_argument("--output", type=Path, help="write JSON to this path instead of stdout")
    inspect_parser.set_defaults(handler=_inspect)

    validate_parser = commands.add_parser("validate", help="validate a book knowledge package")
    validate_parser.add_argument("package", type=Path)
    validate_parser.add_argument("--check-generated", action="store_true", help="fail if principles.md is absent or stale")
    validate_parser.set_defaults(handler=_validate)

    render_parser = commands.add_parser("render", help="render principles.md from principles.yaml")
    render_parser.add_argument("package", type=Path)
    render_parser.add_argument("--output", type=Path, help="write Markdown to a different path")
    render_parser.set_defaults(handler=_render)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.handler(args)
