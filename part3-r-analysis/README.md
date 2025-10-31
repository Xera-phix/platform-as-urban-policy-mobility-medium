# part 2: r statistical analysis

advanced statistical modeling and analysis using R datasets

---

## current status

🔄 **in progress** - setting up r data pipeline

---

## directory structure

```
part2-r-analysis/
├── read_rdata.py           # python interface for .rdata files (pyreadr)
├── read_rdata_rpy2.py      # alternative using rpy2 (requires R)
├── scripts/                # R analysis scripts (coming soon)
├── outputs/                # analysis results
└── README.md
```

---

## what we're working with

### primary dataset
- **file**: `GL_review_PCW.rdata`
- **location**: `../data/part 3/GL_review_PCW/`
- **format**: R data file (.rdata)
- **purpose**: advanced statistical modeling of review sentiment

---

## tools & setup

### python tools
```bash
# install python packages for reading R data
pip install pyreadr        # recommended
pip install rpy2           # alternative (requires R installed)
```

### reading the data
```bash
# using pyreadr (simpler)
python read_rdata.py

# using rpy2 (more powerful, needs R)
python read_rdata_rpy2.py
```

---

## goals for phase 2

- [ ] **import R dataset** - convert .rdata to usable format
- [ ] **statistical validation** - verify phase 1 findings
- [ ] **predictive modeling** - forecast sentiment trends
- [ ] **comparative analysis** - compare with other urban spaces
- [ ] **advanced visualizations** - ggplot2-style charts
- [ ] **integration** - feed results back to dashboard

---

## planned analyses

### statistical tests
- significance testing (pre/during/post periods)
- regression modeling (time-based predictors)
- anova for period comparisons
- correlation analysis

### modeling
- time series forecasting
- sentiment trajectory prediction
- impact quantification
- counterfactual analysis

### visualization
- advanced ggplot2 charts
- statistical plots (qq, residuals)
- interactive dashboards (shiny)
- publication-ready figures

---

## tech stack

- **r programming language** - statistical computing
- **python** - data pipeline integration
- **pyreadr / rpy2** - R-python bridge
- **ggplot2** - advanced visualizations (planned)
- **tidyverse** - data manipulation (planned)

---

## integration with phase 1

phase 2 will enhance phase 1 by:
1. validating gpt sentiment classifications
2. providing statistical rigor
3. generating publication-ready analysis
4. expanding dataset coverage
5. feeding new insights to dashboard

---

## next steps

1. successfully import GL_review_PCW.rdata
2. explore data structure
3. run initial descriptive stats
4. compare with phase 1 results
5. develop modeling strategy
