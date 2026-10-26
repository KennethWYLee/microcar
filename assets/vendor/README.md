# Self-hosted UI packages

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
