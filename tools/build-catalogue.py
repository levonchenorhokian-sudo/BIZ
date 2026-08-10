#!/usr/bin/env python3
"""Render catalogue/catalogue.data.json into a print-ready PDF.

    python3 tools/build-catalogue.py

Outputs:
    catalogue/Merchandize-Catalogue.html   (intermediate, styled for print)
    catalogue/Merchandize-Catalogue.pdf    (A4, via headless Chromium)

To change prices, edit catalogue/catalogue.data.json and re-run. Nothing in
this script needs touching to add products, sections or categories.
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


def find_chrome() -> str | None:
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


def money(v) -> str:
    """2 decimals, but keep sub-cent packaging prices readable."""
    f = float(v)
    return f"{f:,.2f}" if f >= 0.10 else f"{f:,.2f}"


def price_table(items, cur: str, show_range: bool) -> str:
    cols = (
        '<col class="c-prod"><col class="c-range"><col class="c-moq"><col class="c-price">'
        if show_range
        else '<col class="c-prod"><col class="c-moq"><col class="c-price">'
    )
    head = (
        "<th>Product</th><th>Range</th><th class='num'>MOQ</th>"
        f"<th class='num'>From ({cur})</th>"
        if show_range
        else f"<th>Option</th><th class='num'>MOQ</th><th class='num'>From ({cur})</th>"
    )
    rows = []
    for it in items:
        if it.get("hide"):
            continue
        cells = [f"<td class='prod'>{e(it['product'])}</td>"]
        if show_range:
            cells.append(f"<td class='range'>{e(it.get('range', '—'))}</td>")
        cells.append(f"<td class='num moq'>{e(it.get('moq', '—'))}</td>")
        cells.append(f"<td class='num price'>{money(it['from'])}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        f"<table class='price'><colgroup>{cols}</colgroup>"
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"
    )


def build() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    m, cur = d["meta"], d["meta"]["currency"]

    # ---------- cover ----------
    cats = " · ".join(c["name"] for c in d["categories"])
    cover = f"""
<section class="cover">
  <div class="cover-top">
    <div class="wordmark">{e(m['brand'])}</div>
    <div class="edition">{e(m['edition'])}</div>
  </div>
  <div class="cover-mid">
    <p class="eyebrow">{e(m['tagline'])}</p>
    <h1>Product<br>Catalogue<br><span class="amp">&amp;</span> Pricing</h1>
    <p class="cover-cats">{e(cats)}</p>
  </div>
  <div class="cover-foot">
    <div><span class="lbl">Region</span>{e(m['region'])}</div>
    <div><span class="lbl">Currency</span>{e(cur)}, excl. VAT</div>
    <div><span class="lbl">WhatsApp</span>{e(m['contact_whatsapp'])}</div>
    <div><span class="lbl">Email</span>{e(m['contact_email'])}</div>
  </div>
</section>"""

    # ---------- how to read ----------
    tiers = "".join(
        f"<div class='tier'><h4>{e(t['name'])}</h4><p>{e(t['desc'])}</p></div>"
        for t in d["tiers"]
    )
    qb = "".join(
        f"<tr><td>{e(q['range'])}</td><td class='num'>{e(q['adjust'])}</td></tr>"
        for q in d["quantity_breaks"]
    )
    b = d["branding"]
    guide = f"""
<section class="page">
  <p class="eyebrow">How to read this catalogue</p>
  <h2>Ranges, quantities &amp; branding</h2>
  <p class="lead">Every product comes in a range. The price shown is the
  <strong>starting price</strong> — the Essential tier at the stated minimum order
  quantity. Moving up a tier or adding branding moves the price up from there.</p>
  <div class="tiers">{tiers}</div>

  <div class="two-col">
    <div>
      <h3>Quantity breaks</h3>
      <table class="mini"><thead><tr><th>Units per style</th><th class="num">Adjustment</th></tr></thead>
      <tbody>{qb}</tbody></table>
      <p class="fine">Indicative. Breaks apply per style and colourway, not per total order.</p>
    </div>
    <div>
      <h3>{e(b['title'])}</h3>
      {price_table(b['items'], cur, show_range=False)}
      <p class="fine">{e(b['note'])}</p>
    </div>
  </div>

  <div class="callout">
    <h4>How pricing works</h4>
    <p>{e(m['price_disclaimer'])}</p>
    <p class="fine">{e(m['validity'])}</p>
  </div>
