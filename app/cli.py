from flask import Blueprint
from factories import (
    UserFactory,
    ProductCategoryFactory,
    ProductFactory,
    OrderFactory,
    OrderItemFactory,
)
from app.models.user import User
from app.extensions import db

bp = Blueprint("cli", __name__, cli_group=None)


@bp.cli.group()
def demo():
    """Creates data for demo purposes."""
    pass


@demo.command()
def seed():
    """Seed the database with demo data."""
    users = UserFactory.create_batch(2)

    categories = ProductCategoryFactory.create_batch(9)
    for category in categories:
        ProductFactory.create_batch(8, category_id=category.id)

    for user in users:
        orders = OrderFactory.create_batch(5, user_id=user.id)
        for order in orders:
            OrderItemFactory.create_batch(5, order_id=order.id)

    # Create Admin user
    admin_user = UserFactory.create(email="admin@demo.com", admin=True)
    password = User.generate_password()
    admin_user.set_password(password)
    db.session.add(admin_user)
    db.session.commit()
    print(f"Admin user created:\nEmail: admin@demo.com\nPassword: {password}")
    pass


@bp.cli.group()
def storage():
    """Storage commands."""
    pass


@storage.command()
def clean_local():
    """Clean local storage."""
    import shutil
    import os

    shutil.rmtree("app/static/uploads")
    os.makedirs("app/static/uploads")
    open("app/static/uploads/.gitkeep", "w").close()
    print("Local storage cleaned.")
    pass
