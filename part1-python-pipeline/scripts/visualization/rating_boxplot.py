"""
Generate box-and-whisker plot of ratings by construction period.

Shows median, quartiles, and outliers for ratings in pre-construction, during construction,
and post-construction periods. Excludes border months to avoid timeline ambiguity.
"""

import pandas as pd
import matplotlib.pyplot as plt

CONSTRUCTION_START = pd.Timestamp("2016-02-01")
CONSTRUCTION_END = pd.Timestamp("2018-05-31")


def classify_period(date):
    """Classify review date into construction period categories"""
    if pd.isna(date):
        return None
    if date.month == 2 and date.year == 2016:
        return "border_feb2016"
    if date.month == 5 and date.year == 2018:
        return "border_may2018"
    if date < CONSTRUCTION_START:
        return "pre_construction"
    elif CONSTRUCTION_START < date < CONSTRUCTION_END:
        return "during_construction"
    elif date > CONSTRUCTION_END:
        return "post_construction"
    else:
        return None


def generate_rating_boxplot(input_file="tripadvisor_jfkplaza.xlsx"):
    """
    Create box-and-whisker plot of ratings by period.

    Args:
        input_file: Path to Excel file with review data
    """
    df = pd.read_excel(input_file)
    df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
    df["period"] = df["date_of_experience"].apply(classify_period)

    df_filtered = df[
        df["period"].isin(
            ["pre_construction", "during_construction", "post_construction"]
        )
    ]

    plt.figure(figsize=(8, 6))
    df_filtered.boxplot(column="rating", by="period", grid=False)

    plt.title("Ratings by Construction Period — JFK Plaza (TripAdvisor)")
    plt.suptitle("")
    plt.xlabel("Construction Period")
    plt.ylabel("Rating")
    plt.ylim(0.5, 5.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    generate_rating_boxplot()
