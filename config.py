import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".flask_env"))


class Config:
    DIR = os.path.dirname(os.path.abspath(__file__))
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    DATABASE_NAME = "trippy"
    BOOTSTRAP_BOOTSWATCH_THEME = "lux"
    FLASK_ADMIN_SWATCH = "cyborg"
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")
    UPLOAD_FOLDER = f"{base_dir}/app/static/uploads"
    MAX_CONTENT_LENGTH = 10 * 1000 * 1000  # 10MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


class ProductionConfig(Config):
    ENVIRONMENT = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")


class DevelopmentConfig(Config):
    ENVIRONMENT = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(base_dir, "tmp", f"{Config.DATABASE_NAME}.db")
    )
    DATABASE_USER = "root"
    DATABASE_PASSWORD = "root"
    SQLALCHEMY_ECHO = True # log all the statements issued to stderr.

    # Create Development Database if it doesn't exist
    if not os.path.exists(os.path.join(base_dir, "tmp")):
        os.makedirs(os.path.join(base_dir, "tmp"))
    if not os.path.exists(os.path.join(base_dir, "tmp", f"{Config.DATABASE_NAME}.db")):
        with open(
            os.path.join(base_dir, "tmp", f"{Config.DATABASE_NAME}.db"), "w"
        ) as f:
            f.write("")


class TestingConfig(Config):
    ENVIRONMENT = "test"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DATABASE_USER = "root"
    DATABASE_PASSWORD = "root"


def load_config(test=False):
    if test:
        return TestingConfig

    environment = os.environ.get("FLASK_ENV")
    config_mapping = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
    }

    try:
        configuration = config_mapping[environment]()
    except KeyError:
        raise ValueError(f"Invalid environment name: {environment}")

    return configuration