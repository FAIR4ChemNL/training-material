#!/usr/bin/env python3
"""Regenerate sitemap.xml, events/index.md and materials/index.md.

The list of pages and their titles are taken from the YAML front matter
(trainingMaterial.name) of events/*.md and materials/*.md, excluding the
index.md files in those folders.

Usage: python3 scripts/update_indexes.py
Requires: PyYAML (pip install pyyaml)
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://fair4chemnl.github.io/training-material"
SECTIONS = [("materials", "Materials"), ("events", "Events")]


def read_front_matter(path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if not text.startswith("---\n") or len(parts) < 3:
        raise ValueError(f"{path}: no YAML front matter found")
    return yaml.safe_load(parts[1]) or {}


def sort_key(path):
    return (0, int(path.stem), "") if path.stem.isdigit() else (1, 0, path.stem)


def collect(folder):
    pages = []
    for path in sorted((ROOT / folder).glob("*.md"), key=sort_key):
        if path.name == "index.md":
            continue
        meta = read_front_matter(path).get("trainingMaterial") or {}
        name = meta.get("name")
        if not name:
            raise ValueError(f"{path}: missing trainingMaterial.name in YAML")
        pages.append((path, str(name).strip()))
    return pages


def write_index(folder, title, pages):
    lines = [f"# {title}", ""]
    for path, name in pages:
        name = name.replace("[", "\\[").replace("]", "\\]")
        lines.append(f"* [{name}]({path.name})")
    (ROOT / folder / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sitemap(sections):
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<urlset",
        '      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '      http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
    ]
    for folder, pages in sections:
        out += ["", f"<!-- {folder} -->"]
        for path, _ in pages:
            out += [
                "<url>",
                f"  <loc>{BASE_URL}/{folder}/{path.stem}</loc>",
                "  <priority>1.00</priority>",
                "  <changefreq>monthly</changefreq>",
                "</url>",
            ]
    out += ["", "</urlset>"]
    (ROOT / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    sections = []
    for folder, title in SECTIONS:
        pages = collect(folder)
        write_index(folder, title, pages)
        sections.append((folder, pages))
        print(f"{folder}: {len(pages)} pages")
    write_sitemap(sections)


if __name__ == "__main__":
    main()
