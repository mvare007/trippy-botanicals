from sqlalchemy import ForeignKey, String, Float, Integer, desc
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional
from app.models.base_model import BaseModel

class Product(BaseModel):
    __table_name__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=10)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_category.id"), index=True
    )
    category: Mapped["ProductCategory"] = relationship(
        back_populates="products"
    )
    order_items: Mapped["OrderItem"] = relationship(back_populates="product")

    def __repr__(self):
        return "<Product {}>".format(self.name)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.stock > 0

    @staticmethod
    def featured(count=9):
        return Product.query.order_by(desc(Product.stock)).limit(count).all()