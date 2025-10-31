# Part 2: Pennsylvania Google Local Reviews Analysis

Large-scale analysis of Google Local review patterns across Pennsylvania.

---

## Overview

This phase analyzes **21.9 million reviews** from the Pennsylvania Google Local dataset to understand user behavior patterns, location review distribution, and engagement metrics across the state.

---

## Dataset

**Source**: Google Local Reviews - Pennsylvania  
**Location**: `data/part 3/review-Pennsylvania.json/review-Pennsylvania.json`  
**Format**: JSONL (one JSON object per line)

### Dataset Statistics
- **Total Reviews**: 21,944,802
- **Unique Users**: 4,957,916
- **Unique Locations**: 189,836 (identified by gmap_id)
- **Time Period**: Historical Google Local reviews
- **Coverage**: Pennsylvania state-wide

### Data Schema
```json
{
  "user_id": "102412752646300974692",
  "name": "Jennifer Cordón",
  "time": 1630529977304,
  "rating": 5,
  "text": "Review text here...",
  "pics": null,
  "resp": null,
  "gmap_id": "0x89c46d5e4554eae1:0xa2f8b211524ca29a"
}
```

---

## Analysis Scripts

### `analyze_user_locations.py`

Generates user-location summary with review distribution statistics.

**What it does:**
1. Loads 21.9M reviews efficiently (line-by-line JSON parsing)
2. Identifies unique locations via `gmap_id`
3. Counts reviews per user per location
4. Creates user-location matrix for top N most-reviewed locations
5. Outputs CSV with user review patterns

**Memory Optimization:**
- Filters to top N locations BEFORE pivoting
- Avoids creating 4.96M × 189K matrix (would require 877 GB RAM)
- Reduces to manageable size (~50K records for top 5 locations)

**Output:** `data/pennsylvania_user_location_summary.csv` (213 MB)

---

## Quick Start

### Prerequisites
```bash
# From project root
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install pandas tqdm
```

### Run Analysis
```bash
python part2-pennsylvania-analysis/scripts/analyze_user_locations.py
```

---

## Key Findings

### User Behavior Patterns
- **58.3%** of users (2.89M) reviewed only **1 location**
- **41.7%** of users (2.07M) reviewed **2+ locations**
- **Most active user** reviewed **1,036 different locations**

### Review Distribution
- **Top 5 locations** each have ~10,000 reviews
- **Long tail distribution**: 189K locations total
- **Power users**: Small percentage of users contribute disproportionate number of reviews

### Engagement Metrics
- **Average reviews per user**: 4.4 reviews
- **Median reviews per user**: 2 reviews (indicating right-skewed distribution)
- **Location diversity**: 41.7% of users explore multiple locations

---

## Output Format

### `pennsylvania_user_location_summary.csv`

| user_id | no_of_review_locations | loc_f269c5fe | loc_7ac02319 | loc_131aa372 | loc_dc1d6b01 | loc_abb449fa |
|---------|------------------------|--------------|--------------|--------------|--------------|--------------|
| 113789... | 179 | 1 | 1 | 2 | 0 | 2 |
| 106817... | 482 | 1 | 1 | 1 | 0 | 1 |
| 101908... | 278 | 1 | 1 | 0 | 0 | 2 |

**Columns:**
- `user_id`: Unique Google user identifier
- `no_of_review_locations`: Total unique locations reviewed by user
- `loc_*`: Review count at each of top 5 most-reviewed locations

**Sorting:** Users sorted by total review activity (descending)

---

## Technical Details

### Memory-Efficient Processing

**Problem:**  
Creating full user-location matrix would require:
- 4,957,916 users × 189,836 locations = 941,190,941,776 cells
- ~877 GB memory allocation (impossible on most systems)

**Solution:**
1. Compute location totals first (lightweight groupby)
2. Identify top N locations (e.g., top 5)
3. Filter user-location pairs to only top N locations
4. Pivot the reduced dataset (50K records vs 941B)
5. Result: Memory usage drops from 877 GB → ~5 MB

### Performance
- **Load time**: ~5 minutes (22M records)
- **Processing time**: ~3 minutes (groupby, filter, pivot)
- **Total runtime**: ~8 minutes
- **Peak memory**: ~8 GB

---

## Future Work

### Phase 2A: Location Clustering
- Geographic clustering of gmap_id coordinates
- City-level aggregation (extract from gmap_id)
- Regional analysis (Philadelphia, Pittsburgh, etc.)

### Phase 2B: Temporal Analysis
- Review activity over time (using `time` field)
- Seasonal patterns in review behavior
- User lifecycle analysis (new vs returning reviewers)

### Phase 2C: Sentiment Analysis
- Apply GPT-4 sentiment analysis to `text` field
- Compare with `rating` field (star rating)
- Identify sentiment-rating discrepancies

### Phase 2D: Cross-Platform Comparison
- Compare with Part 1 TripAdvisor data
- Multi-platform user identification
- Review quality analysis across platforms

---

## Integration with Other Phases

### Part 1: Love Park TripAdvisor Analysis
- **Scale difference**: 673 reviews (Part 1) vs 21.9M reviews (Part 2)
- **Focus**: Single location detailed analysis vs state-wide patterns
- **Methods**: GPT sentiment + period classification vs user behavior patterns

### Part 3: R Statistical Modeling
- Use Part 2 summary data as input for statistical models
- Predict user review activity patterns
- Hierarchical modeling of location effects

---

## Contributing

This is a research project. Contact for collaboration.

---

## Credits

**Built by**: Luke Pan  
**Part of**: Platform as Urban Policy - Mobility Medium Research  
**Phase**: Part 2 - Large-scale Review Pattern Analysis

---

*Analyzing 21.9M reviews to understand user behavior at scale* 📊
