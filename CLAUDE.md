# CLAUDE.md — Node.js Hosting

This project is built to deploy on Node.js Hosting, a managed Node.js hosting platform. Use this file as context when helping build, debug, or prepare this app for deployment.

## This project specifically

This repo is a **static site served by a minimal Express server** — not a framework app.

| Thing | Where |
| --- | --- |
| Entry point | `server.js` (Express, `express.static`) |
| Static files | **`site/`** — note: not `public/`, unlike the generic examples below |
| Site dependencies | React 18 and three.js are **vendored** into `site/vendor/` as plain files |
| Build | No-op. `site/` is pre-built; nothing compiles |
| Routing | Multi-page static (`index.html`, `mannequin.html`). Unknown paths return **404** — deliberately *not* the SPA catch-all shown below, which would wrongly serve `index.html` for every missing asset |
| Other dirs | `catalogue/`, `tools/` (Python stdlib build scripts) and the `.md` strategy docs are **not** part of the running app |

The site is also deployed to GitHub Pages via `.github/workflows/deploy-pages.yml`. If this app goes live on Node.js Hosting, decide which host is canonical.

## Platform Overview

Node.js Hosting is a managed Node.js PaaS that supports Node.js applications and static sites. Customers upload their project folder through the GoDaddy interface — no Docker, no CI/CD pipelines, no infrastructure config needed. The platform handles SSL, CDN, and server-side compute automatically.

## Deployment Flow

1. Customer uploads their project folder via the Node.js Hosting UI
2. The platform installs dependencies and builds the app
3. The app is deployed to a private preview environment (requires GoDaddy auth to view)
4. Once ready, the customer can publish to production and connect a custom domain

## Requirements

### package.json

Every project must have a valid `package.json` in the root directory with a `start` script. This is how the platform knows how to run the app.

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

The platform runs `npm install` followed by `npm start` to boot the application.

### Entry Point

The app needs a clear entry point referenced by the `start` script. Common patterns:

- `node server.js`
- `node index.js`
- `node app.js`
- `next start` (for Next.js apps)

### Port Binding

The app must listen on the port provided by the `PORT` environment variable. Do not hardcode a port.

```javascript
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

### Static Sites

For static sites with no server-side logic, include a simple server that serves the static files:

```javascript
const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port);
```

## Supported Frameworks

Node.js Hosting supports any Node.js application or framework that can run via `npm start`. This includes but is not limited to:

- Express.js
- Next.js
- Fastify
- Nuxt.js
- Remix
- Nest.js
- Hono
- Koa
- Static sites served via a Node.js server

If your framework produces a production build and can start via a `"start"` script, it will work on Node.js Hosting.

## Single Application Per Upload

Node.js Hosting expects a single application per upload. Monorepos and multi-app setups are not supported unless a single `npm start` command at the root boots everything the app needs.

If your project is a monorepo, extract the specific app you want to deploy into its own folder with its own `package.json` and upload that folder instead.

For example, if your repo has a structure like `packages/api` and `packages/web`, upload just `packages/web` as a standalone project with its own complete `package.json` and `start` script.

## Project Structure

The platform is flexible with structure. As long as the root contains a valid `package.json` with a `start` script, the app will deploy. A typical structure looks like:

```
my-app/
├── package.json        # Required — must include "start" script
├── server.js           # Entry point (or index.js, app.js, etc.)
├── public/             # Static assets (if applicable)
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── routes/             # API routes (if applicable)
├── views/              # Templates (if applicable)
├── .env.example        # Document required env vars (do not upload .env)
└── CLAUDE.md           # This file
```

## Environment Variables

- `PORT` is provided automatically by the platform. Always use `process.env.PORT`.
- Any additional environment variables needed by the app can be configured through the Node.js Hosting UI after upload.
- Never commit secrets or `.env` files in the upload folder.

## What the Platform Handles

You do not need to configure or worry about:

- SSL/TLS certificates — provisioned automatically
- CDN — included out of the box
- Process management — the platform manages restarts and uptime
- Server infrastructure — fully managed compute

## Deploying from AI Coding Tools

Many customers build their apps using AI-powered tools like Replit, Lovable, Bolt, Cursor, or Claude. These apps can be deployed on Node.js Hosting, but often need small adjustments before they're ready.

### How to get your code onto Node.js Hosting

1. Export or download your project as a zip from the AI tool
2. Unzip the folder locally
3. Check and fix the common issues below
4. Upload the folder through the Node.js Hosting UI

### Common issues and fixes

**Missing or incomplete `package.json`**
Some AI tools don't generate a complete `package.json`. Make sure yours exists in the root and includes a `"start"` script. If it's missing, create one:

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {}
}
```

