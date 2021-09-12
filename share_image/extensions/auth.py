"""Plugs methods to handle with the file folder."""
import datetime
import os

from flask_jwt_extended import JWTManager


def init_app(app):
    """Setup authentication."""
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)
    jwt_manager = JWTManager(app)