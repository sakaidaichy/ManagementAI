from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "news.db"
LOG_PATH = LOG_DIR / "bot.log"

CHATWORK_API_TOKEN = os.getenv("CHATWORK_API_TOKEN")
CHATWORK_ROOM_ID = os.getenv("CHATWORK_ROOM_ID")

APP_MODE = os.getenv("APP_MODE", "test")

REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0"

SOURCES = [
    {
        "name": "やまがみ社会保険労務士事務所",
        "url": "https://sr-ky.net/",
        "keywords": ["助成金", "キャリアアップ", "業務改善", "人材開発", "両立支援"],
    },
    {
        "name": "厚生労働省",
        "url": "https://www.mhlw.go.jp/",
        "keywords": ["助成金", "雇用", "労働", "育児", "介護", "法改正", "賃金"],
    },
    {
        "name": "熊本労働局",
        "url": "https://jsite.mhlw.go.jp/kumamoto-roudoukyoku/",
        "keywords": ["助成金", "雇用", "労働", "最低賃金", "求人"],
    },
    {
        "name": "熊本市",
        "url": "https://www.city.kumamoto.jp/",
        "keywords": ["高齢者", "介護", "事業者", "補助金", "助成金"],
    },
    {
        "name": "玉名市",
        "url": "https://www.city.tamana.lg.jp/",
        "keywords": ["高齢介護", "介護", "高齢者", "事業者", "補助金"],
    },
]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI_ANALYSIS = os.getenv("USE_OPENAI_ANALYSIS", "false").lower() == "true"

AI_ANALYSIS_MIN_IMPORTANCE = 4
AI_ANALYSIS_MIN_RELEVANCE = 4