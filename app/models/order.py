import sqlalchemy as sa
import sqlalchemy.orm as orm
from app.models.base_model import BaseModel
from typing import List


class Order(BaseModel):
    __table_name__ = "orders"

    TAX_RATE = 0.23

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("user.id"), index=True)
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
        return sum([(item.product.price * item.quantity) for item in self.items])

    def tax_total(self, tax_rate=TAX_RATE):
        return self.total() * tax_rate

    def net_total(self):
        return self.total() + self.tax_total()