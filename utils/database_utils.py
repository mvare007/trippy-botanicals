from os import environ, makedirs, path

from utils.azure_db_connection import AzureDbConnection, ConnectionSettings

from app.extensions import db
from config import DevelopmentConfig, base_dir

environment = environ.get("FLASK_ENV")


def setup_database_connection(app):
    if environment == "production":
        setup_azure_database_connection(app)
    elif environment == "development":
        create_development_database()
        db.init_app(app)
    elif environment == "test":
        db.init_app(app)
    else:
        raise ValueError(f"Invalid environment name: {environment}")


def create_development_database():
    """
    Creates a development SQLite database in the tmp folder if it doesn't exist.
    Poor man's solution to avoid paying for an Azure SQL database for development :-)
    """

    if environment != "development":
        raise ValueError(
            "This function should only be used in development environment."
        )

    db_name = f"{DevelopmentConfig.DATABASE_NAME}.db"
    if not path.exists(path.join(base_dir, "tmp")):
        makedirs(path.join(base_dir, "tmp"))
    if not path.exists(path.join(base_dir, "tmp", db_name)):
        with open(path.join(base_dir, "tmp", db_name), "w") as f:
            f.write("")


def setup_azure_database_connection(app):
    conn_settings = ConnectionSettings(
        server=environ.get("AZURE_DB_SERVER"),
        database=environ.get("AZURE_DB_NAME"),
        username=environ.get("AZURE_DB_USERNAME"),
        password=environ.get("AZURE_DB_PASSWORD"),
    )
    db_conn = AzureDbConnection(conn_settings)
    db_conn.connect()
