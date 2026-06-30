from app.database import init_db, save_news_items, mark_as_posted


def main():
    init_db()

    test_items = [
        {
            "source": "テスト情報源",
            "title": "テスト助成金の受付開始",
            "url": "https://example.com/test-news-001",
            "category": "助成金",
            "importance": 5,
            "relevance": 5,
            "summary": "テスト要約",
            "impact": "テスト影響",
            "action": "テスト対応",
        }
    ]

    new_items = save_news_items(test_items)

    print(f"保存件数: {len(new_items)}")

    mark_as_posted("https://example.com/test-news-001")

    print("投稿済みフラグ更新テスト完了")


if __name__ == "__main__":
    main()