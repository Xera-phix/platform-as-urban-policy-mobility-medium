import pandas as pd
import matplotlib.pyplot as plt

# === 1. LOAD DATA ===
df = pd.read_excel("tripadvisor_jfkplaza.xlsx")
df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")

# === 2. DEFINE PERIODS ===
start_during = pd.Timestamp("2016-02-01")
end_during = pd.Timestamp("2018-05-31")


def classify_period(date):
    if pd.isna(date):
        return None  # exclude later
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
        return None


df["period"] = df["date_of_experience"].apply(classify_period)

# === 3. FILTER OUT MISSING & BORDERLINE ===
df_filtered = df[
    df["period"].isin(["pre_construction", "during_construction", "post_construction"])
]

# === 4. CREATE BOX & WHISKER PLOT ===
plt.figure(figsize=(8, 6))
df_filtered.boxplot(column="rating", by="period", grid=False)

plt.title("Ratings by Construction Period — JFK Plaza (TripAdvisor)")
plt.suptitle("")  # remove default pandas title
plt.xlabel("Construction Period")
plt.ylabel("Rating")
plt.ylim(0.5, 5.5)
plt.tight_layout()
plt.show()
