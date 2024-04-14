from app import db
from flask import render_template
from flask_login import current_user, login_required
from app.models import User, Product, ProductCategory
import sqlalchemy as sql
from app.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    product_categories = ProductCategory.query.all()

    return render_template("index.html", title="Home", product_categories=product_categories)


@bp.route("/user/<id>")
@login_required
def user(id):
    user = db.first_or_404(sql.select(User).where(User.id == id))

    return render_template("user.html", user=user)


@bp.route("/products<category_id>")
def products(category_id):
    if category_id:
        products = db.all(sql.select(Product).where(Product.category_id.in_(category_id)))
    else:
        products = Product.query.all()

    return render_template("products.html", products=products)
