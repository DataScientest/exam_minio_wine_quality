import os
import pytest
from minio import Minio
import mlflow
from mlflow.tracking import MlflowClient


MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_DATA_BUCKET = os.getenv("MINIO_DATA_BUCKET")
MINIO_MLFLOW_BUCKET = os.getenv("MINIO_MLFLOW_BUCKET")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")


# Test 1: Buckets created in MinIO?
def test_minio_buckets_exist():
    """Test that the required MinIO buckets were created."""
    print(f"\nChecking for MinIO buckets: {MINIO_DATA_BUCKET}, {MINIO_MLFLOW_BUCKET}")
    try:
        print(f"Trying to connect to {MINIO_ENDPOINT} with {MINIO_ACCESS_KEY} and {MINIO_SECRET_KEY}")
        minio_client = Minio(
            endpoint=MINIO_ENDPOINT,
            secure=False,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
        )
        print(f"Connected to {MINIO_ENDPOINT}.")
        assert minio_client.bucket_exists(MINIO_DATA_BUCKET), f"Bucket '{MINIO_DATA_BUCKET}' does not exist."
        assert minio_client.bucket_exists(MINIO_MLFLOW_BUCKET), f"Bucket '{MINIO_MLFLOW_BUCKET}' does not exist."
        print("MinIO buckets exist.")
    except Exception as e:
        pytest.fail(f"Error checking MinIO buckets: {e}")

# Test 2: Experiments tracked by MLflow?
def test_mlflow_experiment_tracked():
    """Test that MLflow has tracked at least one experiment run."""
    print(f"\nChecking for MLflow experiments and runs...")
    try:
        print(f"Trying to connect to {MLFLOW_TRACKING_URI}")
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow_client = MlflowClient()
        print(f"Connected to {MLFLOW_TRACKING_URI}.")
        experiments = mlflow_client.search_experiments()
        assert len(experiments) > 0, "No MLflow experiments found."

        # print(experiments)
    except Exception as e:
        pytest.fail(f"Error checking MLflow experiments/runs: {e}")

# Test 3: Artefacts from DVC stored in the MinIO DVC bucket (dvc-storage)?
def test_dvc_artifacts_in_minio():
    """Test that DVC has pushed artifacts to the MinIO DVC bucket."""
    print(f"\nChecking for objects in DVC bucket: {MINIO_DATA_BUCKET}")
    try:
        minio_client = Minio(
            endpoint=MINIO_ENDPOINT,
            secure=False,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
        )
        objects = minio_client.list_objects(MINIO_DATA_BUCKET, prefix='files/md5/')
        assert len(list(objects)) > 0, "No DVC artifacts found in the bucket."

        # print(f"\n'{MINIO_DATA_BUCKET}' content:")
        # for obj in objects:
        #     print(f"- Name: {obj.object_name}, Last update: {obj.last_modified}")
    except Exception as e:
        pytest.fail(f"Error listing objects in DVC bucket '{MINIO_DATA_BUCKET}': {e}")

# Test 4: MLflow artifacts stored in the MinIO MLflow bucket (mlflow-artifacts)?
def test_mlflow_artifacts_in_minio():
    """Test that MLflow artifacts are stored in the MinIO MLflow bucket."""
    print(f"\nChecking for MLflow artifacts in MinIO bucket: {MINIO_MLFLOW_BUCKET}")
    try:
        minio_client = Minio(
            endpoint=MINIO_ENDPOINT,
            secure=False,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
        )
        objects = minio_client.list_objects(MINIO_MLFLOW_BUCKET, prefix='0/')
        assert len(list(objects)) > 0, "No MLflow artifacts found in the bucket."

        # print(f"\n'{MINIO_MLFLOW_BUCKET}' content:")
        # for obj in objects:
        #     print(f"- Name: {obj.object_name}, Last update: {obj.last_modified}")
    except Exception as e:
        pytest.fail(f"Error listing objects in MLflow artifacts bucket '{MINIO_MLFLOW_BUCKET}': {e}")