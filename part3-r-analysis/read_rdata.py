"""
Read R data files (.rdata) and convert to JSON/CSV using pyreadr
"""

import pyreadr
import json
import pandas as pd
from pathlib import Path


def read_rdata_file(filepath: str, output_format: str = "json"):
    """
    Read an .rdata file and convert to JSON or CSV

    Args:
        filepath: Path to the .rdata file
        output_format: 'json' or 'csv'
    """
    try:
        # Read the rdata file
        print(f"Reading {filepath}...")
        result = pyreadr.read_r(filepath)

        # Show what's inside
        print(f"\nData objects found: {list(result.keys())}")

        # Process each dataframe
        for name, df in result.items():
            print(f"\n--- {name} ---")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"\nFirst few rows:\n{df.head()}")

            # Save to file
            if output_format == "json":
                output_file = f"{name}.json"
                df.to_json(output_file, orient="records", indent=2)
                print(f"\n✓ Saved to {output_file}")

            elif output_format == "csv":
                output_file = f"{name}.csv"
                df.to_csv(output_file, index=False)
                print(f"\n✓ Saved to {output_file}")

        return result

    except FileNotFoundError:
        print(f"❌ Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":

    rdata_file = r"C:\Users\lukez\gpt-sentiment\gpt-sentiment-mvp\data\part 3\GL_review_PCW\GL_review_PCW.rdata"

    print("=" * 60)
    print("R Data File Reader")
    print("=" * 60)

    # Try to read and convert to JSON
    data = read_rdata_file(rdata_file, output_format="json")

    if data:
        print("\n✓ Successfully read and converted!")
    else:
        print("\n⚠ Make sure the file exists and pyreadr is installed:")
        print("   pip install pyreadr")
