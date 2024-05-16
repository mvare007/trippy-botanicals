import logging
from logging.handlers import RotatingFileHandler
from os import path

from config import base_dir


def init_logger(app):
    log_dir = path.join(base_dir, "log")
    log_level = app.config["LOG_LEVEL"]
    app.logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    stream_handler.setFormatter(stream_formatter)
    app.logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler(
        path.join(log_dir, "flask_app.log"), maxBytes=16384, backupCount=20
    )
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.info("Trippy starting up...")
