import pandas as pd
import matplotlib.pyplot as plt

# Load sentiment analysis results from each time period
files = {
    "pre": "pre_output.json",
    "during": "during_output.json", 
    "post": "post_output.json"
}

# Map sentiment labels to numerical scores
sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}

# Process each file and combine into one dataset
dfs = []
for label, path in files.items():
    df = pd.read_json(path)
    df["period"] = label
    df["sentiment_score"] = df["sentiment"].map(sentiment_map)
    df["date"] = pd.to_datetime(df["date"])
    dfs.append(df)

# Combine all periods into single dataframe
full_df = pd.concat(dfs)

# Calculate monthly average sentiment
full_df["month"] = full_df["date"].dt.to_period("M").dt.to_timestamp()
monthly_sentiment = full_df.groupby("month")["sentiment_score"].mean().reset_index()

# Create the plot
plt.figure(figsize=(12, 6))

# Plot sentiment trend line
plt.plot(
    monthly_sentiment["month"], 
    monthly_sentiment["sentiment_score"], 
    marker="o", 
    label="Average Sentiment", 
    color="tab:blue"
)

# Add shaded regions for construction periods
plt.axvspan(
    pd.to_datetime("2015-01-01"), 
    pd.to_datetime("2016-01-31"), 
    color="gray", 
    alpha=0.1, 
    label="Pre-Construction"
)
plt.axvspan(
    pd.to_datetime("2016-02-01"), 
    pd.to_datetime("2018-05-31"), 
    color="orange", 
    alpha=0.1, 
    label="During Construction"
)
plt.axvspan(
    pd.to_datetime("2018-06-01"), 
    pd.to_datetime("2021-12-31"), 
    color="green", 
    alpha=0.1, 
    label="Post-Construction"
)

# Customize plot appearance
plt.title("LOVE Park Sentiment Trend Over Time (Google Reviews)")
plt.xlabel("Date")
plt.ylabel("Average Sentiment Score (-1 to 1)")
plt.ylim(-1.05, 1.05)
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
