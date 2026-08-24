import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "bookmarks.sqlite"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

BOOKMARKS = [
    ("https://modelcontextprotocol.io/introduction", "Intro to MCP", "mcp", 0),
    ("https://modelcontextprotocol.io/docs/concepts/tools", "MCP Tools Concepts", "mcp", 0),
    ("https://modelcontextprotocol.io/docs/concepts/resources", "MCP Resources Concepts", "mcp", 1),
    ("https://www.anthropic.com/news/model-context-protocol", "Introducing MCP", "mcp", 1),
    ("https://github.com/modelcontextprotocol/servers", "MCP Servers Repo", "mcp", 0),
    ("https://www.sqlite.org/docs.html", "SQLite Docs", "reference", 1),
    ("https://www.sqlite.org/lang.html", "SQLite SQL Syntax", "reference", 0),
    ("https://docs.python.org/3/library/sqlite3.html", "Python sqlite3 Module", "reference", 1),
    ("https://peps.python.org/pep-0249/", "PEP 249 - DB API", "reference", 0),
    ("https://flask.palletsprojects.com/", "Flask Docs", "reference", 1),
    ("https://realpython.com/python-sqlite-sqlalchemy/", "Python SQLite Tutorial", "python", 0),
    ("https://realpython.com/python-typing/", "Python Typing Guide", "python", 1),
    ("https://docs.python.org/3/library/pathlib.html", "pathlib Docs", "python", 0),
    ("https://docs.python.org/3/library/venv.html", "Python venv Docs", "python", 1),
    ("https://peps.python.org/pep-0008/", "PEP 8 Style Guide", "python", 0),
    ("https://www.python.org/dev/peps/pep-0020/", "The Zen of Python", "python", 1),
    ("https://nextjs.org/docs", "Next.js Docs", "webdev", 0),
    ("https://tailwindcss.com/docs", "Tailwind CSS Docs", "webdev", 1),
    ("https://developer.mozilla.org/en-US/docs/Web/HTML", "MDN HTML Reference", "webdev", 0),
    ("https://developer.mozilla.org/en-US/docs/Web/JavaScript", "MDN JavaScript Reference", "webdev", 1),
    ("https://vitejs.dev/", "Vite Docs", "webdev", 0),
    ("https://fly.io/docs/", "Fly.io Docs", "hosting", 0),
    ("https://render.com/docs", "Render Docs", "hosting", 1),
    ("https://developers.cloudflare.com/pages/", "Cloudflare Pages Docs", "hosting", 0),
    ("https://docs.netlify.com/", "Netlify Docs", "hosting", 1),
    ("https://turso.tech/", "Turso (libSQL) Site", "hosting", 0),
    ("https://www.anthropic.com/research", "Anthropic Research", "ai", 1),
    ("https://claude.com/", "Claude Homepage", "ai", 0),
    ("https://arxiv.org/abs/1706.03762", "Attention Is All You Need", "ai", 1),
    ("https://huggingface.co/", "Hugging Face", "ai", 0),
    ("https://openai.com/research", "OpenAI Research", "ai", 1),
    ("https://en.wikipedia.org/wiki/REST", "REST (Wikipedia)", "webdev", 0),
    ("https://jsonapi.org/", "JSON:API Spec", "webdev", 1),
    ("https://12factor.net/", "The Twelve-Factor App", "reference", 0),
    ("https://www.python.org/", "Python Homepage", "python", 1),
]

def main():
    if not SCHEMA_PATH.exists():
        sys.exit(f"Schema file not found: {SCHEMA_PATH}")

    if DB_PATH.exists():
        sys.exit(
            f"Database already exists: {DB_PATH}\n"
            "Delete it first if you want to reseed from scratch."
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.executemany(
        "INSERT INTO bookmarks (url, title, tag, read) VALUES (?, ?, ?, ?)",
        BOOKMARKS,
    )
    conn.commit()
    conn.close()

    print(f"Seeded {len(BOOKMARKS)} bookmarks into {DB_PATH}")

if __name__ == "__main__":
    main()
