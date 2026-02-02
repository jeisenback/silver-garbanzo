import os
import pandas as pd
import subprocess
import sys
import re

def make_sample_csv(path, dates):
    df = pd.DataFrame({
        "Date": dates,
        "Description": ["desc"] * len(dates),
        "Amount": ["1.0"] * len(dates),
        "Transaction_Type": ["DEBIT"] * len(dates)
    })
    df.to_csv(path, index=False)

def test_profile_mode_outputs(tmp_path):
    csv_path = tmp_path / "checking__2026-01.csv"
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    cmd = [sys.executable, "-m", "silver_garbanzo.cli", str(csv_path), "--profile", "--dry-run"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert "[PROFILE] Profiling ingest performance and memory usage..." in result.stdout
    assert re.search(r"\[PROFILE\] Time elapsed: [0-9.]+ seconds", result.stdout)
    assert re.search(r"\[PROFILE\] Peak memory usage: [0-9.]+ KiB", result.stdout)
