import os
import sqlite3
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "news.db"

CHATWORK_API_TOKEN = os.getenv("CHATWORK_API_TOKEN")
CHATWORK_ROOM_ID = os.getenv("CHATWORK_ROOM_ID")

SOURCES = [
    {
        "name": "やまがみ社会保険労務士事務所",
        "url": "https://sr-ky.net/",
        "keywords": ["助成金", "キャリアアップ", "業務改善", "人材開発", "両立支援"],
    },
    {
        "name": "厚生労働省",
        "url": "https://www.mhlw.go.jp/",
        "keywords": ["助成金", "雇用", "労働", "育児", "介護", "法改正", "賃金"],
    },
    {
        "name": "熊本労働局",
        "url": "https://jsite.mhlw.go.jp/kumamoto-roudoukyoku/",
        "keywords": ["助成金", "雇用", "労働", "最低賃金", "求人"],
    },
    {
        "name": "熊本市",
        "url": "https://www.city.kumamoto.jp/",
        "keywords": ["高齢者", "介護", "事業者", "補助金", "助成金"],
    },
    {
        "name": "玉名市",
        "url": "https://www.city.tamana.lg.jp/",
        "keywords": ["高齢介護", "介護", "高齢者", "事業者", "補助金"],
    },
]


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            importance INTEGER NOT NULL DEFAULT 3,
            posted INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    # 以前のnews.dbに importance / posted が無い場合の追加対応
    cur.execute("PRAGMA table_info(news)")
    columns = [row[1] for row in cur.fetchall()]

    if "importance" not in columns:
        cur.execute("ALTER TABLE news ADD COLUMN importance INTEGER NOT NULL DEFAULT 3")

    if "posted" not in columns:
        cur.execute("ALTER TABLE news ADD COLUMN posted INTEGER NOT NULL DEFAULT 0")

    conn.commit()
    conn.close()


def fetch_links(source):
    print("\n==============================")
    print(f"【{source['name']}】を確認中")
    print("==============================")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(
            source["url"],
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        response.encoding = response.apparent_encoding

    except Exception as e:
        print(f"取得エラー: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    results = []

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        if not any(keyword in title for keyword in source["keywords"]):
            continue

        full_url = urljoin(source["url"], href)

        results.append({
            "source": source["name"],
            "title": title,
            "url": full_url,
        })

    unique_results = []
    seen_urls = set()

    for item in results:
        if item["url"] in seen_urls:
            continue

        seen_urls.add(item["url"])
        unique_results.append(item)

    return unique_results


def judge_importance(title):
    title = title or ""

    importance_5_keywords = [
        "受付開始",
        "申請受付",
        "申請期限",
        "締切",
        "終了",
        "停止",
        "廃止",
        "変更",
        "改正",
        "義務化",
        "様式変更",
        "要件変更",
        "支給要件",
        "募集開始",
        "公募開始",
    ]

    importance_4_keywords = [
        "助成金",
        "補助金",
        "キャリアアップ",
        "業務改善",
        "人材開発",
        "両立支援",
        "雇用調整",
        "最低賃金",
        "処遇改善",
        "介護報酬",
        "Q&A",
        "リーフレット",
        "パンフレット",
    ]

    for keyword in importance_5_keywords:
        if keyword in title:
            return 5

    for keyword in importance_4_keywords:
        if keyword in title:
            return 4

    return 3


def save_new_items(items):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    new_items = []

    for item in items:
        importance = judge_importance(item["title"])

        try:
            cur.execute("""
                INSERT INTO news (
                    source,
                    title,
                    url,
                    importance,
                    posted,
                    created_at
                )
                VALUES (?, ?, ?, ?, 0, ?)
            """, (
                item["source"],
                item["title"],
                item["url"],
                importance,
                datetime.now().isoformat(timespec="seconds"),
            ))

            item["importance"] = importance
            item["posted"] = 0
            new_items.append(item)

        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    return new_items


def make_chatwork_message(item):
    stars = "★" * item["importance"] + "☆" * (5 - item["importance"])

    return f"""【労務・助成金ニュースBot｜緊急配信】

■重要度
{stars}

■情報源
{item["source"]}

■タイトル
{item["title"]}

■当社への影響
助成金・労務・介護制度・補助金等に関係する可能性があります。
管理部で内容確認を推奨します。

■対応案
□ 原文を確認
□ 現在の申請予定・運用に影響がないか確認
□ 必要に応じて社労士・関係機関へ確認

■参考URL
{item["url"]}

※記事本文の転載ではなく、更新情報の通知です。
※最終判断は管理部および専門家確認のうえ行ってください。
"""


def post_to_chatwork(message):
    if not CHATWORK_API_TOKEN or not CHATWORK_ROOM_ID:
        print("Chatwork設定が未入力のため投稿をスキップしました。")
        return False

    url = f"https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages"

    headers = {
        "X-ChatWorkToken": CHATWORK_API_TOKEN
    }

    data = {
        "body": message
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=15)
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Chatwork投稿エラー: {e}")
        return False


def mark_as_posted(item):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE news
        SET posted = 1
        WHERE url = ?
    """, (item["url"],))

    conn.commit()
    conn.close()


def main():
    print("労務・助成金ニュース候補を取得します。")

    init_db()

    all_items = []

    for source in SOURCES:
        items = fetch_links(source)
        all_items.extend(items)

    new_items = save_new_items(all_items)

    print("\n==============================")
    print("取得完了")
    print(f"取得候補数: {len(all_items)}件")
    print(f"新着保存数: {len(new_items)}件")
    print("==============================")

    if not new_items:
        print("新着ニュースはありません。")
        return

    urgent_items = [item for item in new_items if item["importance"] >= 5]

    if not urgent_items:
        print("緊急配信対象はありません。週報・月報用に保存しました。")
        return

    print("\n【緊急配信対象】")

    for item in urgent_items:
        print("------------------------------")
        print(f"タイトル: {item['title']}")
        print(f"重要度: {item['importance']}")
        print(f"URL: {item['url']}")

        message = make_chatwork_message(item)
        success = post_to_chatwork(message)

        if success:
            mark_as_posted(item)
            print("Chatwork投稿完了")
        else:
            print("Chatwork投稿失敗")


if __name__ == "__main__":
    main()