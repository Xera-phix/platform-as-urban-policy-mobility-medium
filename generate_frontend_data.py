import json
import pandas as pd
from datetime import datetime

# Load TripAdvisor data with periods
with open("data/tripadvisor_jfkplaza_with_periods.json", "r") as f:
    tripadvisor_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(tripadvisor_data)

# Filter out missing dates
df = df[df["period"] != "missing_date"].copy()

# Convert date_written to datetime
df["date_written"] = pd.to_datetime(df["date_written"])

# Calculate statistics by period
period_stats = df.groupby("period").agg({"rating": ["mean", "count"]}).round(2)

print("=== RATINGS BY PERIOD ===")
print(period_stats)

# Calculate monthly rolling averages
df_sorted = df.sort_values("date_written")
df_sorted["year_month"] = df_sorted["date_written"].dt.to_period("M")

monthly_stats = df_sorted.groupby("year_month").agg({"rating": "mean"}).round(2)

print("\n=== MONTHLY AVERAGE RATINGS (sample) ===")
print(monthly_stats.head(20))

# Get review volume by period
volume_by_period = df.groupby("period").size()

print("\n=== REVIEW VOLUME BY PERIOD ===")
print(volume_by_period)

# Export to JSON for frontend
frontend_data = {
    "ratingsByPeriod": [
        {
            "period": "Pre-Construction",
            "avgRating": float(df[df["period"] == "pre_construction"]["rating"].mean()),
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

# Get monthly data for timeline (every 3 months for cleaner visualization)
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

# Export to JSON
with open("data/frontend_data.json", "w") as f:
    json.dump(frontend_data, f, indent=2)

print("\n=== EXPORTED TO data/frontend_data.json ===")
print(f"Periods: {len(frontend_data['ratingsByPeriod'])}")
print(f"Time points: {len(frontend_data['ratingOverTime'])}")
