from os import environ

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Bootstrap - https://bootstrap-flask.readthedocs.io
bootstrap = Bootstrap5()

# Configuration
environment = environ["FLASK_ENV"]
if environment == "production":
    from config import ProductionConfig

    config = ProductionConfig()
elif environment == "development":
    from config import DevelopmentConfig

    config = DevelopmentConfig()
elif environment == "test":
    from config import TestingConfig

    config = TestingConfig()
else:
    raise ValueError("Invalid environment name")

# Flask SQL Alchemy - https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
db = SQLAlchemy()

# Flask Migrate - https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate()

# Flask Login - https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from app import models

    admin = Admin(app, name="Trippy Botanicals", template_mode="bootstrap3")
    admin.add_view(ModelView(models.User, db.session))
    admin.add_view(ModelView(models.Product, db.session))

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    # from app.admin import bp as admin_bp

    # app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.cli import bp as cli_bp

    app.register_blueprint(cli_bp)

    return app
