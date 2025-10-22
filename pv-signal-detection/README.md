# Pharmacovigilance Signal Detection

Prototype pharmacovigilance workflow for pulling adverse event reports from OpenFDA and generating quick signal-screening metrics.

## Portfolio Framing

This project is best understood as a lightweight safety analytics prototype:

- it demonstrates public-data ingestion from OpenFDA
- it creates a simple reproducible pipeline for drug-event review
- it shows how signal metrics can be exported for downstream assessment

## Data

- Source: public OpenFDA drug event endpoint
- Input shape: JSON lines of matching adverse event reports for a specific drug-event query

## How to Run

Run from inside `pv-signal-detection/`:

```bash
pip install -r ../requirements.txt

python src/download_faers.py --drug "adalimumab" --event "headache" --out data/adalimumab_headache.jsonl
python src/disproportionality.py --input data/adalimumab_headache.jsonl --out reports/signal_metrics.csv
```

## What This Produces

- `data/*.jsonl`: raw pulled event reports
- `reports/signal_metrics.csv`: quick metric summary for screening

## Limitations

- The current metric calculation is intentionally simplified for portfolio demonstration
- It is useful for workflow illustration, not for validated regulatory signal detection
- A production version would use complete contingency tables, better background definitions, deduplication, and more robust Bayesian metrics
