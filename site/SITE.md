# Karrgo site — file map

Two static pages. No build step, no npm. Open `Uniform Inquiry.dc.html` in a browser, or serve the
folder (`python3 -m http.server`) — the 3D viewer needs http:// rather than file:// to load textures.

## Pages

| Path | What it is |
| --- | --- |
| `Uniform Inquiry.dc.html` | Home. Hero, about, how-we-work timeline, 3D client viewer, quick inquiry + full spec sheet, floating WhatsApp button. |
| `Products.dc.html` | Product catalogue. Two categories (Food & beverage, Beauty & wellness), filter chips with counts, 23 cards. Each "Ask price" button opens WhatsApp naming that product. |

Markup lives in each file's `<x-dc>` block; behaviour in the `class Component` script below it.

## Supporting files

| Path | What it is |
| --- | --- |
| `products/` | Cut-out product photos, one PNG per catalogue key (e.g. `fnb-polo.png`). Transparent background — they sit on the page ground. |
| `mannequin.html` | The 3D dress form on the home page, loaded in an iframe. three.js, procedural geometry, no model file. Accepts `postMessage({type:'brand', ways:[…]})` from the parent to switch client colourways. |
| `tex/` | Shirt textures for the 3D viewer. |
| `three-d-stage.js` | Viewer shell for `mannequin.html` — camera, lighting, orbit controls, OBJ/GLB export. |
| `image-slot.js` | Drag-and-drop image placeholder web component (client logo plate on the home page). |
| `support.js` | Runtime for the `.dc.html` format. Do not edit. |
| `_ds/industry-…/` | The Industry design system. `styles.css` holds every colour, font and spacing token the pages use via `var(--…)`. |
| `uploads/` | Source artwork, green-screen originals and reference images. Not loaded by the site. |

## Things you'll probably want to change

- **WhatsApp number** — `whatsappNumber` in the `data-props` JSON at the bottom of each page, currently `96170887022`.
- **Destination email** — `contactEmail`, currently `inquiries@karrgo.com`. Submitting the inquiry form opens the visitor's mail client with the spec pre-written; there is no backend.
- **Catalogue** — the `catalogue` array at the top of `Products.dc.html`'s `Component` class. One line per product: `key` (must match a filename in `products/`), `cat` (`fnb` or `bh`), `name`. Add `photo: null` for a product with no image yet — its card shows a "Photo to come" plate. Order in the array is the order on the page.
- **Categories** — the `categories` map beside it.
- **Client carousel** (home page) — the `brands` array in `Uniform Inquiry.dc.html`. One entry per client: `name`, plus `ways[]` of colourways (`swatch` hex, and `map` pointing at a texture in `tex/`, or `null` for plain jersey).
- **Inquiry dropdowns** — `garmentTypes`, `fabrics`, `colorOptions`, `brandingMethods` are empty comma-separated strings. Fill them and the full spec sheet's selects populate.

## Known gaps

- No form backend. Submitting opens a `mailto:` link; uploaded reference images can't ride along, so the confirmation lists their filenames and asks the visitor to attach them.
- No analytics, no routing, no CMS.
- Product photos are AI-generated mockups, not real production shots.
