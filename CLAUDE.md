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
