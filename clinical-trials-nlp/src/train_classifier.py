import argparse, json, re
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

def load_jsonl(path: str) -> pd.DataFrame:
    return pd.read_json(path, lines=True)

def clean_phase_column(df: pd.DataFrame, label_col: str) -> pd.DataFrame:

    df= df.copy()

    df[label_col] = df[label_col].astype(str).str.upper().str.strip()

    na_like = {"", "NA", "NONE", "NAN", "NULL"}
    df.loc[df[label_col].isin(na_like), label_col] = pd.NA

    replace_map = {
        "EARLY_PHASE1": "PHASE 1",
        "PHASE1": "PHASE 1",
        "PHASE2": "PHASE 2",
        "PHASE3": "PHASE 3",
        "PHASE4": "PHASE 4"
    }
    df[label_col] = df[label_col].replace(replace_map)

    # Drop missing labels after cleaning
    df = df[df[label_col].notna()].copy()

    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--text_field", default="brief_summary")
    ap.add_argument("--label_field", default="phase")
    ap.add_argument("--model_out", default="models/baseline.joblib")
    ap.add_argument("--report_out", default="clinical-trials-nlp/reports/metrics.txt")
    args = ap.parse_args()

    Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)

    df = load_jsonl(args.input)

    df = clean_phase_column(df, args.label_field)

    df[args.text_field] = df[args.text_field].fillna("").astype(str).str.strip()
    df = df[df[args.text_field].str.len() > 0].copy()

    #sanity check
    counts = df[args.label_field].value_counts().to_dict()
    if len(counts) < 2:
        raise ValueError(
            f"Need at least 2 classes to train. Got {counts}. "
            "Try increasing --max_records in download step or broadening --query."
        )
    
    print("Class distribution after cleaning/merging: ")
    for k, v in counts.items():
        print(f" {k}: {v}")

    X_train, X_test, y_train, y_test = train_test_split(
        df[args.text_field], df[args.label_field], test_size=0.2, random_state=42, stratify=df[args.label_field]
    )

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=30000, ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=300))
    ])
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    report = classification_report(y_test, y_pred, digits=3)
    print("\n" + report)

    joblib.dump(pipe, args.model_out)
    with open(args.report_out, "w", encoding="utf-8") as f:
        f.write("Class distribution used:\n")
        for k, v in counts.items():
            f.write(f"{k}: {v}\n")
        f.write("\n" + report)

    print(f"\nModel saved to: {args.model_out}")
    print(f"Report saved to: {args.report_out}")
if __name__ == "__main__":
    main()
