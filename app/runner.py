from app.database import init_db, save_news_items, mark_as_posted, update_analysis
from app.logger import logger
from app.chatwork import post_to_chatwork, make_urgent_message
from app.analyzers.rule_based import analyze_by_rules
from app.analyzers.analyzer import analyze_item

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


def analyze_new_items_with_ai(new_items):
    analyzed_items = []

    for item in new_items:
        analyzed_item = analyze_item(item)
        update_analysis(analyzed_item["url"], analyzed_item)
        analyzed_items.append(analyzed_item)

    return analyzed_items


def send_urgent_news(new_items):
    urgent_items = [
    item for item in new_items
    if (
        item.get("category") in ["助成金", "補助金"]
        or "助成金" in item.get("title", "")
        or "補助金" in item.get("title", "")
        or "キャリアアップ" in item.get("title", "")
        or "業務改善" in item.get("title", "")
    )
    and item.get("relevance", 3) >= 4
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
            mark_as_posted(item["url"])
            print(f"緊急配信完了: {item['title']}")
        else:
            print(f"緊急配信失敗: {item['title']}")

    logger.info(f"緊急配信件数: {posted_count}件")
    return posted_count


def run_daily_collection():
    init_db()

    all_items = collect_news()

    rule_analyzed_items = [
        analyze_by_rules(item)
        for item in all_items
    ]

    new_items = save_news_items(rule_analyzed_items)

    ai_analyzed_new_items = analyze_new_items_with_ai(new_items)

    urgent_posted_count = send_urgent_news(ai_analyzed_new_items)

    print("\n==============================")
    print("日次ニュース取得 完了")
    print(f"取得候補数: {len(all_items)}件")
    print(f"新着保存数: {len(new_items)}件")
    print(f"AI分析対象数: {len(ai_analyzed_new_items)}件")
    print(f"緊急配信数: {urgent_posted_count}件")
    print("==============================")

    logger.info(
        f"日次ニュース取得 完了: 取得候補数={len(all_items)}件 / 新着保存数={len(new_items)}件 / AI分析対象数={len(ai_analyzed_new_items)}件 / 緊急配信数={urgent_posted_count}件"
    )

    return {
        "all_count": len(all_items),
        "new_count": len(new_items),
        "ai_analyzed_count": len(ai_analyzed_new_items),
        "urgent_posted_count": urgent_posted_count,
        "new_items": ai_analyzed_new_items,
    }