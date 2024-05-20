import os
from werkzeug.utils import secure_filename
from uuid import uuid4
from flask import current_app


class LocalStorage:
    def __init__(self):
        self.upload_folder = current_app.config["UPLOAD_FOLDER"]

    def upload(self, file):
        _, file_extension = file.filename.rsplit(".", 1)
        filename = secure_filename(f"{uuid4()}.{file_extension}")
        path = self._path(filename)
        file.save(path)
        return path

    def delete(self, file_path):
        os.remove(file_path)

    def _path(self, file_name):
        return os.path.join(self.upload_folder, file_name)
