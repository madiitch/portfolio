# Clinical Trials NLP

**Goal:** Build an NLP pipeline that downloads ClinicalTrials.gov studies, cleans text, and trains a classifier to predict **study phase** from brief summaries. Extend with **endpoint extraction** (NER) to identify primary endpoints.

**Baseline Model - Logistic Regression**
- Dataset: 2000 cancer clinical trials from ClinicalTrials.gov (you can change query and number of records).
- Task: predict trial phase (1-4) from brief summary text.
- Model: TF-IDF + Logistic Regression.
- Accuracy for 2000 cancer clinical trials is 71% on holdout set.
- Observations: class imbalance caused the model to underpredict Phase III and IV.
- Next steps: label normalization and dataset expansion for better coverage.

## How to Run

```bash
# 1. install repo-level requirements
pip install -r ../../requirements.txt

# 2. download a small dataset (e.g., cancer trials)
python src/download_trials.py --query "cancer" --max_records 2000 --out data/trials.jsonl

# 3. train a classifier
python src/train_classifier.py --input data/trials.jsonl --text_field "brief_summary" --label_field "phase" 

# 4. extract endpoints
python src/infer_extract.py --input data/trials.jsonl --out data/endpoints.jsonl

# 5. export to csv
python src/export_endpoints_csv.py --input data/endpoints.jsonl --out reports/endpoints_preview.csv
```

## Deliverables
- **models/** trained baseline model
- **reports/** short markdown with accuracy/F1 and sample endpoint extractions
- **notebooks/** to see results without running

## Future Improvements (to be done if requested)
- Replace regex extraction with spaCy/transformers
- Deploy dashboard for exploration
- Improve model performance with embeddings

