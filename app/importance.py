def judge_importance(title: str) -> int:
    title = title or ""

    importance_5_keywords = [
        "助成金",
        "補助金",
        "キャリアアップ",
        "業務改善",
        "人材開発",
        "両立支援",
        "受付開始",
        "申請受付",
        "申請期限",
        "締切",
        "募集開始",
        "公募開始",
        "要件変更",
        "様式変更",
        "支給要件",
    ]

    importance_4_keywords = [
        "処遇改善",
        "介護報酬",
        "介護保険",
        "最低賃金",
        "法改正",
        "育児",
        "介護休業",
        "社会保険",
        "年金",
        "税",
        "熊本",
        "玉名",
    ]

    low_priority_keywords = [
        "統計",
        "審議会",
        "検討会",
        "報道発表",
        "労働災害発生状況",
        "告発",
    ]

    for keyword in low_priority_keywords:
        if keyword in title:
            return 2

    for keyword in importance_5_keywords:
        if keyword in title:
            return 5

    for keyword in importance_4_keywords:
        if keyword in title:
            return 4

    return 3


def stars(importance: int) -> str:
    return "★" * importance + "☆" * (5 - importance)