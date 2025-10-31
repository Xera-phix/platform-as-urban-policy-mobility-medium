"""
Generate bar chart showing review distribution by construction period.

Visualizes the count of reviews in each period: pre-construction, during construction,
and post-construction. Includes border months for completeness.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Love Park construction timeline (duplicated to avoid complex imports)
CONSTRUCTION_START = pd.Timestamp("2016-02-01")
CONSTRUCTION_END = pd.Timestamp("2018-05-31")


def classify_period(date):
    """
    Classify review date into construction period categories.

    Border months (Feb 2016, May 2018) are flagged separately for edge case
    analysis as exact construction start/end dates are uncertain.
    """
    if pd.isna(date):
        return "missing_date"
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
        return "unclassified"


def generate_period_bar_chart(input_file="tripadvisor_jfkplaza.json"):
    """
    Create bar chart of review counts by construction period.

    Args:
        input_file: Path to reviews JSON file
    """
    df = pd.read_json(input_file)
    df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
    df["period"] = df["date_of_experience"].apply(classify_period)

    period_counts = (
        df["period"]
        .value_counts()
        .reindex(
            [
                "pre_construction",
                "border_feb2016",
                "during_construction",
                "border_may2018",
                "post_construction",
                "missing_date",
            ]
        )
        .dropna()
    )

    plt.figure(figsize=(8, 6))
    period_counts.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.title("Total Reviews by Period — JFK Plaza (TripAdvisor)", fontsize=14)
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    generate_period_bar_chart()
