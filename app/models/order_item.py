import sqlalchemy as sa
import sqlalchemy.orm as orm
from app.models.base_model import BaseModel
from app.models.order import Order
from datetime import datetime, timezone


class OrderItem(BaseModel):
    __table_name__ = "order_items"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    quantity: orm.Mapped[int] = orm.mapped_column(sa.Integer)
    product_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("product.id"), index=True
    )
    order_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('order.id'), index=True)
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
