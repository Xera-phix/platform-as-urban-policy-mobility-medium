# mvp_sentiment.py

import json
import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv

# load env
load_dotenv()

# basic config
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

MODEL = "gpt-3.5-turbo"

client = OpenAI(api_key=API_KEY)

INPUT_FILE = "sample.json"
OUTPUT_JSON = "sample_with_sentiment.json"
OUTPUT_CSV = "sample_with_sentiment.csv"

# helper to call gpt and classify for one snippet
def classify_sentiment(text: str) -> str:
    """
    returns the sentiment of the text as "negative, neutral, positive"
    """
    try:
        prompt = [
            {"role": "system", "content": "You are a sentiment analysis assistant."},
            {"role": "user", "content":
                f"Classify the sentiment of the following review as 'negative', 'neutral' or 'positive' and only respond with one word for each review.\n\n"
                f"Review: \"{text}\""}
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

# main
def main():
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file {INPUT_FILE} not found")

    try:
        # load JSON
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # run sentiment on entries that have text
        for entry in tqdm(data, desc="Classifying"):
            txt = entry.get("text_processed") or entry.get("text")
            if txt:
                entry["sentiment"] = classify_sentiment(txt)
            else:
                entry["sentiment"] = None

        # save out
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # also make a quick CSV and summary
        df = pd.DataFrame(data)
        df.to_csv(OUTPUT_CSV, index=False)
        print("\nSentiment counts:")
        print(df["sentiment"].value_counts(dropna=False))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


