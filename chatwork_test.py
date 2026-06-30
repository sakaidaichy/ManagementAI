import os
import requests
from dotenv import load_dotenv

load_dotenv()

CHATWORK_API_TOKEN = os.getenv("CHATWORK_API_TOKEN")
CHATWORK_ROOM_ID = os.getenv("CHATWORK_ROOM_ID")


def post_to_chatwork(message):
    url = f"https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages"

    headers = {
        "X-ChatWorkToken": CHATWORK_API_TOKEN
    }

    data = {
        "body": message
    }

    response = requests.post(url, headers=headers, data=data, timeout=15)
    response.raise_for_status()

    print("Chatworkへの投稿が完了しました。")


message = """【労務・助成金ニュースBot｜テスト投稿】

このメッセージは、Roumu_News_Botからのテスト投稿です。

今後、助成金・労務・介護制度に関する重要情報を自動配信します。
"""

post_to_chatwork(message)