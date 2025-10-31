"""
Generate user-level statistics for TripAdvisor reviewers.

Aggregates per-user metrics including review count, activity duration, and average
text length. Useful for identifying power users and analyzing reviewer behavior patterns.
"""

import pandas as pd
import numpy as np


def calculate_user_stats(
    input_file="data/tripadvisor_jfkplaza.json",
    output_file="tripadvisor_user_stats.xlsx",
):
    """
    Aggregate review data by user and calculate engagement metrics.

    Args:
        input_file: Path to reviews JSON file
        output_file: Path to save Excel output

    Returns:
        DataFrame with user-level statistics
    """
    reviews = pd.read_json(input_file)
    reviews["date_of_experience"] = pd.to_datetime(
        reviews["date_of_experience"], errors="coerce"
    )
    reviews = reviews.dropna(subset=["date_of_experience", "user_name"])

    if "text" in reviews.columns:
        reviews["text_length"] = reviews["text"].fillna("").apply(len)
    else:
        reviews["text_length"] = 0

    user_stats = reviews.groupby("user_name").agg(
        n_reviews=("rating", "count"),
        n_ratings=("rating", "count"),
        n_first_reviews=("date_of_experience", lambda x: (x == x.min()).sum()),
        n_checkins=(
            ("checkins", "sum")
            if "checkins" in reviews.columns
            else ("rating", lambda x: np.nan)
        ),
        n_photos=(
            ("photos", "sum")
            if "photos" in reviews.columns
            else ("rating", lambda x: np.nan)
        ),
        first_review_date=("date_of_experience", "min"),
        last_review_date=("date_of_experience", "max"),
        days_active=(
            "date_of_experience",
            lambda x: (x.max() - x.min()).days if len(x) > 1 else 0,
        ),
        avg_text_length=("text_length", "mean"),
    )

    user_stats["reviews_per_day_active"] = user_stats["n_reviews"] / user_stats[
        "days_active"
    ].replace(0, np.nan)

    user_stats.to_excel(output_file)
    print(f"✅ User stats table saved as {output_file}")

    return user_stats


if __name__ == "__main__":
    calculate_user_stats()
