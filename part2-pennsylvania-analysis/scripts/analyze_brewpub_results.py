"""
In-depth analysis of brewpub reviews dataset
"""

import csv
import pandas as pd
from pathlib import Path
from collections import Counter
from datetime import datetime

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
CSV_PATH = OUTPUT_DIR / "brewpub_reviews_with_meta.csv"


def main():
    print("=" * 80)
    print("IN-DEPTH ANALYSIS: Pennsylvania Brewpub Reviews")
    print("=" * 80)

    # Load data
    print("\nLoading data...")
    df = pd.read_csv(CSV_PATH)

    print(f"✓ Loaded {len(df):,} reviews")

    # ========== FILTERING CONFIRMATION ==========
    print("\n" + "=" * 80)
    print("1. FILTERING LOGIC CONFIRMATION")
    print("=" * 80)
    print("\nThe CSV contains ALL reviews where the business has 'Brewpub' as ONE OF")
    print("its Google Maps categories. Businesses can have multiple categories.")
    print("\nExample: A brewpub might be categorized as:")
    print("  ['Brewpub', 'Restaurant', 'Bar', 'American restaurant']")
    print(
        "\n→ All reviews for that business are included because 'Brewpub' is present."
    )

    # ========== BASIC STATISTICS ==========
    print("\n" + "=" * 80)
    print("2. DATASET OVERVIEW")
    print("=" * 80)

    unique_brewpubs = df["gmap_id"].nunique()
    unique_reviewers = df["review_user_id"].nunique()
    date_range = pd.to_datetime(df["review_date"])

    print(f"\n📊 Basic Stats:")
    print(f"  • Total reviews:        {len(df):>10,}")
    print(f"  • Unique brewpubs:      {unique_brewpubs:>10,}")
    print(f"  • Unique reviewers:     {unique_reviewers:>10,}")
    print(f"  • Avg reviews/brewpub:  {len(df)/unique_brewpubs:>10.1f}")
    print(
        f"  • Date range:           {date_range.min().date()} to {date_range.max().date()}"
    )
    print(
        f"  • Time span:            {(date_range.max() - date_range.min()).days:,} days"
    )

    # ========== RATING ANALYSIS ==========
    print("\n" + "=" * 80)
    print("3. RATING DISTRIBUTION")
    print("=" * 80)

    rating_counts = df["rating"].value_counts().sort_index()
    total = len(df)

    print("\n⭐ Star Ratings:")
    for rating in sorted(rating_counts.index, reverse=True):
        count = rating_counts[rating]
        pct = (count / total) * 100
        bar = "█" * int(pct / 2)
        print(f"  {rating}★: {count:>8,} ({pct:>5.1f}%) {bar}")

    print(f"\n  Average rating: {df['rating'].mean():.2f}★")
    print(f"  Median rating:  {df['rating'].median():.1f}★")

    # ========== GEOGRAPHIC ANALYSIS ==========
    print("\n" + "=" * 80)
    print("4. GEOGRAPHIC DISTRIBUTION")
    print("=" * 80)

    # Top municipalities by number of brewpubs
    brewpubs_by_city = (
        df.groupby("municipality")["gmap_id"].nunique().sort_values(ascending=False)
    )

    print("\n🏙️  Top 15 Cities by Number of Brewpubs:")
    for i, (city, count) in enumerate(brewpubs_by_city.head(15).items(), 1):
        print(f"  {i:>2}. {city:<25} {count:>3} brewpubs")

    # Top municipalities by number of reviews
    reviews_by_city = df["municipality"].value_counts()

    print("\n📝 Top 15 Cities by Number of Reviews:")
    for i, (city, count) in enumerate(reviews_by_city.head(15).items(), 1):
        print(f"  {i:>2}. {city:<25} {count:>6,} reviews")

    # ========== TEMPORAL ANALYSIS ==========
    print("\n" + "=" * 80)
    print("5. TEMPORAL TRENDS")
    print("=" * 80)

    df["year"] = pd.to_datetime(df["review_date"]).dt.year
    reviews_by_year = df["year"].value_counts().sort_index()

    print("\n📅 Reviews by Year:")
    for year in sorted(reviews_by_year.index):
        count = reviews_by_year[year]
        if count > 0:
            bar = "█" * int(count / 500)
            print(f"  {year}: {count:>6,} {bar}")

    # ========== TOP BREWPUBS ==========
    print("\n" + "=" * 80)
    print("6. MOST REVIEWED BREWPUBS")
    print("=" * 80)

    top_brewpubs = (
        df.groupby(["business_name", "municipality"])
        .agg({"rating": ["count", "mean"], "gmap_id": "first", "avg_rating": "first"})
        .round(2)
    )

    top_brewpubs.columns = ["review_count", "dataset_avg", "gmap_id", "google_avg"]
    top_brewpubs = top_brewpubs.sort_values("review_count", ascending=False)

    print("\n🏆 Top 20 Brewpubs by Review Count:")
    print(f"{'#':<3} {'Name':<35} {'City':<20} {'Reviews':>8} {'Avg★':>6}")
    print("-" * 80)
    for i, ((name, city), row) in enumerate(top_brewpubs.head(20).iterrows(), 1):
        print(
            f"{i:<3} {name[:34]:<35} {city[:19]:<20} {row['review_count']:>8.0f} {row['dataset_avg']:>6.2f}"
        )

    # ========== REVIEW TEXT ANALYSIS ==========
    print("\n" + "=" * 80)
    print("7. REVIEW TEXT CHARACTERISTICS")
    print("=" * 80)

    df["text_length"] = df["review_text"].fillna("").str.len()
    df["word_count"] = df["review_text"].fillna("").str.split().str.len()

    print("\n📝 Text Statistics:")
    print(f"  • Avg characters per review: {df['text_length'].mean():.0f}")
    print(f"  • Avg words per review:      {df['word_count'].mean():.0f}")
    print(f"  • Empty reviews:             {df['review_text'].isna().sum():,}")
    print(
        f"  • Reviews with photos:       {df['has_pics'].sum():,} ({df['has_pics'].sum()/len(df)*100:.1f}%)"
    )
    print(
        f"  • Reviews with response:     {df['has_response'].sum():,} ({df['has_response'].sum()/len(df)*100:.1f}%)"
    )

    # ========== CATEGORY CO-OCCURRENCE ==========
    print("\n" + "=" * 80)
    print("8. CATEGORY CO-OCCURRENCE")
    print("=" * 80)
    print("\nWhat other categories do brewpubs typically have?")

    all_categories = []
    for cats in df["category"].dropna():
        all_categories.extend([c.strip() for c in cats.split("|")])

    cat_counter = Counter(all_categories)

    print("\n🏷️  Top 20 Categories (among brewpub establishments):")
    for i, (cat, count) in enumerate(cat_counter.most_common(20), 1):
        pct = (count / len(df)) * 100
        print(f"  {i:>2}. {cat:<35} {count:>6,} ({pct:>5.1f}% of reviews)")

    # ========== REVIEWER ENGAGEMENT ==========
    print("\n" + "=" * 80)
    print("9. REVIEWER ENGAGEMENT")
    print("=" * 80)

    reviews_per_user = df["review_user_id"].value_counts()

    print("\n👥 User Review Activity:")
    print(f"  • Users with 1 review:       {(reviews_per_user == 1).sum():>8,}")
    print(
        f"  • Users with 2-5 reviews:    {((reviews_per_user >= 2) & (reviews_per_user <= 5)).sum():>8,}"
    )
    print(
        f"  • Users with 6-10 reviews:   {((reviews_per_user >= 6) & (reviews_per_user <= 10)).sum():>8,}"
    )
    print(f"  • Users with 10+ reviews:    {(reviews_per_user > 10).sum():>8,}")
    print(f"  • Max reviews by one user:   {reviews_per_user.max():>8,}")

    # Most active reviewers
    print("\n🌟 Most Active Reviewers:")
    top_reviewers = (
        df.groupby(["review_user_name", "review_user_id"])
        .agg({"rating": ["count", "mean"]})
        .round(2)
    )
    top_reviewers.columns = ["review_count", "avg_rating"]
    top_reviewers = top_reviewers.sort_values("review_count", ascending=False)

    for i, ((name, uid), row) in enumerate(top_reviewers.head(10).iterrows(), 1):
        print(
            f"  {i:>2}. {name[:30]:<30} {row['review_count']:>4.0f} reviews (avg {row['avg_rating']:.1f}★)"
        )

    # ========== SUMMARY INSIGHTS ==========
    print("\n" + "=" * 80)
    print("10. KEY INSIGHTS")
    print("=" * 80)

    positive_reviews = len(df[df["rating"] >= 4])
    negative_reviews = len(df[df["rating"] <= 2])

    print(
        f"""
✓ Dataset Quality:
  - High volume: {len(df):,} reviews across {unique_brewpubs} brewpubs
  - Good temporal coverage: {(date_range.max() - date_range.min()).days // 365} years of data
  - Average {len(df)/unique_brewpubs:.0f} reviews per establishment
  
✓ Rating Sentiment:
  - Overall positive: {positive_reviews/len(df)*100:.1f}% rated 4-5 stars
  - Negative reviews: {negative_reviews/len(df)*100:.1f}% rated 1-2 stars
  - Mean rating: {df['rating'].mean():.2f}★ (above average)
  
✓ Geographic Coverage:
  - {len(df['municipality'].unique())} municipalities represented
  - Top city: {reviews_by_city.index[0]} with {reviews_by_city.iloc[0]:,} reviews
  - Well-distributed across Pennsylvania
  
✓ Data Richness:
  - {df['has_pics'].sum():,} reviews have photos
  - {df['has_response'].sum():,} reviews have owner responses
  - Average review length: {df['word_count'].mean():.0f} words
    """
    )

    print("=" * 80)
    print("Analysis complete! ✓")
    print("=" * 80)


if __name__ == "__main__":
    main()
