import argparse, json, math, csv
from collections import Counter

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="reports/signal_metrics.csv")
    args = ap.parse_args()

    # For demo, compute simple counts and toy PRR with naive background (not production-grade)
    total_reports = 0
    event_count = 0
    with open(args.input, "r", encoding="utf-8") as f:
        for _ in f:
            total_reports += 1
            event_count += 1  # each line is a report hitting the event

    # Fake background: assume 1% baseline for the event across all drugs in a comparable cohort of 100k
    background_total = 100000
    background_event = int(0.01 * background_total)

    # PRR ~ (event/drug / non-event/drug) / (event/all / non-event/all)
    a = event_count
    b = max(total_reports - a, 1)
    c = background_event
    d = max(background_total - c, 1)

    prr = (a / b) / (c / d)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["total_reports","event_count","background_total","background_event","PRR_est"])
        w.writerow([total_reports, event_count, background_total, background_event, round(prr,4)])

    print(f"Wrote metrics to {args.out}")

if __name__ == "__main__":
    main()
