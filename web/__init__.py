from flask import Flask

from web.routes.dashboard import dashboard_bp
from web.routes.news import news_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(news_bp)

    return app