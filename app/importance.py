def judge_importance(title: str) -> int:
    title = title or ""

    importance_5_keywords = [
        "受付開始",
        "申請受付",
        "申請期限",
        "締切",
        "終了",
        "停止",
        "廃止",
        "変更",
        "改正",
        "義務化",
        "様式変更",
        "要件変更",
        "支給要件",
        "募集開始",
        "公募開始",
    ]

    importance_4_keywords = [
        "助成金",
        "補助金",
        "キャリアアップ",
        "業務改善",
        "人材開発",
        "両立支援",
        "最低賃金",
        "処遇改善",
        "介護報酬",
        "Q&A",
        "リーフレット",
        "パンフレット",
    ]

    for keyword in importance_5_keywords:
        if keyword in title:
            return 5

    for keyword in importance_4_keywords:
        if keyword in title:
            return 4

    return 3


def stars(importance: int) -> str:
    return "★" * importance + "☆" * (5 - importance)