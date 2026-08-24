CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    tag TEXT,
    read INTEGER NOT NULL DEFAULT 0,
    saved_date TEXT NOT NULL DEFAULT (date('now'))
);
