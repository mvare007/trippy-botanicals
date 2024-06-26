import sqlalchemy as sql
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.main import bp
from app.main.forms import ChallengeForm, CheckoutForm
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.document import Document
from utils.file_validations import allowed_file
from app.services.checkout_service import CheckoutService


@bp.route("/")
@bp.route("/index")
def index():
    product_categories = ProductCategory.query.all()
    featured_products = Product.featured()

    return render_template(
        "index.html",
        title="Home",
        product_categories=product_categories,
        featured_products=featured_products,
    )


@bp.route("/profile")
@login_required
def profile():
    photos = current_user.documents()
    return render_template("profile.html", photos=photos)


@bp.route("/products?category_id=<category_id>")
@bp.route("/products", defaults={"category_id": None})
def products(category_id):
    """List products by category. If no category is provided, list all products."""
    if category_id:
        products = Product.query.filter(Product.category_id == category_id).all()
    else:
        products = Product.query.all()

    return render_template("products.html", title="Products", products=products)


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


@bp.route("/current_order/items_count")
@login_required
def current_order_items_count():
    """Get number of items in the current order"""
    current_order = current_user.current_order()
    if not current_order:
        return jsonify({"items_count": 0})

    items_count = 0
    for item in current_order.items:
        items_count += item.quantity
    return jsonify({"items_count": items_count})


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


@bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """Checkout current order"""
    form = CheckoutForm()
    order = current_user.current_order()
    if form.validate_on_submit() and order.status == "Pending":
        try:
            CheckoutService(order).process()
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("checkout.html", title="Checkout", form=form)
        flash("Order processed successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("checkout.html", title="Checkout", form=form)


@bp.route("/challenges", methods=["GET", "POST"])
@login_required
def challenges():
    form = ChallengeForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.photo.data
        if not allowed_file(file):
            flash("Invalid file type or file too large", "danger")
            return redirect(request.url)
        else:
            url = Document.upload(file)

            try:
                photo = Document(url=url, owner_id=current_user.id, owner_type="User")
                db.session.add(photo)
                db.session.commit()
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "danger")
                Document.delete(url)
                return render_template("challenges.html", form=form)

            flash("Photo uploaded successfully!", "success")
        return redirect(url_for("main.challenges"))
    return render_template("challenges.html", form=form)
