from flask import Blueprint, render_template

from app.database import init_db, get_recent_news

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    init_db()
    news_items = get_recent_news(limit=50)

    return render_template(
        "dashboard.html",
        news_items=news_items
    )