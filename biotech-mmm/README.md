# Biotech Bayesian Marketing Mix Modeling (MMM)

**Goal:** Simulate a biotech product launch and fit a Bayesian MMM to estimate channel contributions, elasticities, and ROI, then suggest budget reallocation.

## How to Run

```bash
pip install -r ../../requirements.txt

# 1) generate synthetic data
python src/generate_synthetic_data.py --out data/biotech_mmm.csv

# 2) fit Bayesian model (PyMC)
python src/fit_bayesian_mmm.py --input data/biotech_mmm.csv --out reports/mmm_summary.md
```

## Deliverables
- **reports/mmm_summary.md** with key metrics, channel ROI table, and a sample budget shift scenario.
