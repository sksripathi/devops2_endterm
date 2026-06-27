import logging
import os
from pathlib import Path

import boto3
import pandas as pd
from botocore.exceptions import ClientError, ParamValidationError

from config import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, DATASET_FILE, S3_BUCKET_NAME

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).resolve().parent / "data" / DATASET_FILE


def download_dataset() -> None:
    """Download the dataset from S3 if it is not already present locally."""
    logger.info("Checking local dataset")
    logger.info("Dataset path: %s", DATA_PATH)

    if DATA_PATH.exists():
        logger.info("Using local dataset")
        return

    logger.info("Connecting to AWS S3")
    logger.info("Bucket: %s", S3_BUCKET_NAME)
    logger.info("Object: %s", DATASET_FILE)

    if not S3_BUCKET_NAME or not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.warning(
            "AWS S3 settings are missing. Please set the environment variables or place the dataset file in the data folder."
        )
        return

    data_dir = DATA_PATH.parent
    data_dir.mkdir(parents=True, exist_ok=True)

    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY),
            region_name=os.getenv("AWS_REGION", AWS_REGION),
        )
        s3_client.download_file(S3_BUCKET_NAME, DATASET_FILE, str(DATA_PATH))
        logger.info("Download complete")
        logger.info("Dataset file exists: %s", DATA_PATH.exists())
    except (ClientError, ParamValidationError) as e:
        logger.error("S3 download failed: %s", e)
        raise


def load_user_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the user dataset from the local CSV-like text file."""
    logger.info("Loading dataset")
    download_dataset()
    if not path.exists():
        raise FileNotFoundError(f"Dataset file was not found at {path}")
    logger.info("Reading dataset from %s", path)
    return pd.read_csv(
        path,
        sep="|",
        header=None,
        names=["user_id", "age", "gender", "occupation", "zip_code"],
    )


def build_dashboard_data() -> dict:
    """Create the metrics and chart values used by the dashboard."""
    logger.info("Loading dashboard data")
    df = load_user_data()
    df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")

    total_users = int(len(df))
    average_age = round(float(df["age"].mean()), 1)
    youngest_user = int(df["age"].min())
    oldest_user = int(df["age"].max())
    male_users = int((df["gender"] == "M").sum())
    female_users = int((df["gender"] == "F").sum())

    occupation_distribution = (
        df["occupation"].value_counts().sort_values(ascending=False).head(8)
    )
    occupation_labels = [str(label) for label in occupation_distribution.index.tolist()]
    occupation_counts = [int(value) for value in occupation_distribution.tolist()]

    age_groups = pd.cut(
        df["age"],
        bins=[0, 18, 24, 34, 44, 54, 100],
        labels=["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"],
        include_lowest=True,
    )
    age_distribution = age_groups.value_counts().reindex(
        ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"], fill_value=0
    )

    return {
        "total_users": total_users,
        "average_age": average_age,
        "youngest_user": youngest_user,
        "oldest_user": oldest_user,
        "male_users": male_users,
        "female_users": female_users,
        "occupation_labels": occupation_labels,
        "occupation_counts": occupation_counts,
        "age_labels": [str(label) for label in age_distribution.index.tolist()],
        "age_counts": [int(value) for value in age_distribution.tolist()],
        "gender_labels": ["Male", "Female"],
        "gender_counts": [male_users, female_users],
    }
