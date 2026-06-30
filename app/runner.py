from app.database import init_db, save_news_items
from app.logger import logger
from app.chatwork import post_to_chatwork, make_urgent_message
from app.analyzers.analyzer import analyze_items

from collectors import yamagami
from collectors import mhlw
from collectors import kumamoto_labor
from collectors import kumamoto_city
from collectors import tamana_city


COLLECTORS = [
    yamagami,
    mhlw,
    kumamoto_labor,
    kumamoto_city,
    tamana_city,
]


def collect_news():
    logger.info("ニュース取得を開始します。")
    print("ニュース取得を開始します。")

    all_items = []

    for collector in COLLECTORS:
        items = collector.collect()
        all_items.extend(items)

    logger.info(f"ニュース取得完了: {len(all_items)}件")
    return all_items


def send_urgent_news(new_items):
    urgent_items = [
        item for item in new_items
        if item.get("importance", 3) >= 5 and item.get("relevance", 3) >= 4
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

    analyzed_items = analyze_items(all_items)

    new_items = save_news_items(analyzed_items)

    urgent_posted_count = send_urgent_news(new_items)

    print("\n==============================")
    print("日次ニュース取得 完了")
    print(f"取得候補数: {len(all_items)}件")
    print(f"分析済み件数: {len(analyzed_items)}件")
    print(f"新着保存数: {len(new_items)}件")
    print(f"緊急配信数: {urgent_posted_count}件")
    print("==============================")

    logger.info(
        f"日次ニュース取得 完了: 取得候補数={len(all_items)}件 / 分析済み件数={len(analyzed_items)}件 / 新着保存数={len(new_items)}件 / 緊急配信数={urgent_posted_count}件"
    )

    return {
        "all_count": len(all_items),
        "analyzed_count": len(analyzed_items),
        "new_count": len(new_items),
        "urgent_posted_count": urgent_posted_count,
        "new_items": new_items,
    }