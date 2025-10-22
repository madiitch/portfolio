import argparse, json, csv

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f_in, \
         open(args.out, "w", newline="", encoding="utf-8") as f_out:
        w = csv.writer(f_out)
        w.writerow(["nct_id","title","phase","condition","endpoint_1","endpoint_2","endpoint_3"])
        for line in f_in:
            rec = json.loads(line)
            eps = (rec.get("extracted_endpoints") or [])[:3]
            row = [
                rec.get("nct_id"),
                rec.get("title"),
                rec.get("phase"),
                rec.get("condition"),
                eps[0] if len(eps)>0 else "",
                eps[1] if len(eps)>1 else "",
                eps[2] if len(eps)>2 else "",
            ]
            w.writerow(row)

if __name__ == "__main__":
    main()
