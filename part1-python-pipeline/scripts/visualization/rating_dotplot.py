"""
Generate jittered dot plot of ratings over time by construction period.

Shows individual review ratings as dots over time with period-based color coding.
Background shading indicates construction phases. Jitter adds small random offset
to x-axis to prevent overlapping points at same date.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_rating_dotplot(
    input_file="data/tripadvisor_jfkplaza.json",
    output_file="jittered_dotplot_ratings_by_period.png",
):
    """
    Create jittered dot plot visualization of ratings over time.

    Args:
        input_file: Path to reviews JSON file
        output_file: Path to save output PNG
    """
    df = pd.read_json(input_file)
    df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
    df = df.dropna(subset=["date_of_experience", "rating"])

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
    df = df[df["period"].isin(order)]
    df["period"] = pd.Categorical(df["period"], categories=order, ordered=True)

    plt.figure(figsize=(12, 6))
    rng = np.random.default_rng(42)

    date_min = df["date_of_experience"].min()
    date_max = df["date_of_experience"].max()
    plt.axvspan(
        date_min, pre_end, color="#b3c6f7", alpha=0.22, label="Pre-construction"
    )
    plt.axvspan(
        during_lo, during_hi, color="#ffe0b2", alpha=0.22, label="During construction"
    )
    plt.axvspan(
        post_start, date_max, color="#c8e6c9", alpha=0.22, label="Post-construction"
    )

    for period, color in zip(order, ["#1a73e8", "#fbbc04", "#34a853"]):
        group = df[df["period"] == period]
        # Add random jitter to prevent point overlap
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
    plt.savefig(output_file, dpi=200)
    plt.show()


if __name__ == "__main__":
    generate_rating_dotplot()
