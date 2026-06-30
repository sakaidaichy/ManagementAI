from app.config import USE_OPENAI_ANALYSIS
from app.analyzers.rule_based import analyze_by_rules


def analyze_item(item: dict) -> dict:
    if USE_OPENAI_ANALYSIS:
        # 後でOpenAI分析をここに追加します
        return analyze_by_rules(item)

    return analyze_by_rules(item)


def analyze_items(items: list[dict]) -> list[dict]:
    analyzed_items = []

    for item in items:
        analyzed_items.append(analyze_item(item))

    return analyzed_items