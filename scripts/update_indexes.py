#!/usr/bin/env python3
"""Regenerate sitemap.xml, events/index.md, materials/index.md and keywords/.

The list of pages, their titles and keywords are taken from the YAML front
matter (trainingMaterial.name and trainingMaterial.keywords) of events/*.md
and materials/*.md, excluding the index.md files in those folders.

The keywords/ folder is fully generated: it gets an index.md listing all
keywords and one page per keyword; other .md files in it are removed.

Usage: python3 scripts/update_indexes.py
Requires: PyYAML (pip install pyyaml)
"""

from pathlib import Path

import re
from collections import Counter

import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://fair4chemnl.github.io/training-material"
SECTIONS = [("materials", "Materials"), ("events", "Events")]
KEYWORDS_DIR = ROOT / "keywords"


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
        pages.append((path, str(name).strip(), parse_keywords(meta.get("keywords"))))
    return pages


def parse_keywords(value):
    """Keywords can be a comma-separated string or a YAML list."""
    if not value:
        return []
    items = value if isinstance(value, list) else str(value).split(",")
    return [str(k).strip() for k in items if str(k).strip()]


def slugify(keyword):
    return re.sub(r"[^a-z0-9]+", "-", keyword.lower()).strip("-")


def md_escape(text):
    return text.replace("[", "\\[").replace("]", "\\]")


def write_index(folder, title, pages):
    lines = [f"# {title}", ""]
    for path, name, _ in pages:
        lines.append(f"* [{md_escape(name)}]({path.name})")
    (ROOT / folder / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_keywords(sections):
    # group keywords case-insensitively: slug -> {folder: [pages]}
    groups, spellings = {}, {}
    for folder, pages in sections:
        for page in pages:
            for keyword in page[2]:
                slug = slugify(keyword)
                if not slug:
                    continue
                spellings.setdefault(slug, Counter())[keyword] += 1
                in_folder = groups.setdefault(slug, {}).setdefault(folder, [])
                if page not in in_folder:
                    in_folder.append(page)

    # show the most used spelling, preferring lowercase on a tie
    labels = {
        slug: max(counts, key=lambda k: (counts[k], k == k.lower()))
        for slug, counts in spellings.items()
    }
    order = sorted(groups, key=lambda slug: labels[slug].lower())

    KEYWORDS_DIR.mkdir(exist_ok=True)
    for old in KEYWORDS_DIR.glob("*.md"):
        if old.name != "index.md" and old.stem not in groups:
            old.unlink()

    lines = ["# Keywords", ""]
    for slug in order:
        count = sum(len(p) for p in groups[slug].values())
        lines.append(f"* [{md_escape(labels[slug])}]({slug}.md) ({count})")
    (KEYWORDS_DIR / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for slug in order:
        lines = [f"# Keyword: {md_escape(labels[slug])}"]
        for folder, title in SECTIONS:
            pages = groups[slug].get(folder)
            if not pages:
                continue
            lines += ["", f"## {title}", ""]
            for path, name, _ in pages:
                lines.append(f"* [{md_escape(name)}](../{folder}/{path.name})")
        lines += ["", "[All keywords](index.md)"]
        (KEYWORDS_DIR / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(order)


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
        for path, *_ in pages:
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
    print(f"keywords: {write_keywords(sections)} pages")


if __name__ == "__main__":
    main()
