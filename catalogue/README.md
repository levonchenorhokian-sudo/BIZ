# Catalogue — how to edit

The PDF is generated. **Never edit the PDF or the HTML directly** — they are overwritten
on every build. Everything lives in one data file.

## Change a price

1. Open **`catalogue.data.json`**
2. Find the product and change its `"from"` value
3. Rebuild:

```sh
python3 tools/build-catalogue.py
```

That rewrites `Merchandize-Catalogue.pdf`. Nothing else to touch.

## Common edits

| Want to… | Do this in `catalogue.data.json` |
| --- | --- |
| Change a price | Edit that product's `"from"` number |
| Change a minimum order | Edit its `"moq"` |
| Change which tiers a product comes in | Edit its `"range"` string |
| Add a product | Copy any `{ "product": … }` line inside a section's `items` and edit it |
| Remove a product | Delete its line, or add `"hide": true` to keep it for later |
| Reorder products | Move the lines |
| Rename a section | Edit that section's `"name"` |
| Add a section | Copy a whole `{ "name": …, "items": [ … ] }` block |
| Add a category | Copy a whole category block; the cover and "Category N of M" update themselves |
| Change quantity discounts | Edit `quantity_breaks` |
| Change embroidery/print prices | Edit `branding.items` |
| Change tier descriptions | Edit `tiers` |
| Change brand name, contact, disclaimer | Edit `meta` |

## Notes

- **Prices are placeholders.** They are plausible generic figures, not researched
  market rates or costed margins. Replace them with real numbers from supplier
  quotes before sending this to a client.
- Prices are **USD per piece, excluding VAT and branding**, at the stated MOQ.
- Branding (embroidery, print) is priced **separately and added per piece** — that is
  intentional, so a client can see what drives the total.
- The PDF picks up Barlow / Barlow Condensed to match the website. If the fonts are
  missing the build still works but falls back to a system sans; to make font embedding
  permanent, copy the `.woff2` files into `catalogue/fonts/`.

## Files

| File | Role |
| --- | --- |
| `catalogue.data.json` | **The only file you edit.** All products and prices. |
| `Merchandize-Catalogue.pdf` | Generated deliverable — send this to clients. |
| `Merchandize-Catalogue.html` | Generated intermediate (gitignored). |
| `../tools/build-catalogue.py` | The builder. Layout and styling live here. |
