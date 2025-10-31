"""
Export dashboard-ready data from segmented TripAdvisor reviews.

Generates JSON file with aggregated statistics by period and quarterly time series data
optimized for React dashboard consumption. Filters out missing dates and calculates
quarterly rolling averages for cleaner visualization.
"""

import json
import pandas as pd


def export_dashboard_data(
    input_file="data/tripadvisor_jfkplaza_with_periods.json",
    output_file="data/frontend_data.json",
):
    """
    Aggregate review data and export for frontend dashboard.

    Args:
        input_file: Path to reviews JSON with period classifications
        output_file: Path to save frontend-ready JSON
    """
    with open(input_file, "r") as f:
        tripadvisor_data = json.load(f)

    df = pd.DataFrame(tripadvisor_data)
    df = df[df["period"] != "missing_date"].copy()
    df["date_written"] = pd.to_datetime(df["date_written"])

    period_stats = df.groupby("period").agg({"rating": ["mean", "count"]}).round(2)
    print("=== RATINGS BY PERIOD ===")
    print(period_stats)

    df_sorted = df.sort_values("date_written")
    df_sorted["year_month"] = df_sorted["date_written"].dt.to_period("M")
    monthly_stats = df_sorted.groupby("year_month").agg({"rating": "mean"}).round(2)

    print("\n=== MONTHLY AVERAGE RATINGS (sample) ===")
    print(monthly_stats.head(20))

    volume_by_period = df.groupby("period").size()
    print("\n=== REVIEW VOLUME BY PERIOD ===")
    print(volume_by_period)

    frontend_data = {
        "ratingsByPeriod": [
            {
                "period": "Pre-Construction",
                "avgRating": float(
                    df[df["period"] == "pre_construction"]["rating"].mean()
                ),
                "reviews": int(df[df["period"] == "pre_construction"].shape[0]),
            },
            {
                "period": "During Construction",
                "avgRating": float(
                    df[df["period"] == "during_construction"]["rating"].mean()
                ),
                "reviews": int(df[df["period"] == "during_construction"].shape[0]),
            },
            {
                "period": "Post-Construction",
                "avgRating": float(
                    df[df["period"] == "post_construction"]["rating"].mean()
                ),
                "reviews": int(df[df["period"] == "post_construction"].shape[0]),
            },
        ]
    }

    # Quarterly aggregation for cleaner timeline visualization
    monthly_data = []
    for period, group in df_sorted.groupby(df_sorted["date_written"].dt.to_period("Q")):
        if len(group) > 0:
            monthly_data.append(
                {
                    "month": str(period),
                    "rating": float(group["rating"].mean()),
                    "reviews": int(len(group)),
                }
            )

    frontend_data["ratingOverTime"] = monthly_data

    with open(output_file, "w") as f:
        json.dump(frontend_data, f, indent=2)

    print("\n=== EXPORTED TO data/frontend_data.json ===")
    print(f"Periods: {len(frontend_data['ratingsByPeriod'])}")
    print(f"Time points: {len(frontend_data['ratingOverTime'])}")


if __name__ == "__main__":
    export_dashboard_data()
