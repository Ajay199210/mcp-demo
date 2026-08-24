# Bookmark Manager MCP Server

A minimal, read-only [MCP](https://modelcontextprotocol.io) server exposing a SQLite-backed bookmark collection as tools, built as a companion demo for a blog post explaining MCP concepts.

## Structure

- `schema.sql` - defines the single `bookmarks` table (id, url, title, tag, read, saved_date).
- `seed.py` - portable seed script. Refuses to overwrite an existing DB; seeds 34 sample bookmarks across 6 tags (`mcp`, `reference`, `python`, `webdev`, `hosting`, `ai`) into `data/bookmarks.sqlite`.
- `mcp_server/server.py` - the MCP server itself. Read-only by design (no write tools). Exposes three tools:
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

Tip: you can check the seeded data directly, drag `data/bookmarks.sqlite` into [sqliteviewer.app](https://sqliteviewer.app/). A free, in-browser SQLite viewer (nothing is uploaded, it runs client-side).

Then copy `.mcp.json.example` to `.mcp.json`, fill in the absolute path to your venv's Python interpreter and `server.py`, and register it with Claude Code (or any MCP client).

## Configuration

The server reads two environment variables:

- `DB_PATH` - path to the SQLite database (defaults to `data/bookmarks.sqlite` relative to the project root).
- `MCP_TRANSPORT` - `stdio` (default, for local use) or `streamable-http` (for remote hosting). When set to `streamable-http`, the server also binds to `0.0.0.0` and Render's `$PORT` (defaulting to `8000` locally).

## Deployment

Deployed as an always-on Python web service on [Render](https://render.com), with `data/bookmarks.sqlite` committed as read-only seed data. See `.mcp.json.example` for the remote client config once deployed.