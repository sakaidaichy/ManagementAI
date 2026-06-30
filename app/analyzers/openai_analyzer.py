import json

from app.openai_client import get_client
from app.logger import logger


MODEL_NAME = "gpt-4.1-mini"


def analyze_by_openai(item: dict) -> dict:
    client = get_client()

    if client is None:
        logger.warning("OpenAI APIキーが未設定のため、AI分析をスキップします。")
        return item

    title = item.get("title", "")
    source = item.get("source", "")
    url = item.get("url", "")

    prompt = f"""
あなたは介護会社の管理部アシスタントです。

以下のニュースについて、介護会社の管理部向けに分析してください。

【情報源】
{source}

【タイトル】
{title}

【URL】
{url}

必ず次のJSON形式だけで返してください。

{{
  "summary": "200文字以内の要約",
  "impact": "介護会社への影響",
  "action": "管理部が取るべき対応",
  "importance": 1から5の整数,
  "relevance": 1から5の整数,
  "category": "助成金・補助金・労務・社会保険・税務・介護・熊本地域・未分類のいずれか"
}}
"""

    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt,
        )

        text = response.output_text
        data = json.loads(text)

        item["summary"] = data.get("summary", "")
        item["impact"] = data.get("impact", "")
        item["action"] = data.get("action", "")
        item["importance"] = int(data.get("importance", item.get("importance", 3)))
        item["relevance"] = int(data.get("relevance", item.get("relevance", 3)))
        item["category"] = data.get("category", item.get("category", "未分類"))

        return item

    except Exception as e:
        logger.error(f"OpenAI分析エラー: {e}")
        print(f"OpenAI分析エラー: {e}")
        return item