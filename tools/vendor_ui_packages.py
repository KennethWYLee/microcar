"""Fetch pinned public UI assets, or verify the local copies without network access.

Normal mode downloads only the fixed upstream URLs below, verifies every source
SHA-256 before writing, then creates the SVG sprite and Prism bundle. No upstream
installation, package scripts, or build tools are run. --check is read-only and
does not call the network.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
VENDOR = REPO / "assets" / "vendor"
MANIFEST = VENDOR / "manifest.json"
SVG_NS = "http://www.w3.org/2000/svg"

PACKAGES = {
    "lucide": {
        "version": "1.61.0",
        "repository": "https://github.com/lucide-icons/lucide",
        "license": "ISC; MIT for Feather-derived icons (see full LICENSE)",
        "transformation": "Selected SVG geometry combined into symbols; code-2 is the upstream code-xml alias.",
    },
    "fuse": {
        "version": "7.5.0",
        "repository": "https://github.com/krisk/Fuse",
        "license": "Apache-2.0",
        "transformation": "Unmodified full minified ES module.",
    },
    "prism": {
        "version": "1.30.0",
        "repository": "https://github.com/PrismJS/prism",
        "license": "MIT",
        "transformation": "Concatenated core, Python, C-like and Dart components; individual component bytes unchanged.",
    },
}

ICON_HASHES = {
    "search": "283d371c2e433817bb9c0c8310caa6c77fa4177c0f4f1168d9c83b97af7389dc",
    "x": "4a9cdab38fbb96162e7dace28e33f4ca0e49d8963a6162abc3d4691b7d675117",
    "menu": "af6491988ac1ba30dc5414f485bc48713e957e1edb0fbef4a0dd8691c3c21598",
    "chevron-down": "66ea878e72ed3488bb3b464c39dfdccee8d1f78e560dccea40e5e12da0e87e87",
    "arrow-right": "288397fdb73bb4f783cf9eabb726ff47357df1d4e3f1201dd748090579f108b9",
    "arrow-up-right": "50b2503b9d11881142255466b7e3461d022b919735841c321d72003ac9959fe1",
    "book-open": "9b9bed0ff057283d5c5c5a1c71f8d3e927db26a56639603a92fdf7b25961510e",
    "download": "3daeee13ded5a3afa2198b1bb4e2262d163922f97d96ac6ff9953e8ed4fe039d",
    "cpu": "ec83bb69ec029d367d749afc445b39c8e95891ebf99b0400652677c2b149b99c",
    "terminal": "4f9b6488b237757d5cb615ccd07502fa99774826839e2a99017784bdb2596f1a",
    "sparkles": "f5499f33f09d7158151e9bd2ec0faf79ff8fb57292f84fdd7286d96d0f0424d8",
    "code-2": "a6d2110227be375be21da7324d3c09262c1bf019d06bdeab356d515342ab7cce",
    "lightbulb": "e33bbec15b1e64cca958e086850f951c0dc2201cd5778bb3695fda3cb6ea457d",
    "radio": "e55ef723902350caaabb68c8814ba57c4c2d237e0747a5f0520624e6f2f8c861",
    "car": "6d70bc146ca53b9c140a859319df471616c1ee6758bfb31a346d549d1fe92211",
    "circuit-board": "30abef5cc7eaa8fe6121ae4a281c0144cb47e5b73d4ef6b265634c85757f4a66",
    "fan": "6ed585fa7a183086480baf6aaeb531cbe65e977222c6462dcb1e4662a6744b54",
    "network": "626be730feea1e5ea7539fbf78b4a3fcb927ce5d7dc43364f2216908672ac792",
    "check": "7f33acc9a77a61659531044525fc008edebe215bf4dcf1c789c8674ad3277db0",
    "copy": "ea80e566c7a12628a447cb53179b19aea4f60b9143e2becd0d0f20bf260e5718",
    "clock": "e9d3e3acf4d1c280fcf8092293439dc0a4756a908ceb859de144b12451cd1cb9",
    "settings": "0ae27fd0f81999229e3127ac96c5b32edfea448e291d509e76212b917551d66b",
    "compass": "c5a4d147bf48424f48b514712dd61c1b07cb689612a7baef87c88870092c1659",
    "sliders-horizontal": "e43a00e5eb684e6cbb61083bed2528d7a3fa5f265693eb2b5f314cd432aa65f4",
}

PRISM_HASHES = {
    "core": "6caad316dd991f24f8004e0b9c19c055cb5829ff65e973fbee406f96d81b8e7e",
    "python": "ed4385685bcf2d4935c8dbbab4bde16603da1329e092d2bf36c3dadd67e9a85c",
    "clike": "c76ba4e240932bdc75546be30e550f5ba5e13815ff71511c76e9e27ac3072444",
    "dart": "906161333796982dcfee193b58d1cc7e1bf953c158bb25cfd07bf37c85df5e11",
}

EXTRA_SOURCES = {
    "lucide/alias-code-2": (
        "https://raw.githubusercontent.com/lucide-icons/lucide/1.61.0/icons/code-xml.json",
        "15e854f007aa9fbda5799b00468bc46d3c47582c404f549d79b4bac79b733e2b",
    ),
    "lucide/LICENSE": (
        "https://raw.githubusercontent.com/lucide-icons/lucide/1.61.0/LICENSE",
        "b495047bd93a9b06913511076f504daba17d5bbeb3e0650f3bb53a4220329c57",
    ),
    "fuse/fuse.min.mjs": (
        "https://raw.githubusercontent.com/krisk/Fuse/v7.5.0/dist/fuse.min.mjs",
        "5ab524d12492bb233568e9600046e1aaa9623d36ebe689589144f7dc9b1da6f7",
    ),
    "fuse/LICENSE": (
        "https://raw.githubusercontent.com/krisk/Fuse/v7.5.0/LICENSE",
        "cc807e3caa26cdee316bab2ff6fdb508a2f619b74959fe59e513ef6e61635ebe",
    ),
    "prism/LICENSE": (
        "https://raw.githubusercontent.com/PrismJS/prism/v1.30.0/LICENSE",
        "2b947f0901a7ffcf08a89957da9783c0e9c6e72cb6ce8e959f501ab5409e4d2b",
    ),
}

OUTPUT_PATHS = {
    ".gitattributes",
    "lucide/icons.svg",
    "lucide/LICENSE",
    "fuse/fuse.min.mjs",
    "fuse/LICENSE",
    "prism/prism.min.js",
    "prism/LICENSE",
    "README.md",
}

README = """# Self-hosted UI packages

