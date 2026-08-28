from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
import zipfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit
from xml.etree import ElementTree


REPO = Path(__file__).resolve().parents[1]
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
SEVEN_Z_SIGNATURE = b"7z\xbc\xaf\x27\x1c"
EMAIL_RE = re.compile(rb"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
WIFI_ASSIGNMENT_RE = re.compile(
    rb'\b(?:char\s+)?(?P<name>ssid|pass(?:word)?)\s*(?:\[\s*\])?\s*=\s*"'
    rb'(?P<value>[^"\r\n]*)"',
    re.IGNORECASE,
)
TEXT_ARCHIVE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".ino",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
PROHIBITED_MEDIA = {
    "photo-classroom-overview.jpg",
    "photo-line-following-scene.jpg",
    "photo-student-work.jpg",
    "photo-teacher-demo.jpg",
    "real-bootcamp-classroom.jpg",
    "real-bootcamp-desk.jpg",
    "video-line-following-demo-poster.jpg",
    "video-line-following-students-poster.jpg",
    "video-line-following-demo.mp4",
    "video-line-following-students.mp4",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.refs: list[tuple[str, str]] = []
        self.image_alt: list[str | None] = []
        self.h1_count = 0
        self.has_title = False
        self.has_viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "a" and values.get("name"):
            self.ids.append(values["name"] or "")
        for attr in ("href", "src"):
            if values.get(attr):
                self.refs.append((attr, values[attr] or ""))
        if tag == "img":
            self.image_alt.append(values.get("alt"))
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.has_title = True
        if tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = True


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def local_target(page: Path, raw_url: str) -> tuple[Path, str] | None:
    parts = urlsplit(raw_url)
    if parts.scheme.lower() in EXTERNAL_SCHEMES or parts.netloc:
        return None
    raw_path = unquote(parts.path)
    if raw_path.startswith("/"):
        target = REPO / raw_path.lstrip("/")
    elif raw_path:
        target = page.parent / raw_path
    else:
        target = page
    return target.resolve(), unquote(parts.fragment)


def verify_html(errors: list[str]) -> tuple[int, int]:
    pages = sorted(REPO.glob("*.html"))
    parsed = {page.resolve(): parse_page(page) for page in pages}
    ref_count = 0
    for page in pages:
        parser = parsed[page.resolve()]
        if not parser.has_title:
            errors.append(f"Missing title: {page.name}")
        if not parser.has_viewport:
            errors.append(f"Missing viewport: {page.name}")
        if parser.h1_count != 1:
            errors.append(f"Expected one h1 in {page.name}, found {parser.h1_count}")
        if any(alt is None or not alt.strip() for alt in parser.image_alt):
            errors.append(f"Image without alt text: {page.name}")
        duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
        if duplicates:
            errors.append(f"Duplicate ids in {page.name}: {', '.join(duplicates)}")

        for _, raw_url in parser.refs:
            target_info = local_target(page.resolve(), raw_url)
            if target_info is None:
                continue
            ref_count += 1
            target, fragment = target_info
            if not target.exists():
                errors.append(f"Missing local target from {page.name}: {raw_url}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target)
                if target_parser is None:
                    target_parser = parse_page(target)
                    parsed[target] = target_parser
                if fragment not in target_parser.ids:
                    errors.append(f"Missing fragment from {page.name}: {raw_url}")
    return len(pages), ref_count


def verify_code_viewer(errors: list[str]) -> tuple[int, int]:
    script = (REPO / "script.js").read_text(encoding="utf-8")
    keys = set(re.findall(r'^  "([^"]+)": \{', script, flags=re.MULTILINE))
    keys.update(re.findall(r'^codePages\["([^"]+)"\]\s*=\s*\{', script, flags=re.MULTILINE))
    paths = re.findall(r'^\s*path:\s*"([^"]+)"', script, flags=re.MULTILINE)
    for raw_path in paths:
        if not (REPO / raw_path).exists():
            errors.append(f"Missing code viewer source: {raw_path}")

    used_keys: set[str] = set()
    for page in REPO.glob("*.html"):
        for raw_url in re.findall(r'href="([^"]*code-viewer\.html\?[^"#]+)"', page.read_text(encoding="utf-8")):
            used_keys.update(parse_qs(urlsplit(raw_url).query).get("file", []))
    used_keys.update(
        re.findall(
            r'attachInlineCodeBlock\([^,]+,[^,]+,\s*"([^"]+)"',
            script,
        )
    )
    for key in sorted(used_keys - keys):
        errors.append(f"Unknown code viewer key: {key}")
    return len(paths), len(used_keys)


def verify_python(errors: list[str]) -> int:
    files = sorted((REPO / "downloads").rglob("*.py")) + sorted((REPO / "tools").glob("*.py"))
    for path in files:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"Python syntax error: {path.relative_to(REPO)}:{exc.lineno}: {exc.msg}")
    return len(files)


def is_placeholder(value: bytes) -> bool:
    upper = value.strip().upper()
    return not upper or upper.startswith(b"YOUR_WIFI_") or upper in {
        b"SSID",
        b"PASSWORD",
        b"WIFI_SSID",
        b"WIFI_PASSWORD",
    }


def verify_zip_privacy(path: Path, archive: zipfile.ZipFile, errors: list[str]) -> None:
    relative = path.relative_to(REPO)
    for member in archive.infolist():
        member_path = Path(member.filename.replace("\\", "/"))
        lowered_parts = {part.lower() for part in member_path.parts}
        if lowered_parts.intersection({".idea", ".vscode", "__macosx"}) or member_path.name.lower() in {
            ".ds_store",
            "thumbs.db",
        }:
            errors.append(f"Private IDE/system file in {relative}: {member.filename}")
        if member_path.suffix.lower() not in TEXT_ARCHIVE_SUFFIXES:
            continue
        data = archive.read(member)
        for match in WIFI_ASSIGNMENT_RE.finditer(data):
            if not is_placeholder(match.group("value")):
                errors.append(f"Hard-coded Wi-Fi value in {relative}: {member.filename}")
                break


def verify_pptx_privacy(path: Path, archive: zipfile.ZipFile, errors: list[str]) -> None:
    relative = path.relative_to(REPO)
    metadata_fields = {
        "creator",
        "lastModifiedBy",
        "Company",
        "Manager",
        "title",
        "subject",
        "description",
        "keywords",
    }
    for member in archive.infolist():
        normalized = member.filename.replace("\\", "/").lower()
        if not normalized.endswith((".xml", ".rels")):
            continue
        data = archive.read(member)
        if EMAIL_RE.search(data):
            errors.append(f"Published email address in {relative}: {member.filename}")
        if normalized in {"docprops/core.xml", "docprops/app.xml", "docprops/custom.xml"}:
            try:
                root = ElementTree.fromstring(data)
            except ElementTree.ParseError:
                errors.append(f"Invalid metadata XML in {relative}: {member.filename}")
                continue
            for node in root.iter():
                local_name = node.tag.rsplit("}", 1)[-1]
                if local_name in metadata_fields and (node.text or "").strip():
                    errors.append(f"Personal document metadata in {relative}: {local_name}")


def verify_pdf_privacy(path: Path, errors: list[str]) -> None:
    try:
        from pypdf import PdfReader
    except ImportError:
        errors.append("pypdf is unavailable; PDF privacy metadata was not checked")
        return
    try:
        metadata = PdfReader(path).metadata or {}
    except Exception as exc:
        errors.append(f"Unreadable PDF metadata in {path.relative_to(REPO)}: {exc}")
        return
    for field in ("/Author", "/Creator", "/Title", "/Subject", "/Keywords"):
        if str(metadata.get(field, "")).strip():
            errors.append(f"Personal PDF metadata in {path.relative_to(REPO)}: {field}")


def verify_downloads(errors: list[str]) -> tuple[int, int, int]:
    archive_count = 0
    pdf_count = 0
    seven_z_count = 0
    for path in sorted((REPO / "downloads").rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in {".zip", ".pptx"}:
            archive_count += 1
            try:
                with zipfile.ZipFile(path) as archive:
                    bad_member = archive.testzip()
                    if suffix == ".zip":
                        verify_zip_privacy(path, archive, errors)
                    else:
                        verify_pptx_privacy(path, archive, errors)
                if bad_member:
                    errors.append(f"Damaged archive member in {path.relative_to(REPO)}: {bad_member}")
            except zipfile.BadZipFile:
                errors.append(f"Invalid archive: {path.relative_to(REPO)}")
        elif suffix == ".pdf":
            pdf_count += 1
            if path.read_bytes()[:5] != b"%PDF-":
                errors.append(f"Invalid PDF signature: {path.relative_to(REPO)}")
            else:
                verify_pdf_privacy(path, errors)
        elif suffix == ".7z":
            seven_z_count += 1
            if path.read_bytes()[:6] != SEVEN_Z_SIGNATURE:
                errors.append(f"Invalid 7z signature: {path.relative_to(REPO)}")
    return archive_count, pdf_count, seven_z_count


def verify_media_privacy(errors: list[str]) -> None:
    assets = REPO / "assets"
    for name in sorted(PROHIBITED_MEDIA):
        if (assets / name).exists():
            errors.append(f"Original identifying media remains public: assets/{name}")
    for path in sorted(assets.rglob("*.mp4")):
        errors.append(f"Public classroom video requires separate privacy review: {path.relative_to(REPO)}")
    try:
        from PIL import ExifTags, Image
    except ImportError:
        errors.append("Pillow is unavailable; image metadata was not checked")
        return
    private_tags = {"Artist", "Copyright", "GPSInfo", "ImageDescription", "UserComment", "XPAuthor"}
    for path in sorted(assets.rglob("*")):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        try:
            with Image.open(path) as image:
                found = {
                    ExifTags.TAGS.get(tag_id, str(tag_id))
                    for tag_id, value in image.getexif().items()
                    if value not in (None, "", b"")
                }
        except Exception as exc:
            errors.append(f"Unreadable image metadata in {path.relative_to(REPO)}: {exc}")
            continue
        for tag in sorted(found.intersection(private_tags)):
            errors.append(f"Private image metadata in {path.relative_to(REPO)}: {tag}")


def verify_css(errors: list[str]) -> None:
    css = (REPO / "styles.css").read_text(encoding="utf-8")
    required = (
        ".case-code-card pre",
        "color: #101820 !important;",
        "background: #ffffff !important;",
    )
    for snippet in required:
        if snippet not in css:
            errors.append(f"Missing readable code style: {snippet}")


def verify_javascript(errors: list[str]) -> None:
    try:
        result = subprocess.run(
            ["node", "--check", str(REPO / "script.js")],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        errors.append("Node.js is unavailable; script.js was not syntax checked")
        return
    if result.returncode:
        errors.append(f"JavaScript syntax error: {result.stderr.strip()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the static course website and downloads.")
    parser.parse_args()
    errors: list[str] = []

    html_count, ref_count = verify_html(errors)
    viewer_paths, viewer_keys = verify_code_viewer(errors)
    python_count = verify_python(errors)
    archive_count, pdf_count, seven_z_count = verify_downloads(errors)
    verify_media_privacy(errors)
    verify_css(errors)
    verify_javascript(errors)

    uf2_files = list(REPO.rglob("*.uf2"))
    if uf2_files:
        errors.extend(f"Local UF2 is not allowed: {path.relative_to(REPO)}" for path in uf2_files)
    if (REPO / "downloads" / "firmware").exists():
        errors.append("Local firmware directory is not allowed: downloads/firmware")

    print(f"HTML pages: {html_count}")
    print(f"Local references and fragments: {ref_count}")
    print(f"Code viewer paths / used keys: {viewer_paths} / {viewer_keys}")
    print(f"Python files parsed: {python_count}")
    print(f"ZIP/PPTX, PDF, 7z checked: {archive_count}, {pdf_count}, {seven_z_count}")
    if errors:
        print("\nVerification failed:")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)
    print("Website verification passed.")


if __name__ == "__main__":
    main()
