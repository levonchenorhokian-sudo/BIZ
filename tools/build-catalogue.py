#!/usr/bin/env python3
"""Render catalogue/catalogue.data.json into a 2-page A4 price list PDF.

    python3 tools/build-catalogue.py

Outputs:
    catalogue/Merchandize-Catalogue.html   (intermediate, styled for print)
    catalogue/Merchandize-Catalogue.pdf    (A4, via headless Chromium)

To change prices, edit catalogue/catalogue.data.json and re-run.
"""

import base64
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "catalogue" / "catalogue.data.json"
HTML_OUT = ROOT / "catalogue" / "Merchandize-Catalogue.html"
PDF_OUT = ROOT / "catalogue" / "Merchandize-Catalogue.pdf"

FONT_DIRS = [Path("/tmp/fonts/package/files"), ROOT / "catalogue" / "fonts"]
FONTS = [
    ("Barlow", "barlow-latin", [400, 500, 600]),
    ("Barlow Condensed", "barlow-condensed-latin", [500, 600, 700]),
]
CHROME_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
]

e = lambda s: html.escape(str(s), quote=True)
visible = lambda rows: [r for r in rows if not r.get("hide")]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    return shutil.which("chromium") or shutil.which("google-chrome")


def font_face_css() -> str:
    out, found = [], 0
    for family, prefix, weights in FONTS:
        for w in weights:
            for d in FONT_DIRS:
                f = d / f"{prefix}-{w}-normal.woff2"
                if f.exists():
                    b64 = base64.b64encode(f.read_bytes()).decode("ascii")
                    out.append(
                        f"@font-face{{font-family:'{family}';font-style:normal;"
                        f"font-weight:{w};font-display:block;"
                        f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
                    )
                    found += 1
                    break
    if not found:
        print("  ! no Barlow woff2 found — PDF will use fallback fonts")
    return "\n".join(out)


def build() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    m, cur = d["meta"], d["meta"]["currency"]
    products = visible(d["products"])

    rows = "".join(
        f"<tr><td class='p-name'>{e(p['product'])}"
        f"<span class='p-detail'>{e(p.get('detail',''))}</span></td>"
        f"<td class='p-range'>{e(p.get('range','—'))}</td>"
        f"<td class='num p-moq'>{e(p.get('moq','—'))}</td>"
        f"<td class='num p-price'>{float(p['from']):,.2f}</td></tr>"
        for p in products
    )

    ranges = "".join(
        f"<div class='tier'><h4>{e(r['name'])}</h4><p>{e(r['desc'])}</p></div>"
        for r in d["ranges"]
    )
    qb = "".join(
        f"<tr><td>{e(q['range'])}</td><td class='num'>{e(q['adjust'])}</td></tr>"
        for q in d["quantity_breaks"]
    )
    br = "".join(
        f"<tr><td>{e(b['product'])}</td><td class='num'>{e(b['moq'])}</td>"
        f"<td class='num p-price'>{float(b['from']):,.2f}</td></tr>"
        for b in visible(d["branding"])
    )
    steps = "".join(f"<li>{e(s)}</li>" for s in d["steps"])

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{e(m['brand'])} — {e(m['title'])}</title>
<style>
{font_face_css()}

/* Palette from the site's design system so this reads as the same company.
   Print-only document: one deliberate light treatment. */
:root{{
  --ink:#1d1f20; --ink-2:#424244; --ink-3:#5d5d60; --ink-4:#98989b;
  --accent:#5980a6; --accent-700:#416180; --accent-900:#1d2d3d;
  --rule:#d4d4d7; --rule-soft:#e7e7ea; --tint:#f5f7f9; --paper:#fff;
  --head:"Barlow Condensed",system-ui,sans-serif;
  --body:"Barlow",system-ui,sans-serif;
}}
@page{{ size:A4; margin:17mm 16mm 16mm; }}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:10pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
h1,h2,h3,h4{{font-family:var(--head);font-weight:600;margin:0;line-height:1.02;
  text-wrap:balance;letter-spacing:.005em}}
h1{{font-size:44pt;text-transform:uppercase}}
h2{{font-size:20pt;text-transform:uppercase;color:var(--accent-900)}}
h4{{font-size:11pt;text-transform:uppercase;letter-spacing:.05em}}
p{{margin:0 0 6pt}}
.eyebrow{{font-family:var(--head);font-weight:600;font-size:9.5pt;
  text-transform:uppercase;letter-spacing:.16em;color:var(--accent);margin:0 0 6pt}}
