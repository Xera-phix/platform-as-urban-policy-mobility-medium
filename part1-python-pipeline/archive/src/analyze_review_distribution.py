import pandas as pd
from datetime import datetime

# load up our reviews
df = pd.read_json("raw_reviews.json")

# convert those unix timestamps to actual dates
df["date"] = pd.to_datetime(df["datetime"], unit="s", errors="coerce")
df = df.dropna(subset=["date"])

# count reviews for each construction phase
# before construction started
pre_count = len(df[df["date"] < "2016-02-01"])

# while they were working on it
during_count = len(df[(df["date"] >= "2016-02-01") & (df["date"] <= "2018-05-31")])

# after they finished
post_count = len(df[df["date"] > "2018-05-31"])

# show us what we got
total = len(df)

print(f"📊 Total reviews with valid date: {total}")
print(f"🟦 Pre-Construction (before 2016-02): {pre_count}")
print(f"🟧 During Construction (2016-02 to 2018-05): {during_count}")
print(f"🟩 Post-Construction (after 2018-05): {post_count}")
