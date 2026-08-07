#!/usr/bin/env python3
"""Inspect EPUB metadata, navigation, spine order, and stable paragraph blocks.

Uses only the Python standard library. The default output contains no chapter
body. Pass --chapter to include blocks for one TOC entry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET


CONTAINER = "META-INF/container.xml"
CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"
NCX_NS = "http://www.daisy.org/z3986/2005/ncx/"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def resolve(base_file: str, href: str) -> str:
    href = href.split("#", 1)[0]
    return posixpath.normpath(posixpath.join(posixpath.dirname(base_file), href))


class ContentParser(HTMLParser):
    BLOCK_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.tag = ""
        self.parts: list[str] = []
        self.blocks: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.BLOCK_TAGS:
            if self.depth == 0:
                self.tag, self.parts = tag, []
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() not in self.BLOCK_TAGS or self.depth == 0:
            return
        self.depth -= 1
        if self.depth == 0:
            text = clean("".join(self.parts))
            if text:
                self.blocks.append({"tag": self.tag, "text": text})
            self.tag, self.parts = "", []

    def handle_data(self, data: str) -> None:
        if self.depth:
            self.parts.append(data)


def parse_content(raw: bytes) -> list[dict[str, str | int]]:
    parser = ContentParser()
    parser.feed(raw.decode("utf-8", errors="replace"))
    return [
        {"block": index, "tag": item["tag"], "text": item["text"]}
        for index, item in enumerate(parser.blocks, 1)
    ]


def parse_nav(raw: bytes, nav_path: str) -> list[dict[str, str | int]]:
    root = ET.fromstring(raw)
    nav = next(
        (
            node
            for node in root.iter()
            if local(node.tag) == "nav"
            and any(local(k) == "type" and "toc" in (v or "").lower() for k, v in node.attrib.items())
        ),
        None,
    )
    if nav is None:
        return []
    result: list[dict[str, str | int]] = []

    def walk_list(node: ET.Element, level: int) -> None:
        for li in (child for child in node if local(child.tag) == "li"):
            link = next((child for child in li if local(child.tag) == "a" and child.get("href")), None)
            if link is not None:
                result.append({
                    "title": clean("".join(link.itertext())),
                    "doc_path": resolve(nav_path, link.get("href", "")),
                    "level": level,
                })
            for child in li:
                if local(child.tag) == "ol":
                    walk_list(child, level + 1)

    toc_list = next((node for node in nav if local(node.tag) == "ol"), None)
    if toc_list is not None:
        walk_list(toc_list, 1)
    return result


def parse_ncx(raw: bytes, ncx_path: str) -> list[dict[str, str | int]]:
    root = ET.fromstring(raw)
    result: list[dict[str, str | int]] = []

    def walk(point: ET.Element, level: int) -> None:
        label = point.find(f"{{{NCX_NS}}}navLabel/{{{NCX_NS}}}text")
        content = point.find(f"{{{NCX_NS}}}content")
        if content is not None and content.get("src"):
            result.append({
                "title": clean(label.text if label is not None else ""),
                "doc_path": resolve(ncx_path, content.get("src", "")),
                "level": level,
            })
        for child in point.findall(f"{{{NCX_NS}}}navPoint"):
            walk(child, level + 1)

    nav_map = root.find(f".//{{{NCX_NS}}}navMap")
    if nav_map is not None:
        for point in nav_map.findall(f"{{{NCX_NS}}}navPoint"):
            walk(point, 1)
    return result


def select_toc(toc: list[dict], selector: str) -> tuple[int, dict]:
    if selector.isdigit():
        patterns = [rf"^\s*第?\s*{selector}\s*[章节章]", rf"^\s*chapter\s+{selector}\b"]
        for index, item in enumerate(toc):
            if any(re.search(pattern, item["title"], re.I) for pattern in patterns):
                return index, item
        index = int(selector) - 1
        if 0 <= index < len(toc):
            return index, toc[index]
    matches = [(index, item) for index, item in enumerate(toc) if selector.casefold() in item["title"].casefold()]
    if len(matches) == 1:
        return matches[0]
    raise ValueError(f"chapter selector matched {len(matches)} TOC entries: {selector!r}")


def is_numbered_chapter(title: str) -> bool:
    return bool(re.search(r"^\s*(?:第\s*\d+\s*章|chapter\s+\d+\b)", title, re.I))


def inspect_epub(path: Path, chapter: str | None) -> dict:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with zipfile.ZipFile(path) as archive:
        container = ET.fromstring(archive.read(CONTAINER))
        rootfile = container.find(f".//{{{CONTAINER_NS}}}rootfile")
        if rootfile is None or not rootfile.get("full-path"):
            raise ValueError("EPUB container has no rootfile")
        opf_path = rootfile.get("full-path", "")
        opf = ET.fromstring(archive.read(opf_path))

        def values(name: str) -> list[str]:
            return [clean(node.text) for node in opf.findall(f".//{{{DC_NS}}}{name}") if clean(node.text)]

        manifest: dict[str, dict[str, str]] = {}
        for item in opf.findall(f".//{{{OPF_NS}}}manifest/{{{OPF_NS}}}item"):
            item_id = item.get("id", "")
            manifest[item_id] = {
                "doc_path": resolve(opf_path, item.get("href", "")),
                "media_type": item.get("media-type", ""),
                "properties": item.get("properties", ""),
            }

        spine_node = opf.find(f".//{{{OPF_NS}}}spine")
        spine: list[dict[str, str | int]] = []
        if spine_node is not None:
            for index, itemref in enumerate(spine_node.findall(f"{{{OPF_NS}}}itemref"), 1):
                item = manifest.get(itemref.get("idref", ""), {})
                if item:
                    spine.append({"spine_index": index, "doc_path": item["doc_path"], "linear": itemref.get("linear", "yes")})

        toc: list[dict[str, str | int]] = []
        nav_item = next((item for item in manifest.values() if "nav" in item["properties"].split()), None)
        if nav_item:
            toc = parse_nav(archive.read(nav_item["doc_path"]), nav_item["doc_path"])
        if not toc and spine_node is not None and spine_node.get("toc") in manifest:
            ncx_item = manifest[spine_node.get("toc", "")]
            toc = parse_ncx(archive.read(ncx_item["doc_path"]), ncx_item["doc_path"])

        output = {
            "input": {"filename": path.name, "sha256": digest},
            "epub": {"opf_path": opf_path},
            "metadata": {
                "titles": values("title"),
                "creators": values("creator"),
                "languages": values("language"),
                "identifiers": values("identifier"),
                "publishers": values("publisher"),
                "dates": values("date"),
            },
            "toc": toc,
            "spine": spine,
        }
        if chapter:
            selected_index, selected = select_toc(toc, chapter)
            selected_level = int(selected.get("level", 1))
            entries = [selected]
            for item in toc[selected_index + 1 :]:
                if is_numbered_chapter(str(selected["title"])):
                    if is_numbered_chapter(str(item["title"])):
                        break
                elif int(item.get("level", 1)) <= selected_level:
                    break
                entries.append(item)
            documents = []
            for entry in entries:
                doc_path = str(entry["doc_path"])
                spine_item = next((item for item in spine if item["doc_path"] == doc_path), None)
                documents.append({
                    **entry,
                    "spine_index": spine_item["spine_index"] if spine_item else None,
                    "blocks": parse_content(archive.read(doc_path)),
                })
            output["chapter"] = {
                "title": selected["title"],
                "documents": documents,
            }
        return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", type=Path)
    parser.add_argument("--chapter", help="TOC title substring or numbered chapter")
    parser.add_argument("--output", type=Path, help="write JSON to this path instead of stdout")
    args = parser.parse_args()
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


if __name__ == "__main__":
    raise SystemExit(main())
