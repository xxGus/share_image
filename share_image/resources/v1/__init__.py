"""Configure Flask Blueprint and add API routes."""

from flask import Blueprint
from flask_restful import Api

from . import (
    health
)
from .dashboard import (
    dash,
    login,
    register
)

from .backoffice import backoffice

api_v1 = Blueprint("api", __name__, url_prefix="/api/v1")
endpoints = Api(api_v1)


def init_app(app):
    """Add API routes."""
    endpoints.add_resource(dash.ImageUpload, "/dash/image-upload")
    endpoints.add_resource(register.Register, "/dash/register")

    endpoints.add_resource(login.Login, "/login")
    endpoints.add_resource(login.RefreshToken, "/login/refresh")
    
    endpoints.add_resource(backoffice.Backoffice, "/backoffice/uploads-history")

    endpoints.add_resource(health.HealthCheck, '/status')
    app.register_blueprint(api_v1)