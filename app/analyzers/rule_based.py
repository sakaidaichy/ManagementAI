from app.importance import judge_importance
from app.categories import judge_category


def analyze_by_rules(item: dict) -> dict:
    title = item.get("title", "")

    importance = judge_importance(title)
    category = judge_category(title)
    relevance = judge_relevance(title)

    item["importance"] = importance
    item["category"] = category
    item["relevance"] = relevance
    item["summary"] = item.get("summary", "")
    item["impact"] = item.get("impact", "")
    item["action"] = item.get("action", "")

    return item


def judge_relevance(title: str) -> int:
    title = title or ""

    relevance_5_keywords = [
        "助成金",
        "補助金",
        "キャリアアップ",
        "業務改善",
        "人材開発",
        "両立支援",
        "処遇改善",
        "介護報酬",
        "介護保険",
        "高齢者",
        "熊本",
        "玉名",
    ]

    relevance_4_keywords = [
        "雇用",
        "労働",
        "最低賃金",
        "社会保険",
        "年金",
        "税",
        "DX",
        "省力化",
        "IT導入",
    ]

    low_relevance_keywords = [
        "統計",
        "審議会",
        "検討会",
        "報道発表",
        "労働災害発生状況",
        "告発",
    ]

    for keyword in low_relevance_keywords:
        if keyword in title:
            return 2

    for keyword in relevance_5_keywords:
        if keyword in title:
            return 5

    for keyword in relevance_4_keywords:
        if keyword in title:
            return 4

    return 3