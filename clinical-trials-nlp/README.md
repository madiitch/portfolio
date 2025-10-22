# Clinical Trials NLP

End-to-end NLP prototype for clinical trial intelligence: download public trial records, train a baseline phase classifier, and extract candidate endpoints from study summaries.

## Why It Matters

This project is designed like an analyst workflow a biotech or health client might ask for:

- pull a focused corpus from ClinicalTrials.gov
- classify studies for triage or landscape review
- extract endpoint-like text for downstream review
- export results in a stakeholder-friendly format

## Current Baseline

- Dataset: saved sample of cancer-related ClinicalTrials.gov records
- Task: predict study phase from `brief_summary`
- Model: TF-IDF + Logistic Regression
- Saved report: [`reports/metrics.txt`](./reports/metrics.txt)
- Current holdout accuracy on the saved sample: `0.650`

## What The Result Says

- The baseline is useful as a starting point, not a production classifier
- Phase 1 and Phase 2 are learned reasonably well
- Phase 3 and Phase 4 suffer from strong class imbalance
- Better label normalization, more records, and richer text features are the clearest next improvements

## Project Structure

```text
clinical-trials-nlp/
├── data/
├── models/
├── notebook/
├── reports/
└── src/
```

## How to Run

Run from inside `clinical-trials-nlp/`:

```bash
pip install -r ../requirements.txt

python src/download_trials.py --query "cancer" --max_records 2000 --out data/trials.jsonl
python src/train_classifier.py --input data/trials.jsonl --text_field brief_summary --label_field phase
python src/infer_extract.py --input data/trials.jsonl --out data/endpoints.jsonl
python src/export_endpoints_csv.py --input data/endpoints.jsonl --out reports/endpoints_preview.csv
```

## Included Artifacts

- [`reports/metrics.txt`](./reports/metrics.txt): saved classification report
- [`reports/endpoints_preview.csv`](./reports/endpoints_preview.csv): sample endpoint extraction output
- `reports/*.png`: exploratory visuals
- `notebook/eda.ipynb`: exploratory analysis notebook

## Limitations

- Endpoint extraction is rule-based and intentionally lightweight
- Trial phase prediction is limited by class imbalance and a compact dataset
- This is a portfolio prototype, not a validated clinical decision-support tool

## Good Next Steps

- Replace regex extraction with spaCy or transformer-based NER
- Expand data coverage beyond a single query theme
- Add confusion matrix and error analysis outputs
- Package the pipeline into a simple dashboard or API
