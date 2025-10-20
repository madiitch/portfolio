# Clinical Trials NLP

**Goal:** Build an NLP pipeline that downloads ClinicalTrials.gov studies, cleans text, and trains a classifier to predict **study phase** from brief summaries. Extend with **endpoint extraction** (NER) to identify primary endpoints.

**Baseline Model - Logistic Regression**
- Dataset: 2000 cancer clinical trials from ClinicalTrials.gov (you can change query and number of records).
- Task: predict trial phase (1-4) from brief summary text.
- Model: TF-IDF + Logistic Regression.
- Accuracy for 2000 cancer clinical trials is 65% on holdout set.
- Observations: class imbalance caused the model to overpredict Phase 3.
- Next steps: label normalization and dataset expansion for better coverage.

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

