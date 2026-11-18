# Experiment log (newest first)

Template:

```
## E-<nn> <short name>  (<date>)
Idea / hypothesis:
Code: <branch, commit, files>
Setup: device, bins, seeds, validation split file
Validation RMSE: <mean ± std over seeds> vs baseline <...>  (paired diff + CI if available)
Final-set RMSE (only if the idea is finished): ...
Runtime / peak RAM:
Verdict: keep / drop / inconclusive, one sentence why
Deviations from team code:
```

## E-00 T0 setup  (2026-11-18)
Idea / hypothesis: infrastructure only; with all switches off the code must reproduce the team's model.
Code: koopmann-aziz-ext, T0 commits; `utils.py` (LJ_CONFIG), `features.py` (days=), `regression.py` (-what val/final), `koopmann_aziz/*`.
Setup: laptop only, synthetic data (`koopmann_aziz/synth.py`); validation split `koopmann_aziz/splits/val_days_seed0.txt`.
Validation RMSE: not run on pc182 yet.
Final-set RMSE: not run yet (target: 1610.60 kg, seed 0, CPU 511 bins).
Runtime / peak RAM: -
Verdict: pending the pc182 smoke run and baseline.
Deviations from team code: none in model, features or target. Checked on synthetic data: `-what final` predictions are bit-identical to the team's `-what submit`; `read_features` output identical to upstream `features.py`.
Notes:
- Laptop env: Python 3.12.15 (uv build) and all 119 pins identical to pc182 `pip freeze`; pytest 8.3.3 added on the laptop only.
- This branch starts from upstream fd8f0c4, not from the pc182 working copy (the user chose to build from upstream); `koopmann_aziz/run/check_repro_copy.ps1` does the diff against the pc182 copy.
