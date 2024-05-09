from flask import Flask
from config import load_config
from app.main import bp as main_bp
from app.auth import bp as auth_bp
from app.cli import bp as cli_bp
from app.extensions import db, migrate, login_manager, bootstrap, register_flask_admin
from app.models.user import User
from app.models.product_category import ProductCategory
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

def create_app(test=False):
    app = Flask(__name__)
    config = load_config(test)
    app.config.from_object(config)

    with app.app_context():
        register_extensions(app)
        register_blueprints(app)

    return app

def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    register_flask_admin(app, db, [User, Product, ProductCategory, Order, OrderItem])


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cli_bp)