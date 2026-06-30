import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def is_openai_enabled() -> bool:
    return bool(OPENAI_API_KEY)