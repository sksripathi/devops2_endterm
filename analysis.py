from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "u.user"


def load_user_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the user dataset from the local CSV-like text file."""
    return pd.read_csv(
        path,
        sep="|",
        header=None,
        names=["user_id", "age", "gender", "occupation", "zip_code"],
    )


def build_dashboard_data() -> dict:
    """Create the metrics and chart values used by the dashboard."""
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
