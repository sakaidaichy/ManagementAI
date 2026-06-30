from app.database import init_db, save_news_items
from collectors.common import extract_links


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


def main():
    print("日次ニュース取得を開始します。")

    init_db()

    all_items = []

    for source in SOURCES:
        print(f"取得中: {source['name']}")
        items = extract_links(
            source_name=source["name"],
            base_url=source["url"],
            keywords=source["keywords"]
        )
        all_items.extend(items)

    new_items = save_news_items(all_items)

    print("取得完了")
    print(f"取得候補数: {len(all_items)}件")
    print(f"新着保存数: {len(new_items)}件")


if __name__ == "__main__":
    main()