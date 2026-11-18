import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
UPSTREAM_COMMIT = "fd8f0c45e737848b9da53cb4739fd463c9775504"  # team_likable_jelly master, start of this branch

# small trees and permissive leaves so that the model actually learns on ~500 flights
FAST = ["-n_estimators", "150", "-min_child_samples", "5", "-reg_alpha", "1", "-reg_lambda", "1", "-verbose", "-1"]


@pytest.fixture(scope="session")
def synth(tmp_path_factory):
    from koopmann_aziz import synth as s
    out = tmp_path_factory.mktemp("synth")
    paths = s.generate(str(out), n_days=4, n_challenge_per_day=130, n_final_per_day=60, seed=0)
    cfg = os.path.join(str(out), "CONFIG.test")
    s.write_config(paths, cfg)
    paths["config"] = cfg
    paths["root"] = str(out)
    return paths


def run_regression(synth, args, audit_log=None, config=None, check=True):
    """python regression.py <args> in the repo, on the synthetic config; optional open() audit log"""
    env = dict(os.environ, LJ_CONFIG=config or synth["config"], PYTHONUTF8="1",
               LOKY_MAX_CPU_COUNT="4", TEMP=synth["tmp"], TMP=synth["tmp"])
    cmd = [sys.executable]
    if audit_log:
        cmd += [os.path.join(REPO, "koopmann_aziz", "tests", "audit_run.py"), audit_log]
    cmd += ["regression.py"] + list(args)
    p = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        raise AssertionError(f"regression.py failed ({p.returncode}):\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}")
    return p


def ka_result(p):
    lines = [l for l in p.stdout.splitlines() if l.startswith("KA_RESULT ")]
    assert lines, p.stdout[-2000:]
    return json.loads(lines[-1][len("KA_RESULT "):])
