from app.chatwork import make_urgent_message, post_to_chatwork

test_item = {
    "source": "ManagementAI テスト",
    "title": "【テスト配信】ManagementAIの動作確認です",
    "url": "https://example.com",
    "category": "システム",
    "importance": 5,
    "relevance": 5,
    "summary": "これはChatwork配信テストです。",
    "impact": "会社への影響はありません。",
    "action": "正常に受信できるか確認してください。"
}

message = make_urgent_message(test_item)

print("===== Chatworkへ送信する内容 =====")
print(message)

success = post_to_chatwork(message)

if success:
    print("✅ Chatworkへ送信しました。")
else:
    print("❌ Chatworkへの送信に失敗しました。")