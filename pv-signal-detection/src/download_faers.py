import argparse, json, requests, time
from pathlib import Path

API = "https://api.fda.gov/drug/event.json"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drug", required=True, help="Drug name (generic or brand)")
    ap.add_argument("--event", required=True, help="MedDRA PT string, e.g., 'headache'")
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--out", default="data/faers.jsonl")
    args = ap.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    count = 0
    skip = 0
    with open(args.out, "w", encoding="utf-8") as f:
        while count < args.limit:
            params = {
                "search": f'patient.drug.medicinalproduct:"{args.drug}" AND patient.reaction.reactionmeddrapt:"{args.event}"',
                "skip": skip,
                "limit": min(100, args.limit - count)
            }
            r = requests.get(API, params=params, timeout=60)
            if r.status_code != 200:
                print(r.text)
                break
            data = r.json().get("results", [])
            if not data: break
            for row in data:
                f.write(json.dumps(row)+"\n")
            n = len(data)
            count += n
            skip += n
            time.sleep(0.2)
    print(f"Wrote {count} records to {args.out}")
if __name__ == "__main__":
    main()
