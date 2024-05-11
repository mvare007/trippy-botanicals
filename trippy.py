import sqlalchemy as sa
import sqlalchemy.orm as orm

from app import create_app
from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.user import User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "sa": sa,
        "orm": orm,
        "db": db,
        "session": db.session,
        "User": User,
        "ProductCategory": ProductCategory,
        "Product": Product,
        "Order": Order,
        "OrderItem": OrderItem,
    }
