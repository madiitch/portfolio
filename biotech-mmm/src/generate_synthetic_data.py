import argparse, numpy as np, pandas as pd
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_weeks", type=int, default=120)
    ap.add_argument("--out", default="data/biotech_mmm.csv")
    args = ap.parse_args()

    rng = np.random.default_rng(42)
    t = np.arange(args.n_weeks)
    base_demand = 100 + 0.2*t + 10*np.sin(2*np.pi*t/52)
    spend_digital = rng.gamma(5, 200, size=args.n_weeks)
    spend_field = rng.gamma(4, 300, size=args.n_weeks)
    spend_kol = rng.gamma(3, 250, size=args.n_weeks)

    # adstock & saturation (simple)
    def adstock(x, l=0.6):
        y = np.zeros_like(x)
        for i, v in enumerate(x):
            y[i] = v + (y[i-1]*l if i>0 else 0)
        return y
    def sat(x, k=1e-3):
        return np.log1p(k*x)

    X_d = sat(adstock(spend_digital))
    X_f = sat(adstock(spend_field, 0.7))
    X_k = sat(adstock(spend_kol, 0.5))

    noise = rng.normal(0, 5, size=args.n_weeks)
    sales = base_demand + 30*X_d + 45*X_f + 25*X_k + noise
    df = pd.DataFrame({
        "week": t,
        "sales": sales,
        "spend_digital": spend_digital,
        "spend_field": spend_field,
        "spend_kol": spend_kol
    })
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
