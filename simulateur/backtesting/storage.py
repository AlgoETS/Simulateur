from minio import Minio
import importlib.util
import os

# Configure MinIO client
minio_client = Minio(
    endpoint="play.min.io",  # Update to your MinIO endpoint
    access_key="your-access-key",
    secret_key="your-secret-key",
    secure=True  # Set to False if using HTTP
)


def download_strategy_from_minio(strategy_name, download_path="strategies/"):
    bucket_name = "strategy-files"
    object_name = f"{strategy_name}.py"

    # Ensure the download directory exists
    os.makedirs(download_path, exist_ok=True)

    # Download the strategy file
    minio_client.fget_object(bucket_name, object_name, f"{download_path}/{object_name}")

    return f"{download_path}/{object_name}"


def load_strategy(strategy_name):
    file_path = download_strategy_from_minio(strategy_name)

    spec = importlib.util.spec_from_file_location(strategy_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, strategy_name)
