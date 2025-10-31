"""
Convert TripAdvisor Excel data to JSON format.

Converts datetime columns to ISO strings for JSON compatibility. Output uses 'records'
orientation (list of dicts) for easy downstream analysis.
"""

import pandas as pd


def excel_to_json(
    input_file="tripadvisor_jfkplaza.xlsx", output_file="tripadvisor_jfkplaza.json"
):
    """
    Convert Excel file to JSON with datetime serialization.

    Args:
        input_file: Path to Excel file
        output_file: Path to output JSON file
    """
    df = pd.read_excel(input_file)

    for col in ["date_of_experience", "date_written"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    df.to_json(output_file, orient="records", indent=2)
    print(f"✅ Excel file converted to JSON: {output_file}")


if __name__ == "__main__":
    excel_to_json()
