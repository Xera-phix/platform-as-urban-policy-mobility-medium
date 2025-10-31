# love park sentiment analysis

a full-stack research project analyzing how urban renovation affects public sentiment through review data

see it live → [love-in-the-park.vercel.app](https://love-in-the-park.vercel.app)

---

## project overview

this project explores love park's 2016-2018 renovation impact through sentiment analysis of online reviews. combining gpt-powered text analysis, postgresql database infrastructure, statistical modeling, and interactive visualization to tell the story of how construction affects urban spaces.

**research contribution to ongoing publication**

---

## tech stack

### frontend
- **react 18** + **typescript** - type-safe component architecture
- **vite** - lightning-fast build tooling
- **tailwind css** - utility-first styling
- **framer motion** - fluid animations and parallax effects
- **recharts** - interactive data visualization
- **vercel** - serverless deployment

### backend & database
- **supabase** - postgresql database with 673 reviews
- **python 3.12** - data processing pipeline
- **openai gpt-4** - sentiment analysis
- **pandas** + **matplotlib** - data transformation & visualization

### infrastructure
- row-level security (rls) policies for data access
- automated database setup scripts
- typescript service layer for type-safe queries
- environment-based configuration

---

## project structure

```
gpt-sentiment-mvp/
├── part1-frontend/              # interactive dashboard (DEPLOYED)
│   └── review-analytics-dashboard/
│       ├── src/
│       │   ├── components/      # react components
│       │   ├── lib/
│       │   │   ├── supabase.ts     # database client
│       │   │   └── reviewService.ts # data queries
│       │   └── App.tsx
│       └── public/
│           └── frontend_data.json  # pre-computed stats
├── part1-python-pipeline/       # sentiment analysis pipeline
│   ├── scripts/
│   │   ├── analysis/            # statistical analysis
│   │   ├── data_processing/     # etl pipelines
│   │   ├── visualization/       # chart generation
│   │   └── database/            # supabase integration
│   │       ├── setup_supabase.py   # db setup & upload
│   │       └── test_supabase.py    # connection testing
│   └── requirements.txt
├── part2-r-analysis/            # statistical modeling (IN PROGRESS)
│   └── read_rdata.py           # R data import tools
└── data/                        # raw & processed data
    ├── tripadvisor_jfkplaza_with_periods.json
    └── frontend_data.json
```

---

## phase 1: full-stack dashboard ✅

### what we built
- **interactive frontend**: parallax hero, animated stats, dynamic graphs
- **database infrastructure**: postgresql with 673 reviews across 3 construction periods
- **sentiment pipeline**: gpt-powered review analysis (tripadvisor primary source)
- **data processing**: temporal classification, rating aggregation, trend analysis
- **deployment**: production-ready with static data optimization

### database schema
```sql
reviews table:
├── id (bigserial, primary key)
├── review_id (text, unique)
├── user_name (text)
├── rating (integer, 1-5)
├── text (text)
├── date_of_experience (timestamp)
├── date_written (timestamp)
├── title (text)
├── helpful_votes (integer)
├── trip_type (text)
├── period (enum: pre/during/post construction)
└── created_at (timestamp)

indexes: period, date_of_experience, rating, user_name
```

### key findings
- **pre-construction** (before feb 2016): 3.63⭐ avg rating (597 reviews)
- **during construction** (mar 2016 - apr 2018): 3.54⭐ (-2.5% drop, 202 reviews)
- **post-construction** (jun 2018+): 3.90⭐ (+10.2% improvement, 229 reviews)
- **overall impact**: +7.4% sentiment improvement from construction period to post-renovation

### architecture highlights
- **database-first design**: postgresql as single source of truth
- **type-safe queries**: typescript interfaces for all database operations
- **performance optimization**: pre-computed aggregations for dashboard speed
- **security**: row-level security policies for public read-only access
- **scalability**: supabase infrastructure ready for multi-platform expansion

---

## quick start

### 1. clone repository
```bash
git clone https://github.com/Xera-phix/gpt-sentiment-mvp.git
cd gpt-sentiment-mvp
```

### 2. database setup (optional)
```bash
# create .env file
echo "SUPABASE_URL=your_project_url" > .env
echo "SUPABASE_KEY=your_anon_key" >> .env

# setup virtual environment
python -m venv .venv
.venv\Scripts\activate  # windows

# install dependencies
pip install -r requirements.txt

# create database tables (run SQL in supabase dashboard)
python part1-python-pipeline/scripts/database/setup_supabase.py

# upload review data
python part1-python-pipeline/scripts/database/setup_supabase.py --upload

# verify connection
python part1-python-pipeline/scripts/database/test_supabase.py
```

### 3. run dashboard
```bash
cd part1-frontend/review-analytics-dashboard
npm install
npm run dev
```
open [localhost:5173](http://localhost:5173)

### 4. run python analysis
```bash
# from project root
cd part1-python-pipeline/scripts

# data processing
python data_processing/excel_to_json.py
python data_processing/export_dashboard_data.py

# analysis
python analysis/descriptive_stats_by_period.py
python analysis/cumulative_reviews.py

# visualization
python visualization/rating_timeline.py
python visualization/rating_boxplot.py
```

---

## api reference

### reviewService.ts functions

```typescript
// get average ratings by construction period
await getRatingsByPeriod()
// returns: [{ period, avgRating, reviews }]

// get quarterly time series data
await getRatingTimeline()
// returns: [{ month, tripadvisorRating, googleRating, yelpRating }]

// get review volume by platform
await getReviewVolumeByPlatform()
// returns: [{ period, tripadvisor, google, yelp }]

// get all dashboard data in one call
await getAllDashboardData()

// get recent reviews
await getRecentReviews(limit: number)

// get total review count
await getTotalReviewCount()
```

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

## environment variables

### backend (.env)
```bash
OPENAI_API_KEY=sk-proj-...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### frontend (.env.local)
```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_KEY=your-anon-key
```

---

## data sources

- **tripadvisor**: 673 reviews (2011-2018) - primary source
- **database**: supabase postgresql with full review text, metadata, and period classifications
- **r dataset**: `GL_review_PCW.rdata` for advanced statistical analysis

### data pipeline
1. **collection**: scraped tripadvisor reviews → excel
2. **processing**: python etl → json with period classifications
3. **storage**: uploaded to supabase postgresql
4. **aggregation**: pre-computed stats → frontend_data.json
5. **visualization**: react dashboard consumes static json

---

## credits

**built by**: luke pan  
**supervised by**: khalil martin  
**research under**: dr. daniel silver

**tech stack**: react • typescript • python • supabase • postgresql • gpt-4 • vercel

---

## project phases

- [x] **phase 1a**: data collection & sentiment analysis pipeline (python + gpt-4)
- [x] **phase 1b**: database infrastructure (supabase postgresql)
- [x] **phase 1c**: interactive dashboard (react + typescript)
- [x] **phase 1d**: deployment & optimization (vercel)
- [ ] **phase 2a**: statistical modeling (r programming)
- [ ] **phase 2b**: comparative analysis with other urban spaces
- [ ] **phase 3a**: live database integration
- [ ] **phase 3b**: multi-platform expansion (google maps, yelp)
- [ ] **phase 3c**: predictive modeling & insights

---

## features

### dashboard
- ✅ parallax hero with animated title
- ✅ real-time counter animations
- ✅ interactive recharts visualizations
- ✅ before/after comparison slider
- ✅ dark/light mode toggle
- ✅ responsive design (mobile-first)
- ✅ 3d graph toggle
- ✅ social share functionality

### backend
- ✅ postgresql database with 673 reviews
- ✅ automated setup & upload scripts
- ✅ type-safe typescript service layer
- ✅ rls security policies
- ✅ indexed queries for performance
- ✅ period classification system
- ✅ data validation & error handling

---

## demo

**live dashboard** → [https://love-in-the-park.vercel.app](https://love-in-the-park.vercel.app)

---

## contributing

this is a research project. contact for collaboration opportunities.

---

## license

research project - contact for usage

---

*analyzing urban spaces, one review at a time* 🌃✨

