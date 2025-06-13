import pandas as pd
from datetime import datetime

# grab our reviews from the json file
input_file = "raw_reviews.json"  # feel free to change this
df = pd.read_json(input_file)

# toss out any reviews that don't have text
df = df.dropna(subset=["text"])

# fix up those timestamps - they're in unix format (seconds since 1970)
df["date"] = pd.to_datetime(df["datetime"], unit="s", errors="coerce")
df = df.dropna(subset=["date"])  # get rid of any funky dates

# add platform info since it's not in the data
df["platform"] = "google"  # assuming these are google reviews

# just keep the columns we care about
df = df[["date", "platform", "text"]]

# split reviews into our three time periods
# before construction started
pre = df[df["date"] < "2016-02-01"]

# while they were working on it
during = df[(df["date"] >= "2016-02-01") & (df["date"] <= "2018-05-31")]

# after they finished
post = df[df["date"] > "2018-05-31"]

# let's see how many reviews we got in each period
print(f"pre count: {len(pre)}")
print(f"during count: {len(during)}")
print(f"post count: {len(post)}")

# save everything to separate files
pre.to_json("pre.json", orient="records", lines=True)
during.to_json("during.json", orient="records", lines=True)
post.to_json("post.json", orient="records", lines=True)

print("✅ done! files saved: pre.json, during.json, post.json")