These assets are served from this repository; the website does not need a CDN
connection to load them. Exact versions, upstream URLs, original source SHA-256
values, and output SHA-256 values are recorded in `manifest.json`.
The local `.gitattributes` preserves these verified bytes on Windows checkouts.

| Package | Version | License | Local artifact |
| --- | --- | --- | --- |
| Lucide | 1.61.0 | ISC + MIT for Feather-derived icons | `lucide/icons.svg` |
| Fuse.js | 7.5.0 | Apache-2.0 | `fuse/fuse.min.mjs` |
| Prism | 1.30.0 | MIT | `prism/prism.min.js` |

Full upstream license texts are preserved in each package directory. They apply
to these assets independently of this website's own teaching-content license.

## Loading

- Lucide is a selected SVG symbol sprite. The host SVG supplies `fill: none`,
  `stroke: currentColor`, and its preferred stroke width. Symbols use the original
  24 by 24 viewBox and upstream geometry. `code-2` is the documented upstream alias
  of `code-xml`; its metadata source and hash are recorded in the manifest.
- Fuse is the full ES module; import `fuse/fuse.min.mjs` from a module or via
  dynamic `import()`. It has no runtime dependencies.
- Prism exposes the global `Prism` API with Python and Dart languages. The bundle
  also includes C-like because Dart requires it. Use `data-manual` on its script
  tag, or set `window.Prism.manual = true` before loading, when highlighting is
  controlled by the website. No remote autoloader is included.

## Rebuild and verify

From the repository root:

```powershell
python -B tools/vendor_ui_packages.py --check
python -B tools/vendor_ui_packages.py
```

