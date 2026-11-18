"""Helpers for the Koopmann-Aziz extension modes of regression.py (-what val / final):
output folders and names, write guards, peak-RAM monitor, git info, smoke-day choice."""
import json
import os
import subprocess
import threading
import time

import psutil

# folders of the reproduction that must never be written to (brief, hard rule 2)
PROTECTED_PARTS = [
    "/likable_jelly/preds", "/likable_jelly/scores", "/likable_jelly/experiments",
    "/data/prc2024/lj/submissions",
]
SUBFOLDERS = ["preds", "scores", "logs", "submissions"]
CLIMB_FOLDER = "classic__1e-2__5_500_40_daltitude_1_-0.5_1_masses"


def _norm(p):
    return os.path.abspath(p).replace("\\", "/").rstrip("/").lower()


def ext_folders(config):
    if not hasattr(config, "EXT_FOLDER"):
        raise SystemExit("config has no EXT_FOLDER entry: set LJ_CONFIG to koopmann_aziz/config/CONFIG.<machine>")
    root = config.EXT_FOLDER
    out = {}
    for s in SUBFOLDERS:
        out[s] = os.path.join(root, s)
        os.makedirs(out[s], exist_ok=True)
    return out


def guard_output(path, config):
    """refuse to write anywhere except below EXT_FOLDER, and never into the reproduction folders"""
    p, root = _norm(path), _norm(config.EXT_FOLDER)
    if not (p == root or p.startswith(root + "/")):
        raise RuntimeError(f"refusing to write {path}: not below EXT_FOLDER={config.EXT_FOLDER}")
    for part in PROTECTED_PARTS:  # also catches a mis-set EXT_FOLDER
        if part in p:
            raise RuntimeError(f"refusing to write {path}: protected reproduction folder ({part})")
    return path


def run_name(what, variant, model_params):
    device = model_params.get("device", "cpu")
    return f"{what}__{variant}__{device}_b{model_params.get('max_bin')}__seed{model_params.get('random_state')}"


def available_days(config, what="challenge_set"):
    folder = os.path.join(config.FOLDER_DATA, CLIMB_FOLDER, what)
    return sorted(f[:-len(".parquet")] for f in os.listdir(folder) if f.endswith(".parquet"))


def smoke_days(val_days, n, available):
    """n days present in the data: half validation days, half training days (at least one each)"""
    av = sorted(available)
    vd = [d for d in av if d in set(val_days)]
    td = [d for d in av if d not in set(val_days)]
    nv = max(1, n // 2) if vd else 0
    nt = max(1, n - nv)
    days = sorted(vd[:nv] + td[:nt])
    if not days:
        raise SystemExit("smoke: no day files found")
    return days


def git_info():
    def run(*cmd):
        try:
            return subprocess.check_output(["git", *cmd], stderr=subprocess.DEVNULL, text=True).strip()
        except Exception:
            return "unknown"
    return {"commit": run("rev-parse", "HEAD"),
            "dirty": run("status", "--porcelain", "--untracked-files=no") not in ("", "unknown")}


class PeakRSS:
    """samples the resident memory of this process every @period seconds"""
    def __init__(self, period=2.0):
        self.period = period
        self.peak = 0
        self._stop = threading.Event()
        self._proc = psutil.Process()

    def _loop(self):
        while not self._stop.is_set():
            try:
                self.peak = max(self.peak, self._proc.memory_info().rss)
            except Exception:
                pass
            self._stop.wait(self.period)

    def start(self):
        self.peak = self._proc.memory_info().rss
        threading.Thread(target=self._loop, daemon=True).start()
        return self

    def stop(self):
        self._stop.set()
        self.peak = max(self.peak, self._proc.memory_info().rss)
        return self.peak / 2**30


def write_json(obj, path, config):
    guard_output(path, config)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, default=str)


class Timer:
    def __init__(self):
        self.t0 = time.time()

    def __call__(self):
        return time.time() - self.t0
