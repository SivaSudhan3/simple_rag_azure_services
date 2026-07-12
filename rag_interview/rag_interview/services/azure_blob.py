from io import BytesIO
from typing import BinaryIO

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, ContentSettings

from rag_interview.core.config.config import blobsettings

class BlobStorageService:

    def __init__(
        self
     
    ):

        self.client = BlobServiceClient.from_connection_string(
            blobsettings.STORAGE_CONNECTION_STRING
        )

        self.container = self.client.get_container_client(
            blobsettings.STORAGE_CONTAINER
        )
    def create_container(self) -> None:
        """
        Creates the container if it does not already exist.
        """

        try:
             self.container.create_container()

        except Exception:
            # Container already exists
            pass

    def upload(
        self,
        blob_name: str,
        data: bytes,
        content_type: str,
    ) -> str:
        """
        Upload bytes to Azure Blob Storage.

        Returns
        -------
        str
            Blob name
        """

        blob = self.container.get_blob_client(blob_name)

        blob.upload_blob(
            data=data,
            overwrite=True,
            content_settings=ContentSettings(
            content_type=content_type
            ),
        )

        return blob_name

    def upload_stream(
        self,
        blob_name: str,
        stream: BinaryIO,
        content_type: str,
    ) -> str:
        """
        Upload a file-like object.
        """

        blob = self.container.get_blob_client(blob_name)

        blob.upload_blob(
            data=stream,
            overwrite=True,
            content_settings=ContentSettings(
            content_type=content_type
            ),
        )

        return blob_name

    def download(
        self,
        blob_name: str,
    ) -> bytes:
        """
        Download blob as bytes.
        """

        blob = self.container.get_blob_client(blob_name)

        downloader =  blob.download_blob()

        return downloader.readall()

    def download_stream(
        self,
        blob_name: str,
    ) -> BytesIO:
        """
        Download blob as stream.
        """

        data =  self.download(blob_name)

        return BytesIO(data)

    def exists(
        self,
        blob_name: str,
    ) -> bool:
        """
        Returns True if blob exists.
        """

        blob = self.container.get_blob_client(blob_name)

        return  blob.exists()

    def delete(
        self,
        blob_name: str,
    ) -> None:
        """
        Delete blob.
        """

        blob = self.container.get_blob_client(blob_name)

        try:

             blob.delete_blob()

        except ResourceNotFoundError:

            pass

    def get_url(
        self,
        blob_name: str,
    ) -> str:
        """
        Returns blob URL.

        This is NOT a SAS URL.
        """

        blob = self.container.get_blob_client(blob_name)

        return blob.url

    def list_blobs(self):
        """
        List all blobs.
        """

        blobs = []

        for blob in self.container.list_blobs():

            blobs.append(blob.name)

        return blobs

    def close(self):
        """
        Close underlying Azure clients.
        """

        self.client.close()