.lead{{font-size:10pt;color:var(--ink-2);max-width:64ch}}
.fine{{font-size:7.8pt;color:var(--ink-4);line-height:1.45;margin:7pt 0 0}}
.lbl{{display:block;font-family:var(--head);font-size:7.8pt;text-transform:uppercase;
  letter-spacing:.12em;color:var(--ink-4)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}

/* masthead */
.masthead{{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1.6pt solid var(--ink);padding-bottom:7pt;margin-bottom:26pt}}
.wordmark{{font-family:var(--head);font-weight:700;font-size:18pt;
  text-transform:uppercase;letter-spacing:.03em}}
.edition{{font-family:var(--head);font-size:9.5pt;text-transform:uppercase;
  letter-spacing:.14em;color:var(--ink-4)}}
h1{{margin:0 0 10pt}}

/* product list — the whole point of page 1, so it gets the room */
table.products{{width:100%;border-collapse:collapse;margin-top:20pt}}
table.products th{{font-family:var(--head);font-weight:600;font-size:8.4pt;
  text-transform:uppercase;letter-spacing:.1em;color:var(--ink-3);text-align:left;
  padding:0 7pt 5pt;border-bottom:.8pt solid var(--rule)}}
table.products td{{padding:11pt 7pt;border-bottom:.5pt solid var(--rule-soft);
  vertical-align:baseline}}
table.products tbody tr:nth-child(even) td{{background:var(--tint)}}
.p-name{{font-family:var(--head);font-weight:600;font-size:14pt;
  text-transform:uppercase;letter-spacing:.01em;color:var(--ink);line-height:1.05}}
.p-detail{{display:block;font-family:var(--body);font-weight:400;font-size:8.8pt;
  text-transform:none;letter-spacing:0;color:var(--ink-3);margin-top:2pt}}
.p-range{{font-size:8.8pt;color:var(--ink-3)}}
.p-moq{{font-size:9.4pt;color:var(--ink-3)}}
.p-price{{font-family:var(--head);font-weight:600;font-size:15pt;
  color:var(--accent-900);white-space:nowrap}}
td.p-price::before{{content:"from ";font-family:var(--body);font-weight:400;
  font-size:8pt;color:var(--ink-4)}}
col.c-name{{width:auto}} col.c-range{{width:23%}}
col.c-moq{{width:11%}} col.c-price{{width:19%}}

/* page 2 */
.page2{{page-break-before:always}}
.block{{margin-bottom:20pt}}
.block > h2{{padding-bottom:6pt;margin-bottom:10pt;border-bottom:1.6pt solid var(--ink)}}
.tiers{{display:grid;grid-template-columns:repeat(3,1fr);gap:12pt}}
.tier{{border-top:1.6pt solid var(--accent);padding-top:7pt}}
.tier h4{{color:var(--accent-900);margin-bottom:4pt}}
.tier p{{font-size:9pt;color:var(--ink-3);margin:0}}
.two-col{{display:grid;grid-template-columns:1fr 1.25fr;gap:22pt}}
.two-col h4{{color:var(--accent-700);padding-bottom:4pt;margin-bottom:6pt;
  border-bottom:.6pt solid var(--rule-soft)}}
table.mini{{width:100%;border-collapse:collapse;font-size:9.4pt}}
table.mini td{{padding:5pt 6pt;border-bottom:.5pt solid var(--rule-soft)}}
table.mini tbody tr:nth-child(even) td{{background:var(--tint)}}
table.mini .p-price{{font-size:11pt}}
ol.steps{{margin:0;padding-left:17pt;font-size:10pt;color:var(--ink-2)}}
ol.steps li{{margin-bottom:6pt}}
.contact{{display:grid;grid-template-columns:1fr 1fr;gap:14pt;
  border-top:1.6pt solid var(--ink);border-bottom:.6pt solid var(--rule);
  padding:11pt 0;font-size:12.5pt}}
.contact strong{{font-weight:600}}
</style></head>
<body>

<header class="masthead">
  <div class="wordmark">{e(m['brand'])}</div>
  <div class="edition">{e(m['edition'])}</div>
</header>

<p class="eyebrow">{e(m['eyebrow'])}</p>
<h1>{e(m['title'])}</h1>
<p class="lead">{e(m['intro'])}</p>

<table class="products">
  <colgroup><col class="c-name"><col class="c-range"><col class="c-moq"><col class="c-price"></colgroup>
  <thead><tr>
    <th>Product</th><th>Range</th><th class="num">Min. order</th>
    <th class="num">Price ({cur})</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="fine">{e(m['disclaimer'])} {e(m['validity'])}</p>

<section class="page2">
  <div class="block">
    <h2>The three ranges</h2>
    <div class="tiers">{ranges}</div>
  </div>

  <div class="block">
    <h2>Quantity &amp; branding</h2>
    <div class="two-col">
      <div>
        <h4>Quantity breaks</h4>
        <table class="mini"><tbody>{qb}</tbody></table>
        <p class="fine">Applies per style and colour, not per total order.</p>
      </div>
      <div>
        <h4>Branding — added per piece</h4>
        <table class="mini"><tbody>{br}</tbody></table>
        <p class="fine">On top of the garment price. One-off setup may apply on screen print and woven labels.</p>
      </div>
    </div>
  </div>

  <div class="block">
    <h2>How it works</h2>
    <ol class="steps">{steps}</ol>
  </div>

  <div class="contact">
    <div><span class="lbl">WhatsApp</span><strong>{e(m['contact_whatsapp'])}</strong></div>
    <div><span class="lbl">Email</span><strong>{e(m['contact_email'])}</strong></div>
  </div>
  <p class="fine">{e(m['disclaimer'])}</p>
</section>

</body></html>"""

    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(doc, encoding="utf-8")
    print(f"  products : {len(products)}")
    print(f"  html     : {HTML_OUT.relative_to(ROOT)}")

    chrome = find_chrome()
    if not chrome:
        print("  ! no Chromium found — HTML written, PDF skipped")
        sys.exit(1)
    r = subprocess.run(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
         "--no-pdf-header-footer", "--virtual-time-budget=20000",
         f"--print-to-pdf={PDF_OUT}", HTML_OUT.as_uri()],
        capture_output=True, text=True, timeout=180,
    )
    if not PDF_OUT.exists():
        print("  ! PDF not produced\n" + r.stderr[-1500:])
        sys.exit(1)
    print(f"  pdf      : {PDF_OUT.relative_to(ROOT)} "
          f"({PDF_OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    build()
