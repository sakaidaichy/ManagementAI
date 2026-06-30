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
    item["summary"] = ""
    item["impact"] = ""
    item["action"] = ""

    return item


def judge_relevance(title: str) -> int:
    title = title or ""

    relevance_5_keywords = [
        "介護",
        "高齢者",
        "処遇改善",
        "助成金",
        "キャリアアップ",
        "業務改善",
        "人材開発",
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
        "補助金",
        "DX",
    ]

    for keyword in relevance_5_keywords:
        if keyword in title:
            return 5

    for keyword in relevance_4_keywords:
        if keyword in title:
            return 4

    return 3