Then run `npm install` locally to generate the correct dependencies.

**Hardcoded ports**
AI tools often hardcode a port like `3000` or `8080`. Replace any hardcoded port with `process.env.PORT`:

```javascript
// Before (common in AI-generated code)
app.listen(3000);

// After (ready for Node.js Hosting)
app.listen(process.env.PORT || 3000);
```

**Dependencies in the wrong place**
AI tools sometimes put production dependencies under `"devDependencies"`. Move anything the app needs at runtime into `"dependencies"`.

**Missing entry point**
Make sure the file referenced in your `"start"` script actually exists. AI tools sometimes generate a `main.js` but the start script points to `index.js`, or vice versa.

**Replit-specific files**
Replit projects often include `.replit` and `replit.nix` config files. These are not needed and can be removed before upload. Focus on having a clean `package.json` with the correct `"start"` script.

**Lovable / Bolt exports**
These tools often export frontend-only apps with no server. If your export doesn't include a server file, add a simple one to serve your static files:

```javascript
const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'dist')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port);
```

Make sure to add `express` to your dependencies: `npm install express --save`

### Quick validation

Before uploading, run this locally to confirm everything works:

```bash
npm install
npm start
```

If your app starts and is accessible at `http://localhost:3000` (or whatever port), it's ready for Node.js Hosting.

## Framework Setup Examples

### Express.js
Ensure `express` is in `dependencies` (not `devDependencies`) and the `start` script points to your server file.

### Next.js
Use `next build` as a `build` script and `next start` as the `start` script:

```json
{
  "scripts": {
    "build": "next build",
    "start": "next start"
  }
}
```

Next.js apps work out of the box with server-side rendering, API routes, and static generation.

### Nuxt.js
Similar to Next.js — build then start:

```json
{
  "scripts": {
    "build": "nuxt build",
    "start": "node .output/server/index.mjs"
  }
}
```

### Remix
```json
{
  "scripts": {
    "build": "remix build",
    "start": "remix-serve build"
  }
}
```

### Fastify
Same pattern as Express — bind to `process.env.PORT` and use `0.0.0.0` as the host:

```javascript
fastify.listen({ port: process.env.PORT || 3000, host: '0.0.0.0' });
```

### Nest.js
```json
{
  "scripts": {
    "build": "nest build",
    "start": "node dist/main"
  }
}
```

### Network Connectivity

Only outbound connections on ports 80 (HTTP) and 443 (HTTPS) are allowed from the container. Connections to GoDaddy databases are also supported.

Do not rely on arbitrary outbound ports or external services reachable only on non-standard ports — those connections will be blocked at runtime. Design the app to communicate over HTTP/HTTPS only.

## Database (Managed MySQL)

Node.js Hosting includes a managed MySQL database for every app. The platform provisions the database automatically and injects connection credentials as environment variables — no manual setup required.

### Environment Variables

The following environment variables are available at runtime:

| Variable | Description |
|----------|-------------|
| `DB_HOST` | Database hostname |
| `DB_PORT` | Database port (typically 3306) |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |

These are set automatically by the platform. Do not hardcode database credentials — always read from `process.env`.

### Connecting to the Database

Install the `mysql2` driver:

```bash
npm install mysql2
```

Basic connection example:

```javascript
const mysql = require('mysql2/promise');

async function query(sql, params) {
  const connection = await mysql.createConnection({
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT || '3306'),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
  });

  try {
    const [rows] = await connection.execute(sql, params);
    return rows;
  } finally {
    await connection.end();
  }
}
```

### Best Practices

- **Use short-lived connections** — open a connection per request and close it in a `finally` block.
- **Use parameterized queries** — never interpolate user input directly into SQL strings.
- **Preview and publish share the same database** — both environments connect to the same MySQL instance. Plan migrations and schema changes accordingly.
- **Use an ORM if preferred** — `mysql2` works with ORMs like Prisma and Drizzle that support MySQL.

### Importing Data

You can import a `.sql` dump file (up to 100 MB) through the Node.js Hosting UI. The import replaces existing tables, so back up data if needed.

### External Databases

Only the managed MySQL database and GoDaddy-hosted databases are reachable from the container. External databases on arbitrary hosts and non-standard ports (e.g. 3306, 5432) are **not reachable** because the platform only allows outbound traffic on ports 80 (HTTP) and 443 (HTTPS). If your external database is accessible over HTTPS (e.g. PlanetScale, Neon, Turso, Supabase), store the connection URL in Secrets through the Node.js Hosting UI and access it via `process.env.YOUR_SECRET_NAME` in your code.

