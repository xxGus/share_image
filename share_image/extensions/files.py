
from os import environ as env
from os import mkdir, path


def init_app(app):
    """Setup the file folder and files max length."""
    file_folder = path.abspath("files")

    env["FILE_FOLDER"] = file_folder

    if not path.isdir(file_folder):
        mkdir(file_folder)

    app.config["MAX_CONTENT_LENGHT"] = 2.566 * 1024 * 1024 