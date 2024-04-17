import sqlalchemy as sql
from flask import jsonify, render_template, request
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.main.forms import CheckoutForm
from app.models import Order, OrderItem, Product, ProductCategory


@bp.route("/")
@bp.route("/index")
def index():
    product_categories = ProductCategory.query.all()

    return render_template(
        "index.html", title="Home", product_categories=product_categories
    )


@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@bp.route("/products?category_id=<category_id>")
@bp.route("/products", defaults={"category_id": None})
def products(category_id):
    """List products by category. If no category is provided, list all products."""
    if category_id:
        products = Product.query.filter(Product.category_id == category_id).all()
    else:
        products = Product.query.all()

    return render_template("products.html", products=products)


@bp.route("/orders/<id>/update", methods=["PATCH"])
@login_required
def update_order(id):
    """Add a product to an order. If the product is already in the order, increase the quantity by 1."""
    params = request.json
    product_id = params.get("product_id")

    existing_item = db.session.execute(
        sql.select(OrderItem)
        .where(OrderItem.order_id == id)
        .where(OrderItem.product_id == product_id)
    ).scalar()

    if existing_item:
        existing_item.quantity += 1
        db.session.commit()
    else:
        item = OrderItem(order_id=id, product_id=product_id, quantity=1)
        db.session.add(item)
        db.session.commit()
    order = db.first_or_404(sql.select(Order).where(Order.id == id))

    return jsonify(
        {
            "order": order.to_dict(
                show=[
                    "id",
                    "status",
                    "items",
                    "items.quantity",
                    "items.product",
                    "items.product.id",
                    "items.product.name",
                    "created_at",
                ]
            ),
            "total": order.total(),
        }
    )


@bp.route("/orders", methods=["POST"])
@login_required
def create_order():
    """Create a new order."""
    order = Order(user_id=current_user.id)
    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict(show=["id"]))


@bp.route("/current_order")
@login_required
def get_current_order():
    """Get current order"""
    order = current_user.current_order()

    return jsonify(
        {
            "order": order.to_dict(
                show=[
                    "id",
                    "items",
                    "items.quantity",
                    "items.product",
                    "items.product.id",
                    "items.product.name",
                    "items.product.price",
                ]
            ),
            "total": order.total(),
        }
    )


@bp.route("/order_items/<id>", methods=["DELETE"])
@login_required
def delete_order_item(id):
    """Delete an order item ."""
    item = db.first_or_404(sql.select(OrderItem).where(OrderItem.id == id))
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()

    return jsonify({"message": "Order Item deleted successfully"})


@bp.route("/checkout")
@login_required
def checkout():
    """Checkout current order"""
    form = CheckoutForm()
    return render_template("checkout.html", form=form)
