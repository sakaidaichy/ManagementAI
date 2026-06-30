from app.analyzers.openai_analyzer import analyze_by_openai
from app.chatwork import make_urgent_message, post_to_chatwork


def main():
    test_item = {
        "source": "テスト",
        "title": "キャリアアップ助成金の支給要件が変更されました",
        "url": "https://example.com/test-ai-message",
        "category": "助成金",
        "importance": 5,
        "relevance": 5,
    }

    analyzed_item = analyze_by_openai(test_item)

    message = make_urgent_message(analyzed_item)

    print("=== Chatwork投稿文プレビュー ===")
    print(message)

    # APP_MODE=testなら実際にはChatwork投稿されず、ターミナル表示のみです。
    post_to_chatwork(message)


if __name__ == "__main__":
    main()