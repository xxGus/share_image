"""Plugs the application with the database."""

from os import environ as env

from mongoengine import connect, disconnect


def init_app(_app):
    """Connect to the database."""
    disconnect()
    connect(env.get("DB_NAME"), host=env.get("DB_CONNECTION"))
