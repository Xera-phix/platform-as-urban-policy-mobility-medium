"""
Set up Supabase database for Love Park review data.

Creates tables, uploads review data, and sets up indexes for optimal querying.
Run this once after creating your Supabase project.
"""

import os
import json
import pandas as pd
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_supabase_client():
    """
    Initialize Supabase client with credentials.

    Set these environment variables:
        SUPABASE_URL: Your project URL from Supabase dashboard
        SUPABASE_KEY: Your project API key (anon/public key)
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "Missing Supabase credentials!\n"
            "Set SUPABASE_URL and SUPABASE_KEY environment variables.\n"
            "Find these in your Supabase project settings > API"
        )

    return create_client(url, key)


def create_reviews_table(supabase: Client):
    """
    Create reviews table with proper schema.

    Note: Table creation is done via Supabase SQL Editor.
    This function provides the SQL for you to run manually.
    """
    sql = """
    -- Create reviews table
    CREATE TABLE IF NOT EXISTS reviews (
        id BIGSERIAL PRIMARY KEY,
        review_id TEXT UNIQUE,
        user_name TEXT,
        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
        text TEXT,
        date_of_experience TIMESTAMP WITH TIME ZONE,
        date_written TIMESTAMP WITH TIME ZONE,
        title TEXT,
        helpful_votes INTEGER DEFAULT 0,
        trip_type TEXT,
        period TEXT CHECK (period IN (
            'pre_construction',
            'during_construction', 
            'post_construction',
            'border_feb2016',
            'border_may2018',
            'missing_date'
        )),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Create indexes for common queries
    CREATE INDEX IF NOT EXISTS idx_reviews_period ON reviews(period);
    CREATE INDEX IF NOT EXISTS idx_reviews_date_experience ON reviews(date_of_experience);
    CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
    CREATE INDEX IF NOT EXISTS idx_reviews_user ON reviews(user_name);

    -- Enable Row Level Security (RLS) - Read-only public access
    ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

    -- Allow anyone to read reviews
    CREATE POLICY "Reviews are viewable by everyone"
        ON reviews FOR SELECT
        USING (true);
    """

    print("\n" + "=" * 60)
    print("COPY THIS SQL AND RUN IN SUPABASE SQL EDITOR:")
    print("=" * 60)
    print(sql)
    print("=" * 60)
    print("\nSteps:")
    print("1. Go to your Supabase dashboard")
    print("2. Click 'SQL Editor' in the left sidebar")
    print("3. Paste the SQL above")
    print("4. Click 'Run' or press Ctrl+Enter")
    print("5. Come back and run this script again with --upload")


def upload_reviews(
    supabase: Client, json_file="data/tripadvisor_jfkplaza_with_periods.json"
):
    """
    Upload review data to Supabase.

    Args:
        supabase: Supabase client instance
        json_file: Path to reviews JSON with period classifications
    """
    print(f"\n📂 Loading reviews from {json_file}...")

    with open(json_file, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    print(f"✓ Loaded {len(reviews)} reviews")

    # Prepare data for upload
    batch_size = 100
    uploaded = 0
    errors = []

    print(f"\n⬆️  Uploading reviews in batches of {batch_size}...")

    for i in range(0, len(reviews), batch_size):
        batch = reviews[i : i + batch_size]

        # Clean and format each review
        formatted_batch = []
        for review in batch:
            # Convert dates from various formats to ISO string
            def format_date(date_value):
                if not date_value or date_value == "":
                    return None
                if isinstance(date_value, (int, float)):
                    # Unix timestamp in milliseconds
                    return pd.Timestamp(date_value, unit="ms").isoformat()
                elif isinstance(date_value, str):
                    # Already a string, convert to proper ISO format
                    try:
                        ts = pd.to_datetime(date_value)
                        # Check if it's NaT (Not a Time)
                        if pd.isna(ts):
                            return None
                        return ts.isoformat()
                    except:
                        return None
                return None

            # Generate unique review_id if missing
            review_id = review.get("review_id")
            if not review_id or review_id == "":
                # Use combination of user, date, and index for uniqueness
                date_str = review.get("date_of_experience", "")
                user = review.get("user_name", "unknown")
                review_id = f"trip_{user}_{date_str}_{i}"

            formatted_review = {
                "review_id": review_id,
                "user_name": review.get("user_name"),
                "rating": int(review.get("rating", 0)),
                "text": review.get("text"),
                "date_of_experience": format_date(review.get("date_of_experience")),
                "date_written": format_date(review.get("date_written")),
                "title": review.get("title"),
                "helpful_votes": int(review.get("helpful_votes", 0)),
                "trip_type": review.get("trip_type"),
                "period": review.get("period", "missing_date"),
            }
            formatted_batch.append(formatted_review)

        try:
            result = supabase.table("reviews").upsert(formatted_batch).execute()
            uploaded += len(formatted_batch)
            print(f"  ✓ Uploaded batch {i//batch_size + 1} ({uploaded}/{len(reviews)})")
        except Exception as e:
            error_msg = f"Batch {i//batch_size + 1} failed: {str(e)}"
            errors.append(error_msg)
            print(f"  ✗ {error_msg}")

    print(f"\n{'='*60}")
    print(f"✅ Upload complete!")
    print(f"   Successfully uploaded: {uploaded}/{len(reviews)} reviews")

    if errors:
        print(f"\n⚠️  Encountered {len(errors)} errors:")
        for error in errors:
            print(f"   - {error}")

    return uploaded, errors


def verify_upload(supabase: Client):
    """Verify data was uploaded correctly"""
    print("\n🔍 Verifying upload...")

    # Count total reviews
    result = supabase.table("reviews").select("id", count="exact").execute()
    total = result.count
    print(f"   Total reviews in database: {total}")

    # Count by period
    periods = supabase.table("reviews").select("period", count="exact").execute()
    print(f"\n   Reviews by period:")

    for period in ["pre_construction", "during_construction", "post_construction"]:
        result = (
            supabase.table("reviews")
            .select("id", count="exact")
            .eq("period", period)
            .execute()
        )
        print(f"     - {period}: {result.count}")

    # Average rating by period
    print(f"\n   Average ratings:")
    for period in ["pre_construction", "during_construction", "post_construction"]:
        result = (
            supabase.table("reviews").select("rating").eq("period", period).execute()
        )
        if result.data:
            ratings = [r["rating"] for r in result.data]
            avg = sum(ratings) / len(ratings)
            print(f"     - {period}: {avg:.2f} ⭐")


def main():
    """Main setup workflow"""
    import sys

    print("\n🚀 Supabase Setup for Love Park Reviews")
    print("=" * 60)

    if "--help" in sys.argv:
        print(
            """
Usage:
    python setup_supabase.py              # Show SQL for table creation
    python setup_supabase.py --upload     # Upload review data
    python setup_supabase.py --verify     # Verify uploaded data

Environment Variables Required:
    SUPABASE_URL   - Your project URL from Supabase dashboard
    SUPABASE_KEY   - Your anon/public API key
        """
        )
        return

    if "--upload" in sys.argv or "--verify" in sys.argv:
        try:
            supabase = get_supabase_client()
            print("✓ Connected to Supabase")
        except ValueError as e:
            print(f"\n❌ {str(e)}")
            return

        if "--upload" in sys.argv:
            upload_reviews(supabase)

        if "--verify" in sys.argv:
            verify_upload(supabase)
    else:
        # Default: show SQL for table creation
        create_reviews_table(None)


if __name__ == "__main__":
    main()
