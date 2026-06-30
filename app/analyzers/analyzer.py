from app.config import (
    USE_OPENAI_ANALYSIS,
    AI_ANALYSIS_MIN_IMPORTANCE,
    AI_ANALYSIS_MIN_RELEVANCE,
)
from app.analyzers.rule_based import analyze_by_rules
from app.analyzers.openai_analyzer import analyze_by_openai


def should_use_openai(item: dict) -> bool:
    importance = item.get("importance", 3)
    relevance = item.get("relevance", 3)

    return (
        USE_OPENAI_ANALYSIS
        and importance >= AI_ANALYSIS_MIN_IMPORTANCE
        and relevance >= AI_ANALYSIS_MIN_RELEVANCE
    )


def analyze_item(item: dict) -> dict:
    item = analyze_by_rules(item)

    if should_use_openai(item):
        item = analyze_by_openai(item)

    return item


def analyze_items(items: list[dict]) -> list[dict]:
    analyzed_items = []

    for item in items:
        analyzed_items.append(analyze_item(item))

    return analyzed_items