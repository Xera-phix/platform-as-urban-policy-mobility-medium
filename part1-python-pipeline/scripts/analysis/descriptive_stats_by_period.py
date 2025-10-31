"""
Analyze Love Park review sentiment by construction period.

Classifies reviews into pre-construction, during construction, and post-construction
periods based on the park's 2016-2018 renovation timeline. Generates descriptive
statistics and saves segmented dataset for dashboard visualization.
"""

import pandas as pd

# Love Park construction timeline: February 2016 - May 2018
CONSTRUCTION_START = pd.Timestamp("2016-02-01")
CONSTRUCTION_END = pd.Timestamp("2018-05-31")


def classify_period(date):
    """
    Classify review date into construction period categories.

    Args:
        date: Pandas Timestamp of review date

    Returns:
        str: One of: pre_construction, during_construction, post_construction,
             border_feb2016, border_may2018, missing_date, or unclassified

    Note:
        Border months (Feb 2016, May 2018) are flagged separately for edge case
        analysis as exact construction start/end dates are uncertain.
    """
    if pd.isna(date):
        return "missing_date"

    # Flag border months for manual review
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


if __name__ == "__main__":
    df = pd.read_json("data/tripadvisor_jfkplaza.json")
    df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
    df["period"] = df["date_of_experience"].apply(classify_period)

    total_reviews = len(df)
    period_summary = (
        df["period"].value_counts().rename_axis("period").reset_index(name="count")
    )
    period_summary["percent"] = (period_summary["count"] / total_reviews * 100).round(1)

    print("\n=== REVIEW COUNTS BY PERIOD ===")
    print(period_summary)

    print("\n=== RATING STATS PER PERIOD ===")
    print(df.groupby("period")["rating"].describe())

    output_file = "tripadvisor_jfkplaza_with_periods.json"
    df.to_json(output_file, orient="records", indent=2)
    print(f"\n✅ Saved segmented dataset as {output_file}")
