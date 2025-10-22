import argparse, json, re
from pathlib import Path

# Simple rule-based endpoint extractor for demo. Replace with spaCy/transformers NER as needed.
ENDPOINT_PATTERNS = [
    r"primary endpoint[s]?:?\s*(.*?)(?:\.|;|$)",
    r"primary outcome[s]?:?\s*(.*?)(?:\.|;|$)",
    r"key (?:secondary|efficacy) endpoint[s]?:?\s*(.*?)(?:\.|;|$)",
    r"(?:main|key) outcome measure[s]?:?\s*(.*?)(?:\.|;|$)",
    r"(?:objective|aim)s?:?\s*(.*?)(?:\.|;|$)",
    r"will assess\s+(.*?)(?:\.|;|$)",
    r"to assess\s+(.*?)(?:\.|;|$)",
    r"to evaluate\s+(.*?)(?:\.|;|$)",
    r"to determine\s+(.*?)(?:\.|;|$)",
    r"efficacy of\s+(.*?)(?:\.|;|$)",
    r"measur(?:e|ement) of\s+(.*?)(?:\.|;|$)",
]

def extract_endpoints(text):
    endpoints = []
    for pat in ENDPOINT_PATTERNS:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            endpoint = match.group(1)
            endpoint = endpoint.strip().strip(":;,.")
            if endpoint:
                endpoints.append(endpoint)
    return endpoints

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="data/endpoints.jsonl")
    args = ap.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    with open(args.input,"r",encoding="utf-8") as f_in, open(args.out,"w",encoding="utf-8") as f_out:
        for line in f_in:
            rec = json.loads(line)
            rec["extracted_endpoints"] = extract_endpoints(rec.get("brief_summary",""))
            f_out.write(json.dumps(rec, ensure_ascii=False)+"\n")
    print(f"Wrote endpoint annotations to {args.out}")

if __name__ == "__main__":
    main()
