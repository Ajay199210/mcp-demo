from mcp.server.mcpserver import MCPServer
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("DB_PATH", Path(__file__).parent.parent / "data" / "bookmarks.sqlite"))
TRANSPORT = os.environ.get("MCP_TRANSPORT", "stdio")
PORT = int(os.environ.get("PORT", 8000))

mcp = MCPServer("bookmark-manager")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def format_bookmark(row) -> str:
    line = f"[{row['id']}] {row['title']} — {row['url']}"
    if row["tag"]:
        line += f" (#{row['tag']})"
    line += " (read)" if row["read"] else " (unread)"
    return line

def format_bookmarks(rows) -> str:
    return "\n".join(format_bookmark(row) for row in rows)

@mcp.tool()
def list_all() -> str:
    """List all bookmarks, read or unread."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, title, url, tag, read FROM bookmarks ORDER BY saved_date DESC, id DESC"
    ).fetchall()
    conn.close()

    if not rows:
        return "No bookmarks saved yet."
    return format_bookmarks(rows)

@mcp.tool()
def get_unread() -> str:
    """List all unread bookmarks."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, title, url, tag, read FROM bookmarks WHERE read = 0"
    ).fetchall()
    conn.close()

    if not rows:
        return "No unread bookmarks."
    return format_bookmarks(rows)

@mcp.tool()
def search_by_tag(tag: str) -> str:
    """List all bookmarks matching a given tag."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, title, url, tag, read FROM bookmarks WHERE tag = ?",
        (tag,),
    ).fetchall()
    conn.close()

    if not rows:
        return f"No bookmarks tagged '{tag}'."
    return format_bookmarks(rows)

if __name__ == "__main__":
    if TRANSPORT in ("streamable-http", "sse"):
        mcp.run(transport=TRANSPORT, host="0.0.0.0", port=PORT)
    else:
        mcp.run(transport=TRANSPORT)
