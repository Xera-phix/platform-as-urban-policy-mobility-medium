

see it live → [love-in-the-park.vercel.app](https://love-in-the-park.vercel.app)

---

## what is this?

an ultra-minimal dashboard exploring how love park's renovation changed how people feel about the space. all real data. all vibes.

---

## what's inside?

- **parallax hero**  
  love park in the background, title up front, smooth scroll
- **animated stats**  
  real ratings before & after construction, counting up as you scroll
- **interactive graphs**  
  see the sentiment shift, review volume, and more
- **before/after slider**  
  drag to compare the park pre- and post-renovation
- **key findings**  
  apple-style, minimal, just the facts
- **share button**  
  tweet, link, or just flex your data
- **methodology**  
  how the analysis was done, in 4 chill steps
- **dark mode**  
  because, obviously

---

## how the data magic happens

- **python sentiment pipeline**  
  all reviews (from tripadvisor, google, yelp) are run through gpt-4 and open-source llms (like mistral & llama 3) to classify each as positive, neutral, or negative. this is done with scripts like `mvp_sentiment.py` and helpers in `/src`.
- **data cleaning & splitting**  
  scripts like `clean_and_split_reviews.py` and `analyze_review_distribution.py` prep the raw data, sort by time period, and handle missing stuff.
- **statistical analysis**  
  pandas + matplotlib for all the stats, boxplots, and period breakdowns. see `tripadvisor_boxwhisker_plot.py`, `tripadvisor_bar.py`, etc.
- **frontend data**  
  `generate_frontend_data.py` and `generate_multiplatform_data.py` crunch the numbers and export everything as json for the dashboard to use.
- **graphs**  
  all the charts you see (timeline, bar, volume) are made in python first, then rendered interactively in the frontend with recharts.

---

## tech stack

- react + typescript
- vite
- tailwind css (custom dark theme)
- framer motion (for all the smooth stuff)
- recharts (for the graphs)
- python (pandas, matplotlib, openai, tqdm)

---

## credits

built by luke pan  
under the direct supervision of khalil martain  
research conducted under dr. daniel silver

---

## try it

[https://love-in-the-park.vercel.app](https://love-in-the-park.vercel.app)

---

## want to run it?

```bash
# backend (python)
pip install -r requirements.txt
python generate_frontend_data.py
# (or run any of the scripts in /src for custom analysis)

# frontend (react)
cd review-analytics-dashboard
npm install
npm run dev
```

open your browser to [localhost:5173](http://localhost:5173)

---

## enjoy the vibes 🌃
