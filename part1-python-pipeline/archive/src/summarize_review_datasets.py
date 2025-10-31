import pandas as pd
from datetime import datetime

# Load datasets
google = pd.read_json("raw_reviews.json")
yelp = pd.read_json("yelp_jfk_plaza_reviews.json")

# Harmonize date and star columns
google["date"] = (
    pd.to_datetime(google["datetime"], unit="s", errors="coerce")
    if "datetime" in google.columns
    else pd.to_datetime(google["date"], errors="coerce")
)
google["star_rating"] = google[
    [c for c in ["google_maps_star_rating", "rating", "stars"] if c in google.columns][
        0
    ]
]
yelp["date"] = pd.to_datetime(yelp["date"], errors="coerce")
yelp["star_rating"] = yelp[[c for c in ["rating", "stars"] if c in yelp.columns][0]]


# Summary function
def dataset_summary(df, name):
    n_reviews = len(df)
    date_min = df["date"].min()
    date_max = df["date"].max()
    avg_rating = df["star_rating"].mean()
    median_rating = df["star_rating"].median()
    n_missing_text = df["text"].isna().sum() if "text" in df.columns else "N/A"
    n_missing_rating = df["star_rating"].isna().sum()
    return {
        "dataset": name,
        "n_reviews": n_reviews,
        "date_range": f"{date_min.date()} to {date_max.date()}",
        "avg_rating": round(avg_rating, 2),
        "median_rating": median_rating,
        "missing_text": n_missing_text,
        "missing_rating": n_missing_rating,
    }


# Get summaries
google_summary = dataset_summary(google, "Google")
yelp_summary = dataset_summary(yelp, "Yelp")


# Print concise insights
def print_insights(g, y):
    print("--- Google Reviews ---")
    for k, v in g.items():
        print(f"{k}: {v}")
    print("\n--- Yelp Reviews ---")
    for k, v in y.items():
        print(f"{k}: {v}")
    print("\n--- Key Insights ---")
    print(f"Google reviews: {g['n_reviews']} | Yelp reviews: {y['n_reviews']}")
    print(f"Google date range: {g['date_range']} | Yelp date range: {y['date_range']}")
    print(f"Google avg rating: {g['avg_rating']} | Yelp avg rating: {y['avg_rating']}")
    print(
        f"Google median rating: {g['median_rating']} | Yelp median rating: {y['median_rating']}"
    )
    print(
        f"Google missing text: {g['missing_text']} | Yelp missing text: {y['missing_text']}"
    )
    print(
        f"Google missing ratings: {g['missing_rating']} | Yelp missing ratings: {y['missing_rating']}"
    )
    if g["avg_rating"] > y["avg_rating"]:
        print("Google reviews are on average more positive.")
    elif g["avg_rating"] < y["avg_rating"]:
        print("Yelp reviews are on average more positive.")
    else:
        print("Average ratings are similar.")
    if g["date_range"] != y["date_range"]:
        print("Date ranges differ: consider this when comparing trends.")


if __name__ == "__main__":
    print_insights(google_summary, yelp_summary)
