"""The Application entry point."""
from flask import Flask
from share_image.extensions import configurations
from share_image.resources import v1
from flask_cors import CORS


def create_app():
    """
    The application start function.

    Please, consult README.md file to see the importance of FLASK_APP env var
    """
    app = Flask(__name__)
    configurations.load_extensions(app)

    v1.init_app(app)

    return app


if __name__ == "__main__":
    APP = create_app()

    APP.run(host="0.0.0.0")
