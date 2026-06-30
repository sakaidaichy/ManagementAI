def judge_category(title: str) -> str:
    title = title or ""

    rules = {
        "助成金": [
            "助成金",
            "キャリアアップ",
            "業務改善",
            "人材開発",
            "両立支援",
        ],
        "補助金": [
            "補助金",
            "公募",
            "省力化",
            "IT導入",
            "持続化",
        ],
        "労務": [
            "労働",
            "雇用",
            "最低賃金",
            "育児",
            "介護休業",
            "法改正",
        ],
        "社会保険": [
            "年金",
            "健康保険",
            "厚生年金",
            "社会保険",
            "保険料",
        ],
        "税務": [
            "税",
            "年末調整",
            "源泉",
            "所得税",
            "住民税",
        ],
        "介護": [
            "介護",
            "高齢者",
            "介護報酬",
            "処遇改善",
            "BCP",
            "感染症",
        ],
        "熊本・地域": [
            "熊本",
            "玉名",
            "地域",
            "市",
            "県",
        ],
    }

    for category, keywords in rules.items():
        for keyword in keywords:
            if keyword in title:
                return category

    return "未分類"