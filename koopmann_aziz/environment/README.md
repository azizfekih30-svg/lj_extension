`requirements_pc182.txt`: `pip freeze` of the pc182 venv `Koopmann-Aziz-lj24` (Python 3.12.15), 2026-11-18.

Laptop venv (identical pins, checked with a sorted diff of the freezes):

    python -m pip install --user uv
    python -m uv python install 3.12.15
    python -m uv venv --python 3.12.15 C:\Users\azizf\venvs\Koopmann-Aziz-lj24
    python -m uv pip install --python C:\Users\azizf\venvs\Koopmann-Aziz-lj24\Scripts\python.exe -r requirements_pc182.txt
    python -m uv pip install --python C:\Users\azizf\venvs\Koopmann-Aziz-lj24\Scripts\python.exe pytest==8.3.3   # laptop only

Not in the pc182 venv (would need approval and an exact pin before use there):
pytest (laptop only), catboost / xgboost (T2), optuna (T3).
