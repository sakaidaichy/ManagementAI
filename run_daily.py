from app.runner import run_daily_collection


def main():
    result = run_daily_collection()

    if result["new_count"] == 0:
        print("新着ニュースはありません。")
        return

    print("\n【新着ニュース】")

    for i, item in enumerate(result["new_items"], start=1):
        print("------------------------------")
        print(f"{i}. {item['title']}")
        print(f"情報源: {item['source']}")
        print(f"カテゴリ: {item.get('category', '未分類')}")
        print(f"重要度: {item.get('importance', 3)}")
        print(f"URL: {item['url']}")


if __name__ == "__main__":
    main()