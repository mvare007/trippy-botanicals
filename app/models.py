from datetime import datetime, timezone
from typing import List, Optional
from app.extensions import db, login_manager

import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask import json
from flask_login import UserMixin
from sqlalchemy.orm.attributes import QueryableAttribute
from werkzeug.security import check_password_hash, generate_password_hash



class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=None, _path=None):
        """Return a dictionary representation of this model."""

        show = show or []
        _hide = _hide or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(["id", "modified_at", "created_at"])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        _path=("%s.%s" % (_path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data


class User(UserMixin, BaseModel):
    __table_name__ = "users"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sa.String(255), index=True)
    last_name: orm.Mapped[str] = orm.mapped_column(sa.String(255), index=True)
    address: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(255))
    zip_code: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(8))
    location: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(255))
    vat_number: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(9))
    phone: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(16))
    last_login: orm.Mapped[Optional[sa.DateTime]] = orm.mapped_column(sa.DateTime)
    date_joined: orm.Mapped[sa.DateTime] = orm.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    email: orm.Mapped[str] = orm.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: orm.WriteOnlyMapped[Optional[str]] = orm.mapped_column(
        sa.String(255)
    )
    admin: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.text('0'))
    created_at: orm.Mapped[sa.DateTime] = orm.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    orders: orm.Mapped[List["Order"]] = orm.relationship(
        back_populates="user", lazy="dynamic"
    )

    def __repr__(self):
        return "<User {}>".format(self.full_name())

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def current_order(self):
        return self.orders.filter(Order.status == "Pending").first()

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_last_login(self):
        self.last_login = datetime.now(timezone.utc)
        db.session.add(self)

    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))


class ProductCategory(BaseModel):
    __table_name__ = "product_categories"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), index=True, unique=True)
    description: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(255))
    products: orm.Mapped["Product"] = orm.relationship(back_populates="category")

    def __repr__(self):
        return "<ProductCategory {}>".format(self.name)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __table_name__ = "products"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), index=True)
    description: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(255))
    price: orm.Mapped[float] = orm.mapped_column(sa.Float)
    stock: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=10)
    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey(ProductCategory.id), index=True
    )
    category: orm.Mapped["ProductCategory"] = orm.relationship(
        back_populates="products"
    )
    order_items: orm.Mapped["OrderItem"] = orm.relationship(back_populates="product")

    def __repr__(self):
        return "<Product {}>".format(self.name)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.stock > 0

    @staticmethod
    def featured(count=9):
        return Product.query.order_by(Product.stock).limit(count).all()


class Order(BaseModel):
    __table_name__ = "orders"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(User.id), index=True)
    status: orm.Mapped[str] = orm.mapped_column(sa.String(20), default="Pending")
    created_at: orm.Mapped[sa.DateTime] = orm.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    user: orm.Mapped["User"] = orm.relationship(back_populates="orders")
    items: orm.Mapped[List["OrderItem"]] = orm.relationship(
        back_populates="order", lazy="dynamic"
    )

    def __repr__(self):
        return "<Order {}>".format(self.id)

    def __str__(self):
        return self.id

    def total(self):
        if not self.items:
            return 0
        return sum([item.product.price * item.quantity for item in self.items])


class OrderItem(BaseModel):
    __table_name__ = "order_items"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    quantity: orm.Mapped[int] = orm.mapped_column(sa.Integer)
    product_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey(Product.id), index=True
    )
    order_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Order.id), index=True)
    product: orm.Mapped["Product"] = orm.relationship(back_populates="order_items")
    order: orm.Mapped["Order"] = orm.relationship(back_populates="items")
    created_at: orm.Mapped[sa.DateTime] = orm.mapped_column(
        sa.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return "<OrderItem {}>".format(self.product.name)

    def __str__(self):
        return self.product.name
