from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import load_config

# Bootstrap - https://bootstrap-flask.readthedocs.io
bootstrap = Bootstrap5()

# Loads the configuration class for the environment specified in FLASK_ENVIRONMENT env variable
config = load_config()

# Flask SQL Alchemy - https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
db = SQLAlchemy()

# Flask Migrate - https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate()

# Flask Login - https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."

# Application Factory
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
    admin.add_view(ModelView(models.ProductCategory, db.session))
    admin.add_view(ModelView(models.Product, db.session))
    admin.add_view(ModelView(models.Order, db.session))

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.cli import bp as cli_bp

    app.register_blueprint(cli_bp)

    return app
