from flask import Flask

from app.auth import bp as auth_bp
from app.cli import bp as cli_bp
from app.extensions import (
    bootstrap,
    db,
    login_manager,
    migrate,
    register_flask_admin,
    toolbar,
)
from app.main import bp as main_bp
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.user import User
from config import load_config
from utils.database_utils import setup_database_connection
from utils.logger import init_logger


def create_app(test=False):
    app = Flask(__name__)
    config = load_config(test)
    app.config.from_object(config)

    with app.app_context():
        init_logger(app)
        register_extensions(app)
        register_blueprints(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    setup_database_connection(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    toolbar.init_app(app)
    register_flask_admin(app, db, [User, Product, ProductCategory, Order, OrderItem])


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cli_bp)
