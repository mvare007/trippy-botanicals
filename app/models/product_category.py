from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as orm
from app.models.base_model import BaseModel


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