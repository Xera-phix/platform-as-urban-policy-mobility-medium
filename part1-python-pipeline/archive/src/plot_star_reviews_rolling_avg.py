import pandas as pd
import matplotlib.pyplot as plt

# Load all reviews (including those without text)
df = pd.read_json("raw_reviews.json")

# Convert date column
if "datetime" in df.columns:
    df["date"] = pd.to_datetime(df["datetime"], unit="s", errors="coerce")
else:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")


# Use the correct star rating column
def get_star_col(df):
    for col in ["google_maps_star_rating", "rating", "stars"]:
        if col in df.columns:
            return col
    raise ValueError("No star rating column found.")


star_col = get_star_col(df)

# Sort by date and set as index for rolling
plot_df = df.sort_values("date").set_index("date")

# Calculate rolling average (30 days)
rolling_avg = plot_df[star_col].rolling("30D").mean()

plt.figure(figsize=(12, 6))
plt.scatter(
    plot_df.index, plot_df[star_col], alpha=0.4, label="Reviews", c="black", s=20
)
plt.plot(
    rolling_avg.index,
    rolling_avg,
    color="red",
    label="30-day Rolling Average",
    linewidth=2,
)

# Highlight periods
date_min = plot_df.index.min()
date_max = plot_df.index.max()
plt.axvspan(
    date_min,
    pd.Timestamp("2016-02-01"),
    color="blue",
    alpha=0.1,
    label="Pre-construction",
)
plt.axvspan(
    pd.Timestamp("2016-02-01"),
    pd.Timestamp("2018-05-31"),
    color="orange",
    alpha=0.1,
    label="During construction",
)
plt.axvspan(
    pd.Timestamp("2018-05-31"),
    date_max,
    color="green",
    alpha=0.1,
    label="Post-construction",
)

plt.xlabel("Date")
plt.ylabel("Star Rating")
plt.title("Google Maps Star Ratings Over Time (with 30-day Rolling Average)")
plt.legend()
plt.tight_layout()
plt.show()