## Persistent Storage (Filesystem)

The container filesystem is **rebuilt from your uploaded code on every deploy**. Any files your app writes at runtime under the app directory (e.g. `./data`, `./uploads`, `./tmp`) are **lost on the next deploy**. Only two locations survive a redeploy:

| Path | Web-served? | In code (zip) downloads? | Use for |
|------|-------------|--------------------------|---------|
| `public/assets` | Yes (publicly) | Yes | Public files you want served on the web (images, generated static assets). |
| `/private` | No | No | Private runtime data you must keep durable — file-based databases (SQLite), caches, generated files that should not be public. |

Both are also readable/writable from the Node.js Hosting UI's **File Manager** (App tab → `public/assets`, Private Storage tab → `/private`), including uploading and downloading files.

### File-based databases (SQLite, etc.)

Store the database file under `/private` so it persists across deploys and is never exposed publicly or included in code downloads:

```javascript
const path = require('node:path');
const Database = require('better-sqlite3');

// /private is durable across deploys; a path under the app dir is NOT.
const dbPath = path.join('/private', 'app.db');
const db = new Database(dbPath);
```

For most apps the **managed MySQL database** above is the simpler choice (no filesystem management, backups handled by the platform). Reach for `/private` when you specifically need a file-based store.

### Writing files at runtime

```javascript
const fs = require('node:fs/promises');
const path = require('node:path');

// Durable + private (survives redeploys, never web-served):
await fs.writeFile(path.join('/private', 'cache.json'), data);

// Durable + public (survives redeploys, served on the web):
await fs.writeFile(path.join(__dirname, 'public', 'assets', 'report.pdf'), pdf);
```

## Pre-Upload Checklist

Before uploading to Node.js Hosting, verify:

- [ ] `package.json` exists in the root directory
- [ ] `package.json` has a `"start"` script
- [ ] All production dependencies are in `"dependencies"` (not `"devDependencies"`)
- [ ] App listens on `process.env.PORT`
- [ ] No hardcoded ports, secrets, database credentials, or local file paths
- [ ] If using the managed database, `mysql2` is in `"dependencies"` and code reads `DB_*` env vars
- [ ] Any files written at runtime that must survive a redeploy go under `/private` (private) or `public/assets` (public) — not the app directory
- [ ] App runs locally with `npm install && npm start`
- [ ] If using a build step, `"build"` script is defined in `package.json`
- [ ] All outbound connections use HTTP (port 80) or HTTPS (port 443)
- [ ] No `.npmrc` with private registry URLs or auth tokens — all packages are available on the public npm registry

## Troubleshooting

### App won't start
- Check that `"start"` script exists in `package.json`
- Make sure the entry point file referenced in `"start"` actually exists
- Verify all dependencies are listed under `"dependencies"`

### Port errors
- Never hardcode a port number — always use `process.env.PORT`
- For frameworks that need a host, bind to `0.0.0.0` not `localhost`

### Missing modules
- Ensure all required packages are in `"dependencies"`, not `"devDependencies"`
- The platform runs `npm install --production` so dev dependencies are not installed

### Package registry
The platform only installs packages from the public npm registry (https://registry.npmjs.org). Private registries are not accessible during the install step.

- Do not include an `.npmrc` file that points to a private registry or contains auth tokens. It will break the install.
- Remove any `publishConfig` field from `package.json` that references a non-public registry.
- Scoped packages like `@yourorg/package` must be publicly published on npmjs.com. Private scoped packages cannot be installed.
- If a package is only available privately, find a public alternative or copy the code you need directly into the project.

### Build failures
- If the app needs a build step (TypeScript, Next.js, etc.), add a `"build"` script
- Check that build output paths match what the `"start"` script expects

## Getting Help

If you run into issues deploying, reach out through the Node.js Hosting interface or contact GoDaddy support.

---

# Project conventions

The sections below predate the hosting guidance above and apply to work in this repo generally.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## MCP free-tier usage policy

Operate under free-tier limits. Never purchase credits, upgrade a plan, enable paid usage, or exceed a free allowance without explicit user approval. Use Google Maps and Exa for initial discovery. Use Firecrawl only for qualified prospects. Use Hunter and Apollo selectively for Tier A leads. Use Playwright or Apify only when simpler tools fail.

Never print, commit, or paste API keys. Credentials live only in the Claude Code environment secrets (or a gitignored `.env`), referenced by `.mcp.json` via `${VAR}`. See `MCP_SETUP.md` for status, verification tests, and the recommended tool-usage order.
