# MCP Setup — Lebanon Uniform Market-Validation Project

This document records the MCP integration plan and **verified current status** for
the market-research stack (business discovery → research → extraction → enrichment
→ storage). It contains **no secret values** and never should.

> **Honest status as of setup:** No MCP in the target stack is connected-and-verified
> yet. Two independent blockers apply — see [Environment reality](#environment-reality).
> This file is the applied configuration + the exact steps to finish, per service.

---

## Environment reality

Detected by inspection (not assumed):

| Property | Value |
|---|---|
| Claude client | **Claude Code** CLI `2.1.220`, **managed remote/web execution** |
| OS | Ubuntu 24.04.4 LTS (Linux 6.18.5, x86_64) |
| Shell | `/bin/bash` |
| Node / npm / npx | v22.22.2 / 10.9.7 (`npx` available for stdio MCPs) |
| Python / uv / uvx | 3.11.15 / uv 0.8.17 |
| Docker | 29.3.1 (available) |
| Existing MCP servers | `github`, `claude-code-remote` — **injected by the platform**, not by local config |
| User config `mcpServers` | **none** at global or project scope (`/root/.claude.json`) |
| Provider env vars present | **none** (Google/Exa/Firecrawl/Airtable/Hunter/Apollo/Apify all unset) |

**Two blockers that prevent live connect-and-verify in the current session:**

1. **No credentials exist.** Every credentialed server (all except Playwright) is
   blocked on human API-key/OAuth creation. Nothing to authenticate with yet.
2. **This managed session cannot hot-load newly added MCP tools.** Proven, not
   assumed: the official Playwright MCP was added and `claude mcp list` reported it
   `√ Connected`, yet its `mcp__playwright__*` tools did **not** become callable in
   the running session (ToolSearch found none). New MCP servers only become callable
   after the platform starts a **fresh session**.

**Consequence (respecting the "no success without a real test call" rule):** all
verification tests must run in a **new session started after** (a) credentials are set
and (b) `.mcp.json` is present. Playwright is the one server that will verify next
session with **no credential**.

---

## Files created by this setup

| File | Purpose | Secrets? |
|---|---|---|
| `.mcp.json` | Project-scoped MCP definitions using `${ENV_VAR}` interpolation | No |
| `.env.example` | Variable **names** only | No |
| `.gitignore` | Excludes `.env` / `.env.*` (keeps `.env.example`) | — |
| `CLAUDE.md` | Free-tier usage policy + secret-handling rule appended | No |
| `MCP_SETUP.md` | This document | No |

Secrets belong in **Claude Code web environment secrets** (preferred) or a local
gitignored `.env`. `.mcp.json` reads them via `${VAR}` — values never touch the repo.

---

## Recommended usage order (free-tier preservation)

1. **Google Maps** — initial business discovery
2. **Exa** — supplemental discovery + web research
3. **Firecrawl** — only after a business qualifies
4. **Playwright** — only when Firecrawl fails (JS-rendered / interactive pages)
5. **Hunter** — only Tier A / top-priority leads (limited free credits)
6. **Apollo** — only larger organizations (optional)
7. **Apify** — specialized fallback only (optional)

---

## Per-server status

Legend: **Installed** = defined in `.mcp.json`; **Auth** = credential present;
**Verified** = a real tool call succeeded in a session.

### 1. Google Maps / Places — business discovery
- **Installed:** Yes (`@modelcontextprotocol/server-google-maps` via npx). ⚠️ Confirm
  publisher/maintenance at first-run approval; swap for a maintained Places MCP if stale.
- **Auth:** No. Needs `GOOGLE_MAPS_API_KEY`.
- **Human action:** Create a key in Google Cloud Console → enable **Places API**
  (+ Geocoding if needed). Restrict the key to those APIs only; disable unrelated APIs.
  Google Cloud requires a billing account even for free monthly credit — **you decide**
  before enabling.
- **Verify next session:** search `"Hotels in Beirut, Lebanon"`; confirm names,
  addresses, and Place IDs are returned.

### 2. Exa — web research / company discovery
- **Installed:** Yes (`exa-mcp-server` via npx). ⚠️ Confirm at approval.
- **Auth:** No. Needs `EXA_API_KEY` (Exa dashboard; free tier available).
- **Verify next session:** search `"Lebanese hotel groups official websites"`; confirm
  live results with usable source URLs.

### 3. Firecrawl — website extraction
- **Installed:** Yes (`firecrawl-mcp` via npx). ⚠️ Confirm at approval.
- **Auth:** No. Needs `FIRECRAWL_API_KEY` (free credits available).
- **Verify next session:** scrape **one** public page only (preserve credits); confirm
  title/main text/links/markdown.

### 4. Airtable — database storage
- **Installed:** Yes (`airtable-mcp-server` via npx — community, widely used).
  ⚠️ Prefer official OAuth if/when available; confirm at approval.
- **Auth:** No. Needs `AIRTABLE_API_KEY` (personal access token) scoped to **one base**.
- **Human action:** Create a base named **`Lebanon Uniform Market Validation`** with a
  table **`Prospects`**; create a PAT limited to that base
  (`data.records:read/write`, `schema.bases:read`).
- **Verify next session:** list bases → open base → read `Prospects` → create test
  record `"MCP Connection Test — Delete Me"` → read → delete.

### 5. Hunter — email enrichment
- **Installed:** **No.** No confirmed official/maintained Hunter MCP was identified.
  Options: (a) vet a community Hunter MCP before adding, or (b) a small custom wrapper
  over Hunter's official REST API. Not fabricated into `.mcp.json`.
- **Auth:** Reserve `HUNTER_API_KEY` name (in `.env.example`).
- **Free-tier note:** very limited credits — no bulk search during setup; account/credit
  check only, then reserve for Tier A leads.

### 6. Playwright — browser interaction (fallback)
- **Installed:** Yes (`@playwright/mcp@latest`, official Microsoft). Browsers already
  present in this environment (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`).
- **Auth:** **Not required** (open source, local).
- **Verify next session:** open one public page; read title + heading + one link; close
  session. **Do not** bypass CAPTCHAs/paywalls/anti-bot or access private accounts.

### 7. Apollo — contact enrichment (optional)
- **Installed:** **No.** API/MCP access is typically gated behind a paid Apollo plan.
  If the free plan excludes API access, status is:
  `Account available, MCP/API access requires upgrade` — **not connected**. No paid plan
  will be activated automatically.

### 8. Apify — specialized extraction (optional)
- **Installed:** Yes (`@apify/actors-mcp-server` via npx, official). ⚠️ Confirm at approval.
- **Auth:** No. Needs `APIFY_TOKEN` (free account).
- **Cost guard:** before running any Actor, check whether it is free / has a rental fee /
  charges compute. Do not run chargeable Actors without explicit approval.

---

## Verification matrix (current)

| MCP | Installed | Authenticated | Test call succeeded | Free tier | Main capability | Remaining action |
|---|---|---|---|---|---|---|
| Google Maps/Places | Yes | No | No | Unknown (billing acct may be required) | Business discovery | Create + restrict `GOOGLE_MAPS_API_KEY` |
| Exa | Yes | No | No | Yes | Web research | Create `EXA_API_KEY` |
| Firecrawl | Yes | No | No | Yes | Website extraction | Create `FIRECRAWL_API_KEY` |
| Airtable | Yes | No | No | Yes | Database storage | Create base + `Prospects` + scoped PAT |
| Hunter | No | No | No | Yes (tiny) | Email enrichment | Choose MCP impl / custom wrapper + key |
| Playwright | Yes | Not required | No (loads next session) | Open source | Browser interaction | Restart session to load + test |
| Apollo | No | No | No | API likely paid | Contact enrichment | Confirm free API access or skip |
| Apify | Yes | No | No | Yes | Specialized extraction | Create `APIFY_TOKEN` |

---

## Troubleshooting

- **`claude mcp list` shows "Connected" but tools aren't callable:** expected in the
  managed session — tools load on a **fresh session**, not mid-session.
- **Server fails to start with empty env:** the `${VAR}` was unset — set the secret in
  environment settings, then start a new session.
- **npx package differs from expectation:** the first-run approval prompt is your gate —
  verify publisher/repo/maintenance before approving; swap the package if unmaintained.
- **Removing a server:** `claude mcp remove <name> -s <scope>`.

---

## Readiness

**NOT READY** — no discovery or storage MCP is connected-and-verified yet (no credentials
present; managed session cannot hot-load tools). Once `GOOGLE_MAPS_API_KEY`, `EXA_API_KEY`,
`FIRECRAWL_API_KEY`, and the Airtable base + PAT are set and a new session is started, the
core stack can be verified and Phase 1 (the 300-company research) can begin.
