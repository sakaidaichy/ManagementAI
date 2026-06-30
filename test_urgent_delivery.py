from app.runner import send_urgent_news

test_items = [
    {
        "source": "ManagementAI テスト",
        "title": "【重要テスト】キャリアアップ助成金の申請期限が変更されました",
        "url": "https://example.com/urgent-test",
        "category": "助成金",
        "importance": 5,
        "relevance": 5,
        "summary": "キャリアアップ助成金の申請期限変更を想定したテスト配信です。",
        "impact": "正社員化コース等の申請予定がある場合、期限確認が必要です。",
        "action": "申請予定案件の有無を確認し、必要に応じて社労士へ確認してください。",
    }
]

send_urgent_news(test_items)