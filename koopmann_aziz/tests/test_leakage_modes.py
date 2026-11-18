"""Leakage control and behaviour of the -what val / final modes."""
import os
import shutil

import numpy as np
import pandas as pd
import pytest

from conftest import FAST, ka_result, run_regression
from koopmann_aziz import split


def _norm(p):
    return os.path.abspath(p).replace("\\", "/").lower()


def audited(synth, tmp_path, args):
    log = str(tmp_path / "audit.log")
    p = run_regression(synth, args, audit_log=log)
    entries = [l.rstrip("\n").split("\t", 1) for l in open(log, encoding="utf-8") if "\t" in l]
    return p, entries


@pytest.mark.parametrize("what", ["val", "final"])
def test_no_truth_file_is_opened(synth, tmp_path, what):
    p, entries = audited(synth, tmp_path, ["-what", what, "-variant", "audit"] + FAST)
    raw = _norm(synth["raw"])
    opened = [_norm(path) for _, path in entries]
    assert opened, "audit hook recorded nothing"
    assert any("flights/challenge_set.parquet" in o for o in opened), "audit hook misses pandas reads"
    bad = [o for o in opened if o.startswith(raw) or "flight_list" in o or "test_final" in o]
    assert not bad, f"training code opened truth/test files: {bad}"


@pytest.mark.parametrize("what", ["val", "final"])
def test_writes_only_below_ext(synth, tmp_path, what):
    p, entries = audited(synth, tmp_path, ["-what", what, "-variant", "audit"] + FAST)
    ext, tmp = _norm(synth["ext"]), _norm(synth["tmp"])
    writes = [_norm(path) for mode, path in entries if mode == "W"]
    assert any(w.startswith(ext) for w in writes)
    bad = [w for w in writes if not (w.startswith(ext + "/") or w.startswith(tmp + "/") or "__pycache__" in w
                                     or w.endswith(".pyc") or "/temp/" in w or w.endswith("/nul") or w == "nul")]
    assert not bad, f"writes outside EXT_FOLDER: {bad}"


def test_final_refuses_labelled_test_set(synth, tmp_path):
    """if the test flight table ever carried tow values, the final mode must stop"""
    root = tmp_path / "leaky"
    shutil.copytree(synth["lj"], root / "lj")
    f = root / "lj" / "flights" / "final_submission_set.parquet"
    df = pd.read_parquet(f)
    df["tow"] = 70000.0
    df.to_parquet(f, index=False)
    cfg = tmp_path / "CONFIG.leaky"
    cfg.write_text(open(synth["config"]).read().replace(synth["lj"].replace("\\", "/"),
                                                        str(root / "lj").replace("\\", "/")))
    assert str(root / "lj").replace("\\", "/") in cfg.read_text()
    p = run_regression(synth, ["-what", "final", "-variant", "leaky"] + FAST, config=str(cfg), check=False)
    assert p.returncode != 0
    assert "non-missing tow" in p.stderr


def test_val_mode(synth):
    r = ka_result(run_regression(synth, ["-what", "val", "-variant", "vt", "-random_state", "1"] + FAST))
    assert os.path.basename(r["output"]) == "val__vt__cpu_b511__seed1.csv"
    pred = pd.read_csv(r["output"])
    val_days = set(split.load_val_days())
    assert set(pred.day) <= val_days and len(pred) == r["n_val"]
    # training part: all other flights (C56X/A310 excluded by the team code)
    fl = pd.read_parquet(os.path.join(synth["lj"], "flights", "challenge_set.parquet"))
    fl = fl[~fl.aircraft_type.isin(["C56X", "A310"])]
    assert r["n_train"] + r["n_val"] == len(fl)
    rmse = np.sqrt(np.mean((pred.tow - pred.tow_pred) ** 2))
    assert abs(rmse - r["val_rmse"]) < 1e-6
    # the model must learn something: beat the per-type mean load fraction of the training part
    m = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..",
                                 "aircraft_type_masses.csv")).set_index("aircraft_type")
    tr = fl[~split.offblock_day(fl).isin(val_days)]
    frac = ((tr.tow - m.loc[tr.aircraft_type, "oew"].values) /
            (m.loc[tr.aircraft_type, "mtow"].values - m.loc[tr.aircraft_type, "oew"].values)).mean()
    const = m.loc[pred.aircraft_type, "oew"].values + frac * (m.loc[pred.aircraft_type, "mtow"].values -
                                                              m.loc[pred.aircraft_type, "oew"].values)
    rmse_const = np.sqrt(np.mean((pred.tow - const) ** 2))
    assert rmse < 0.8 * rmse_const, (rmse, rmse_const)


def test_smoke_outputs_are_named_smoke(synth):
    r = ka_result(run_regression(synth, ["-what", "val", "-smoke_days", "2"] + FAST))
    assert os.path.basename(r["output"]).startswith("val__SMOKE-baseline__")


def test_average_and_compare(synth):
    import subprocess, sys
    from conftest import REPO
    for s in [0, 1]:
        run_regression(synth, ["-what", "val", "-variant", "avg", "-random_state", str(s)] + FAST)
    env = dict(os.environ, LJ_CONFIG=synth["config"])
    p = subprocess.run([sys.executable, "-m", "koopmann_aziz.average", "--what", "val", "--variant", "avg",
                        "--seeds", "0-1"], cwd=REPO, env=env, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert "KA_AVG val seeds=2" in p.stdout
    a = os.path.join(synth["ext"], "preds", "val__avg__cpu_b511__seed0.csv")
    p = subprocess.run([sys.executable, "-m", "koopmann_aziz.average", "--compare", a, a], cwd=REPO, env=env,
                       capture_output=True, text=True)
    assert "max_abs_diff=0.000000" in p.stdout, p.stdout + p.stderr
