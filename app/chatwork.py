import requests

from app.config import CHATWORK_API_TOKEN, CHATWORK_ROOM_ID, APP_MODE
from app.importance import stars
from app.logger import logger


def post_to_chatwork(message: str) -> bool:
    if APP_MODE != "production":
        print("\n【TEST MODE】Chatworkには投稿しません。")
        print("-------- 投稿予定メッセージ --------")
        print(message)
        print("----------------------------------")
        logger.info("TEST MODEのためChatwork投稿をスキップ")
        return True

    if not CHATWORK_API_TOKEN or not CHATWORK_ROOM_ID:
        print("Chatwork設定が未入力のため投稿をスキップしました。")
        logger.warning("Chatwork設定が未入力です。")
        return False

    url = f"https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages"

    headers = {
        "X-ChatWorkToken": CHATWORK_API_TOKEN
    }

    data = {
        "body": message
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=15)
        response.raise_for_status()
        logger.info("Chatwork投稿成功")
        return True

    except Exception as e:
        print(f"Chatwork投稿エラー: {e}")
        logger.error(f"Chatwork投稿エラー: {e}")
        return False


def make_urgent_message(item: dict) -> str:
    importance = item.get("importance", 3)

    summary = item.get("summary") or "要約は未作成です。原文の確認をお願いします。"
    impact = item.get("impact") or "助成金・労務・介護制度・補助金等に関係する可能性があります。"
    action = item.get("action") or "原文確認、申請予定・社内運用への影響確認、必要に応じた専門家確認をお願いします。"

    return f"""【労務・助成金ニュースBot｜緊急配信】

■重要度
{stars(importance)}

■会社関連度
{stars(item.get("relevance", 3))}

■カテゴリ
{item.get("category", "未分類")}

■情報源
{item.get("source", "")}

■タイトル
{item.get("title", "")}

■要約
{summary}

■当社への影響
{impact}

■管理部対応
{action}

■参考URL
{item.get("url", "")}

※記事本文の転載ではなく、更新情報の通知です。
※最終判断は管理部および専門家確認のうえ行ってください。
"""