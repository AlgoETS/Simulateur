from minio import Minio
from django.conf import settings
from threading import Lock

class MinioClient:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MinioClient, cls).__new__(cls)
                    cls._instance.client = Minio(
                        settings.AWS_S3_ENDPOINT_URL,
                        access_key=settings.AWS_ACCESS_KEY_ID,
                        secret_key=settings.AWS_SECRET_ACCESS_KEY,
                        secure=settings.AWS_S3_VERIFY,
                    )
        return cls._instance

    def __getattr__(self, name):
        return getattr(self.client, name)

minio_client = MinioClient()


def upload_file(file):
    minio_client.put_object(
        'mybucket',
        file.name,
        file,
        length=file.size,
        content_type=file.content_type
    )