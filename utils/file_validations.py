from flask import current_app


def allowed_file(file):
    filename = file.filename
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
        and file.content_length < current_app.config["MAX_CONTENT_LENGTH"]
    )
