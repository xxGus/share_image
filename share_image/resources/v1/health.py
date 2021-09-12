from flask_restful import Resource
from share_image.utils.http_reponses import success


class HealthCheck(Resource):
    """Provide a GET method to check if the system is available."""

    def get(self):
        """Always return success, to check API availability."""
        return success({"v": "1.0"})
