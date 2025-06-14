# gpt-sentiment-mvp

a lightweight tool for analyzing public sentiment on urban design changes — built with gpt-4 and open-source llms (like mistral & llama 3). this project was made to help city planners understand how people really feel about places like jfk plaza (love park) in philadelphia.

## what it does

- runs public feedback through gpt models to classify sentiment (positive, neutral, negative)
- benchmarks cost, speed, and performance across models (open-source vs. api-based)
- visualizes trends over time (bar charts, line graphs, boxplots, etc.)
- saves city teams hours of manual reading & tagging

## why it matters

urban planning teams often collect tons of public input — but reading thousands of comments is slow, expensive, and subjective. this project automates that process while staying flexible enough to be reused on new datasets, different parks, and future civic projects.

## how it works

```bash
gpt-sentiment-mvp/
├── data/              # your input files go here (json format)
├── graphs/            # output graphs are saved here
├── src/               # main script & helpers
│   └── mvp_sentiment.py
├── .env               # store your api key here
├── README.md
