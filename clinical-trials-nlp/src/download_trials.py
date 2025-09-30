import json, argparse, requests, sys, time
from pathlib import Path

API = "https://clinicaltrials.gov/api/query/study_fields"
FIELDS = ["NCTId","BriefTitle","BriefSummary","Phase","Condition","StudyType"]

def fetch(query: str, max_records: int = 1000):
    page_size = 200
    out = []
    for min_rnk in range(1, max_records+1, page_size):
        max_rnk = min(min_rnk + page_size - 1, max_records)
        params = {
            "expr": query,
            "fields": ",".join(FIELDS),
            "min_rnk": min_rnk,
            "max_rnk": max_rnk,
            "fmt": "json"
        }
        r = requests.get(API, params=params, timeout=60)
        r.raise_for_status()
        studies = r.json().get("StudyFieldsResponse", {}).get("StudyFields", [])
        for s in studies:
            rec = {
                "nct_id": (s.get("NCTId") or [""])[0],
                "title": (s.get("BriefTitle") or [""])[0],
                "brief_summary": (s.get("BriefSummary") or [""])[0],
                "phase": (s.get("Phase") or [""])[0],
                "condition": (s.get("Condition") or [""])[0],
                "study_type": (s.get("StudyType") or [""])[0],
            }
            out.append(rec)
        time.sleep(0.2)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--max_records", type=int, default=1000)
    ap.add_argument("--out", default="data/trials.jsonl")
    args = ap.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    data = fetch(args.query, args.max_records)
    with open(args.out, "w", encoding="utf-8") as f:
        for row in data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(data)} records to {args.out}")

if __name__ == "__main__":
    main()
