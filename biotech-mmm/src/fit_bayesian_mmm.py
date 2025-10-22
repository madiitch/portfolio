import argparse, os
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MPL_CACHE_DIR = PROJECT_ROOT / ".cache" / "matplotlib"
PYTENSOR_CACHE_DIR = PROJECT_ROOT / ".cache" / "pytensor"
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
PYTENSOR_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))
os.environ.setdefault("PYTENSOR_FLAGS", f"compiledir={PYTENSOR_CACHE_DIR},cxx=")

import arviz as az
import pymc as pm

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="reports/mmm_summary.md")
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--tune", type=int, default=1000)
    ap.add_argument("--chains", type=int, default=2)
    ap.add_argument("--cores", type=int, default=1)
    ap.add_argument("--target_accept", type=float, default=0.9)
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
        idata = pm.sample(
            draws=args.draws,
            tune=args.tune,
            chains=args.chains,
            cores=args.cores,
            target_accept=args.target_accept,
            progressbar=False,
        )

    summary = az.summary(idata, var_names=["alpha","betas","sigma"]).to_markdown()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# MMM Summary\n\n")
        f.write(summary)
        f.write("\n\nInterpretation: Larger posterior mean beta implies higher marginal impact given the standardized features.")

    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
