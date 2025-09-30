# Clinical Trials NLP

**Goal:** Build an NLP pipeline that downloads ClinicalTrials.gov studies, cleans text, and trains a classifier to predict **study phase** from brief summaries. Extend with **endpoint extraction** (NER) to identify primary endpoints.

## Why It Matters
Sponsors and investors need rapid landscape scans. A light classifier + NER can triage studies by phase and extract endpoints for competitive intel.

## Data
- Source: ClinicalTrials.gov API (public). Scripts will download JSON for specified conditions/keywords.

## How to Run

```bash
# 1) install repo-level requirements
pip install -r ../../requirements.txt

# 2) download a small dataset (e.g., oncology trials)
python src/download_trials.py --query "oncology" --max_records 1000 --out data/trials.jsonl

# 3) train a baseline classifier
python src/train_classifier.py --input data/trials.jsonl --text_field "brief_summary" --label_field "phase" --out models/baseline.joblib

# 4) run NER inference on summaries to extract endpoints
python src/infer_extract.py --input data/trials.jsonl --out data/endpoints.jsonl
```

## Deliverables
- **models/** trained baseline model
- **reports/** short markdown with accuracy/F1 and sample endpoint extractions
- **notebooks/** optional EDA

