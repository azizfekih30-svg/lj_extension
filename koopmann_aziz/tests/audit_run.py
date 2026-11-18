"""Run a script with a Python audit hook that logs every file open (path, mode).

    python audit_run.py <log_file> <script.py> [args...]

Used by test_leakage.py to prove that training/feature code never opens the truth
files and never writes outside EXT_FOLDER."""
import os
import runpy
import sys

log_path = sys.argv[1]
script = sys.argv[2]
sys.argv = sys.argv[2:]
_log = open(log_path, "w", encoding="utf-8")


def hook(event, args):
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        path = os.fsdecode(args[0])
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else ""
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in "wax+") or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        _log.write(f"{'W' if writing else 'R'}\t{os.path.abspath(path)}\n")
        _log.flush()


sys.addaudithook(hook)
# pyarrow reads parquet through its own C++ filesystem layer, invisible to the hook: log
# pandas-level reads too
import pandas as pd  # noqa: E402

for name in ["read_parquet", "read_csv"]:
    orig = getattr(pd, name)

    def wrapped(path, *a, __orig=orig, **k):
        if isinstance(path, (str, os.PathLike)):
            _log.write(f"R\t{os.path.abspath(os.fspath(path))}\n")
            _log.flush()
        return __orig(path, *a, **k)
    setattr(pd, name, wrapped)

sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
runpy.run_path(script, run_name="__main__")
