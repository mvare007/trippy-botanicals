from app import db, login_manager
from typing import Optional
import sqlalchemy as sql
import sqlalchemy.orm as orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sql.String(255), index=True)
    last_name: orm.Mapped[str] = orm.mapped_column(sql.String(255), index=True)
    address: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))
    zip_code: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(8))
    location: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))
    vat_number: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(9))
    phone: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(16))
    date_joined: orm.Mapped[sql.DateTime] = orm.mapped_column(sql.DateTime, default=sql.func.now())
    last_login: orm.Mapped[Optional[sql.DateTime]] = orm.mapped_column(sql.DateTime)
    email: orm.Mapped[str] = orm.mapped_column(sql.String(120), index=True, unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.full_name())

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))