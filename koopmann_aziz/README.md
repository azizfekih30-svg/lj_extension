# Koopmann-Aziz extension of likable_jelly (PRC Data Challenge 2024)

Bachelor thesis, RWTH Aachen ILR (Mohamed Aziz Fekih, supervisor Constantin Koopmann).
This folder holds everything added on top of the team's code; the team's own files are edited
only where a switch is needed, and every switch defaults to the team's behaviour.

Branch `koopmann-aziz-ext` starts at upstream
[team_likable_jelly](https://github.com/PRC-Data-Challenge-2024/team_likable_jelly) commit
`fd8f0c4` (unchanged). The pc182 reproduction copy has three documented differences from it
(`CONFIG` paths and the two METAR feature scripts reading fewer columns). This branch does not
need them: the METAR features already exist on pc182 and are not recomputed, and the config is
handled by `LJ_CONFIG` (below). `run/check_repro_copy.ps1` verifies on pc182 that there is no
other difference.

## Switches (all default to the team's behaviour)

| switch | where | default | effect |
|---|---|---|---|
| `LJ_CONFIG=<file>` | env, `utils.read_config` | unset → `CONFIG` | machine config: `config/CONFIG.pc182`, `config/CONFIG.laptop` (generated, git-ignored) |
| `-what val` | `regression.py` | (team: `valid`, `submit`) | train on challenge_set minus the held-out days, report validation RMSE, write `ext/preds/val__<variant>__<device>_b<bins>__seed<k>.csv` |
| `-what final` | `regression.py` | | train on full challenge_set, write `ext/submissions/final__<variant>__<device>_b<bins>__seed<k>.csv` (bit-identical to the team's `-what submit`, tested) |
| `-variant <name>` | `regression.py` | `baseline` | label used in output names |
| `-split_file <txt>` | `regression.py` | `koopmann_aziz/splits/val_days_seed0.txt` | held-out days |
| `-smoke_days N` | `regression.py`, `features.read_features(days=)` | 0 = all days | read only N day files (half validation, half training); outputs named `SMOKE-<variant>` |
| `-<lightgbm param> <v>` | `regression.py` (team) | team values | e.g. `-device gpu -max_bin 255` |

## Validation split

72 days (6 per month, seed 0) of the UTC calendar day of `actual_offblock_time`, listed in
`splits/val_days_seed0.txt` (≈ 19.7 % of the days). All flights of a day are on the same side.
Regenerate/check with `python -m koopmann_aziz.split --seed 0` (the test suite checks the file
equals the generator output).

## Outputs (pc182: `E:\Koopmann-Aziz\results\prc2024\likable_jelly\ext\`)

* `preds/val__…csv`: flight_id, aircraft_type, day, tow (challenge label), tow_pred
* `submissions/final__…csv`: flight_id, tow (C56X and A310 flights are absent, as in the team's submission)
* `scores/<name>.json`: run info (commit, params, split, n, RMSE, runtime, peak RAM); `scores/<name>__importance.csv`
* `logs/`: one log per python call plus `…__summary__….txt` (the pasted block)
* `submissions_team_format/`: where the team's own `-what submit` would write under `CONFIG.pc182`

Code below `koopmann_aziz/ext.py: guard_output` refuses to write anywhere but `EXT_FOLDER`
and never into the reproduction folders. No training or feature code reads `raw\flight_list.csv`
or a test-set `tow` column (audit-hook test `tests/test_leakage_modes.py`); the final mode stops if
the test flight table ever carries `tow` values.

## Laptop

```
C:\Users\azizf\venvs\Koopmann-Aziz-lj24\Scripts\python.exe        # 3.12.15, pins = environment/requirements_pc182.txt (+ pytest, laptop only)
python -m koopmann_aziz.synth --write-config                     # synthetic data in koopmann_aziz/_synth + config/CONFIG.laptop
python -m pytest                                                 # all tests (about 1.5 min)
powershell -ExecutionPolicy Bypass -File koopmann_aziz\run\run_lj.ps1 -Machine laptop -Python C:\Users\azizf\venvs\Koopmann-Aziz-lj24\Scripts\python.exe -MinFreeRamGB 1 -Extra "-n_estimators 200 -min_child_samples 5"
```

## pc182

From the repo folder `E:\Koopmann-Aziz\repos\prc_2024\team_likable_jelly_Koopmann-Aziz-ext`:

```
git pull
powershell -ExecutionPolicy Bypass -File koopmann_aziz\run\run_lj.ps1 -What val -Seeds 0
```

The script sets the venv, `TEMP` and caches on E:, checks RAM/disk/other trainings, runs a 2-day
smoke step, then the real run, and prints the block between
`===== KOOPMANN-AZIZ SUMMARY BEGIN =====` and `… END =====` (also saved in `ext\logs`).
Averaging seeds: `python -m koopmann_aziz.average --what final --variant baseline --seeds 0-19`.
