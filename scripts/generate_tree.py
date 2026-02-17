#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "tree.json"

SKIP_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".bundle",
    ".sass-cache",
    "_site",
    "vendor",
    "assets",
    "images",
    "scripts",
}

INCLUDE_EXTS = {".md"}


def read_front_matter_permalink(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end_idx = lines[1:].index("---") + 1
    except ValueError:
        return None
    for line in lines[1:end_idx]:
        if line.strip().startswith("permalink:"):
            return line.split(":", 1)[1].strip()
    return None


def url_for_md(path: Path) -> str:
    permalink = read_front_matter_permalink(path)
    if permalink:
        return permalink
    rel = path.relative_to(ROOT).as_posix()
    if path.name.lower() == "readme.md":
        return "/" + str(path.parent.relative_to(ROOT)).replace("\\", "/") + "/"
    return "/" + rel.replace(".md", ".html")


def build_tree(dir_path: Path) -> dict | None:
    items: list[dict] = []

    for entry in sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            if entry.name in SKIP_DIRS:
                continue
            child = build_tree(entry)
            if child:
                items.append(child)
        else:
            if entry.suffix.lower() not in INCLUDE_EXTS:
                continue
            if entry.name.lower() == "readme.md":
                # Directory node will link to README via permalink
                continue
            url = url_for_md(entry)
            items.append(
                {
                    "type": "file",
                    "name": entry.stem.replace("_", " "),
                    "path": entry.relative_to(ROOT).as_posix(),
                    "url": url,
                }
            )

    # Include a directory node only if it has README or children
    readme = dir_path / "README.md"
    has_readme = readme.exists()
    if not items and not has_readme:
        return None

    node = {
        "type": "dir",
        "name": dir_path.name.replace("_", " "),
        "path": dir_path.relative_to(ROOT).as_posix(),
        "url": url_for_md(readme) if has_readme else None,
        "children": items,
    }
    return node


def main() -> None:
    tree = build_tree(ROOT)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(tree, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
