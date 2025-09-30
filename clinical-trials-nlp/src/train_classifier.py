import argparse, json, re
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)

def clean_phase(x: str):
    x = (x or "").upper()
    if "PHASE 4" in x: return "Phase 4"
    if "PHASE 3" in x: return "Phase 3"
    if "PHASE 2" in x: return "Phase 2"
    if "PHASE 1" in x: return "Phase 1"
    if "EARLY" in x: return "Phase 1/2"
    return "Unknown"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--text_field", default="brief_summary")
    ap.add_argument("--label_field", default="phase")
    ap.add_argument("--out", default="models/baseline.joblib")
    args = ap.parse_args()

    df = load_jsonl(args.input)
    df["label"] = df[args.label_field].map(clean_phase)
    df[args.text_field] = df[args.text_field].fillna("")
    df = df[df["label"] != "Unknown"].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        df[args.text_field], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=30000, ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=200))
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    print(classification_report(y_test, y_pred))
    Path("models").mkdir(exist_ok=True, parents=True)
    joblib.dump(pipe, args.out)
    with open("reports/metrics.txt","w") as f:
        f.write(classification_report(y_test, y_pred))
    print(f"Model saved to {args.out}")

if __name__ == "__main__":
    main()
