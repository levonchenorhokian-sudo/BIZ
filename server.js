/**
 * Production server for the static site in site/.
 *
 * The site itself is plain HTML/CSS/JS with its dependencies (React, three.js)
 * vendored as files — there is nothing to compile. This server exists only so
 * the project can run on a Node hosting platform, which expects an npm start
 * that binds to the port it supplies.
 *
 *   npm install && npm start
 *
 * Local default is 3000; hosting platforms override it via PORT.
 */

const path = require('path');
const express = require('express');

const app = express();

// The platform injects PORT. Never hard-code it.
const port = process.env.PORT || 3000;
// Bind on all interfaces: containers are unreachable on 127.0.0.1.
const host = process.env.HOST || '0.0.0.0';

const siteRoot = path.join(__dirname, 'site');

// express.static handles MIME types, caching headers, range requests and
// directory-traversal protection, and serves site/index.html at "/".
// extensions:['html'] lets "/products" resolve to "products.html" if more
// pages are added later.
app.use(express.static(siteRoot, { extensions: ['html'] }));

app.use((req, res) => {
  res.status(404).type('text/plain').send('Not found');
});

app.listen(port, host, () => {
  console.log(`Serving ${siteRoot} on http://${host}:${port}`);
});
