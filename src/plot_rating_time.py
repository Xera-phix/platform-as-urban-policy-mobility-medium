#!/usr/bin/env python3
# plot_ratings_time.py
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser(
        description="Plot star rating over time from cleaned TripAdvisor JSON."
    )
    ap.add_argument(
        "json",
        nargs="?",
        default="data/tripadvisor_jfkplaza.json",
        help="input JSON file (default: data/tripadvisor_jfkplaza.json)",
    )
    ap.add_argument(
        "--out",
        default="rating_over_time.png",
        help="Output PNG path [default: %(default)s]",
    )
    ap.add_argument(
        "--window",
        type=int,
        default=3,
        help="Rolling window in months [default: %(default)s]",
    )
    args = ap.parse_args()

    df = pd.read_json(args.json)
    # Ensure datetime and drop any rows without experience dates or ratings (should be clean already)
    df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
    df = df.dropna(subset=["date_of_experience", "rating"])

    # Aggregate to monthly
    monthly = (
        df.set_index("date_of_experience")
        .sort_index()
        .resample("MS")
        .agg(
            avg_rating=("rating", "mean"),
            median_rating=("rating", "median"),
            n_reviews=("rating", "count"),
        )
        .dropna(subset=["avg_rating"])
    )
    # Rolling average for smoothing
    monthly["avg_rating_roll"] = (
        monthly["avg_rating"].rolling(args.window, min_periods=1).mean()
    )

    # ---- PLOT ----
    plt.figure(figsize=(11, 6))
    ax1 = plt.gca()

    # Bars: review counts (secondary axis)
    ax2 = ax1.twinx()
    ax2.bar(monthly.index, monthly["n_reviews"], width=25, alpha=0.25, align="center")
    ax2.set_ylabel("reviews / month", labelpad=10)
    ax2.margins(x=0)

    # Lines: average rating + rolling average
    ax1.plot(monthly.index, monthly["avg_rating"], marker="o", linewidth=1, alpha=0.6)
    ax1.plot(monthly.index, monthly["avg_rating_roll"], linewidth=2)

    # Shade construction periods
    pre_end = pd.Timestamp("2016-02-01")
    during_lo = pd.Timestamp("2016-03-01")
    during_hi = pd.Timestamp("2018-04-30")
    post_start = pd.Timestamp("2018-06-01")
    date_min = monthly.index.min()
    date_max = monthly.index.max()
    pre = ax1.axvspan(
        date_min, pre_end, color="#b3c6f7", alpha=0.22, label="Pre-construction"
    )
    during = ax1.axvspan(
        during_lo, during_hi, color="#ffe0b2", alpha=0.22, label="During construction"
    )
    post = ax1.axvspan(
        post_start, date_max, color="#c8e6c9", alpha=0.22, label="Post-construction"
    )

    # Labels and cosmetics
    ax1.set_title(
        "JFK Plaza (LOVE Park) — Star Rating Over Time (by Date of Experience)"
    )
    ax1.set_xlabel("year")
    ax1.set_ylabel("average star rating")
    ax1.set_ylim(1, 5)  # TripAdvisor stars
    ax1.grid(True, which="both", axis="both", alpha=0.25)

    # Legend (combine lines and shaded regions)
    lines = ax1.get_lines()
    labels = ["monthly avg", f"{args.window}-month rolling avg"]
    handles = list(lines) + [pre, during, post]
    labels += ["Pre-construction", "During construction", "Post-construction"]
    ax1.legend(handles, labels, loc="upper right")

    # Tight layout & save
    plt.tight_layout()
    out_path = Path(args.out)
    plt.savefig(out_path, dpi=180)
    print(f"saved -> {out_path.resolve()}")


if __name__ == "__main__":
    pd.set_option("display.max_columns", 50)
    main()
