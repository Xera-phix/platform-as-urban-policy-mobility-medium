import pandas as pd
import matplotlib.pyplot as plt

# load JSON with periods (or run classification here if not saved yet)
df = pd.read_json("tripadvisor_jfkplaza.json")
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

# count per period
period_counts = (
    df["period"]
    .value_counts()
    .reindex(
        [
            "pre_construction",
            "border_feb2016",
            "during_construction",
            "border_may2018",
            "post_construction",
            "missing_date",
        ]
    )
    .dropna()
)

# plot bar chart
plt.figure(figsize=(8, 6))
period_counts.plot(kind="bar", color="skyblue", edgecolor="black")

plt.title("Total Reviews by Period — JFK Plaza (TripAdvisor)", fontsize=14)
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
