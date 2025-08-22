import pandas as pd

# load JSON
df = pd.read_json("data/tripadvisor_jfkplaza.json")

# ensure datetime
df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")

# define boundaries
start_during = pd.Timestamp("2016-02-01")
end_during = pd.Timestamp("2018-05-31")


# classify period
def classify_period(date):
    if pd.isna(date):
        return "missing_date"
    if date.month == 2 and date.year == 2016:
        return "border_feb2016"
    if date.month == 5 and date.year == 2018:
        return "border_may2018"
    if date < start_during:
        return "pre_construction"
    elif start_during < date < end_during:
        return "during_construction"
    elif date > end_during:
        return "post_construction"
    else:
        return "unclassified"


df["period"] = df["date_of_experience"].apply(classify_period)

# summary counts & percentages
total_reviews = len(df)
period_summary = (
    df["period"].value_counts().rename_axis("period").reset_index(name="count")
)
period_summary["percent"] = (period_summary["count"] / total_reviews * 100).round(1)

print("\n=== REVIEW COUNTS BY PERIOD ===")
print(period_summary)

# rating stats per period
print("\n=== RATING STATS PER PERIOD ===")
print(df.groupby("period")["rating"].describe())

# optional: save segmented dataset
df.to_json("tripadvisor_jfkplaza_with_periods.json", orient="records", indent=2)
print("\n✅ Saved segmented dataset as tripadvisor_jfkplaza_with_periods.json")
