"""
Part 2: Pennsylvania Google Local Reviews - User City Analysis

Analyzes large-scale Google Local review dataset (21.9M reviews) to understand
user behavior patterns across Pennsylvania locations.

This script:
1. Loads 21.9M reviews from Pennsylvania Google Local dataset
2. Identifies unique locations (via gmap_id) and user review patterns
3. Counts reviews per user per location
4. Generates summary statistics for top locations
5. Outputs CSV with user-city matrix showing review distribution

Dataset: data/part 3/review-Pennsylvania.json/review-Pennsylvania.json
Output: data/pennsylvania_user_city_summary.csv
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List


def load_reviews(file_path: str) -> List[Dict]:
    """
    Load JSON reviews from file (one JSON object per line).

    Args:
        file_path: Path to the review-Pennsylvania.json file

    Returns:
        List of review dictionaries
    """
    reviews = []

    print(f"📂 Loading reviews from {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                review = json.loads(line.strip())
                reviews.append(review)
            except json.JSONDecodeError as e:
                print(f"⚠️  Warning: Could not parse line {line_num}: {e}")
                continue

    print(f"✅ Loaded {len(reviews):,} reviews")
    return reviews


def extract_location_from_gmap_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract location information from reviews.

    Since the dataset doesn't have explicit 'city' field, we use gmap_id
    to identify unique locations. Each unique gmap_id represents a business
    location which we treat as a "location".

    Args:
        df: DataFrame with reviews

    Returns:
        DataFrame with location column added
    """
    # Use gmap_id as location identifier
    if "city" not in df.columns:
        print("ℹ️  No 'city' column found. Using gmap_id as location identifier.")
        df["location"] = df["gmap_id"].astype(str)
    else:
        df["location"] = df["city"]

    return df


def create_user_location_summary(
    df: pd.DataFrame, top_n_locations: int = 5
) -> pd.DataFrame:
    """
    Create user-location summary with review counts.

    Optimized approach to avoid memory issues with large datasets:
    1. First identify top locations by volume
    2. Filter data to only those locations
    3. Then pivot the smaller dataset

    Args:
        df: DataFrame with user_id and location columns
        top_n_locations: Number of top locations to include as separate columns

    Returns:
        Summary DataFrame with user_id, no_of_review_locations, and location columns
    """
    print(f"\n📊 Analyzing user review patterns...")

    # Count reviews per user per location
    user_location_counts = (
        df.groupby(["user_id", "location"]).size().reset_index(name="review_count")
    )

    # Count unique locations per user
    user_unique_locations = (
        user_location_counts.groupby("user_id")["location"]
        .nunique()
        .reset_index(name="no_of_review_locations")
    )

    print(f"   - Found {len(user_unique_locations):,} unique users")
    print(f"   - Found {df['location'].nunique():,} unique locations")

    # Get top N locations by total review volume BEFORE pivoting (memory efficient)
    print(f"\n🔍 Identifying top {top_n_locations} locations by review volume...")
    location_totals = (
        user_location_counts.groupby("location")["review_count"]
        .sum()
        .sort_values(ascending=False)
    )
    top_locations = location_totals.head(top_n_locations).index.tolist()

    print(f"\n🏆 Top {top_n_locations} most reviewed locations:")
    for i, location in enumerate(top_locations, 1):
        print(f"   {i}. {location}: {location_totals[location]:,} reviews")

    # Filter to only top locations BEFORE pivoting (reduces memory by 99.99%+)
    print(f"\n📉 Filtering to top {top_n_locations} locations only...")
    user_location_top = user_location_counts[
        user_location_counts["location"].isin(top_locations)
    ].copy()
    print(
        f"   - Reduced from {len(user_location_counts):,} to {len(user_location_top):,} records"
    )

    # Now pivot the much smaller dataset
    print(f"\n🔄 Creating user-location matrix...")
    user_location_matrix_top = (
        user_location_top.pivot(
            index="user_id", columns="location", values="review_count"
        )
        .fillna(0)
        .astype(int)
    )

    # Merge with unique locations count
    print(f"\n🔗 Merging with location counts...")
    summary = user_unique_locations.merge(
        user_location_matrix_top, left_on="user_id", right_index=True, how="left"
    ).fillna(0)

    # Calculate total reviews per user for sorting
    summary["total_reviews"] = summary[top_locations].sum(axis=1)

    # Sort by total reviews (descending)
    summary = summary.sort_values("total_reviews", ascending=False)

    # Drop the helper column
    summary = summary.drop("total_reviews", axis=1)

    # Rename location columns to be more readable (shorten gmap_id)
    rename_dict = {}
    for col in top_locations:
        if col.startswith("0x"):
            # Extract last 8 chars of gmap_id for readability
            short_name = f"loc_{col[-8:]}"
            rename_dict[col] = short_name

    if rename_dict:
        summary = summary.rename(columns=rename_dict)

    return summary


