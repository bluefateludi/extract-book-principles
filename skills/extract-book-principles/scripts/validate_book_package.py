#!/usr/bin/env python3
"""Validate a book knowledge package and optionally regenerate principles.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment error
    print("error: PyYAML is required (python -m pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2)


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EXTRACTION_TYPES = {"explicit", "inferred", "adapted", "external"}
CONFIDENCE = {"low", "medium", "high"}
REVIEW_STATUS = {"draft", "reviewing", "verified", "published"}
EVIDENCE_TYPES = {"paraphrase", "short_quote", "synthesis"}
REQUIRED_FILES = {"metadata.yaml", "sources.yaml", "book-map.md", "summary.md", "principles.yaml"}


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def render_principles(data: dict, metadata: dict) -> str:
    lines = [
        "<!-- GENERATED FROM principles.yaml; DO NOT EDIT DIRECTLY. -->",
        "",
        f"# {metadata['title']}：原则",
        "",
        f"> 范围：{metadata.get('scope', {}).get('label', '未注明')}。事实来源为 `principles.yaml`。",
        "",
    ]
    labels = {"explicit": "作者明确表达", "inferred": "归纳", "adapted": "应用改写", "external": "外部来源"}
    for item in data["principles"]:
        lines.extend([
            f"## {item['title']}",
            "",
            item["statement"],
            "",
            f"- ID：`{item['id']}`",
            f"- 类型：{labels[item['extraction_type']]} (`{item['extraction_type']}`)",
            f"- 可信度：`{item['confidence']}`；审核：`{item['review_status']}`",
            "- 应用：" + "；".join(item["applications"]),
            "- 边界：" + "；".join(item["boundaries"]),
            "- 来源：",
        ])
        for ref in item["source_refs"]:
            loc = ref["locator"]
            block = str(loc["block_start"])
            if loc.get("block_end") and loc["block_end"] != loc["block_start"]:
                block += f"–{loc['block_end']}"
            lines.append(
                f"  - `{ref['source_id']}`，第{ref['chapter']}章“{ref['section']}”，"
                f"spine {loc['spine_index']}，`{loc['doc_path']}`，block {block}；{ref['evidence_summary']}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def validate(package: Path) -> tuple[list[str], dict | None, dict | None]:
    errors: list[str] = []
    missing = sorted(name for name in REQUIRED_FILES if not (package / name).is_file())
    errors.extend(f"missing required file: {name}" for name in missing)
    if missing:
        return errors, None, None
    try:
        metadata = load_yaml(package / "metadata.yaml")
        sources_doc = load_yaml(package / "sources.yaml")
        principles_doc = load_yaml(package / "principles.yaml")
    except (OSError, yaml.YAMLError) as error:
        return [f"cannot read YAML: {error}"], None, None

    for document_name, document in (("metadata.yaml", metadata), ("sources.yaml", sources_doc), ("principles.yaml", principles_doc)):
        if not isinstance(document, dict):
            errors.append(f"{document_name}: root must be a mapping")

    if errors:
        return errors, metadata, principles_doc

    for field in ("schema_version", "package_id", "book_id", "edition_id", "title", "authors", "language", "source_format", "scope", "processing"):
        if not metadata.get(field):
            errors.append(f"metadata.yaml: missing {field}")
    for field in ("package_id", "book_id", "edition_id"):
        value = metadata.get(field, "")
        if value and not ID_PATTERN.fullmatch(str(value)):
            errors.append(f"metadata.yaml: invalid {field}: {value}")
    if metadata.get("source_format") not in {"epub", "pdf", "docx", "markdown", "txt", "html", "ocr-pdf"}:
        errors.append("metadata.yaml: unsupported source_format")

    sources = sources_doc.get("sources", [])
    if not isinstance(sources, list) or not sources:
        errors.append("sources.yaml: sources must be a non-empty list")
        sources = []
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        prefix = f"sources.yaml: sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        for field in ("id", "type", "title", "role"):
            if not source.get(field):
                errors.append(f"{prefix} missing {field}")
        source_id = source.get("id", "")
        if source_id in source_ids:
            errors.append(f"{prefix} duplicate id: {source_id}")
        if source_id and not ID_PATTERN.fullmatch(str(source_id)):
            errors.append(f"{prefix} invalid id: {source_id}")
        source_ids.add(source_id)

    if principles_doc.get("package_id") != metadata.get("package_id"):
        errors.append("principles.yaml: package_id does not match metadata.yaml")
    principles = principles_doc.get("principles", [])
    if not isinstance(principles, list) or not principles:
        errors.append("principles.yaml: principles must be a non-empty list")
        principles = []
    principle_ids: set[str] = set()
    for index, item in enumerate(principles):
        prefix = f"principles.yaml: principles[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        for field in ("id", "title", "statement", "extraction_type", "source_refs", "applications", "boundaries", "confidence", "review_status"):
            if not item.get(field):
                errors.append(f"{prefix} missing {field}")
        principle_id = item.get("id", "")
        if principle_id in principle_ids:
            errors.append(f"{prefix} duplicate id: {principle_id}")
        if principle_id and not ID_PATTERN.fullmatch(str(principle_id)):
            errors.append(f"{prefix} invalid id: {principle_id}")
        principle_ids.add(principle_id)
        if item.get("extraction_type") not in EXTRACTION_TYPES:
            errors.append(f"{prefix} invalid extraction_type")
        if item.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix} invalid confidence")
        if item.get("review_status") not in REVIEW_STATUS:
            errors.append(f"{prefix} invalid review_status")
        for list_field in ("applications", "boundaries"):
            if not isinstance(item.get(list_field), list) or not all(isinstance(value, str) and value.strip() for value in item.get(list_field, [])):
                errors.append(f"{prefix} {list_field} must be a non-empty string list")
        refs = item.get("source_refs", [])
        if not isinstance(refs, list):
            errors.append(f"{prefix} source_refs must be a list")
            refs = []
        for ref_index, ref in enumerate(refs):
            ref_prefix = f"{prefix} source_refs[{ref_index}]"
            if ref.get("source_id") not in source_ids:
                errors.append(f"{ref_prefix} unknown source_id: {ref.get('source_id')}")
            for field in ("chapter", "section", "evidence_type", "evidence_summary", "locator"):
                if ref.get(field) in (None, "", {}):
                    errors.append(f"{ref_prefix} missing {field}")
            if ref.get("evidence_type") not in EVIDENCE_TYPES:
                errors.append(f"{ref_prefix} invalid evidence_type")
            locator = ref.get("locator", {})
            for field in ("format", "spine_index", "doc_path", "block_start"):
                if locator.get(field) in (None, ""):
                    errors.append(f"{ref_prefix} locator missing {field}")
            if locator.get("format") != "epub":
                errors.append(f"{ref_prefix} MVP locator format must be epub")
            start, end = locator.get("block_start"), locator.get("block_end", locator.get("block_start"))
            if not isinstance(start, int) or start < 1 or not isinstance(end, int) or end < start:
                errors.append(f"{ref_prefix} invalid block range")
    return errors, metadata, principles_doc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--render", action="store_true", help="regenerate principles.md after validation")
    parser.add_argument("--check-generated", action="store_true", help="fail if principles.md is absent or stale")
    args = parser.parse_args()
    errors, metadata, principles_doc = validate(args.package)
    if not errors and metadata and principles_doc:
        expected = render_principles(principles_doc, metadata)
        generated = args.package / "principles.md"
        if args.render:
            generated.write_text(expected, encoding="utf-8")
        if args.check_generated and (not generated.is_file() or generated.read_text(encoding="utf-8") != expected):
            errors.append("principles.md is missing or stale; run with --render")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.package}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
