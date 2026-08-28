# Bookmark Manager MCP Server

A minimal, read-only [MCP](https://modelcontextprotocol.io) server exposing a SQLite-backed bookmark collection as tools, built as a companion demo for a [blog post](http://curiousthoughts.blog/building-and-deploying-a-minimal-mcp-server) explaining MCP core concepts.

## Structure

- `schema.sql` - defines the single `bookmarks` table.
- `seed.py` - Seeds 35 sample bookmarks across 6 tags (mcp, reference, python, webdev, hosting, ai) into `data/bookmarks.sqlite`.
- `mcp_server/server.py` - the MCP server. Exposes three tools (read-only):
  - `list_all` - list every bookmark.
  - `get_unread` - list unread bookmarks.
  - `search_by_tag` - list bookmarks matching a given tag.
- `.mcp.json.example` - sample local (stdio) and remote (streamable-http) client configs.

## Local setup

```powershell
# Windows (PowerShell)
python -m venv mcp_server\.venv
.\mcp_server\.venv\Scripts\Activate.ps1
pip install -r mcp_server\requirements.txt
python seed.py
```

```bash
# macOS/Linux (or Git Bash on Windows)
python -m venv mcp_server/.venv
source mcp_server/.venv/bin/activate
pip install -r mcp_server/requirements.txt
python seed.py
```

Tip: You can check the seeded data directly by dragging the SQLite file into [sqliteviewer.app](https://sqliteviewer.app/). A free, in-browser SQLite viewer that runs client-side.

Then copy `.mcp.json.example` to `.mcp.json`, fill in the absolute path to your venv's Python interpreter and `server.py`, and register it with Claude Code (or any MCP client).

## Configuration

The server reads three environment variables:

- `DB_PATH` - path to the SQLite database (defaults to `data/bookmarks.sqlite` relative to the project root).
- `MCP_TRANSPORT` - `stdio` (default, for local use) or `streamable-http` (for remote hosting).
- `PORT` - port to bind when `MCP_TRANSPORT=streamable-http` (defaults to `8000`, Render sets this automatically).

When `MCP_TRANSPORT=streamable-http`, the server also binds to host `0.0.0.0`.

## Deployment

Deployed as a web service on [Render](https://render.com)'s free tier, with `data/bookmarks.sqlite` committed as read-only seed data. Live endpoint: [`https://mcp-demo-pzap.onrender.com/mcp`](https://mcp-demo-pzap.onrender.com/mcp) *(see `.mcp.json.example` for remote client config)*.

> **Note**: on the free tier, the service spins down after inactivity. If an AI client (like Claude or Qwen) hangs or times out on a tool call, visit the URL above in a browser first (it'll show "Not Found" or an error which is expected) to wake the instance, then try again a few seconds later.