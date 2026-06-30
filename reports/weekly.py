from app.database import init_db, get_news_since
from app.importance import stars


MAX_WEEKLY_ITEMS = 10
MAIN_NEWS_COUNT = 3


PRIORITY_KEYWORDS = [
    "助成金",
    "補助金",
    "キャリアアップ",
    "業務改善",
    "人材開発",
    "両立支援",
    "公募",
    "申請",
    "募集",
]


LOW_PRIORITY_KEYWORDS = [
    "労働災害",
    "労災",
    "統計",
    "審議会",
    "検討会",
    "報道発表",
    "告発",
]


def priority_score(item):
    title = item.get("title", "")
    category = item.get("category", "")

    score = 0

    if category in ["助成金", "補助金"]:
        score += 100

    for keyword in PRIORITY_KEYWORDS:
        if keyword in title:
            score += 50

    for keyword in LOW_PRIORITY_KEYWORDS:
        if keyword in title:
            score -= 100

    score += item.get("importance", 3) * 10
    score += item.get("relevance", 3) * 5

    return score


def make_weekly_report():
    init_db()

    items = get_news_since(days=7)

    if not items:
        return "【ManagementAI 週間ニュース】\n\n直近7日間のニュースはありません。"

    sorted_items = sorted(
        items,
        key=lambda item: (
            priority_score(item),
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
    lines.append("直近7日間のニュースから、助成金・補助金情報を優先して最大10件に絞って配信します。")
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