from __future__ import annotations

import argparse
import re
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree


REPO = Path(__file__).resolve().parents[1]
EMAIL_RE = re.compile(rb"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
CONTACT_REPLACEMENT = "聯絡方式未公開".encode("utf-8")
WIFI_ASSIGNMENT_RE = re.compile(
    rb'(?P<prefix>\b(?:char\s+)?(?P<name>ssid|pass(?:word)?)\s*(?:\[\s*\])?\s*=\s*")'
    rb'(?P<value>[^"\r\n]*)'
    rb'(?P<suffix>")',
    re.IGNORECASE,
)
PPTX_TEXT_MEMBERS = (".xml", ".rels")
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


def _rewrite_zip(path: Path, transform) -> None:
    with zipfile.ZipFile(path, "r") as source:
        members = [(info, source.read(info.filename)) for info in source.infolist()]

    with tempfile.NamedTemporaryFile(
        prefix=f"{path.stem}-", suffix=path.suffix, dir=path.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
    try:
        with zipfile.ZipFile(temporary, "w") as target:
            for info, data in members:
                result = transform(info, data)
                if result is None:
                    continue
                target.writestr(info, result)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def sanitize_wifi_archive(path: Path) -> None:
    def transform(info: zipfile.ZipInfo, data: bytes) -> bytes:
        if Path(info.filename).suffix.lower() not in TEXT_ARCHIVE_SUFFIXES:
            return data

        def replace(match: re.Match[bytes]) -> bytes:
            name = match.group("name").lower()
            placeholder = b"YOUR_WIFI_SSID" if name == b"ssid" else b"YOUR_WIFI_PASSWORD"
            return match.group("prefix") + placeholder + match.group("suffix")

        return WIFI_ASSIGNMENT_RE.sub(replace, data)

    _rewrite_zip(path, transform)


def remove_ide_files_from_zip(path: Path) -> None:
    def transform(info: zipfile.ZipInfo, data: bytes) -> bytes | None:
        parts = Path(info.filename.replace("\\", "/")).parts
        if any(part.lower() in {".idea", ".vscode", "__macosx"} for part in parts):
            return None
        if Path(info.filename).name.lower() in {".ds_store", "thumbs.db"}:
            return None
        return data

    _rewrite_zip(path, transform)


def sanitize_pptx(path: Path) -> None:
    core_fields = {
        "creator",
        "lastModifiedBy",
        "title",
        "subject",
        "description",
        "keywords",
        "category",
        "contentStatus",
    }
    app_fields = {"Company", "Manager"}

    def transform(info: zipfile.ZipInfo, data: bytes) -> bytes | None:
        normalized = info.filename.replace("\\", "/").lower()
        if normalized == "docprops/custom.xml":
            root = ElementTree.fromstring(data)
            for child in list(root):
                root.remove(child)
            data = ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)
        elif normalized == "docprops/core.xml":
            root = ElementTree.fromstring(data)
            for node in root.iter():
                if node.tag.rsplit("}", 1)[-1] in core_fields:
                    node.text = None
            data = ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)
        elif normalized == "docprops/app.xml":
            root = ElementTree.fromstring(data)
            for node in root.iter():
                if node.tag.rsplit("}", 1)[-1] in app_fields:
                    node.text = None
            data = ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)
        if normalized.endswith(PPTX_TEXT_MEMBERS):
            data = EMAIL_RE.sub(CONTACT_REPLACEMENT, data)
        return data

    _rewrite_zip(path, transform)


def sanitize_pdf(path: Path) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as exc:  # pragma: no cover - environment diagnostic
        raise RuntimeError("pypdf is required to sanitize PDF metadata") from exc

    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(
        {
            "/Author": "",
            "/Creator": "",
            "/Producer": "",
            "/Title": "",
            "/Subject": "",
            "/Keywords": "",
        }
    )
    with tempfile.NamedTemporaryFile(
        prefix=f"{path.stem}-", suffix=path.suffix, dir=path.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
    try:
        with temporary.open("wb") as handle:
            writer.write(handle)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def sanitize_repo(repo: Path) -> None:
    for name in ("ameba-ai.zip", "ameba-nn.zip"):
        sanitize_wifi_archive(repo / "downloads" / "extensions" / "other-car" / name)
    remove_ide_files_from_zip(
        repo / "downloads" / "extensions" / "board-library" / "mango-library.zip"
    )
    for path in sorted((repo / "downloads").rglob("*.pptx")):
        sanitize_pptx(path)
    for path in sorted((repo / "downloads").rglob("*.pdf")):
        sanitize_pdf(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove private credentials, personal metadata, and IDE files from public downloads."
    )
    parser.add_argument("--repo", type=Path, default=REPO)
    args = parser.parse_args()
    sanitize_repo(args.repo.resolve())


if __name__ == "__main__":
    main()
