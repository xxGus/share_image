"""Plugs all App extensions."""

from os import environ as env

from . import (
    auth,
    cors,
    database,
    files,
)


def __load_test_only(app):
    """Load extensions related to tests and development environment."""
    extensions = [cors]

    for ext in extensions:
        ext.init_app(app)


def __load_production_only(app):
    """Load extensions used only at a production environment."""
    extensions = [cors]

    for ext in extensions:
        ext.init_app(app)


def load_extensions(app):
    """Attach App extensions."""
    extensions = [auth, database, cors]

    for ext in extensions:
        ext.init_app(app)

    if env.get("FLASK_ENV") == "development":
        __load_test_only(app)
    elif env.get("FLASK_ENV") == "production":
        __load_production_only(app)
