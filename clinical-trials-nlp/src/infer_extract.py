import argparse, json, re
from pathlib import Path

# Simple rule-based endpoint extractor for demo. Replace with spaCy/transformers NER as needed.
ENDPOINT_PATTERNS = [
    r"primary endpoint[s]?:?\s*(.*?)(?:\.|;|$)",
    r"primary outcome[s]?:?\s*(.*?)(?:\.|;|$)",
    r"key (?:secondary|efficacy) endpoint[s]?:?\s*(.*?)(?:\.|;|$)",
    r"(?:main|key) outcome measure[s]?:?\s*(.*?)(?:\.|;|$)",
    r"(?:objective|aim)s?:?\s*(.*?)(?:\.|;|$)",
    r"will assess\s*(.*?)(?:\.|;|$)",
    r"measure(?:s|ment) of\s*(.*?)(?:\.|;|$)",
]

def extract(text: str):
    text = (text or "").lower()
    hits = []
    for pat in ENDPOINT_PATTERNS:
        m = re.search(pat, text)
        if m: hits.append(m.group(1).strip())
    return list(dict.fromkeys(hits))[:5]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="data/endpoints.jsonl")
    args = ap.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    with open(args.input,"r",encoding="utf-8") as f_in, open(args.out,"w",encoding="utf-8") as f_out:
        for line in f_in:
            rec = json.loads(line)
            rec["extracted_endpoints"] = extract(rec.get("brief_summary",""))
            f_out.write(json.dumps(rec, ensure_ascii=False)+"\n")
    print(f"Wrote endpoint annotations to {args.out}")

if __name__ == "__main__":
    main()
