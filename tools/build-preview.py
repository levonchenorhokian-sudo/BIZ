#!/usr/bin/env python3
"""Build a single-file, self-contained preview of site/ for publishing as an Artifact.

The published Artifact runs under a strict CSP that blocks every external host, so
everything the page needs has to be inlined:

  - local <script src> and <link rel=stylesheet> become inline <script>/<style>
  - Google Fonts links are replaced with @font-face data URIs (real Barlow)
  - the mannequin.html iframe (three.js + 7.3MB of textures) is swapped for a still,
    keeping the artifact small and fast to load in a side panel

The repo's site/ is never modified. Output goes to preview/index.html.

Usage:  python3 tools/build-preview.py
"""

import base64
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "preview" / "index.html"
FONT_DIR = Path("/tmp/fonts/package/files")

# (css family name, fontsource file prefix, weights)
FONTS = [
    ("Barlow", "barlow-latin", [400, 500, 600]),
    ("Barlow Condensed", "barlow-condensed-latin", [500, 600, 700]),
]


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def font_css() -> str:
    """@font-face rules with woff2 inlined, so type renders correctly under CSP."""
    out = []
    missing = []
    for family, prefix, weights in FONTS:
        for w in weights:
            f = FONT_DIR / f"{prefix}-{w}-normal.woff2"
            if not f.exists():
                missing.append(f.name)
                continue
            out.append(
                f"@font-face{{font-family:'{family}';font-style:normal;"
                f"font-weight:{w};font-display:swap;"
                f"src:url({data_uri(f, 'font/woff2')}) format('woff2');}}"
            )
    if missing:
        print(f"  ! missing font files (will fall back): {', '.join(missing)}")
    return "\n".join(out)


def mannequin_srcdoc() -> str:
    """A still of the 3D viewer. three.js + textures are too heavy for an artifact."""
    shot = SITE / "screenshots" / "preview-mannequin.png"
    if shot.exists():
        img = (
            f'<img src="{data_uri(shot, "image/png")}" alt="3D dress form"'
            ' style="max-width:100%;max-height:100%;object-fit:contain">'
        )
        note = "3D viewer — still image in preview. Run the site locally to spin it."
    else:
        img = ""
        note = "3D viewer unavailable in preview."
    return (
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;height:100%;display:grid;place-items:center;"
        "background:#f2f2f0;font:12px/1.4 system-ui,sans-serif;color:#8a8a86}"
        "figure{margin:0;display:grid;gap:6px;place-items:center;padding:8px}</style>"
        f"<figure>{img}<figcaption>{note}</figcaption></figure>"
    )


def build() -> None:
    doc = (SITE / "index.html").read_text(encoding="utf-8")

    # 1. Drop Google Fonts (CSP blocks the CDN); real faces are inlined instead.
    doc = re.sub(
        r'[ \t]*<link[^>]*(fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>\n?',
        "", doc,
    )

    # 2. Inline local stylesheets.
    def sub_css(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith(("http://", "https://", "//")):
            return m.group(0)
        p = (SITE / href).resolve()
        if not p.exists():
            print(f"  ! stylesheet not found, left as-is: {href}")
            return m.group(0)
        print(f"  inlined css   {href}")
        return "<style>\n" + p.read_text(encoding="utf-8") + "\n</style>"

    doc = re.sub(
        r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s*/?>', sub_css, doc
    )

    # 3. Inline local scripts, preserving document order.
    def sub_js(m: re.Match) -> str:
        src = m.group(1)
        if src.startswith(("http://", "https://", "//")):
            return m.group(0)
        p = (SITE / src.lstrip("./")).resolve()
        if not p.exists():
            print(f"  ! script not found, left as-is: {src}")
            return m.group(0)
        body = p.read_text(encoding="utf-8")
        # The dc-runtime parses documentElement.outerHTML to find the <x-dc>
        # template. If its source is inlined as plain text, it matches its own
        # source instead of the real template and renders its own code. Ship
        # any such file base64-encoded and eval it synchronously at the same
        # document position, so the source is never literal HTML text.
        if "x-dc" in body:
            b64 = base64.b64encode(body.encode("utf-8")).decode("ascii")
            print(f"  inlined js    {src}  (base64 eval — self-parsing runtime)")
            return (
                "<script>(0,eval)(new TextDecoder().decode("
                f'Uint8Array.from(atob("{b64}"),c=>c.charCodeAt(0))))</script>'
            )
        print(f"  inlined js    {src}")
        return "<script>\n" + body.replace("</script>", "<\\/script>") + "\n</script>"

    doc = re.sub(r'<script\s+src="([^"]+)"\s*>\s*</script>', sub_js, doc)

    # 4. Swap the three.js iframe for a still.
    before = doc
    doc = re.sub(
        r'(<iframe\b[^>]*?)\ssrc="mannequin\.html"',
        lambda m: m.group(1) + ' srcdoc="' + html.escape(mannequin_srcdoc(), quote=True) + '"',
        doc,
    )
    print("  3D iframe     " + ("-> still image" if doc != before else "! not matched"))

    # 5. Inject fonts + a preview marker as the first thing in <head>.
    css = font_css()
    doc = doc.replace(
        "<head>",
        "<head>\n<title>Merchandize — site preview</title>\n<style>\n" + css + "\n</style>",
        1,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    mb = OUT.stat().st_size / 1_048_576
    print(f"\n  wrote {OUT.relative_to(ROOT)}  ({mb:.2f} MB)")
    if mb > 15:
        print("  ! over 15MB — artifact limit is 16MB")


if __name__ == "__main__":
    build()