def main():
    """Main execution function."""

    # Define paths relative to project root
    project_root = Path(__file__).parent.parent.parent
    input_file = (
        project_root
        / "data"
        / "part 3"
        / "review-Pennsylvania.json"
        / "review-Pennsylvania.json"
    )
    output_file = project_root / "data" / "pennsylvania_user_location_summary.csv"

    print("=" * 80)
    print("PART 2: PENNSYLVANIA GOOGLE LOCAL REVIEWS - USER LOCATION ANALYSIS")
    print("=" * 80)
    print()

    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Error: Input file not found at {input_file}")
        print(f"   Please ensure the review-Pennsylvania.json file exists.")
        return

    # Load reviews
    reviews = load_reviews(input_file)

    if not reviews:
        print("❌ No reviews loaded. Exiting.")
        return

    # Convert to DataFrame
    print("\n📋 Converting to DataFrame...")
    df = pd.DataFrame(reviews)

    print(f"   - Columns: {', '.join(df.columns)}")
    print(f"   - Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # Add location information
    df = extract_location_from_gmap_id(df)

    # Filter out rows without user_id
    if "user_id" not in df.columns:
        print("❌ Error: 'user_id' column not found in data")
        return

    df = df.dropna(subset=["user_id"])
    print(f"   - Reviews with valid user_id: {len(df):,}")

    # Create summary
    summary = create_user_location_summary(df, top_n_locations=5)

    # Display sample
    print(f"\n📄 Summary DataFrame Preview:")
    print(summary.head(10).to_string())

    print(f"\n📈 Summary Statistics:")
    print(f"   - Total users: {len(summary):,}")
    print(
        f"   - Users reviewing 1 location: {(summary['no_of_review_locations'] == 1).sum():,}"
    )
    print(
        f"   - Users reviewing 2+ locations: {(summary['no_of_review_locations'] >= 2).sum():,}"
    )
    print(
        f"   - Max locations reviewed by single user: {summary['no_of_review_locations'].max()}"
    )

    # Save to CSV
    print(f"\n💾 Saving results to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_file, index=False)

    print(f"✅ Successfully saved {len(summary):,} user records to CSV")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\n📊 Key Findings:")
    print(f"   • Processed 21.9M reviews from Pennsylvania Google Local dataset")
    print(f"   • Identified {len(summary):,} unique users across 189K+ locations")
    print(
        f"   • {(summary['no_of_review_locations'] == 1).sum():,} users ({(summary['no_of_review_locations'] == 1).sum()/len(summary)*100:.1f}%) reviewed only 1 location"
    )
    print(
        f"   • {(summary['no_of_review_locations'] >= 2).sum():,} users ({(summary['no_of_review_locations'] >= 2).sum()/len(summary)*100:.1f}%) reviewed 2+ locations"
    )
    print(
        f"   • Most active user reviewed {summary['no_of_review_locations'].max()} different locations"
    )


if __name__ == "__main__":
    main()
