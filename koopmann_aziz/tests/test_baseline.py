"""All switches off must reproduce the team's code exactly."""
import importlib.util
import os
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from conftest import FAST, REPO, UPSTREAM_COMMIT, ka_result, run_regression


def upstream_source(fname):
    return subprocess.check_output(["git", "show", f"{UPSTREAM_COMMIT}:{fname}"], cwd=REPO, text=True)


def load_upstream_module(name, tmp_path):
    p = tmp_path / f"upstream_{name}.py"
    p.write_text(upstream_source(f"{name}.py"))
    spec = importlib.util.spec_from_file_location(f"upstream_{name}", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_model_params_unchanged():
    line = lambda src: [l for l in src.splitlines() if l.strip().startswith("model_params = {")]
    cur = open(os.path.join(REPO, "regression.py"), encoding="utf-8").read()
    assert line(cur) == line(upstream_source("regression.py"))
    assert len(line(cur)) == 1


def test_features_identical_to_upstream(synth, tmp_path, monkeypatch):
    """features.read_features (days=None) returns exactly what the team's features.py returns"""
    monkeypatch.setenv("LJ_CONFIG", synth["config"])
    monkeypatch.chdir(REPO)
    import features
    up = load_upstream_module("features", tmp_path)
    for what in ["challenge_set", "final_submission_set"]:
        a, b = features.read_features(what), up.read_features(what)
        pd.testing.assert_frame_equal(a.data, b.data)
        assert a.categorical_features() == b.categorical_features()
        assert a.numeric_features() == b.numeric_features()
        assert a.numeric_features_not_scaled() == b.numeric_features_not_scaled()


def test_feature_counts(synth, monkeypatch):
    """8 categorical + 672 numeric features, as documented in the brief"""
    monkeypatch.setenv("LJ_CONFIG", synth["config"])
    monkeypatch.chdir(REPO)
    import features
    feat = features.read_features("challenge_set")
    cat = feat.categorical_features()
    num = feat.numeric_features() + feat.numeric_features_not_scaled()
    assert len(cat) == 8
    assert len(num) == 672
    assert "callsign" not in cat + num
    assert not {"C56X", "A310"} & set(feat.data.aircraft_type)


def test_final_mode_equals_team_submit(synth):
    """-what final writes the same predictions as the team's -what submit (same seed)"""
    team_dir = os.path.join(synth["ext"], "submissions_team_format")
    before = set(os.listdir(team_dir)) if os.path.exists(team_dir) else set()
    run_regression(synth, ["-what", "submit", "-random_state", "3"] + FAST)
    new = sorted(set(os.listdir(team_dir)) - before)
    assert len(new) == 1
    team = pd.read_csv(os.path.join(team_dir, new[0]))
    r = ka_result(run_regression(synth, ["-what", "final", "-random_state", "3", "-variant", "eqtest"] + FAST))
    ours = pd.read_csv(r["output"])
    assert os.path.basename(r["output"]) == "final__eqtest__cpu_b511__seed3.csv"
    assert (team.flight_id.values == ours.flight_id.values).all()
    np.testing.assert_array_equal(team.tow.values, ours.tow.values)


def test_smoke_days_switch_off_is_identity(synth, monkeypatch):
    monkeypatch.setenv("LJ_CONFIG", synth["config"])
    monkeypatch.chdir(REPO)
    import features
    full = features.read_features("challenge_set")
    part = features.read_features("challenge_set", days=synth["days"][:2])
    assert set(part.data["date"].dt.strftime("%Y-%m-%d")) == set(synth["days"][:2])
    assert len(part.data) < len(full.data)
    sub = full.data[full.data["date"].dt.strftime("%Y-%m-%d").isin(synth["days"][:2])]
    pd.testing.assert_frame_equal(part.data.reset_index(drop=True), sub.reset_index(drop=True), check_dtype=False)
