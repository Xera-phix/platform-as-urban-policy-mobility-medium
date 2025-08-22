import pandas as pd
from datetime import datetime

# --- Load Google reviews ---
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

# --- Load Yelp reviews ---
yelp = pd.read_json("yelp_jfk_plaza_reviews.json")
yelp["date"] = pd.to_datetime(yelp["date"], errors="coerce")
yelp["star_rating"] = yelp[[c for c in ["rating", "stars"] if c in yelp.columns][0]]
yelp["source"] = "Yelp"


# --- Summary function ---
def print_summary(df, name):
    print(f"\n--- {name} Reviews ---")
    print(f"Total reviews: {len(df)}")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Average star rating: {df['star_rating'].mean():.2f}")
    print(f"Median star rating: {df['star_rating'].median():.2f}")
    print(
        f"Star rating distribution:\n{df['star_rating'].value_counts().sort_index().to_string()}"
    )
    if "text" in df.columns:
        text_lengths = df["text"].dropna().apply(lambda x: len(str(x)))
        print(
            f"Reviews with text: {text_lengths.count()} (avg length: {text_lengths.mean():.1f} chars)"
        )
    else:
        print("No review text available.")


# --- Print summaries ---
print_summary(google, "Google")
print_summary(yelp, "Yelp")

# --- Combined insights ---
print("\n--- Combined Insights ---")
if google["date"].min() < yelp["date"].min():
    print(
        f"Google reviews start earlier ({google['date'].min().date()}) than Yelp ({yelp['date'].min().date()})"
    )
else:
    print(
        f"Yelp reviews start earlier ({yelp['date'].min().date()}) than Google ({google['date'].min().date()})"
    )

if google["date"].max() > yelp["date"].max():
    print(
        f"Google reviews end later ({google['date'].max().date()}) than Yelp ({yelp['date'].max().date()})"
    )
else:
    print(
        f"Yelp reviews end later ({yelp['date'].max().date()}) than Google ({google['date'].max().date()})"
    )

print(
    f"Google average: {google['star_rating'].mean():.2f}, Yelp average: {yelp['star_rating'].mean():.2f}"
)
if abs(google["star_rating"].mean() - yelp["star_rating"].mean()) > 0.2:
    print("Noticeable difference in average star ratings between platforms.")
else:
    print("Average star ratings are similar between platforms.")
