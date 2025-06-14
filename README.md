# GPT-Enabled Sentiment Analysis for Urban Policy Feedback

This project implements an end-to-end sentiment analysis pipeline using GPT-4 and open-source large language models (Mistral, LLaMA 3) to evaluate public feedback on urban policy changes. It was developed to assist the City of Philadelphia's Department of Urban Planning in interpreting public responses to the redesign of JFK Plaza (LOVE Park).

## 🧠 Key Features

- **Multi-model sentiment classification:** Classifies feedback using GPT-4 and benchmarked open-source LLMs.
- **Custom labeling schema:** Applies a task-specific sentiment rubric aligned with civic planning goals.
- **Interactive visualization:** Generates temporal trends and statistical insights for public sentiment over time.
- **Cost-aware evaluation:** Benchmarks inference cost, latency, and accuracy for each model.
- **Lightweight pipeline:** Scripted for simple local or cloud deployment with minimal dependencies.

## 📊 Example Use Case

Analyze public feedback from surveys, Twitter, or review platforms (e.g., Yelp) regarding:
- Park redesign reception
- Skateboarding policy controversies
- New art installations (e.g., the Portal)
- Civic engagement trends over time

## 📁 Project Structure

```bash
gpt-sentiment-mvp/
├── data/
│   ├── input.json             # Raw feedback data
│   └── labels.json            # Ground truth for evaluation
├── graphs/
│   └── sentiment_trends.png   # Auto-generated visualizations
├── src/
│   ├── mvp_sentiment.py       # Main analysis pipeline
│   ├── utils.py               # Preprocessing and helpers
├── .env                       # Your OpenAI API key
├── README.md                  # You're here
