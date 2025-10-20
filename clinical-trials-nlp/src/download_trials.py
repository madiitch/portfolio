import argparse, json, time
from pathlib import Path
import requests

API = "https://clinicaltrials.gov/api/v2/studies"

def fetch(query: str, max_records: int = 1000, page_size: int = 100):
    """
    Fetch studies from ClinicalTrials.gov v2 API.

    We page using nextPageToken returned by the API, NOT numeric offsets.
    We stop when we hit max_records or there are no more pages.
    """
    out = []
    page_token = None

    while len(out) < max_records:
        params = {
            "query.term": query,
            "pageSize": page_size,
        }
        if page_token:
            params["pageToken"] = page_token

        r = requests.get(API, params=params, timeout=60)
        r.raise_for_status()
        payload = r.json()

        studies = payload.get("studies", []) or []
        for s in studies:
            protocol = s.get("protocolSection", {}) or {}
            id_info = protocol.get("identificationModule", {}) or {}
            desc = protocol.get("descriptionModule", {}) or {}
            design = protocol.get("designModule", {}) or {}
            cond = protocol.get("conditionsModule", {}) or {}

            rec = {
                "nct_id": id_info.get("nctId"),
                "title": id_info.get("briefTitle"),
                "brief_summary": desc.get("briefSummary"),
                "phase": (design.get("phases") or [None])[0] if design.get("phases") else None,
                "condition": (cond.get("conditions") or [None])[0] if cond.get("conditions") else None,
                "study_type": design.get("studyType"),
            }
            out.append(rec)
            if len(out) >= max_records:
                break

        page_token = payload.get("nextPageToken")
        if not page_token or not studies:
            break

        time.sleep(0.2)  # be polite

    return out[:max_records]

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
