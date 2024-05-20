import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel
from utils.azure_storage_blob import AzureStorageBlob
from utils.local_storage import LocalStorage
from flask import url_for
from datetime import datetime, timezone
from config import environment
from pathlib import PureWindowsPath


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

    def display(self):
        if environment == "test" or environment == "development":
            filename = self.url.split("static\\")[-1]
            filename = PureWindowsPath(filename).as_posix()
            return url_for("static", filename=filename)
        else:
            return self.url

    @validates("url")
    def validate_url(self, key, url):
        if not url:
            raise AssertionError("URL is required.")
        return url

    @classmethod
    def delete(self):
        if environment == "test" or environment == "development":
            LocalStorage().delete(self.url)
        else:
            storage_blob = AzureStorageBlob()
            storage_blob.delete_blob(self.url)

    @classmethod
    def upload(self, file):
        if environment == "test" or environment == "development":
            return LocalStorage().upload(file)
        else:
            storage_blob = AzureStorageBlob()
            return storage_blob.upload_blob(file)
