#!/usr/bin/env python3
"""Make a fresh `.dc.html` site export runnable as a standalone static site.

    python3 tools/patch-site.py

The design tool exports code that assumes its own authoring environment, so each
new export needs the same three fixes. This script is idempotent — safe to re-run
after dropping in a new export.

1. React is never shipped or referenced, but support.js requires window.React /
   window.ReactDOM and the pages call React.createRef(). Without it every page
   renders blank. Vendored React UMD is injected before support.js.
2. mannequin.html resolves three.js from unpkg.com. Repointed at vendor/three/
   so the site works offline and on any host. The importmap `integrity` block is
   dropped with it (those SRI hashes were for the unpkg URLs).
3. Cross-page links use the original export filenames ("Uniform Inquiry.dc.html",
   "Products.dc.html"). Rewritten to the served names (index.html, products.html).
"""

import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

REACT_TAGS = (
    '<script src="./vendor/react.production.min.js"></script>\n'
    '<script src="./vendor/react-dom.production.min.js"></script>\n'
)
SUPPORT_TAG = '<script src="./support.js"></script>'

# original export name -> served name
RENAMES = {
    "Uniform Inquiry.dc.html": "index.html",
    "Products.dc.html": "products.html",
}

LOCAL_IMPORTMAP = """{
  "imports": {
    "three": "./vendor/three/three.module.js",
    "three/addons/controls/OrbitControls.js": "./vendor/three/addons/controls/OrbitControls.js",
    "three/addons/exporters/OBJExporter.js": "./vendor/three/addons/exporters/OBJExporter.js",
    "three/addons/exporters/GLTFExporter.js": "./vendor/three/addons/exporters/GLTFExporter.js"
  }
}"""


def patch_page(p: Path) -> list[str]:
    src = original = p.read_text(encoding="utf-8")
    done = []

    # 1. React before support.js
    if "vendor/react.production.min.js" not in src:
        if SUPPORT_TAG in src:
            src = src.replace(SUPPORT_TAG, REACT_TAGS + SUPPORT_TAG, 1)
            done.append("react")
        else:
            done.append("! support.js tag not found — React NOT injected")

    # 2. cross-page links
    for old, new in RENAMES.items():
        for quoted in (f'"{old}"', f'"{old.replace(" ", "%20")}"'):
            if quoted in src:
                src = src.replace(quoted, f'"{new}"')
                done.append(f"link {old} -> {new}")

    if src != original:
        p.write_text(src, encoding="utf-8")
    return done


def patch_mannequin(p: Path) -> list[str]:
    src = original = p.read_text(encoding="utf-8")
    if "unpkg.com" not in src:
        return []
    src = re.sub(
        r'<script type="importmap">\s*\{.*?\}\s*</script>',
        '<script type="importmap">\n' + LOCAL_IMPORTMAP + "\n</script>",
        src,
        count=1,
        flags=re.S,
    )
    if src != original:
        p.write_text(src, encoding="utf-8")
        return ["three.js -> vendor/three"]
    return ["! importmap not matched"]


def main() -> None:
    if not SITE.is_dir():
        sys.exit("site/ not found")

    vendor = SITE / "vendor"
    if not (vendor / "react.production.min.js").exists():
        print("  ! site/vendor/react.production.min.js missing — pages will render blank.")
        print("    Restore vendor/ (react, react-dom, three) before serving.")

    for name in ("index.html", "products.html"):
        p = SITE / name
        if not p.exists():
            print(f"  - {name}: absent, skipped")
            continue
        d = patch_page(p)
        print(f"  {name}: {', '.join(d) if d else 'already patched'}")

    m = SITE / "mannequin.html"
    if m.exists():
        d = patch_mannequin(m)
        print(f"  mannequin.html: {', '.join(d) if d else 'already local'}")

    # Report assets the code-only export strips.
    missing = []
    prod_dir = SITE / "products"
    if prod_dir.is_dir():
        readme = prod_dir / "README.md"
        expected = re.findall(r"^- (\S+\.png)$", readme.read_text(encoding="utf-8"), re.M) if readme.exists() else []
        missing = [f for f in expected if not (prod_dir / f).exists()]
    if missing:
        print(f"\n  ! {len(missing)}/{len(expected)} product photos missing from site/products/")
        print(f"    e.g. {', '.join(missing[:4])}…")
        print("    Cards render as empty plates until the PNGs are dropped in.")

    for t in ("shirt-forest.png", "shirt-sand.png", "fabric-noise.png"):
        if not (SITE / "tex" / t).exists():
            print(f"  ! texture missing: tex/{t}")


if __name__ == "__main__":
    main()
