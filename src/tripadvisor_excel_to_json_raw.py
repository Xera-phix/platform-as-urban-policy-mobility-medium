import pandas as pd

# read excel
df = pd.read_excel("tripadvisor_jfkplaza.xlsx")

# optional: convert datetime columns to ISO strings for JSON compatibility
for col in ["date_of_experience", "date_written"]:
    if col in df.columns:
        df[col] = df[col].astype(str)

# export to json (records = list of dicts, good for analysis later)
df.to_json("tripadvisor_jfkplaza.json", orient="records", indent=2)

print("✅ Excel file converted to JSON: tripadvisor_jfkplaza.json")
