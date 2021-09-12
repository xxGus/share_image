"""Plugs methods to handle CORS."""

from flask_cors import CORS


def init_app(app):
    """Attach CORS library to Flask app."""
    CORS(app, resources={r"/api/*": {"origins": "*"}})
