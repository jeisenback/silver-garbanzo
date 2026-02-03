import pandas as pd

from silver_garbanzo.ingest import ingest


def make_sample_csv(path, dates):
    df = pd.DataFrame({
        "Date": dates,
        "Description": ["desc"] * len(dates),
        "Amount": ["1.0"] * len(dates),
        "Transaction_Type": ["DEBIT"] * len(dates)
    })
    df.to_csv(path, index=False)

def test_dry_run_does_not_write_registry(tmp_path):
    csv_path = tmp_path / "checking__2026-01.csv"
    registry_path = tmp_path / "ingested_ranges.csv"
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    # Create empty registry
    with open(registry_path, "w", encoding="utf-8") as f:
        f.write("account,start_date,end_date,source_file,ingested_at\n")
    ingest(str(csv_path), dry_run=True, registry_path=str(registry_path))
    # Registry should be unchanged
    with open(registry_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1  # Only header

def test_normal_ingest_writes_registry(tmp_path):
    csv_path = tmp_path / "checking__2026-01.csv"
    registry_path = tmp_path / "ingested_ranges.csv"
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    with open(registry_path, "w", encoding="utf-8") as f:
        f.write("account,start_date,end_date,source_file,ingested_at\n")
    ingest(str(csv_path), dry_run=False, registry_path=str(registry_path))
    # Registry should have header + 1 row
    with open(registry_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 2
    assert "checking__2026-01.csv" in lines[1]
