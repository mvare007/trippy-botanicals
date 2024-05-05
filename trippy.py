import sqlalchemy as sa
import sqlalchemy.orm as orm

from app import create_app
from app.extensions import db
from app.models import Order, OrderItem, Product, ProductCategory, User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "sa": sa,
        "orm": orm,
        "db": db,
        "User": User,
        "ProductCategory": ProductCategory,
        "Product": Product,
        "Order": Order,
        "OrderItem": OrderItem,
    }
