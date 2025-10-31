"""
Test Supabase connection and query reviews.

Quick script to verify your Supabase setup is working correctly.
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()


def test_connection():
    """Test basic Supabase connection"""
    print("\n🔌 Testing Supabase connection...")

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        print("❌ Missing credentials! Check your .env file")
        return False

    try:
        supabase = create_client(url, key)
        print("✅ Connected to Supabase!")
        return supabase
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None


def test_queries(supabase):
    """Test various queries"""
    print("\n📊 Running test queries...\n")

    # Count total reviews
    result = supabase.table("reviews").select("id", count="exact").execute()
    print(f"Total reviews: {result.count}")

    # Reviews by period
    print("\nReviews by period:")
    for period in ["pre_construction", "during_construction", "post_construction"]:
        result = (
            supabase.table("reviews")
            .select("id", count="exact")
            .eq("period", period)
            .execute()
        )
        print(f"  {period}: {result.count}")

    # Average ratings
    print("\nAverage ratings by period:")
    for period in ["pre_construction", "during_construction", "post_construction"]:
        result = (
            supabase.table("reviews").select("rating").eq("period", period).execute()
        )
        if result.data:
            ratings = [r["rating"] for r in result.data]
            avg = sum(ratings) / len(ratings)
            print(f"  {period}: {avg:.2f} ⭐")

    # Sample recent reviews
    print("\nSample reviews (most recent 3):")
    result = (
        supabase.table("reviews")
        .select("user_name, rating, title, date_of_experience")
        .order("date_of_experience", desc=True)
        .limit(3)
        .execute()
    )
    for i, review in enumerate(result.data, 1):
        print(f"\n  {i}. {review['user_name']} - {review['rating']}⭐")
        print(f"     {review['title']}")
        print(f"     {review['date_of_experience']}")


if __name__ == "__main__":
    print("=" * 60)
    print("SUPABASE CONNECTION TEST")
    print("=" * 60)

    supabase = test_connection()

    if supabase:
        try:
            test_queries(supabase)
            print("\n" + "=" * 60)
            print("✅ All tests passed! Your Supabase setup is working!")
            print("=" * 60)
        except Exception as e:
            print(f"\n❌ Query failed: {e}")
            print("\nMake sure you've:")
            print("1. Created the 'reviews' table (run setup_supabase.py first)")
            print("2. Uploaded data (run setup_supabase.py --upload)")
