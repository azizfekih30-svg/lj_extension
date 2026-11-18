"""Average prediction files by variant and seeds (replaces average_prediction.py -istop N).

    python -m koopmann_aziz.average --what final --variant baseline --device cpu --bins 511 --seeds 0-19
writes <EXT_FOLDER>/submissions/final__baseline__cpu_b511__avg<n>.csv  (or preds/ for --what val)
and, for val, prints the RMSE of the average (validation labels come from challenge_set).

    python -m koopmann_aziz.average --compare A.csv B.csv
prints the per-flight difference of two prediction files (no truth involved), e.g. a new
baseline run against the reproduction file lj_full_seed0.csv.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils  # noqa: E402
from koopmann_aziz import ext  # noqa: E402


def parse_seeds(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def average(files, col):
    dfs = [pd.read_csv(f) for f in files]
    base = dfs[0].flight_id.values
    for f, d in zip(files, dfs):
        if len(d) != len(base) or not (d.flight_id.values == base).all():
            raise SystemExit(f"flight_id mismatch in {f}")
    out = dfs[0].drop(columns=[c for c in ["tow", "tow_pred"] if c in dfs[0]]).copy()
    out[col] = np.mean([d[col].values for d in dfs], axis=0)
    return out, dfs


def compare(a, b):
    da, db = pd.read_csv(a), pd.read_csv(b)
    ca = "tow_pred" if "tow_pred" in da else "tow"
    cb = "tow_pred" if "tow_pred" in db else "tow"
    m = da[["flight_id", ca]].merge(db[["flight_id", cb]], on="flight_id", suffixes=("_a", "_b"), how="outer",
                                    indicator=True)
    both = m[m._merge == "both"]
    d = both.iloc[:, 1].values - both.iloc[:, 2].values
    print(f"KA_COMPARE rows_a={len(da)} rows_b={len(db)} common={len(both)} "
          f"only_a={(m._merge == 'left_only').sum()} only_b={(m._merge == 'right_only').sum()} "
          f"max_abs_diff={np.abs(d).max():.6f} rms_diff={np.sqrt(np.mean(d**2)):.6f} kg")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--what", choices=["val", "final"])
    ap.add_argument("--variant")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--bins", default="511")
    ap.add_argument("--seeds", default="0-19")
    ap.add_argument("--compare", nargs=2)
    a = ap.parse_args()
    if a.compare:
        return compare(*a.compare)
    config = utils.read_config()
    folders = ext.ext_folders(config)
    sub = "preds" if a.what == "val" else "submissions"
    seeds = parse_seeds(a.seeds)
    files = [os.path.join(folders[sub], f"{a.what}__{a.variant}__{a.device}_b{a.bins}__seed{s}.csv") for s in seeds]
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        raise SystemExit("missing prediction files:\n  " + "\n  ".join(missing))
    col = "tow_pred" if a.what == "val" else "tow"
    out, dfs = average(files, col)
    if a.what == "val":
        out["tow"] = dfs[0]["tow"].values
        rmse = lambda p: float(np.sqrt(np.mean((out["tow"].values - p) ** 2)))
        singles = [rmse(d[col].values) for d in dfs]
        print(f"KA_AVG val seeds={len(seeds)} rmse_avg={rmse(out[col].values):.2f} "
              f"single_mean={np.mean(singles):.2f} single_std={np.std(singles, ddof=1) if len(singles) > 1 else 0:.2f}")
    fout = os.path.join(folders[sub], f"{a.what}__{a.variant}__{a.device}_b{a.bins}__avg{len(seeds)}.csv")
    out.to_csv(ext.guard_output(fout, config), index=False)
    print("written", fout)


if __name__ == "__main__":
    main()
