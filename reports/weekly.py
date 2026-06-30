from app.database import init_db, get_news_since
from app.importance import stars


MAX_WEEKLY_ITEMS = 10
MAIN_NEWS_COUNT = 3


def make_weekly_report():
    init_db()

    items = get_news_since(days=7)

    if not items:
        return "【ManagementAI 週間ニュース】\n\n直近7日間のニュースはありません。"

    # 重要度・関連度・新しさ順で並び替え
    sorted_items = sorted(
        items,
        key=lambda item: (
            item.get("importance", 3),
            item.get("relevance", 3),
            item.get("created_at", ""),
        ),
        reverse=True,
    )

    selected_items = sorted_items[:MAX_WEEKLY_ITEMS]

    main_items = selected_items[:MAIN_NEWS_COUNT]
    other_items = selected_items[MAIN_NEWS_COUNT:]

    lines = []
    lines.append("【ManagementAI 週間ニュース】")
    lines.append("")
    lines.append("直近7日間の労務・助成金・介護関連ニュースから、重要度の高い情報を最大10件に絞って配信します。")
    lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    lines.append("🔥 今週の重要ニュース")
    lines.append("━━━━━━━━━━━━━━")
    lines.append("")

    for i, item in enumerate(main_items, start=1):
        lines.append(f"■{i}. {item.get('title', '')}")
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

    if other_items:
        lines.append("━━━━━━━━━━━━━━")
        lines.append("📌 その他の注目ニュース")
        lines.append("━━━━━━━━━━━━━━")
        lines.append("")

        for item in other_items:
            lines.append(
                f"・{stars(item.get('importance', 3))} "
                f"【{item.get('category', '未分類')}】"
                f"{item.get('title', '')}"
            )
            lines.append(f"  {item.get('url', '')}")

        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    lines.append("📊 今週の集計")
    lines.append("━━━━━━━━━━━━━━")
    lines.append(f"取得ニュース：{len(items)}件")
    lines.append(f"週報掲載：{len(selected_items)}件")
    lines.append("")
    lines.append("※最終判断は管理部および専門家確認のうえ行ってください。")

    return "\n".join(lines)