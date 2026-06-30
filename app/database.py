from app.importance import judge_importance
from app.categories import judge_category

import sqlite3
from datetime import datetime
from app.config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            category TEXT DEFAULT '未分類',
            importance INTEGER DEFAULT 3,
            relevance INTEGER DEFAULT 3,
            summary TEXT DEFAULT '',
            impact TEXT DEFAULT '',
            action TEXT DEFAULT '',
            posted INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_news_items(items):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    new_items = []

    for item in items:
        item["importance"] = judge_importance(item["title"])
        item["category"] = judge_category(item["title"])
        try:
            cur.execute("""
                INSERT INTO news (
                    source,
                    title,
                    url,
                    category,
                    importance,
                    posted,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, 0, ?)
            """, (
                item["source"],
                item["title"],
                item["url"],
                item.get("category", "未分類"),
                item.get("importance", 3),
                datetime.now().isoformat(timespec="seconds"),
            ))

            new_items.append(item)

        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    return new_items