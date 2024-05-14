import sqlalchemy as sa
import sqlalchemy.orm as orm
from app.models.base_model import BaseModel

from datetime import datetime, timezone


class Document(BaseModel):
    __table_name__ = "documents"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    url: orm.Mapped[str] = orm.mapped_column(sa.String)
    owner_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, index=True)
    owner_type: orm.Mapped[str] = orm.mapped_column(sa.String(255), index=True)
    created_at: orm.Mapped[sa.DateTime] = orm.mapped_column(
        sa.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return "<Document {}>".format(self.url)

    def __str__(self):
        return self.url

    # Fields that should be read-only after creation
    _readonly_fields = (
        "url",
        "owner_id",
        "owner_type",
    )

    def __setattr__(self, key, value):
        if key in self._readonly_fields and self.id is not None:
            raise AttributeError(f"{key} is read-only after creation.")
        super().__setattr__(key, value)
