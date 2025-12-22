"""
Histograms of reviewer activity:
1. Number of review locations (brewpubs) per reviewer
2. Number of review municipalities per reviewer
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)
INPUT_PATH = OUTPUT_DIR / "reviewer_tally.csv"


def main():
    print("=" * 60)
    print("Generating Reviewer Activity Histograms")
    print("=" * 60)

    # Load reviewer tally data
    print("\nLoading reviewer tally data...")
    df = pd.read_csv(INPUT_PATH)
    print(f"  Loaded {len(df):,} reviewers")

    # Create figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # ========== Histogram 1: Number of Reviews (Locations) ==========
    ax1 = axes[0]

    # Cap at 20 for visualization (group 20+ together)
    reviews_capped = df["num_reviews"].clip(upper=20)

    ax1.hist(
        reviews_capped,
        bins=range(1, 23),
        edgecolor="black",
        alpha=0.7,
        color="steelblue",
    )
    ax1.set_xlabel("Number of Reviews per Reviewer", fontsize=11)
    ax1.set_ylabel("Number of Reviewers", fontsize=11)
    ax1.set_title(
        "Distribution of Review Counts per Reviewer", fontsize=12, fontweight="bold"
    )
    ax1.set_xticks(range(1, 22))
    ax1.set_xticklabels([str(i) if i < 20 else "20+" for i in range(1, 22)])

    # Add summary stats
    mean_reviews = df["num_reviews"].mean()
    median_reviews = df["num_reviews"].median()
    ax1.axvline(
        mean_reviews,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {mean_reviews:.1f}",
    )
    ax1.axvline(
        median_reviews,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Median: {median_reviews:.0f}",
    )
    ax1.legend()

    # Add count annotations for first few bars
    counts = reviews_capped.value_counts().sort_index()
    for i in range(1, min(6, len(counts) + 1)):
        if i in counts.index:
            ax1.annotate(
                f"{counts[i]:,}",
                xy=(i, counts[i]),
                ha="center",
                va="bottom",
                fontsize=8,
            )

    # ========== Histogram 2: Number of Unique Municipalities ==========
    ax2 = axes[1]

    # Cap at 15 for visualization
    municipalities_capped = df["unique_municipalities"].clip(upper=15)

    ax2.hist(
        municipalities_capped,
        bins=range(1, 18),
        edgecolor="black",
        alpha=0.7,
        color="forestgreen",
    )
    ax2.set_xlabel("Number of Unique Municipalities per Reviewer", fontsize=11)
    ax2.set_ylabel("Number of Reviewers", fontsize=11)
    ax2.set_title(
        "Distribution of Municipality Coverage per Reviewer",
        fontsize=12,
        fontweight="bold",
    )
    ax2.set_xticks(range(1, 17))
    ax2.set_xticklabels([str(i) if i < 15 else "15+" for i in range(1, 17)])

    # Add summary stats
    mean_muni = df["unique_municipalities"].mean()
    median_muni = df["unique_municipalities"].median()
    ax2.axvline(
        mean_muni,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {mean_muni:.2f}",
    )
    ax2.axvline(
        median_muni,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Median: {median_muni:.0f}",
    )
    ax2.legend()

    # Add count annotations for first few bars
    counts_muni = municipalities_capped.value_counts().sort_index()
    for i in range(1, min(6, len(counts_muni) + 1)):
        if i in counts_muni.index:
            ax2.annotate(
                f"{counts_muni[i]:,}",
                xy=(i, counts_muni[i]),
                ha="center",
                va="bottom",
                fontsize=8,
            )

    plt.tight_layout()

    # Save figure
    output_path = FIGURES_DIR / "reviewer_histograms.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"\nSaved: {output_path}")

    # Also save individual figures
    # Figure 1: Reviews histogram
    fig1, ax1_single = plt.subplots(figsize=(10, 6))
    ax1_single.hist(
        reviews_capped,
        bins=range(1, 23),
        edgecolor="black",
        alpha=0.7,
        color="steelblue",
    )
    ax1_single.set_xlabel("Number of Reviews per Reviewer", fontsize=12)
    ax1_single.set_ylabel("Number of Reviewers", fontsize=12)
    ax1_single.set_title(
        "Distribution of Review Counts per Reviewer\n(Pennsylvania Brewpubs)",
        fontsize=13,
        fontweight="bold",
    )
    ax1_single.set_xticks(range(1, 22))
    ax1_single.set_xticklabels([str(i) if i < 20 else "20+" for i in range(1, 22)])
    ax1_single.axvline(
        mean_reviews,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {mean_reviews:.1f}",
    )
    ax1_single.axvline(
        median_reviews,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Median: {median_reviews:.0f}",
    )
    ax1_single.legend()

    output_path1 = FIGURES_DIR / "histogram_review_counts.png"
    plt.savefig(output_path1, dpi=150, bbox_inches="tight")
    print(f"Saved: {output_path1}")
    plt.close(fig1)

    # Figure 2: Municipalities histogram
    fig2, ax2_single = plt.subplots(figsize=(10, 6))
    ax2_single.hist(
        municipalities_capped,
        bins=range(1, 18),
        edgecolor="black",
        alpha=0.7,
        color="forestgreen",
    )
    ax2_single.set_xlabel("Number of Unique Municipalities per Reviewer", fontsize=12)
    ax2_single.set_ylabel("Number of Reviewers", fontsize=12)
    ax2_single.set_title(
        "Distribution of Municipality Coverage per Reviewer\n(Pennsylvania Brewpubs)",
        fontsize=13,
        fontweight="bold",
    )
    ax2_single.set_xticks(range(1, 17))
    ax2_single.set_xticklabels([str(i) if i < 15 else "15+" for i in range(1, 17)])
    ax2_single.axvline(
        mean_muni,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {mean_muni:.2f}",
    )
    ax2_single.axvline(
        median_muni,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Median: {median_muni:.0f}",
    )
    ax2_single.legend()

    output_path2 = FIGURES_DIR / "histogram_municipalities.png"
    plt.savefig(output_path2, dpi=150, bbox_inches="tight")
    print(f"Saved: {output_path2}")
    plt.close(fig2)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    print("\nReview Counts:")
    print(f"  Mean:   {df['num_reviews'].mean():.2f}")
    print(f"  Median: {df['num_reviews'].median():.0f}")
    print(f"  Max:    {df['num_reviews'].max()}")
    print(f"  Std:    {df['num_reviews'].std():.2f}")

    print("\nMunicipality Counts:")
    print(f"  Mean:   {df['unique_municipalities'].mean():.2f}")
    print(f"  Median: {df['unique_municipalities'].median():.0f}")
    print(f"  Max:    {df['unique_municipalities'].max()}")
    print(f"  Std:    {df['unique_municipalities'].std():.2f}")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
