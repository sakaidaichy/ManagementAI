from app.analyzers.openai_analyzer import analyze_by_openai


def main():
    test_item = {
        "source": "テスト",
        "title": "キャリアアップ助成金の支給要件が変更されました",
        "url": "https://example.com/test",
        "category": "助成金",
        "importance": 5,
        "relevance": 5,
    }

    result = analyze_by_openai(test_item)

    print("=== AI分析結果 ===")
    print(f"要約: {result.get('summary')}")
    print(f"影響: {result.get('impact')}")
    print(f"対応: {result.get('action')}")
    print(f"重要度: {result.get('importance')}")
    print(f"関連度: {result.get('relevance')}")
    print(f"カテゴリ: {result.get('category')}")


if __name__ == "__main__":
    main()