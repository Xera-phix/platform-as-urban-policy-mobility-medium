"""
Analyze Google Local reviews to create user-city summary statistics.

This script processes Pennsylvania Google Local reviews to identify:
1. How many unique cities each user has reviewed
2. How many reviews each user made in each city

Output: CSV file with user_id, no_of_review_cities, and counts per city.
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


def extract_city_from_gmap_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract city information from reviews.

    Since the dataset doesn't have explicit 'city' field, we'll use gmap_id
    to identify unique locations. Each unique gmap_id represents a business
    which we'll treat as a "location".

    Args:
        df: DataFrame with reviews

    Returns:
        DataFrame with city/location column added
    """
    # Use gmap_id as location identifier
    # In real scenario, you'd geocode or use a lookup table
    # For now, we'll create location groups from gmap_id

    if "city" not in df.columns:
        print("ℹ️  No 'city' column found. Using gmap_id as location identifier.")
        df["city"] = df["gmap_id"].astype(str)

    return df


def create_user_city_summary(df: pd.DataFrame, top_n_cities: int = 5) -> pd.DataFrame:
    """
    Create user-city summary with review counts.

    Optimized approach to avoid memory issues with large datasets:
    1. First identify top cities by volume
    2. Filter data to only those cities
    3. Then pivot the smaller dataset

    Args:
        df: DataFrame with user_id and city columns
        top_n_cities: Number of top cities to include as separate columns

    Returns:
        Summary DataFrame with user_id, no_of_review_cities, and city columns
    """
    print(f"\n📊 Analyzing user review patterns...")

    # Count reviews per user per city
    user_city_counts = (
        df.groupby(["user_id", "city"]).size().reset_index(name="review_count")
    )

    # Count unique cities per user
    user_unique_cities = (
        user_city_counts.groupby("user_id")["city"]
        .nunique()
        .reset_index(name="no_of_review_cities")
    )

    print(f"   - Found {len(user_unique_cities):,} unique users")
    print(f"   - Found {df['city'].nunique():,} unique locations")

    # Get top N cities by total review volume BEFORE pivoting (memory efficient)
    print(f"\n🔍 Identifying top {top_n_cities} locations by review volume...")
    city_totals = (
        user_city_counts.groupby("city")["review_count"]
        .sum()
        .sort_values(ascending=False)
    )
    top_cities = city_totals.head(top_n_cities).index.tolist()

    print(f"\n🏆 Top {top_n_cities} most reviewed locations:")
    for i, city in enumerate(top_cities, 1):
        print(f"   {i}. {city}: {city_totals[city]:,} reviews")

    # Filter to only top cities BEFORE pivoting (reduces memory by 99.99%+)
    print(f"\n📉 Filtering to top {top_n_cities} locations only...")
    user_city_top = user_city_counts[user_city_counts["city"].isin(top_cities)].copy()
    print(
        f"   - Reduced from {len(user_city_counts):,} to {len(user_city_top):,} records"
    )

    # Now pivot the much smaller dataset
    print(f"\n🔄 Creating user-city matrix...")
    user_city_matrix_top = (
        user_city_top.pivot(index="user_id", columns="city", values="review_count")
        .fillna(0)
        .astype(int)
    )

    # Merge with unique cities count
    print(f"\n🔗 Merging with city counts...")
    summary = user_unique_cities.merge(
        user_city_matrix_top, left_on="user_id", right_index=True, how="left"
    ).fillna(0)

    # Calculate total reviews per user for sorting
    summary["total_reviews"] = summary[top_cities].sum(axis=1)

    # Sort by total reviews (descending)
    summary = summary.sort_values("total_reviews", ascending=False)

    # Drop the helper column
    summary = summary.drop("total_reviews", axis=1)

    # Rename city columns to be more readable (shorten gmap_id)
    rename_dict = {}
    for col in top_cities:
        if col.startswith("0x"):
            # Extract last 8 chars of gmap_id for readability
            short_name = f"loc_{col[-8:]}"
            rename_dict[col] = short_name

    if rename_dict:
        summary = summary.rename(columns=rename_dict)

    return summary


def main():
    """Main execution function."""

    # Define paths
    project_root = Path(__file__).parent.parent.parent.parent
    input_file = (
        project_root
        / "data"
        / "part 3"
        / "review-Pennsylvania.json"
        / "review-Pennsylvania.json"
    )
    output_file = project_root / "data" / "pennsylvania_user_city_summary.csv"

    print("=" * 80)
    print("PENNSYLVANIA GOOGLE LOCAL REVIEWS - USER CITY ANALYSIS")
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

    # Add city/location information
    df = extract_city_from_gmap_id(df)

    # Filter out rows without user_id
    if "user_id" not in df.columns:
        print("❌ Error: 'user_id' column not found in data")
        return

    df = df.dropna(subset=["user_id"])
    print(f"   - Reviews with valid user_id: {len(df):,}")

    # Create summary
    summary = create_user_city_summary(df, top_n_cities=5)

    # Display sample
    print(f"\n📄 Summary DataFrame Preview:")
    print(summary.head(10).to_string())

    print(f"\n📈 Summary Statistics:")
    print(f"   - Total users: {len(summary):,}")
    print(
        f"   - Users reviewing 1 location: {(summary['no_of_review_cities'] == 1).sum():,}"
    )
    print(
        f"   - Users reviewing 2+ locations: {(summary['no_of_review_cities'] >= 2).sum():,}"
    )
    print(
        f"   - Max locations reviewed by single user: {summary['no_of_review_cities'].max()}"
    )

    # Save to CSV
    print(f"\n💾 Saving results to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_file, index=False)

    print(f"✅ Successfully saved {len(summary):,} user records to CSV")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
