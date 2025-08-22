import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Load and harmonize Google reviews ---
google = pd.read_json("raw_reviews.json")
if "datetime" in google.columns:
    google["date"] = pd.to_datetime(google["datetime"], unit="s", errors="coerce")
else:
    google["date"] = pd.to_datetime(google["date"], errors="coerce")
google["star_rating"] = google[
    [c for c in ["google_maps_star_rating", "rating", "stars"] if c in google.columns][
        0
    ]
]
google["source"] = "Google"

# --- Load and harmonize Yelp reviews ---
yelp = pd.read_json("yelp_jfk_plaza_reviews.json")
# Yelp date is usually a string like 'YYYY-MM-DD'
yelp["date"] = pd.to_datetime(yelp["date"], errors="coerce")
yelp["star_rating"] = yelp[[c for c in ["rating", "stars"] if c in yelp.columns][0]]
yelp["source"] = "Yelp"

# --- Combine ---
df = pd.concat([google, yelp], ignore_index=True)


# --- Rolling Average Plot with Dots in Background ---
plt.figure(figsize=(14, 7))

# Plot all individual reviews as dim dots in the background
for source, color, marker in [("Google", "#1a73e8", "o"), ("Yelp", "#d93025", "s")]:
    mask = df["source"] == source
    plt.scatter(
        df.loc[mask, "date"],
        df.loc[mask, "star_rating"],
        color=color,
        alpha=0.15,
        s=18,
        marker=marker,
        label=(
            f"{source} Review" if source == "Google" else None
        ),  # Only label one set for legend clarity
    )

# Calculate rolling average (30 days) for each source
window = 30
for source, color, marker in [("Google", "#1a73e8", "o"), ("Yelp", "#d93025", "s")]:
    mask = df["source"] == source
    temp = df.loc[mask, ["date", "star_rating"]].sort_values("date")
    temp = temp.set_index("date").resample("D").mean().interpolate()
    temp["rolling_avg"] = (
        temp["star_rating"].rolling(window, min_periods=1, center=True).mean()
    )
    plt.plot(
        temp.index,
        temp["rolling_avg"],
        label=f"{source} 30-day Rolling Avg",
        color=color,
        linewidth=2.5,
        alpha=0.95,
    )

# Highlight periods with more visible bands and annotation
date_min = df["date"].min()
date_max = df["date"].max()
plt.axvspan(
    date_min,
    pd.Timestamp("2016-02-01"),
    color="#b3c6f7",
    alpha=0.25,
    label="Pre-construction",
)
plt.axvspan(
    pd.Timestamp("2016-02-01"),
    pd.Timestamp("2018-05-31"),
    color="#ffe0b2",
    alpha=0.25,
    label="During construction",
)
plt.axvspan(
    pd.Timestamp("2018-05-31"),
    date_max,
    color="#c8e6c9",
    alpha=0.25,
    label="Post-construction",
)

# Add grid, set y-limits, and improve ticks
plt.ylim(0, 5)
plt.yticks(range(0, 6))
plt.grid(axis="y", linestyle="--", alpha=0.5)

# Improve legend (avoid duplicate period labels)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(
    by_label.values(), by_label.keys(), loc="upper right", fontsize=12, frameon=True
)

plt.xlabel("Date", fontsize=13)
plt.ylabel("Average Star Rating", fontsize=13)
plt.title(
    "Average Star Ratings Over Time (30-day Rolling Avg): Google vs. Yelp",
    fontsize=16,
    fontweight="bold",
)
plt.tight_layout()
plt.show()
