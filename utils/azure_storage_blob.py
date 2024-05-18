import logging
import sys
from os import environ

from azure.storage.blob import BlobServiceClient
from werkzeug.utils import secure_filename
from uuid import uuid4


class AzureStorageBlob:
    def __init__(self):
        self._init_logger()
        self.container_name = environ.get("AZURE_STORAGE_CONTAINER_NAME")
        self.blob_service_client = BlobServiceClient.from_connection_string(
            environ.get("AZURE_STORAGE_CONNECTION_STRING"), logging_enable=True
        )

        try:
            self.container_client = self.blob_service_client.get_container_client(
                container=self.container_name
            )
            self.container_client.get_container_properties()
        except Exception as e:
            self.container_client = self.blob_service_client.create_container(
                self.container_name
            )

    def upload_blob(self, file):
        _, file_extension = file.filename.rsplit(".", 1)
        filename = secure_filename(f"{uuid4()}.{file_extension}")
        self.container_client.upload_blob(filename, file)
        return self._build_url(filename)

    def download_blob(self, file_path, blob_name):
        blob_client = self.container_client.get_blob_client(blob=blob_name)
        with open(file_path, "wb") as data:
            data.write(blob_client.download_blob().readall())

    def delete_blob(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob=blob_name)
        blob_client.delete_blob()

    def list_blobs(self):
        return self.container_client.list_blobs()

    def _init_logger(_self):
        logger = logging.getLogger("azure.storage.blob")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(stream=sys.stdout)
        logger.addHandler(handler)

    def _build_url(self, blob_name):
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}"
