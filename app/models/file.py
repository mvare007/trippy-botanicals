import sqlalchemy as sa
import sqlalchemy.orm as orm
from app.models.base_model import BaseModel

from datetime import datetime, timezone


class File(BaseModel):
    __table_name__ = "files"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    url: orm.Mapped[str] = orm.mapped_column(sa.String)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("user.id"), index=True)
    user: orm.Mapped["User"] = orm.relationship(back_populates="files")
    created_at: orm.Mapped[sa.DateTime] = orm.mapped_column(
        sa.DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return "<File {}>".format(self.url)

    def __str__(self):
        return self.url
