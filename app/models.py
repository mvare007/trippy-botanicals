from app import db, login_manager
from typing import Optional
import sqlalchemy as sql
import sqlalchemy.orm as orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from hashlib import md5

class User(UserMixin, db.Model):
    __table_name__ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sql.String(255), index=True)
    last_name: orm.Mapped[str] = orm.mapped_column(sql.String(255), index=True)
    address: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))
    zip_code: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(8))
    location: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))
    vat_number: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(9))
    phone: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(16))
    last_login: orm.Mapped[Optional[sql.DateTime]] = orm.mapped_column(sql.DateTime)
    email: orm.Mapped[str] = orm.mapped_column(sql.String(120), index=True, unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))
    admin: orm.Mapped[bool] = orm.mapped_column(sql.Boolean, default=False)
    orders: orm.WriteOnlyMapped['Order'] = orm.relationship(back_populates='user', order_by='Order.created_at')
    created_at: orm.Mapped[sql.DateTime] = orm.mapped_column(sql.DateTime, default=sql.func.now())

    def __repr__(self):
        return '<User {}>'.format(self.full_name())

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_last_login(self):
        self.last_login = datetime.utcnow(timezone.utc)
        db.session.add(self)

    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

class ProductCategory(db.Model):
    __table_name__ = 'product_categories'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sql.String(255), index=True, unique=True)
    description: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))
    products: orm.WriteOnlyMapped['Product'] = orm.relationship(back_populates='product_category')

    def __repr__(self):
        return '<ProductCategory {}>'.format(self.name)

    def __str__(self):
        return self.name

class Product(db.Model):
    __table_name__ = 'products'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sql.String(255), index=True)
    description: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))
    price: orm.Mapped[float] = orm.mapped_column(sql.Float)
    category_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey(ProductCategory.id), index=True)
    category: orm.WriteOnlyMapped['ProductCategory'] = orm.relationship(back_populates='product_category')

    def __repr__(self):
        return '<Product {}>'.format(self.name)

    def __str__(self):
        return self.name

class OrderItem(db.Model):
    __table_name__ = 'order_items'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    product_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey(Product.id), index=True)
    product: orm.WriteOnlyMapped['Product'] = orm.relationship(back_populates='product')
    quantity: orm.Mapped[int] = orm.mapped_column(sql.Integer)
    order_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey(Order.id), index=True)
    order: orm.WriteOnlyMapped['Order'] = orm.relationship(back_populates='order')

    def __repr__(self):
        return '<OrderItem {}>'.format(self.product.name)

    def __str__(self):
        return self.product.name

class Order(db.Model):
    __table_name__ = 'orders'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey(User.id), index=True)
    user: orm.WriteOnlyMapped['User'] = orm.relationship(back_populates='user')
    items: orm.WriteOnlyMapped['OrderItem'] = orm.relationship(back_populates='order')
    created_at: orm.Mapped[sql.DateTime] = orm.mapped_column(sql.DateTime, default=sql.func.now())

    def __repr__(self):
        return '<Order {}>'.format(self.id)

    def __str__(self):
        return self.id

    def total(self):
        return sum([item.product.price * item.quantity for item in self.items])