</section>"""

    # ---------- categories ----------
    body = []
    for ci, c in enumerate(d["categories"], 1):
        secs = []
        for s in c["sections"]:
            secs.append(
                f"<div class='sec'><h3>{e(s['name'])}</h3>"
                f"{price_table(s['items'], cur, show_range=True)}</div>"
            )
        n = sum(len([i for i in s["items"] if not i.get("hide")]) for s in c["sections"])
        body.append(f"""
<section class="page cat" id="{e(c['id'])}">
  <header class="cat-head">
    <p class="eyebrow">Category {ci} of {len(d['categories'])} · {n} products</p>
    <h2>{e(c['name'])}</h2>
    <p class="lead">{e(c['blurb'])}</p>
  </header>
  {''.join(secs)}
</section>""")

    closing = f"""
<section class="page closing">
  <p class="eyebrow">Next step</p>
  <h2>Getting a real quote</h2>
  <ol class="steps">
    <li><strong>Tell us the list.</strong> Styles, rough quantities, colours and your deadline.</li>
    <li><strong>We cost it in writing.</strong> Itemised, with branding priced separately so you can see what drives the total.</li>
    <li><strong>You approve a sample.</strong> Nothing goes into production before you hold the real thing.</li>
    <li><strong>We deliver to a date.</strong> Your spec stays on file, so the reorder is one message.</li>
  </ol>
  <div class="contact-box">
    <div><span class="lbl">WhatsApp</span><strong>{e(m['contact_whatsapp'])}</strong></div>
    <div><span class="lbl">Email</span><strong>{e(m['contact_email'])}</strong></div>
  </div>
  <p class="fine">{e(m['price_disclaimer'])}</p>
