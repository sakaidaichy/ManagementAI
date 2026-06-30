from flask import Flask

from web.routes.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(dashboard_bp)

    return app