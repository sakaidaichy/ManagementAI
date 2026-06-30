from app.database import init_db, get_recent_news
from app.chatwork import make_urgent_message, post_to_chatwork


def main():
    init_db()

    items = get_recent_news(limit=50)

    if not items:
        print("DBにニュースがありません。先に python run_daily.py を実行してください。")
        return

    # 重要度・関連度が高い順に並んでいるため、先頭をテスト配信
    item = items[0]

    print("以下の記事をテスト配信します。")
    print(f"タイトル: {item.get('title')}")
    print(f"情報源: {item.get('source')}")
    print(f"重要度: {item.get('importance')}")
    print(f"関連度: {item.get('relevance')}")
    print(f"URL: {item.get('url')}")

    message = make_urgent_message(item)

    success = post_to_chatwork(message)

    if success:
        print("✅ 実際の記事を使ったテスト配信が完了しました。")
    else:
        print("❌ テスト配信に失敗しました。")


if __name__ == "__main__":
    main()