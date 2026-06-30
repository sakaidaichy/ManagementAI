from openai import OpenAI

from app.config import OPENAI_API_KEY


def get_client():
    if not OPENAI_API_KEY:
        return None

    return OpenAI(api_key=OPENAI_API_KEY)