# Biotech Bayesian Marketing Mix Modeling

Bayesian MMM prototype for a synthetic biotech launch scenario. The goal is to estimate channel contribution and show how a commercial analytics engagement could support budget decisions.

## What It Demonstrates

- synthetic data generation for a launch-style weekly sales series
- simple adstock and saturation transforms
- Bayesian coefficient estimation with PyMC
- stakeholder-friendly markdown output

## How to Run

Run from inside `biotech-mmm/`:

```bash
pip install -r ../requirements.txt

python src/generate_synthetic_data.py --out data/biotech_mmm.csv
python src/fit_bayesian_mmm.py --input data/biotech_mmm.csv --out reports/mmm_summary.md
```

For a faster smoke test, you can lower sampling settings:

```bash
python src/fit_bayesian_mmm.py --input data/biotech_mmm.csv --out reports/mmm_summary.md --draws 200 --tune 200 --chains 2 --cores 1
```

## Outputs

- `data/biotech_mmm.csv`: synthetic weekly spend and sales data
- `reports/mmm_summary.md`: posterior summary table and interpretation text

## Notes

- The dataset is synthetic by design so the repo stays portable and privacy-safe
- This is a compact modeling example rather than a full production MMM stack with hierarchical priors, holdout validation, and scenario simulation dashboards
