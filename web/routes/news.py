from flask import Blueprint, render_template, request

from app.database import init_db, search_news

news_bp = Blueprint("news", __name__)


@news_bp.route("/news")
def news_index():
    init_db()

    keyword = request.args.get("keyword", "")
    category = request.args.get("category", "")
    min_importance = request.args.get("min_importance", "0")

    try:
        min_importance = int(min_importance)
    except ValueError:
        min_importance = 0

    news_items = search_news(
        keyword=keyword,
        category=category,
        min_importance=min_importance,
    )

    return render_template(
        "news.html",
        news_items=news_items,
        keyword=keyword,
        category=category,
        min_importance=min_importance,
    )