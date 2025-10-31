# love park sentiment analysis

a multi-phase research project analyzing how urban renovation affects public sentiment through review data

see it live → [love-in-the-park.vercel.app](https://love-in-the-park.vercel.app)

---

## project overview

this project explores love park's 2016-2018 renovation impact through sentiment analysis of online reviews. combining gpt-powered text analysis, statistical modeling, and interactive visualization to tell the story of how construction affects urban spaces.

**research contribution to ongoing publication**

---

## project structure

```
gpt-sentiment-mvp/
├── part1-frontend/              # interactive dashboard (DEPLOYED)
│   └── review-analytics-dashboard/
├── part1-python-pipeline/       # sentiment analysis pipeline
│   ├── src/                     # core analysis scripts
│   ├── figures/                 # generated visualizations
│   └── *.py                     # data processing scripts
├── part2-r-analysis/            # statistical modeling (IN PROGRESS)
│   └── read_rdata.py           # R data import tools
└── data/                        # raw & processed data
    ├── part 3/                  # R analysis data
    └── frontend_data.json       # dashboard data
```

---

## phase 1: dashboard + python pipeline ✅

### what we built
- **interactive frontend**: react + typescript dashboard with parallax, animations, graphs
- **sentiment pipeline**: gpt-powered review analysis (google maps, yelp, tripadvisor)
- **data processing**: multi-platform review aggregation and temporal analysis
- **visualizations**: rating trends, volume analysis, before/after comparisons

### tech stack
- **frontend**: react 18, typescript, vite, tailwind css, framer motion, recharts
- **backend**: python 3.12, openai gpt-4, pandas, matplotlib
- **deployment**: vercel (frontend), local (python)

### key findings
- **pre-construction** (before 2016): 3.63 ⭐ average rating
- **during construction** (2016-2018): 3.54 ⭐ (-2.5% drop)
- **post-construction** (2018+): 3.90 ⭐ (+10.2% improvement, +7.4% overall)

---

## phase 2: statistical modeling 🔄

### current focus
working with `GL_review_PCW.rdata` for advanced statistical analysis

### tools
- r programming language
- python (rpy2, pyreadr)
- statistical modeling packages

### goals
- deeper statistical validation
- predictive modeling
- comparative analysis with other urban spaces

---

## quick start

### frontend dashboard
```bash
cd part1-frontend/review-analytics-dashboard
npm install
npm run dev
```
open [localhost:5173](http://localhost:5173)

### python pipeline
```bash
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\activate
pip install -r requirements.txt

# run scripts
cd part1-python-pipeline
python generate_frontend_data.py
```

### r analysis
```bash
cd part2-r-analysis
python read_rdata.py
```

---

## data sources

- **tripadvisor**: 620+ reviews (2011-2018)
- **google maps**: supplementary review data
- **yelp**: cross-platform validation
- **r dataset**: advanced statistical analysis data

---

## credits

**built by**: luke pan  
**supervised by**: khalil martain  
**research under**: dr. daniel silver

---

## project phases

- [x] **phase 1a**: sentiment analysis pipeline (python + gpt)
- [x] **phase 1b**: interactive dashboard (react + typescript)
- [x] **phase 1c**: deployment (vercel)
- [ ] **phase 2a**: statistical modeling (r)
- [ ] **phase 2b**: comparative analysis
- [ ] **phase 3**: integration & insights

---

## demo

live dashboard → [https://love-in-the-park.vercel.app](https://love-in-the-park.vercel.app)

---

## license

research project - contact for usage

---

enjoy the vibes 🌃
