from flask import Blueprint
from factories import (
    UserFactory,
    ProductCategoryFactory,
    ProductFactory,
    OrderFactory,
    OrderItemFactory,
)
from random import randint

bp = Blueprint("cli", __name__, cli_group=None)


@bp.cli.group()
def demo():
    """Creates data for demo purposes."""
    pass


@demo.command()
def seed():
    UserFactory.create_batch(15)

    categories = ProductCategoryFactory.create_batch(9)
    for category in categories:
        ProductFactory.create_batch(12, product_category=category)

    orders = OrderFactory.create_batch(35)
    for order in orders:
        OrderItemFactory.create_batch(5, order=order)

    # Create Admin user
    admin_user = UserFactory.create(email="admin@demo.com", admin=True)
    admin_user.set_password("admin")
    print("Admin user created:\nEmail: admin@demo.com\nPassword: admin")
    pass
