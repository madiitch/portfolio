# Pharmacovigilance Signal Detection (FAERS/OpenFDA)

**Goal:** Implement disproportionality analyses (PRR, ROR, EBGM-lite) on adverse event reports to surface drug-event signals.

## Data
- FAERS via OpenFDA API (public). The download script pulls quarterly counts for specified drugs/events.

## How to Run

```bash
pip install -r ../../requirements.txt

# Example: count event terms for a drug
python src/download_faers.py --drug "adalimumab" --event "headache" --out data/adalimumab_headache.jsonl

# Compute disproportionality metrics (requires a background rate file; script can approximate from pulls)
python src/disproportionality.py --input data/adalimumab_headache.jsonl --out reports/signal_metrics.csv
```
