"""Build search entries from the public navigation, headings and case links only."""

from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "assets" / "search-index.json"


def clean(text: str) -> str:
    return " ".join(text.split())


class PublicPage(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.description = ""
        self.title = ""
        self.nav_links: list[str] = []
        self.headings: list[tuple[str, str]] = []
        self.cases: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.keywords: list[str] = []
        self.chip_depth = 0
        self.sections: list[str] = []
        self.articles: list[str] = []
        self.in_nav = False
        self.heading = ""
        self.heading_text: list[str] = []
        self.heading_id = ""
        self.case_href = ""
        self.case_text: list[str] = []
        self.in_case_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = (attr.get("class") or "").split()
        if tag == "div" and (self.chip_depth or "chip-list" in classes):
            self.chip_depth += 1
        if attr.get("id"):
            self.ids.add(attr["id"] or "")
        if tag == "meta" and attr.get("name") == "description":
            self.description = attr.get("content") or ""
        if tag == "section":
            self.sections.append(attr.get("id") or "")
        if tag == "article":
            self.articles.append(attr.get("id") or "")
        if tag == "nav" and "site-nav" in classes:
            self.in_nav = True
        if tag == "a":
            href = attr.get("href") or ""
            if self.in_nav and href.endswith(".html"):
                self.nav_links.append(href)
            if "case-index-card" in classes:
                self.case_href = href
                self.case_text = []
        if tag == "strong" and self.case_href:
            self.in_case_title = True
        if tag in {"h1", "h2"} or (tag == "h3" and self.articles and self.articles[-1]):
            self.heading = tag
            self.heading_text = []
            self.heading_id = attr.get("id") or (self.articles[-1] if tag == "h3" else next((i for i in reversed(self.sections) if i), ""))

    def handle_data(self, data: str) -> None:
        if self.chip_depth:
            self.keywords.append(data)
        if self.heading:
            self.heading_text.append(data)
        if self.in_case_title:
            self.case_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.chip_depth:
            self.chip_depth -= 1
        if tag == "section" and self.sections:
            self.sections.pop()
        if tag == "article" and self.articles:
            self.articles.pop()
        if tag == "nav":
            self.in_nav = False
        if tag == self.heading:
            text = clean("".join(self.heading_text))
            if tag == "h1":
                self.title = text
            elif self.heading_id and text:
                self.headings.append((self.heading_id, text))
            self.heading = ""
        if tag == "strong":
            self.in_case_title = False
        if tag == "a" and self.case_href:
            title = clean("".join(self.case_text))
            if title:
                self.cases.append((self.case_href, title))
            self.case_href = ""


def parse(path: Path) -> PublicPage:
    page = PublicPage()
    page.feed(path.read_text(encoding="utf-8"))
    return page


def build_entries() -> list[dict[str, str]]:
    home = parse(REPO / "index.html")
    # Keep the existing public course order; never scan source projects or downloads.
    pages = list(dict.fromkeys(["index.html", "setup.html", "bootcamp.html", *home.nav_links]))
    entries: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(url: str, title: str, category: str, summary: str, keywords: str) -> None:
        if url not in seen:
            seen.add(url)
            entries.append({"url": url, "title": title, "category": category,
                            "summary": summary, "keywords": keywords})

    for filename in pages:
        assert Path(filename).name == filename and filename.endswith(".html"), filename
    parsed = {filename: parse(REPO / filename) for filename in pages}
    for filename, page in parsed.items():
        add(filename, page.title, "課程頁面", page.description, clean(page.title + " " + " ".join(page.keywords)))
    for filename, page in parsed.items():
        category = page.title.split("：", 1)[0]
        for anchor, title in page.headings:
            assert anchor in page.ids, (filename, anchor)
            add(f"{filename}#{anchor}", title, category, f"前往「{page.title}」的這個段落。", page.description)
        for href, title in page.cases:
            parts = urlsplit(href)
            assert not parts.path and parts.fragment in page.ids, (filename, href)
            add(filename + href, title, category, f"閱讀「{page.title}」中的案例與程式。", page.title)
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify the checked-in index without writing.")
    args = parser.parse_args()
    entries = build_entries()
    expected = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("Search index is stale; run tools/build_ui_search_index.py.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Public search entries: {len(entries)}; index {'verified' if args.check else 'built'}.")


if __name__ == "__main__":
    main()
