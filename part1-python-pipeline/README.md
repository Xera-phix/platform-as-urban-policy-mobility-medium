# part 1: python sentiment analysis pipeline

gpt-powered sentiment analysis of love park reviews across multiple platforms

---

## directory structure

```
part1-python-pipeline/
├── scripts/
│   ├── analysis/               # statistical analysis
│   │   ├── tripadvisor_descriptive_statistics.py
│   │   ├── tripadvisor_descriptive_statistics_SPLIT.py
│   │   ├── tripadvisor_user_stats.py
│   │   ├── tripadvisor_user_stats_table.py
│   │   ├── tripadvisor_cumulative_reviews_over_time.py
│   │   └── user_stats_by_platform.py
│   ├── visualization/          # plotting & charts
│   │   ├── plot_rating_time.py
│   │   ├── tripadvisor_bar.py
│   │   ├── tripadvisor_boxwhisker_plot.py
│   │   └── tripadvisor_jittered_dotplot.py
│   └── data_processing/        # data transformation
│       ├── generate_frontend_data.py
│       ├── generate_multiplatform_data.py
│       └── tripadvisor_excel_to_json_raw.py
├── outputs/
│   ├── figures/                # generated charts
│   └── data/                   # processed data files
├── archive/                    # old scripts & experiments
└── README.md
```

---

## what's in each folder

### `scripts/analysis/`
statistical analysis and descriptive statistics
- calculate rating distributions
- user engagement metrics
- temporal trends analysis
- cross-platform comparisons

### `scripts/visualization/`
chart generation and plotting
- time series plots
- bar charts & distributions
- box-and-whisker plots
- jittered scatter plots

### `scripts/data_processing/`
data transformation and export
- convert raw excel/csv to json
- aggregate multi-platform data
- generate frontend dashboard data
- clean and normalize reviews

### `outputs/`
generated files (not tracked in git)
- `figures/` - png charts and visualizations
- `data/` - processed json/csv files

### `archive/`
historical scripts and experiments
- old google/yelp analysis
- deprecated plotting methods
- experimental features

---

## quick start

```bash
# from project root
cd part1-python-pipeline

# install dependencies
pip install -r ../requirements.txt

# set up environment
cp ../.env.example ../.env
# add your OPENAI_API_KEY to .env
```

---

## common workflows

### generate frontend data
```bash
python scripts/data_processing/generate_frontend_data.py
```

### create visualizations
```bash
python scripts/visualization/tripadvisor_bar.py
python scripts/visualization/plot_rating_time.py
```

### run statistical analysis
```bash
python scripts/analysis/tripadvisor_descriptive_statistics.py
python scripts/analysis/user_stats_by_platform.py
```

### process raw data
```bash
python scripts/data_processing/tripadvisor_excel_to_json_raw.py
python scripts/data_processing/generate_multiplatform_data.py
```

---

## tech stack

- **python 3.12**
- **openai gpt-4 api** - sentiment classification
- **pandas** - data manipulation
- **matplotlib** - visualizations
- **numpy** - statistical computations
- **json** - data serialization

---

## key findings

- **pre-construction** (before 2016): 3.63⭐ (338 reviews)
- **during construction** (2016-2018): 3.54⭐ (114 reviews, -2.5%)
- **post-construction** (2018+): 3.90⭐ (156 reviews, +10.2%, +7.4% overall)

---

## contributing

when adding new scripts:
- place in appropriate subfolder (`analysis`, `visualization`, `data_processing`)
- add docstrings explaining purpose
- use consistent naming: `{platform}_{function}_{type}.py`
- save outputs to `outputs/` folder
- update this README
