# Hosting karrgo.net

The site in `site/` is a plain static site — no build step, no server, no database.
That means hosting is free and takes about 15 minutes.

---

## Why not GitHub Pages

This repo is **private**, and GitHub Pages on a private repo requires a paid GitHub
plan. Making the repo public would publish `BUSINESS_VISION.md`, `catalogue/`
pricing, and `MCP_SETUP.md` along with the site — so that route is not worth it.

**Recommended: Netlify.** Free, deploys from a private repo, free HTTPS, and it can
receive the inquiry form submissions (see "Make the form actually work" below).
Cloudflare Pages is an equally good alternative but wants the domain's nameservers
moved to Cloudflare; Netlify works with the DNS staying at GoDaddy.

---

## Step 1 — Deploy

`netlify.toml` in the repo root already tells Netlify to publish the `site/`
folder with no build command, so there is nothing to configure.

1. Sign up at **netlify.com** (free — "Sign up with GitHub" is easiest).
2. **Add new site → Import an existing project → GitHub**.
3. Authorise Netlify, then pick **levonchenorhokian-sudo/BIZ**.
4. Set **Branch to deploy** to `claude/lebanon-uniform-strategy-zob4rv`
   (that is currently this repo's default branch).
5. Leave build command empty and publish directory as `site` — `netlify.toml`
   sets both. Click **Deploy**.

You get a temporary URL like `random-name-1234.netlify.app`. **Open it and confirm
the site loads** before touching DNS.

> No-git alternative: download the `site/` folder and drag it onto
> **app.netlify.com/drop**. Instant hosting, but you must re-drag after every
> change — the git route redeploys automatically on each push.

---

## Step 2 — Point karrgo.net at it

In Netlify: **Domain management → Add a domain → `karrgo.net`**. Netlify then shows
you the exact DNS records to create. Use what Netlify shows — the values below are
the current standard ones, but confirm against the dashboard.

Then in **GoDaddy → My Products → Domains → karrgo.net → DNS → Manage DNS**:

| Action | Type | Name | Value | TTL |
| --- | --- | --- | --- | --- |
| Edit or add | `A` | `@` | `75.2.60.5` | 600 |
| Edit or add | `CNAME` | `www` | `your-site-name.netlify.app` | 600 |

- **Delete GoDaddy's parking records first.** A fresh domain ships with an `A` record
  on `@` pointing at a GoDaddy parking page and often a `CNAME` on `www`. Remove or
  overwrite both, or the domain will keep showing the parking page.
- Leave any `MX` records alone if you set up email (see below).

DNS usually propagates in 10–30 minutes, occasionally a few hours.

## Step 3 — HTTPS

Once DNS resolves, Netlify issues a free Let's Encrypt certificate automatically
(**Domain management → HTTPS → Verify DNS configuration**). Then turn on
**Force HTTPS**. Don't buy an SSL certificate from GoDaddy — you don't need one.

---

## Before you go live

### The brand does not match the domain
`site/` is currently the **Merchandize** build. The domain is **karrgo.net**. The
header, the footer and `inquiries@merchandize.com` all still say Merchandize.

The Karrgo two-page build is in git history at **`9e93f7f`** (it also adds a
products page), but its 23 product photos were stripped from that export and were
never supplied, so its catalogue cards render empty. Decide which build ships
before pointing DNS.

### The contact email needs to exist
The site tells visitors to email `inquiries@merchandize.com`. On karrgo.net you want
something like `inquiries@karrgo.net`, and **the mailbox has to actually exist** —
buying the domain does not create email. Free/cheap options:

- **Zoho Mail** — free tier for one custom-domain mailbox
- **Google Workspace** — paid, ~$6/user/month
- **GoDaddy email** — they will upsell this at checkout; not required

Whichever you pick, it adds `MX` records at GoDaddy. Those are separate from the
`A`/`CNAME` records above and do not conflict.

### Make the form actually work
Right now submitting the inquiry form opens the visitor's own mail client via
`mailto:` — so if they have no mail client configured, the inquiry is simply lost,
and attached reference images never make it.

Netlify Forms fixes this for free: add `netlify` to the `<form>` tag and
submissions land in the Netlify dashboard with email notifications. Worth doing
before you drive any traffic.

### Other pre-launch items
- The hero claims **"Lebanon's number one uniform provider"** — an unsubstantiated
  superlative for a business that has not launched. Replace it.
- The inquiry dropdowns (`garmentTypes`, `fabrics`, `colorOptions`,
  `brandingMethods`) are **empty strings**, so those selects render with no options.
- The catalogue PDF is still branded Merchandize.

---

## After it is live

Pushing to the deploy branch redeploys automatically — no manual step.

Quick check that everything resolved:

```sh
curl -sI https://karrgo.net | head -1        # expect HTTP/2 200
curl -sI http://karrgo.net | head -1         # expect a 301 to https
```
