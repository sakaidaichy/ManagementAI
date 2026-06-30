import sqlite3
from datetime import datetime

from app.config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
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

    cur.execute("PRAGMA table_info(news)")
    columns = [row[1] for row in cur.fetchall()]

    add_columns = {
        "category": "TEXT DEFAULT '未分類'",
        "importance": "INTEGER DEFAULT 3",
        "relevance": "INTEGER DEFAULT 3",
        "summary": "TEXT DEFAULT ''",
        "impact": "TEXT DEFAULT ''",
        "action": "TEXT DEFAULT ''",
        "posted": "INTEGER DEFAULT 0",
    }

    for column_name, column_type in add_columns.items():
        if column_name not in columns:
            cur.execute(f"ALTER TABLE news ADD COLUMN {column_name} {column_type}")

    conn.commit()
    conn.close()


def save_news_items(items):
    conn = get_connection()
    cur = conn.cursor()

    new_items = []

    for item in items:
        try:
            cur.execute("""
                INSERT INTO news (
                    source,
                    title,
                    url,
                    category,
                    importance,
                    relevance,
                    summary,
                    impact,
                    action,
                    posted,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
            """, (
                item.get("source", ""),
                item.get("title", ""),
                item.get("url", ""),
                item.get("category", "未分類"),
                item.get("importance", 3),
                item.get("relevance", 3),
                item.get("summary", ""),
                item.get("impact", ""),
                item.get("action", ""),
                datetime.now().isoformat(timespec="seconds"),
            ))

            new_items.append(item)

        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    return new_items


def update_analysis(url: str, item: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE news
        SET
            category = ?,
            importance = ?,
            relevance = ?,
            summary = ?,
            impact = ?,
            action = ?
        WHERE url = ?
    """, (
        item.get("category", "未分類"),
        item.get("importance", 3),
        item.get("relevance", 3),
        item.get("summary", ""),
        item.get("impact", ""),
        item.get("action", ""),
        url,
    ))

    conn.commit()
    conn.close()


def mark_as_posted(url: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE news
        SET posted = 1
        WHERE url = ?
    """, (url,))

    conn.commit()
    conn.close()


def get_recent_news(limit: int = 30):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            source,
            title,
            url,
            category,
            importance,
            relevance,
            summary,
            impact,
            action,
            created_at
        FROM news
        ORDER BY
            importance DESC,
            relevance DESC,
            created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    items = []

    for row in rows:
        items.append({
            "source": row[0],
            "title": row[1],
            "url": row[2],
            "category": row[3],
            "importance": row[4],
            "relevance": row[5],
            "summary": row[6],
            "impact": row[7],
            "action": row[8],
            "created_at": row[9],
        })

    return items