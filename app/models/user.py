from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime, timezone
from typing import List, Optional
from app.models.base_model import BaseModel
from app.models.order import Order
from app.models.document import Document


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
    admin: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.text("0"))
    created_at: orm.Mapped[sa.DateTime] = orm.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    orders: orm.Mapped[List["Order"]] = orm.relationship(
        back_populates="user", lazy="dynamic"
    )

    documents: orm.Mapped[List["Document"]] = orm.relationship(
        back_populates="owner", lazy="dynamic"
    )

    def __repr__(self):
        return "<User {}>".format(self.full_name())

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def current_order(self):
        """Return the current order for the user."""
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
        db.session.commit()

    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def documents(self):
        return Document.query.filter_by(owner_id=self.id, owner_type="User").all()