`--check` reads local files and does not connect to the network or modify files.
Normal mode fetches the pinned upstream sources, rejects any SHA-256 mismatch
before writing, and regenerates the assets and manifest. It does not install
packages or execute upstream scripts. To update a package, review its upstream
release and license, then deliberately update the pinned version, URLs and hashes
in the script before rebuilding.
"""


def source_records() -> dict[str, dict[str, str]]:
    sources = {}
    for name, digest in ICON_HASHES.items():
        upstream_name = "code-xml" if name == "code-2" else name
        sources[f"lucide/{name}"] = {
            "url": f"https://raw.githubusercontent.com/lucide-icons/lucide/1.61.0/icons/{upstream_name}.svg",
            "sha256": digest,
        }
    for name, digest in PRISM_HASHES.items():
        sources[f"prism/{name}"] = {
            "url": f"https://raw.githubusercontent.com/PrismJS/prism/v1.30.0/components/prism-{name}.min.js",
            "sha256": digest,
        }
    for name, (url, digest) in EXTRA_SOURCES.items():
        sources[name] = {"url": url, "sha256": digest}
    return sources


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_source(item: tuple[str, dict[str, str]]) -> tuple[str, bytes]:
    name, source = item
    request = urllib.request.Request(
        source["url"], headers={"User-Agent": "microcar-ui-vendor/1"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read()
    if sha256(data) != source["sha256"]:
        raise ValueError(f"Upstream SHA-256 mismatch: {name}")
    return name, data


def make_sprite(sources: dict[str, bytes]) -> bytes:
    alias_metadata = json.loads(sources["lucide/alias-code-2"])
    aliases = {alias["name"] for alias in alias_metadata.get("aliases", [])}
    if "code-2" not in aliases:
        raise ValueError("The upstream code-2 alias was not confirmed.")

    ET.register_namespace("", SVG_NS)
    sprite = ET.Element(f"{{{SVG_NS}}}svg")
    allowed = {"path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "g"}
    for name in ICON_HASHES:
        source = ET.fromstring(sources[f"lucide/{name}"])
        if source.tag != f"{{{SVG_NS}}}svg" or source.get("viewBox") != "0 0 24 24":
            raise ValueError(f"Unexpected SVG root or viewBox: {name}")
        symbol = ET.SubElement(
            sprite,
            f"{{{SVG_NS}}}symbol",
            {
                "id": name,
                "viewBox": "0 0 24 24",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
        )
        for child in source:
            for element in child.iter():
                if element.tag.removeprefix(f"{{{SVG_NS}}}") not in allowed:
                    raise ValueError(f"Unexpected SVG element: {name}")
                if any(key.lower().startswith("on") for key in element.attrib):
                    raise ValueError(f"Unexpected SVG event attribute: {name}")
            symbol.append(child)
    ET.indent(sprite, space="  ")
    header = "<!-- Lucide 1.61.0 selected icons; ISC/MIT. See LICENSE and ../manifest.json. -->\n"
    return header.encode("utf-8") + ET.tostring(sprite, encoding="utf-8") + b"\n"


def make_outputs(sources: dict[str, bytes]) -> dict[str, bytes]:
    prism_header = b"/*! PrismJS 1.30.0 | core + Python + C-like + Dart | MIT | see LICENSE */\n"
    prism = prism_header + b"\n".join(sources[f"prism/{name}"] for name in PRISM_HASHES) + b"\n"
    return {
        ".gitattributes": b"# Preserve verified upstream bytes on every platform.\n* -text\n",
        "lucide/icons.svg": make_sprite(sources),
        "lucide/LICENSE": sources["lucide/LICENSE"],
        "fuse/fuse.min.mjs": sources["fuse/fuse.min.mjs"],
        "fuse/LICENSE": sources["fuse/LICENSE"],
        "prism/prism.min.js": prism,
        "prism/LICENSE": sources["prism/LICENSE"],
        "README.md": README.encode("utf-8"),
    }


def rebuild() -> None:
    records = source_records()
    with ThreadPoolExecutor(max_workers=8) as pool:
        sources = dict(pool.map(fetch_source, records.items()))
    outputs = make_outputs(sources)
    manifest = {
        "schema_version": 1,
        "packages": PACKAGES,
        "sources": records,
        "outputs": {
            name: {"sha256": sha256(data), "bytes": len(data)}
            for name, data in outputs.items()
        },
    }
    for name, data in outputs.items():
        target = VENDOR / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Vendored {len(PACKAGES)} packages from {len(records)} verified sources.")


def check() -> list[str]:
    if not MANIFEST.is_file():
        return ["Missing assets/vendor/manifest.json; run the vendoring script first."]
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"Cannot read vendor manifest: {exc}"]
    if not isinstance(manifest, dict):
        return ["Vendor manifest must be a JSON object."]
    problems = []
    if manifest.get("schema_version") != 1:
        problems.append("Unsupported vendor manifest schema.")
    if manifest.get("packages") != PACKAGES:
        problems.append("Vendor package versions or transformations differ from the script.")
    if manifest.get("sources") != source_records():
        problems.append("Vendor source URLs or SHA-256 values differ from the script.")
    outputs = manifest.get("outputs", {})
    if not isinstance(outputs, dict) or set(outputs) != OUTPUT_PATHS:
        return problems + ["Unexpected vendor output paths in the manifest."]
    for name in sorted(OUTPUT_PATHS):
        target = VENDOR / name
        expected = outputs[name]
        if not target.is_file():
            problems.append(f"Missing vendor output: {name}")
            continue
        data = target.read_bytes()
        if not isinstance(expected, dict) or expected != {"sha256": sha256(data), "bytes": len(data)}:
            problems.append(f"Vendor output SHA-256 or size mismatch: {name}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify local assets; no network or writes.")
    args = parser.parse_args()
    if args.check:
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Vendor verification passed: {len(PACKAGES)} packages, {len(OUTPUT_PATHS)} assets; offline and read-only.")
        return 0
    try:
        rebuild()
    except (OSError, ValueError, urllib.error.URLError, ET.ParseError) as exc:
        print(f"Vendor rebuild stopped: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
