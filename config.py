import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".flaskenv"))


class BaseConfig:
    DIR = os.path.dirname(os.path.abspath(__file__))
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    BOOTSTRAP_BOOTSWATCH_THEME = "lux"
    FLASK_ADMIN_SWATCH = "cyborg"
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")
    UPLOAD_FOLDER = f"{base_dir}/app/static/uploads"
    MAX_CONTENT_LENGTH = 10 * 1000 * 1000  # 10MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    LOG_LEVEL = "DEBUG"


class ProductionConfig(BaseConfig):
    ENVIRONMENT = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    LOG_LEVEL = "WARNING"


class DevelopmentConfig(BaseConfig):
    ENVIRONMENT = "development"
    DATABASE_NAME = "trippy"
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(base_dir, "tmp", f"{DATABASE_NAME}.db")
    )
    DATABASE_USER = "root"
    DATABASE_PASSWORD = "root"
    SQLALCHEMY_ECHO = True  # log all the statements issued to stderr.


class TestingConfig(BaseConfig):
    ENVIRONMENT = "test"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DATABASE_USER = "root"
    DATABASE_PASSWORD = "root"
    WTF_CSRF_ENABLED = False


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