</section>"""

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{e(m['brand'])} — {e(m['doc_title'])}</title>
<style>
{font_face_css()}

/* Palette lifted from the site's design system so the catalogue reads as the
   same company. Print-only document: one deliberate light treatment. */
:root{{
  --ink:#1d1f20; --ink-2:#424244; --ink-3:#5d5d60; --ink-4:#98989b;
  --accent:#5980a6; --accent-700:#416180; --accent-900:#1d2d3d;
  --rule:#d4d4d7; --rule-soft:#e7e7ea; --tint:#f5f7f9; --paper:#ffffff;
  --head:"Barlow Condensed",system-ui,sans-serif;
  --body:"Barlow",system-ui,sans-serif;
}}
@page{{ size:A4; margin:16mm 14mm 18mm; }}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:9.2pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}}

h1,h2,h3,h4{{font-family:var(--head);font-weight:600;margin:0;text-wrap:balance;
  letter-spacing:.005em;line-height:1.02}}
h1{{font-size:52pt;text-transform:uppercase}}
h2{{font-size:26pt;text-transform:uppercase;color:var(--accent-900)}}
h3{{font-size:12.5pt;text-transform:uppercase;letter-spacing:.04em;color:var(--accent-700)}}
h4{{font-size:10.5pt;text-transform:uppercase;letter-spacing:.05em}}
p{{margin:0 0 6pt}}
strong{{font-weight:600}}

.eyebrow{{font-family:var(--head);font-weight:600;font-size:8.5pt;
  text-transform:uppercase;letter-spacing:.16em;color:var(--accent);margin:0 0 5pt}}
.lead{{font-size:10pt;color:var(--ink-2);max-width:62ch}}
.fine{{font-size:7.4pt;color:var(--ink-4);line-height:1.45;margin:5pt 0 0}}
.lbl{{display:block;font-family:var(--head);font-size:7.4pt;text-transform:uppercase;
  letter-spacing:.12em;color:var(--ink-4)}}

/* ---------- cover ---------- */
.cover{{height:calc(297mm - 34mm);display:flex;flex-direction:column;
  justify-content:space-between;page-break-after:always}}
.cover-top{{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1.4pt solid var(--ink);padding-bottom:6pt}}
.wordmark{{font-family:var(--head);font-weight:700;font-size:17pt;
  text-transform:uppercase;letter-spacing:.03em}}
.edition{{font-family:var(--head);font-size:9pt;text-transform:uppercase;
  letter-spacing:.14em;color:var(--ink-4)}}
.cover-mid h1{{margin:0 0 14pt}}
.cover-mid .amp{{color:var(--accent)}}
.cover-cats{{font-family:var(--head);font-size:13pt;text-transform:uppercase;
  letter-spacing:.07em;color:var(--ink-3);margin:0}}
.cover-foot{{display:grid;grid-template-columns:repeat(4,1fr);gap:10pt;
  border-top:.6pt solid var(--rule);padding-top:8pt;font-size:8.6pt}}

/* ---------- pages ---------- */
.page{{page-break-before:always}}
.cat-head{{border-bottom:1.4pt solid var(--ink);padding-bottom:8pt;margin-bottom:12pt}}
.cat-head h2{{margin:0 0 6pt}}
/* Sections may split across pages so pages pack densely; a heading never
   orphans at the foot of a page, and no single row is ever split. */
.sec{{margin:0 0 13pt}}
.sec h3{{padding-bottom:3pt;margin-bottom:0;break-after:avoid;
  border-bottom:.6pt solid var(--rule-soft)}}

/* ---------- tables ---------- */
table{{width:100%;border-collapse:collapse;font-size:8.8pt}}
thead{{display:table-header-group}}
tr{{break-inside:avoid}}
th{{font-family:var(--head);font-weight:600;font-size:7.8pt;text-transform:uppercase;
  letter-spacing:.09em;color:var(--ink-3);text-align:left;
  padding:4pt 5pt;border-bottom:.6pt solid var(--rule)}}
td{{padding:3.3pt 5pt;border-bottom:.4pt solid var(--rule-soft);vertical-align:baseline}}
tbody tr:nth-child(even) td{{background:var(--tint)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.prod{{color:var(--ink)}}
.range{{color:var(--ink-3);font-size:8.2pt}}
.moq{{color:var(--ink-3)}}
/* Scoped to td: the wrapping <table class="price"> shares the class name and
   would otherwise pick up the "from " pseudo-element itself. */
td.price{{font-weight:600;color:var(--accent-900);white-space:nowrap}}
td.price::before{{content:"from ";font-weight:400;font-size:7.2pt;color:var(--ink-4)}}
col.c-prod{{width:auto}} col.c-range{{width:27%}}
col.c-moq{{width:11%}} col.c-price{{width:17%}}
table.mini td{{padding:3.3pt 5pt}}

/* ---------- guide page ---------- */
.tiers{{display:grid;grid-template-columns:repeat(3,1fr);gap:9pt;margin:10pt 0 14pt}}
.tier{{border-top:1.4pt solid var(--accent);padding-top:6pt;break-inside:avoid}}
.tier h4{{color:var(--accent-900);margin-bottom:3pt}}
.tier p{{font-size:8.4pt;color:var(--ink-3);margin:0}}
.two-col{{display:grid;grid-template-columns:1fr 1.15fr;gap:16pt;margin-bottom:14pt}}
.two-col h3{{margin-bottom:5pt;padding-bottom:3pt;border-bottom:.6pt solid var(--rule-soft)}}
.callout{{background:var(--tint);border-left:2.2pt solid var(--accent);padding:9pt 11pt;break-inside:avoid}}
.callout h4{{color:var(--accent-900);margin-bottom:4pt}}
.callout p{{font-size:8.4pt;color:var(--ink-2);margin:0 0 4pt}}

/* ---------- closing ---------- */
.steps{{margin:8pt 0 14pt;padding-left:16pt;font-size:9.4pt;color:var(--ink-2)}}
.steps li{{margin-bottom:5pt}}
.contact-box{{display:grid;grid-template-columns:1fr 1fr;gap:12pt;
  border-top:1.4pt solid var(--ink);border-bottom:.6pt solid var(--rule);
  padding:9pt 0;margin-bottom:10pt;font-size:11pt}}
</style></head>
<body>
{cover}
{guide}
{''.join(body)}
{closing}
</body></html>"""

    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(doc, encoding="utf-8")

    total = sum(
        len([i for i in s["items"] if not i.get("hide")])
        for c in d["categories"]
        for s in c["sections"]
    ) + len(d["branding"]["items"])
    print(f"  categories : {len(d['categories'])}")
    print(f"  products   : {total}")
    print(f"  html       : {HTML_OUT.relative_to(ROOT)}")

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
    print(f"  pdf        : {PDF_OUT.relative_to(ROOT)} "
          f"({PDF_OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    build()
