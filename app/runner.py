from app.database import init_db, save_news_items
from app.logger import logger
from app.chatwork import post_to_chatwork, make_urgent_message

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


def collect_news():
    logger.info("ニュース取得を開始します。")
    print("ニュース取得を開始します。")

    all_items = []

    for source in SOURCES:
        print(f"取得中: {source['name']}")

        items = extract_links(
            source_name=source["name"],
            base_url=source["url"],
            keywords=source["keywords"],
        )

        all_items.extend(items)

    logger.info(f"ニュース取得完了: {len(all_items)}件")
    return all_items


def send_urgent_news(new_items):
    urgent_items = [
        item for item in new_items
        if item.get("importance", 3) >= 5
    ]

    if not urgent_items:
        print("緊急配信対象はありません。")
        logger.info("緊急配信対象なし")
        return 0

    posted_count = 0

    for item in urgent_items:
        message = make_urgent_message(item)
        success = post_to_chatwork(message)

        if success:
            posted_count += 1
            print(f"緊急配信完了: {item['title']}")
        else:
            print(f"緊急配信失敗: {item['title']}")

    logger.info(f"緊急配信件数: {posted_count}件")
    return posted_count


def run_daily_collection():
    init_db()

    all_items = collect_news()
    new_items = save_news_items(all_items)

    urgent_posted_count = send_urgent_news(new_items)

    print("\n==============================")
    print("日次ニュース取得 完了")
    print(f"取得候補数: {len(all_items)}件")
    print(f"新着保存数: {len(new_items)}件")
    print(f"緊急配信数: {urgent_posted_count}件")
    print("==============================")

    logger.info(
        f"日次ニュース取得 完了: 取得候補数={len(all_items)}件 / 新着保存数={len(new_items)}件 / 緊急配信数={urgent_posted_count}件"
    )

    return {
        "all_count": len(all_items),
        "new_count": len(new_items),
        "urgent_posted_count": urgent_posted_count,
        "new_items": new_items,
    }