"""
Merge review-Pennsylvania.json with meta-Pennsylvania.json
Filter for brewery-related businesses and extract municipality.

Output: brewery_reviews_with_meta.csv
"""

import json
import re
import csv
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "part 3"
META_PATH = DATA_DIR / "meta-Pennsylvania.json" / "meta-Pennsylvania.json"
REVIEW_PATH = DATA_DIR / "review-Pennsylvania.json" / "review-Pennsylvania.json"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_municipality(address: str) -> str:
    """
    Extract municipality (city) from address string.
    Format: "Business Name, Street, City, State ZIP"
    """
    if not address:
        return ""

    # Split by comma and try to find city
    parts = [p.strip() for p in address.split(",")]

    # Typical format: Name, Street, City, State ZIP
    # We want the second-to-last part before "PA XXXXX"
    for i, part in enumerate(parts):
        if re.search(r"\bPA\s+\d{5}", part):
            # This part contains state and ZIP, city is the previous part
            if i > 0:
                return parts[i - 1]
            # If state/zip is in same part as city (rare), try to extract
            match = re.match(r"^(.+?)\s+PA\s+\d{5}", part)
            if match:
                return match.group(1).strip()

    # Fallback: if no PA ZIP found, try last meaningful part
    if len(parts) >= 3:
        return parts[-2]  # Second to last

    return ""


def is_brewpub(categories: list) -> bool:
    """
    Check if this place is specifically a Brewpub.

    A brewpub is a brewery that sells its beer on-site (restaurant + brewery).
    This is a strict filter - only matches "Brewpub" category exactly.
    """
    if not categories:
        return False

    for cat in categories:
        if cat.lower() == "brewpub":
            return True

    return False


def load_brewpub_metadata() -> dict:
    """Load meta file and filter for Brewpub businesses only."""
    print(f"Loading metadata from: {META_PATH}")

    brewpubs = {}
    total_places = 0

    with open(META_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                place = json.loads(line)
                total_places += 1

                if is_brewpub(place.get("category", [])):
                    gmap_id = place.get("gmap_id")
                    if gmap_id:
                        brewpubs[gmap_id] = {
                            "name": place.get("name", ""),
                            "address": place.get("address", ""),
                            "gmap_id": gmap_id,
                            "description": place.get("description", ""),
                            "latitude": place.get("latitude"),
                            "longitude": place.get("longitude"),
                            "category": place.get("category", []),
                            "avg_rating": place.get("avg_rating"),
                            "num_of_reviews": place.get("num_of_reviews"),
                            "misc": place.get("MISC", {}),
                            "municipality": extract_municipality(
                                place.get("address", "")
                            ),
                        }
            except json.JSONDecodeError:
                continue

    print(f"  Total places: {total_places:,}")
    print(f"  Brewpubs found: {len(brewpubs):,}")
    return brewpubs


def process_reviews(brewpubs: dict):
    """Stream through reviews and match with brewpub metadata."""
    print(f"\nProcessing reviews from: {REVIEW_PATH}")
    print("  (This may take a few minutes for the 6.7GB file...)")

    output_path = OUTPUT_DIR / "brewpub_reviews_with_meta.csv"

    fieldnames = [
        "review_user_id",
        "review_user_name",
        "review_time",
        "review_date",
        "rating",
        "review_text",
        "has_pics",
        "has_response",
        "gmap_id",
        "business_name",
        "address",
        "municipality",
        "latitude",
        "longitude",
        "category",
        "description",
        "avg_rating",
        "num_of_reviews",
    ]

    matched_reviews = 0
    total_reviews = 0

    with open(output_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(REVIEW_PATH, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue

                try:
                    review = json.loads(line)
                    total_reviews += 1

                    gmap_id = review.get("gmap_id")
                    if gmap_id and gmap_id in brewpubs:
                        meta = brewpubs[gmap_id]

                        # Convert timestamp to readable date
                        timestamp_ms = review.get("time", 0)
                        review_date = (
                            datetime.fromtimestamp(timestamp_ms / 1000).strftime(
                                "%Y-%m-%d"
                            )
                            if timestamp_ms
                            else ""
                        )

                        row = {
                            "review_user_id": review.get("user_id", ""),
                            "review_user_name": review.get("name", ""),
                            "review_time": timestamp_ms,
                            "review_date": review_date,
                            "rating": review.get("rating", ""),
                            "review_text": review.get("text", ""),
                            "has_pics": bool(review.get("pics")),
                            "has_response": bool(review.get("resp")),
                            "gmap_id": gmap_id,
                            "business_name": meta["name"],
                            "address": meta["address"],
                            "municipality": meta["municipality"],
                            "latitude": meta["latitude"],
                            "longitude": meta["longitude"],
                            "category": (
                                "|".join(meta["category"]) if meta["category"] else ""
                            ),
                            "description": meta["description"] or "",
                            "avg_rating": meta["avg_rating"],
                            "num_of_reviews": meta["num_of_reviews"],
                        }
                        writer.writerow(row)
                        matched_reviews += 1

                except json.JSONDecodeError:
                    continue

                # Progress update
                if line_num % 1_000_000 == 0:
                    print(
                        f"  Processed {line_num:,} reviews, matched {matched_reviews:,}..."
                    )

    print(f"\n✓ Done!")
    print(f"  Total reviews processed: {total_reviews:,}")
    print(f"  Brewpub reviews matched: {matched_reviews:,}")
    print(f"  Output saved to: {output_path}")

    return matched_reviews


def main():
    print("=" * 60)
    print("Merge Brewpub Reviews with Metadata")
    print("=" * 60)

    # Step 1: Load brewpub metadata
    brewpubs = load_brewpub_metadata()

    if not brewpubs:
        print("\n⚠ No brewpubs found!")
        return

    # Show sample categories found (all categories that brewpubs have)
    all_categories = set()
    for b in brewpubs.values():
        all_categories.update(b["category"])
    print(f"\nCategories associated with brewpubs:")
    for cat in sorted(all_categories)[:20]:
        print(f"  - {cat}")
    if len(all_categories) > 20:
        print(f"  ... and {len(all_categories) - 20} more")

    # Step 2: Process reviews
    matched = process_reviews(brewpubs)

    # Step 3: Summary
    if matched > 0:
        print("\n" + "=" * 60)
        print("Sample municipalities with brewpub reviews:")
        municipalities = set(
            b["municipality"] for b in brewpubs.values() if b["municipality"]
        )
        for m in sorted(municipalities)[:15]:
            print(f"  - {m}")
        if len(municipalities) > 15:
            print(f"  ... and {len(municipalities) - 15} more")


if __name__ == "__main__":
    main()
