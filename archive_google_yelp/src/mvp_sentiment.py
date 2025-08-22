# mvp_sentiment.py - Analyzes sentiment of reviews using GPT-3.5

import json
import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv

# Load API key from environment
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. Please check your .env file."
    )

MODEL = "gpt-3.5-turbo"
client = OpenAI(api_key=API_KEY)


def classify_sentiment(text: str) -> str:
    """
    Uses GPT-3.5 to analyze the sentiment of a review text.
    Returns 'negative', 'neutral', or 'positive'.
    """
    try:
        prompt = [
            {"role": "system", "content": "You are a sentiment analysis assistant."},
            {
                "role": "user",
                "content": f"Classify the sentiment of the following review as 'negative', 'neutral' or 'positive' and only respond with one word for each review.\n\n"
                f'Review: "{text}"',
            },
        ]

        resp = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.0,
            max_tokens=4,
        )

        return resp.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"Error classifying sentiment: {e}")
        return None


def run_sentiment_pipeline(input_path, output_path_json, output_path_csv):
    """
    Processes a JSON file of reviews, adds sentiment analysis, and saves results
    to both JSON and CSV formats.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for entry in tqdm(data, desc=f"Classifying {os.path.basename(input_path)}"):
            txt = entry.get("text_processed") or entry.get("text")
            if txt:
                entry["sentiment"] = classify_sentiment(txt)
            else:
                entry["sentiment"] = None

            # Ensure Google Maps star rating is included if present
            # If the field is named differently, adjust as needed (e.g., 'rating', 'stars', etc.)
            if "rating" in entry:
                entry["google_maps_star_rating"] = entry["rating"]
            elif "stars" in entry:
                entry["google_maps_star_rating"] = entry["stars"]
            # else: do not add if not present

        with open(output_path_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        df = pd.DataFrame(data)
        # Ensure the google_maps_star_rating column is present in the CSV if available
        if "google_maps_star_rating" not in df.columns:
            # Try to add from rating or stars if present
            if "rating" in df.columns:
                df["google_maps_star_rating"] = df["rating"]
            elif "stars" in df.columns:
                df["google_maps_star_rating"] = df["stars"]
        df.to_csv(output_path_csv, index=False)

        print(f"\n✅ Finished: {output_path_json}")
        print("Sentiment counts:")
        print(df["sentiment"].value_counts(dropna=False))

    except Exception as e:
        print(f"An error occurred: {e}")


# Run on sample file if script is executed directly
if __name__ == "__main__":
    run_sentiment_pipeline(
        "sample.json", "sample_with_sentiment.json", "sample_with_sentiment.csv"
    )
