import logging
from app.config import LOG_PATH

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("roumu_news_bot")