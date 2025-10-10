import pandas as pd
import numpy as np

# Load TripAdvisor data
# Adjust path as needed
reviews = pd.read_json("data/tripadvisor_jfkplaza.json")

# Ensure date and text columns are correct
reviews["date_of_experience"] = pd.to_datetime(reviews["date_of_experience"], errors="coerce")
reviews = reviews.dropna(subset=["date_of_experience", "user_name"])

# Calculate text length
if "text" in reviews.columns:
    reviews["text_length"] = reviews["text"].fillna("").apply(len)
else:
    reviews["text_length"] = 0

# Group by user
user_stats = reviews.groupby("user_name").agg(
    n_reviews=("rating", "count"),
    n_ratings=("rating", "count"),  # same as n_reviews for this dataset
    n_first_reviews=("date_of_experience", lambda x: (x == x.min()).sum()),
    n_checkins=("checkins", "sum") if "checkins" in reviews.columns else ("rating", lambda x: np.nan),
    n_photos=("photos", "sum") if "photos" in reviews.columns else ("rating", lambda x: np.nan),
    first_review_date=("date_of_experience", "min"),
    last_review_date=("date_of_experience", "max"),
    days_active=("date_of_experience", lambda x: (x.max() - x.min()).days if len(x) > 1 else 0),
    avg_text_length=("text_length", "mean"),
)

# Reviews per days active
user_stats["reviews_per_day_active"] = user_stats["n_reviews"] / user_stats["days_active"].replace(0, np.nan)

# Save to Excel
user_stats.to_excel("tripadvisor_user_stats.xlsx")

print("User stats table saved as tripadvisor_user_stats.xlsx")
