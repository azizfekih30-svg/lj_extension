import os

import pandas as pd
import pytest

from conftest import REPO
from koopmann_aziz import ext, split


def test_committed_split_is_reproducible():
    days = split.load_val_days(split.DEFAULT_SPLIT)
    assert days == split.make_val_days(seed=0, frac=0.2)
    assert len(days) == 72
    months = pd.Series(pd.to_datetime(days)).dt.month.value_counts()
    assert (months == 6).all() and len(months) == 12
    assert days == sorted(days) and len(set(days)) == len(days)


def test_split_is_grouped_by_offblock_day(synth):
    df = pd.read_parquet(os.path.join(synth["lj"], "flights", "challenge_set.parquet"))
    day = split.offblock_day(df)
    val = day.isin(split.load_val_days())
    assert val.any() and (~val).any()
    # every calendar day of offblock is entirely on one side
    assert (day[val].unique().tolist() != []) and set(day[val]).isdisjoint(set(day[~val]))
    # offblock day, not the 'date' column: flights leaving the evening before belong to that day
    early = df.actual_offblock_time.dt.strftime("%Y-%m-%d") != df.date.dt.strftime("%Y-%m-%d")
    assert early.any()
    assert (day[early] == df.actual_offblock_time[early].dt.strftime("%Y-%m-%d")).all()


def test_smoke_days_have_both_sides():
    val = split.load_val_days()
    av = [str(d.date()) for d in pd.date_range("2022-01-01", "2022-12-31")]
    d = ext.smoke_days(val, 2, av)
    assert len(d) == 2 and sum(x in val for x in d) == 1


def test_config_env_switch(monkeypatch, tmp_path):
    import utils
    cfg = tmp_path / "CONFIG.x"
    cfg.write_text("FOLDER_DATA = /some/where\nEXT_FOLDER = /ext\n")
    monkeypatch.setenv("LJ_CONFIG", str(cfg))
    c = utils.read_config()
    assert c.FOLDER_DATA == "/some/where" and c.EXT_FOLDER == "/ext"
    assert c.flights == os.path.join("/some/where", "flights")
    # unset -> the team's original file name "CONFIG" in the working directory
    monkeypatch.delenv("LJ_CONFIG")
    monkeypatch.chdir(REPO)
    assert utils.read_config().FOLDER_DATA == "/disk3/testprc"


def test_pc182_config_keys():
    import utils
    os.environ["LJ_CONFIG"] = os.path.join(REPO, "koopmann_aziz", "config", "CONFIG.pc182")
    try:
        c = utils.read_config()
    finally:
        del os.environ["LJ_CONFIG"]
    assert c.FOLDER_DATA == "E:/Koopmann-Aziz/data/prc2024/lj"
    assert c.EXT_FOLDER == "E:/Koopmann-Aziz/results/prc2024/likable_jelly/ext"
    # the team's submit mode must not write into the reproduction's submissions folder
    assert c.SUBMISSIONS_FOLDER.startswith(c.EXT_FOLDER + "/")
    assert c.TEMP_FOLDER.startswith("E:/") and "Koopmann-Aziz" in c.TEMP_FOLDER


def test_guard_output(tmp_path):
    class C:
        EXT_FOLDER = str(tmp_path / "ext")
    assert ext.guard_output(str(tmp_path / "ext" / "preds" / "a.csv"), C)
    with pytest.raises(RuntimeError):
        ext.guard_output(str(tmp_path / "elsewhere.csv"), C)
    with pytest.raises(RuntimeError):
        ext.guard_output(str(tmp_path / "ext2" / "a.csv"), C)

    class Bad:
        EXT_FOLDER = "E:/Koopmann-Aziz/results/prc2024/likable_jelly/preds"
    with pytest.raises(RuntimeError):
        ext.guard_output("E:/Koopmann-Aziz/results/prc2024/likable_jelly/preds/x.csv", Bad)


def test_run_name():
    assert ext.run_name("val", "t1a", {"device": "gpu", "max_bin": 255, "random_state": 3}) == "val__t1a__gpu_b255__seed3"
