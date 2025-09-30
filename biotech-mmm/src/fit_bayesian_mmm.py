import argparse, pandas as pd, numpy as np
import pymc as pm, arviz as az
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="reports/mmm_summary.md")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    y = df["sales"].values
    X = df[["spend_digital","spend_field","spend_kol"]].values
    X = (X - X.mean(0)) / X.std(0)

    with pm.Model() as m:
        alpha = pm.Normal("alpha", 0, 5)
        betas = pm.Normal("betas", 0, 1, shape=X.shape[1])
        sigma = pm.Exponential("sigma", 1.0)
        mu = alpha + pm.math.dot(X, betas)
        obs = pm.Normal("obs", mu, sigma, observed=y)
        idata = pm.sample(1000, tune=1000, chains=2, target_accept=0.9, progressbar=False)

    summary = az.summary(idata, var_names=["alpha","betas","sigma"]).to_markdown()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# MMM Summary\n\n")
        f.write(summary)
        f.write("\n\nInterpretation: Larger posterior mean beta implies higher marginal impact given the standardized features.")

    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
