from mvp_sentiment import run_sentiment_pipeline

periods = {
    "pre": ("pre.json", "pre_output.json", "pre_output.csv"),
    "during": ("during.json", "during_output.json", "during_output.csv"),
    "post": ("post.json", "post_output.json", "post_output.csv")
}

for label, (input_file, out_json, out_csv) in periods.items():
    print(f"\n🔁 Running sentiment analysis on {label} period...")
    run_sentiment_pipeline(input_file, out_json, out_csv)
