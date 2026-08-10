# Merchandize site — file map

Static site. No build step, no npm. Serve the folder and open it — the 3D viewer needs
http:// rather than file:// to load its textures:

```sh
cd site && python3 -m http.server 8080
# then open http://localhost:8080/
```

## Changes made when this was committed into BIZ

- `Uniform Inquiry.dc.html` was renamed to **`index.html`** so the site serves at `/`
  on any static host. Nothing referenced it by name.
- **`vendor/` was added.** The zip as exported could not render standalone: `support.js`
  requires `window.React` / `window.ReactDOM`, and the page calls `React.createRef()`,
  but no React was shipped or referenced — the page rendered blank. React 18.3.1 UMD is
  now vendored locally and loaded before `support.js` in `index.html`.
- `mannequin.html`'s importmap pointed at **unpkg.com** for three.js. It now points at
  the locally vendored `vendor/three/` (three 0.184.0 + OrbitControls/OBJExporter/GLTFExporter).
  The `integrity` block was dropped since those SRI hashes applied to the unpkg URLs.
  The site is now fully self-contained — no CDN needed except Google Fonts.

## Files

| Path | What it is |
| --- | --- |
| `Uniform Inquiry.dc.html` | The whole page: hero, about, how-we-work timeline, quick inquiry + full spec sheet, floating WhatsApp button. Markup lives in the `<x-dc>` block, behaviour in the `class Component` script below it. |
| `mannequin.html` | The 3D dress form, loaded in an iframe by the page. three.js, procedural geometry, no model file. Accepts a `postMessage({type:'brand', ways:[…]})` from the parent to switch client colourways. |
| `tex/` | Shirt textures: `shirt-forest.png`, `shirt-sand.png` (Holy Basil print, front+back baked into one UV layout) and `fabric-noise.png` (bump). |
| `three-d-stage.js` | Viewer shell used by `mannequin.html` — camera, lighting, orbit controls, OBJ/GLB export. |
| `image-slot.js` | The drag-and-drop image placeholder web component (client logo plate). Drops persist in localStorage per slot id. |
| `support.js` | Runtime for the `.dc.html` format. Do not edit. |
| `_ds/industry-…/` | The Industry design system: `styles.css` holds every colour, font and spacing token the page uses via `var(--…)`. |
| `uploads/` | Source artwork and reference images. |

## Things you'll probably want to change

- **WhatsApp number** — `whatsappNumber` in the `data-props` JSON near the bottom of `Uniform Inquiry.dc.html`, currently `96170887022`.
- **Destination email** — `contactEmail` in the same block. Submitting opens the visitor's mail client with the spec pre-written; there is no backend.
- **Catalogue dropdowns** — `garmentTypes`, `fabrics`, `colorOptions`, `brandingMethods` are empty comma-separated strings. Fill them and the full spec sheet's selects populate.
- **Client carousel** — the `brands` array at the top of the `Component` class in `Uniform Inquiry.dc.html`. One entry per client: `name`, plus `ways[]` of colourways (`swatch` hex, and `map` pointing at a texture in `tex/`, or `null` for plain jersey).

## Known gaps

- Uploaded reference images can't ride along on a `mailto:` link — the confirmation screen lists the filenames and asks the visitor to attach them.
- No form backend, no analytics, no routing. One page.
