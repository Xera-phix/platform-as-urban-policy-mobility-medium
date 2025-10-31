"""
Generate cumulative review visualizations by construction period.

Creates boxplot and stacked bar charts showing rating distribution across pre-construction,
during-construction, and post-construction periods. Excludes border months (Feb 2016, May 2018)
where construction timeline is uncertain.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ═══ Data Preparation ═══
df = pd.read_excel("data/tripadvisor_jfkplaza.xlsx")
df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

df = df.dropna(subset=["date_of_experience", "rating"]).copy()
df = df[(df["rating"] >= 1) & (df["rating"] <= 5)].copy()

# Exclude border months where exact construction dates are uncertain
border = (
    (df["date_of_experience"].dt.year == 2016)
    & (df["date_of_experience"].dt.month == 2)
) | (
    (df["date_of_experience"].dt.year == 2018)
    & (df["date_of_experience"].dt.month == 5)
)
df = df.loc[~border].copy()

# Love Park construction timeline
pre_end = pd.Timestamp("2016-02-01")
during_lo = pd.Timestamp("2016-03-01")
during_hi = pd.Timestamp("2018-04-30")
post_start = pd.Timestamp("2018-06-01")


def period_of(dt):
    """Classify date into construction period"""
    if dt < pre_end:
        return "pre"
    if during_lo <= dt <= during_hi:
        return "during"
    if dt >= post_start:
        return "post"
    return np.nan


df["period"] = df["date_of_experience"].apply(period_of)
order = ["pre", "during", "post"]
df = df[df["period"].isin(order)].copy()
df["period"] = pd.Categorical(df["period"], categories=order, ordered=True)

# ═══ Summary Statistics ═══
summary = (
    df.groupby("period", observed=True)["rating"]
    .agg(
        count="count",
        mean="mean",
        std="std",
        q25=lambda s: s.quantile(0.25),
        median="median",
        q75=lambda s: s.quantile(0.75),
    )
    .reindex(order)
)
print("\n=== Ratings by Period ===")
print(summary.round(3))

# ═══ Boxplot Visualization ═══
# Notched boxes show confidence interval for median
# 5-95% whiskers avoid always showing 1 and 5 as outliers
fig = plt.figure(figsize=(9, 6))
data = [df.loc[df["period"] == p, "rating"].to_numpy() for p in order]
labels = [f"{p.title()} (n={len(arr)})" for p, arr in zip(order, data)]
positions = np.arange(1, len(order) + 1)

bp = plt.boxplot(
    data,
    positions=positions,
    labels=labels,
    notch=True,
    whis=(5, 95),
    showmeans=False,
    manage_ticks=False,
)

means = [arr.mean() for arr in data]
plt.plot(positions, means, marker="o", linestyle="None")

# Jittered points show distribution density
rng = np.random.default_rng(42)
for i, arr in enumerate(data, start=1):
    x = rng.normal(loc=i, scale=0.03, size=len(arr))
    plt.plot(x, arr, marker=".", linestyle="None", alpha=0.25)

plt.title("JFK Plaza (TripAdvisor) — Ratings by Period (Notched Box; 5–95% whiskers)")
plt.ylabel("Rating (1–5)")
plt.ylim(0.8, 5.2)
plt.grid(True, axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("boxplot_ratings_pre_during_post_fixed.png", dpi=200)
plt.show()

# ═══ Rating Distribution Chart ═══
tab = (
    df.pivot_table(
        index="period", columns="rating", values="user_name", aggfunc="count"
    )
    .reindex(order)
    .fillna(0)
)
prop = tab.div(tab.sum(axis=1), axis=0)

ax = prop.plot(kind="bar", stacked=True, figsize=(9, 6))
ax.set_title("Rating Distribution by Period (Proportions)")
ax.set_ylabel("Proportion")
ax.set_xlabel("")
plt.legend(title="Rating", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("stacked_props_ratings_by_period.png", dpi=200)
plt.show()
