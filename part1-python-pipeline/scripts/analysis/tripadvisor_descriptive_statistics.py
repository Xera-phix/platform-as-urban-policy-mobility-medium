import pandas as pd

# === 1. LOAD DATA FROM EXCEL ===
df = pd.read_excel("data/tripadvisor_jfkplaza.xlsx")

total_rows = len(df)

print("\n=== BASIC INFO ===")
print(f"Total reviews: {total_rows}")
print(df.dtypes)

# === 2. DATA COMPLETENESS (counts + percentages) ===
print("\n=== DATA COMPLETENESS ===")
for col in df.columns:
    non_null_count = df[col].notna().sum()
    missing_count = df[col].isna().sum()
    non_null_pct = (non_null_count / total_rows) * 100
    missing_pct = (missing_count / total_rows) * 100
    print(
        f"{col:20} | Present: {non_null_count} ({non_null_pct:.1f}%) | Missing: {missing_count} ({missing_pct:.1f}%)"
    )

# === 3. NUMERIC COLUMN STATS ===
print("\n=== NUMERIC COLUMN STATS ===")
numeric_cols = df.select_dtypes(include=["number"]).columns
print(df[numeric_cols].describe().T)

# === 4. RATING DISTRIBUTION ===
print("\n=== RATING DISTRIBUTION ===")
rating_counts = df["rating"].value_counts().sort_index()
for rating, count in rating_counts.items():
    pct = (count / total_rows) * 100
    print(f"Rating {rating}: {count} reviews ({pct:.1f}%)")

# === 5. DATE RANGES ===
if "date_of_experience" in df.columns:
    df["date_of_experience"] = pd.to_datetime(df["date_of_experience"], errors="coerce")
    print(
        f"\ndate_of_experience: {df['date_of_experience'].min()} → {df['date_of_experience'].max()}"
    )
if "date_written" in df.columns:
    df["date_written"] = pd.to_datetime(df["date_written"], errors="coerce")
    print(f"date_written:      {df['date_written'].min()} → {df['date_written'].max()}")

# === 6. DELAY BETWEEN EXPERIENCE & WRITTEN DATE (in days) ===
if "date_of_experience" in df.columns and "date_written" in df.columns:
    mask = df["date_of_experience"].notna() & df["date_written"].notna()
    delays = (df.loc[mask, "date_written"] - df.loc[mask, "date_of_experience"]).dt.days
    print("\n=== DELAY BETWEEN EXPERIENCE & WRITTEN DATE (days) ===")
    print(delays.describe())

# === 7. OPTIONAL: SAVE CLEANED DATA FOR LATER ===
df.to_json(
    "tripadvisor_jfkplaza_clean.json", orient="records", indent=2, date_format="iso"
)
print("\n✅ Cleaned dataset saved as tripadvisor_jfkplaza_clean.json")
