"""
Tally statistics for each reviewer in the brewpub dataset.
"""

import pandas as pd
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
INPUT_PATH = OUTPUT_DIR / "brewpub_reviews_with_meta.csv"
OUTPUT_PATH = OUTPUT_DIR / "reviewer_tally.csv"


def main():
    print("=" * 60)
    print("Reviewer Tally Analysis")
    print("=" * 60)

    # Load data
    print("\nLoading brewpub reviews...")
    df = pd.read_csv(INPUT_PATH)
    print(f"  Loaded {len(df):,} reviews")

    # Aggregate by reviewer (using user_id only - users can change display names)
    print("\nCalculating reviewer statistics...")

    reviewer_stats = (
        df.groupby("review_user_id")
        .agg(
            review_user_name=(
                "review_user_name",
                "first",
            ),  # Use first name encountered
            num_reviews=("rating", "count"),
            unique_municipalities=("municipality", "nunique"),
            num_responses=("has_response", "sum"),
        )
        .reset_index()
    )

    # Convert has_response sum to integer
    reviewer_stats["num_responses"] = reviewer_stats["num_responses"].astype(int)

    # Sort by number of reviews descending
    reviewer_stats = reviewer_stats.sort_values("num_reviews", ascending=False)

    # Save to CSV
    reviewer_stats.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to: {OUTPUT_PATH}")

    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTotal unique reviewers: {len(reviewer_stats):,}")

    print("\nReview Count Distribution:")
    print(
        f"  1 review:        {(reviewer_stats['num_reviews'] == 1).sum():,} reviewers"
    )
    print(
        f"  2-5 reviews:     {((reviewer_stats['num_reviews'] >= 2) & (reviewer_stats['num_reviews'] <= 5)).sum():,} reviewers"
    )
    print(
        f"  6-10 reviews:    {((reviewer_stats['num_reviews'] >= 6) & (reviewer_stats['num_reviews'] <= 10)).sum():,} reviewers"
    )
    print(
        f"  11+ reviews:     {(reviewer_stats['num_reviews'] > 10).sum():,} reviewers"
    )

    print("\nUnique Municipalities Visited:")
    print(
        f"  1 municipality:  {(reviewer_stats['unique_municipalities'] == 1).sum():,} reviewers"
    )
    print(
        f"  2-3 municipalities: {((reviewer_stats['unique_municipalities'] >= 2) & (reviewer_stats['unique_municipalities'] <= 3)).sum():,} reviewers"
    )
    print(
        f"  4+ municipalities:  {(reviewer_stats['unique_municipalities'] >= 4).sum():,} reviewers"
    )

    print("\nResponse Rate:")
    reviewers_with_responses = (reviewer_stats["num_responses"] > 0).sum()
    print(
        f"  Reviewers who received at least 1 response: {reviewers_with_responses:,} ({reviewers_with_responses/len(reviewer_stats)*100:.1f}%)"
    )

    print("\nTop 15 Most Active Reviewers:")
    print(f"{'Name':<35} {'Reviews':>8} {'Municipalities':>15} {'Responses':>10}")
    print("-" * 70)
    for _, row in reviewer_stats.head(15).iterrows():
        name = (
            row["review_user_name"][:34]
            if pd.notna(row["review_user_name"])
            else "Unknown"
        )
        print(
            f"{name:<35} {row['num_reviews']:>8} {row['unique_municipalities']:>15} {row['num_responses']:>10}"
        )

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
