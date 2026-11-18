"""The synthetic data folder must match DATA_STRUCTURE_lj.md (pc182): paths, columns, dtypes,
roughly the missing shares. The expected structure is parsed from the markdown itself, so
the generator is checked against the documentation, not against itself."""
import os
import re

import pandas as pd
import pytest

from conftest import REPO

MD = os.path.join(REPO, "koopmann_aziz", "DATA_STRUCTURE_lj.md")
PREFIXES = {"E:/Koopmann-Aziz/data/prc2024/lj\\": "lj", "E:/Koopmann-Aziz/data/prc2024/raw\\": "raw"}
SKIP = ["\\submissions", "download.log", "ram_monitor.log", "run_lj.log"]


def parse_md():
    """{relative path: {"columns": [(name, dtype, share|None)], "patterns": [(pattern, count, dtype, lo, hi)]}}"""
    spec, cur, mode = {}, None, None
    for line in open(MD, encoding="utf-8"):
        m = re.match(r"^### `(.+)`", line)
        if m:
            cur = None
            path = m.group(1)
            for pre, root in PREFIXES.items():
                if path.startswith(pre) and not any(s in path for s in SKIP):
                    cur = (root, path[len(pre):].replace("\\", "/"))
                    spec[cur] = {"columns": [], "patterns": []}
            mode = None
            continue
        if cur is None:
            continue
        if line.startswith("| column | dtype"):
            mode = "col"
            continue
        if line.startswith("| pattern | count"):
            mode = "pat"
            continue
        if not line.startswith("| `"):
            if not line.startswith("| ---"):
                mode = None if not line.startswith("|") else mode
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if mode == "col":
            share = None
            if len(cells) > 2:
                try:
                    share = float(cells[2])
                except ValueError:
                    share = None
            spec[cur]["columns"].append((cells[0], cells[1], share))
        elif mode == "pat":
            lo, hi = [float(x) for x in cells[3].split("-")]
            spec[cur]["patterns"].append((cells[0], int(cells[1]), cells[2], lo, hi))
    return spec


SPEC = parse_md()


def test_spec_parsed():
    assert len(SPEC) >= 20
    flights = SPEC[("lj", "flights/challenge_set.parquet")]
    assert [c[0] for c in flights["columns"]][:3] == ["flight_id", "date", "callsign"]
    climb = SPEC[("lj", "classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses/challenge_set/2022-01-01.parquet")]
    assert sum(p[1] for p in climb["patterns"]) == 542


def _read(root, rel):
    path = os.path.join(root, rel)
    if rel.endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_parquet(path)


@pytest.mark.parametrize("key", sorted(SPEC), ids=lambda k: f"{k[0]}/{k[1]}")
def test_file_matches_spec(synth, key):
    root = synth["lj"] if key[0] == "lj" else synth["raw"]
    path = os.path.join(root, key[1])
    assert os.path.exists(path), f"missing synthetic file {path}"
    df = _read(root, key[1])
    s = SPEC[key]
    if s["columns"]:
        assert list(df.columns) == [c[0] for c in s["columns"]], key
        for name, dtype, share in s["columns"]:
            got = str(df[name].dtype)
            assert got == dtype, f"{key}: {name} dtype {got} != documented {dtype}"
            if share is not None and len(df) >= 200 and name != "tow":
                assert abs(df[name].isna().mean() - share) < 0.12, f"{key}: {name} missing share"
    if s["patterns"]:
        assert len(df.columns) == sum(p[1] for p in s["patterns"])
        for pat, count, dtype, lo, hi in s["patterns"]:
            rx = re.compile("^" + re.escape(pat).replace(re.escape("<i>"), r"\d+") + "$")
            cols = [c for c in df.columns if rx.match(c)]
            # 'climbmass_<i>' must not also swallow 'takeoffmass_<i>' etc.: the regex is anchored
            assert len(cols) == count, f"{key}: pattern {pat}: {len(cols)} columns, documented {count}"
            for c in cols:
                assert str(df[c].dtype) == dtype, f"{key}: {c} dtype"
            shares = df[cols].isna().mean()
            assert shares.min() >= lo - 0.15 and shares.max() <= hi + 0.15, f"{key}: {pat} missing shares"


def test_day_folders_complete(synth):
    lj = synth["lj"]
    for folder in ["classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses", "classic__1e-2__20_cruise", "classic__1e-2_wind"]:
        for what in ["challenge_set", "final_submission_set"]:
            files = sorted(os.listdir(os.path.join(lj, folder, what)))
            assert files == [f"{d}.parquet" for d in synth["days"]]


def test_test_files_have_no_labels(synth):
    """mirror of the pc182 leakage check: tow in a test file must be all missing"""
    for path in [os.path.join(synth["lj"], "flights", "final_submission_set.parquet"),
                 os.path.join(synth["lj"], "flights", "final_submission_set.csv"),
                 os.path.join(synth["raw"], "test_final.csv"), os.path.join(synth["raw"], "test.csv")]:
        df = pd.read_parquet(path) if path.endswith(".parquet") else pd.read_csv(path)
        assert df["tow"].notna().sum() == 0, path
