# Hosting

The site in `site/` is a plain static site — no build step, no server, no database.

**Live now:** https://levonchenorhokian-sudo.github.io/BIZ/
**Target domain:** karrgo.net (bought at GoDaddy — DNS not pointed yet)

---

## How it deploys

GitHub Pages, via `.github/workflows/deploy-pages.yml`.

Every push to `claude/lebanon-uniform-strategy-zob4rv` that touches `site/`
redeploys automatically. Nothing to run by hand.

Two things worth knowing:

- **Pages had to be enabled manually.** The workflow token cannot create a Pages
  site (`Resource not accessible by integration`), so Settings → Pages → Source →
  *GitHub Actions* was a one-time human step. It is done.
- **`.nojekyll` is required.** Jekyll strips directories beginning with `_`, which
  would delete `_ds/` — the design system the pages load every colour and font
  from — and serve an unstyled page. The file is committed and the workflow also
  writes it into the artifact.

### Check a deploy

Actions tab → "Deploy site to GitHub Pages". Green means live within a minute.

---

## Pointing karrgo.net at it

**Do the DNS first, then the custom domain.** Adding the domain to Pages before DNS
resolves makes the site unreachable — the `github.io` URL starts redirecting to a
domain that does not answer yet.

### Step 1 — GoDaddy DNS

**GoDaddy → My Products → karrgo.net → DNS → Manage DNS.** Delete the parking
records GoDaddy ships with (an `A` on `@`, usually a `CNAME` on `www`), then add:

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| `A` | `@` | `185.199.108.153` | 600 |
| `A` | `@` | `185.199.109.153` | 600 |
| `A` | `@` | `185.199.110.153` | 600 |
| `A` | `@` | `185.199.111.153` | 600 |
| `CNAME` | `www` | `levonchenorhokian-sudo.github.io` | 600 |

All four `A` records are needed — they are GitHub's Pages load balancers.
Leave any `MX` records alone if you set up email.

Propagation is usually 10–30 minutes. Check with:

```sh
dig +short karrgo.net
dig +short www.karrgo.net
```

### Step 2 — Tell Pages about the domain

Add a `CNAME` file containing `karrgo.net` to `site/`, or set it in
Settings → Pages → Custom domain. Then tick **Enforce HTTPS** once the
certificate is issued (automatic, free, a few minutes).

Do **not** buy an SSL certificate from GoDaddy. You do not need one.

---

## Before you send anyone the link

### The brand does not match the domain
`site/` is the **Merchandize** build; the domain is **karrgo.net**. The header,
footer and `inquiries@merchandize.com` all say Merchandize.

The Karrgo two-page build (adds a products page) is in history at **`9e93f7f`**,
but the 23 product photos were stripped from that export and never supplied, so
its catalogue cards render empty. Decide which build ships.

### The contact email does not exist
The site tells visitors to email an address that has no mailbox behind it. Buying a
domain does not create email. Zoho Mail has a free single-mailbox tier; Google
Workspace is about $6/user/month.

### The form loses inquiries
Submitting opens the visitor's own mail client via `mailto:`. If they have no mail
client configured, the inquiry is silently lost, and attached reference images never
send. GitHub Pages cannot process forms — it serves static files only. Options:

- **Formspree** / **Basin** — free tiers, works on Pages, a one-line form change
- **Netlify** instead of Pages — free form handling built in (see below)

### Other gaps
- The hero claims **"Lebanon's number one uniform provider"** — an unsubstantiated
  superlative for a business that has not launched.
- The inquiry dropdowns (`garmentTypes`, `fabrics`, `colorOptions`,
  `brandingMethods`) are empty strings, so those selects have no options.

---

## Repo visibility

Pages on a **private** repo needs a paid GitHub plan, so this repo was made
**public** to host for free. That publishes everything in it, not just the site —
including `BUSINESS_VISION.md`, `catalogue/catalogue.data.json` (pricing) and
`MCP_SETUP.md`.

If that is not wanted, the fix is to move `site/` into its own public repo and set
this one back to private.

## Alternative: Netlify

`netlify.toml` is still in the repo, so Netlify remains a drop-in alternative. It
deploys from a **private** repo on the free tier and handles forms — the two things
Pages cannot do. Import the repo at netlify.com and point DNS at Netlify instead.
