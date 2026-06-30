from app.database import init_db, get_recent_news
from app.importance import stars


def make_weekly_report():
    init_db()

    items = get_recent_news(limit=20)

    if not items:
        return "【労務・助成金ニュース週報】\n\n今週のニュースはありません。"

    lines = []
    lines.append("【労務・助成金ニュース週報】")
    lines.append("")
    lines.append("今週確認された主な労務・助成金・介護関連ニュースです。")
    lines.append("")

    for i, item in enumerate(items, start=1):
        lines.append(f"■{i}. {item['title']}")
        lines.append(f"重要度：{stars(item.get('importance', 3))}")
        lines.append(f"関連度：{stars(item.get('relevance', 3))}")
        lines.append(f"カテゴリ：{item.get('category', '未分類')}")
        lines.append(f"情報源：{item.get('source', '')}")

        if item.get("summary"):
            lines.append(f"要約：{item['summary']}")

        if item.get("impact"):
            lines.append(f"影響：{item['impact']}")

        if item.get("action"):
            lines.append(f"対応：{item['action']}")

        lines.append(f"URL：{item.get('url', '')}")
        lines.append("")

    lines.append("※最終判断は管理部および専門家確認のうえ行ってください。")

    return "\n".join(lines)