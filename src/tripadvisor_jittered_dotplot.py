import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load TripAdvisor data (adjust path as needed)
df = pd.read_json("data/tripadvisor_jfkplaza.json")

# Ensure date and rating columns are correct
df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
df = df.dropna(subset=["date_of_experience", "rating"])


# --- Define construction periods ---
pre_end = pd.Timestamp("2016-02-01")
during_lo = pd.Timestamp("2016-03-01")
during_hi = pd.Timestamp("2018-04-30")
post_start = pd.Timestamp("2018-06-01")


def period_of(dt):
    if dt < pre_end:
        return "pre"
    if during_lo <= dt <= during_hi:
        return "during"
    if dt >= post_start:
        return "post"
    return np.nan


df["period"] = df["date_of_experience"].apply(period_of)
order = ["pre", "during", "post"]
df = df[df["period"].isin(order)]
df["period"] = pd.Categorical(df["period"], categories=order, ordered=True)

# --- Plot ---
plt.figure(figsize=(12, 6))
rng = np.random.default_rng(42)

# Shade periods
date_min = df["date_of_experience"].min()
date_max = df["date_of_experience"].max()
plt.axvspan(date_min, pre_end, color="#b3c6f7", alpha=0.22, label="Pre-construction")
plt.axvspan(
    during_lo, during_hi, color="#ffe0b2", alpha=0.22, label="During construction"
)
plt.axvspan(
    post_start, date_max, color="#c8e6c9", alpha=0.22, label="Post-construction"
)

# Jittered dot plot by period
for period, color in zip(order, ["#1a73e8", "#fbbc04", "#34a853"]):
    group = df[df["period"] == period]
    # Jitter x by a few days for visibility
    x = group["date_of_experience"] + pd.to_timedelta(
        rng.normal(0, 10, size=len(group)), unit="D"
    )
    plt.plot(
        x,
        group["rating"],
        ".",
        alpha=0.35,
        label=f"{period.title()} (n={len(group)})",
        color=color,
    )

plt.yticks([1, 2, 3, 4, 5])
plt.ylim(0.8, 5.2)
plt.xlabel("Year")
plt.ylabel("Star Rating")
plt.title("Jittered Dot Plot of TripAdvisor Star Ratings by Construction Period")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.legend(loc="lower left", fontsize=11, frameon=True)
plt.tight_layout()
plt.savefig("jittered_dotplot_ratings_by_period.png", dpi=200)
plt.show()
