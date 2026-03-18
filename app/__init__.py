"""
Application factory for MotionMate.
"""

from flask import Flask
from .config import get_config
from .models.db import init_db
from .routes.main import main_bp
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .routes.exercises import exercises_bp
from .routes.sessions import sessions_bp


def create_app(config_name: str = None) -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    cfg = get_config(config_name)
    app.config.from_object(cfg)

    init_db(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(exercises_bp, url_prefix="/exercises")
    app.register_blueprint(sessions_bp, url_prefix="/sessions")

    return app
