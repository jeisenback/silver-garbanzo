def test_cli_normal_ingest(tmp_path, monkeypatch):
    """Test CLI normal ingest (no profile, no dry-run) writes to registry and prints success."""
    import re
    from silver_garbanzo.cli import run_cli
    csv_path = tmp_path / "checking__2026-01.csv"
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    rules_path = config_dir / "rules.json"
    rules_path.write_text('[{"category": "test", "pattern": ".*"}]')
    monkeypatch.setenv("SILVER_GARBANZO_CONFIG_DIR", str(config_dir))
    # Set registry path to tmp_path for isolation
    registry_path = tmp_path / "ingested_ranges.csv"
    import io
    from contextlib import redirect_stdout
    monkeypatch.setenv("SILVER_GARBANZO_REGISTRY_PATH", str(registry_path))
    f = io.StringIO()
    with redirect_stdout(f):
        run_cli([str(csv_path)])
    output = f.getvalue()
    assert re.search(r"Ingested: checking__2026-01.csv \(2026-01-01-2026-01-31\)", output)
    # Registry should have header + 1 row
    with open(registry_path, "r", encoding="utf-8") as regf:
        lines = regf.readlines()
    assert len(lines) == 2
    assert "checking__2026-01.csv" in lines[1]
def test_cli_missing_required_argument(monkeypatch):
    """Test CLI exits with error if required csv_file argument is missing."""
    import pytest
    from silver_garbanzo.cli import run_cli
    import contextlib
    f = io.StringIO()
    with pytest.raises(SystemExit):
        with contextlib.redirect_stderr(f):
            run_cli([])
    output = f.getvalue()
    assert "usage:" in output or "the following arguments are required" in output
def test_cli_config_validation_failure(tmp_path, monkeypatch):
    """Test CLI exits with error if required config is missing or invalid."""
    import pytest
    import sys
    from silver_garbanzo.cli import run_cli
    csv_path = tmp_path / "checking__2026-01.csv"
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    # No config dir at all
    monkeypatch.setenv("SILVER_GARBANZO_CONFIG_DIR", str(tmp_path / "no_config"))
    f = io.StringIO()
    with pytest.raises(SystemExit):
        with redirect_stdout(f):
            run_cli([str(csv_path), "--dry-run"])
    output = f.getvalue()
    assert "[CONFIG VALIDATION FAILED]" in output
    assert "Missing required config: rules.json" in output

import io
import os
import re
import pandas as pd
from contextlib import redirect_stdout
import pytest
from silver_garbanzo.ingest import ingest
from silver_garbanzo.cli import run_cli


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

def test_cli_dry_run_outputs(tmp_path, monkeypatch):
    csv_path = tmp_path / "checking__2026-01.csv"
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    rules_path = config_dir / "rules.json"
    rules_path.write_text('[{"category": "test", "pattern": ".*"}]')
    monkeypatch.setenv("SILVER_GARBANZO_CONFIG_DIR", str(config_dir))
    registry_path = tmp_path / "ingested_ranges.csv"
    # Ensure registry file exists and is empty
    registry_path.write_text("account,start_date,end_date,source_file,ingested_at\n")
    monkeypatch.setenv("SILVER_GARBANZO_REGISTRY_PATH", str(registry_path))
    f = io.StringIO()
    with redirect_stdout(f):
        run_cli([str(csv_path), "--dry-run"])
    output = f.getvalue()
    assert "[DRY-RUN] No state or output files will be written." in output
    assert re.search(r"\[DRY-RUN\] Would append to registry: checking, 2026-01-01-2026-01-31, checking__2026-01.csv", output)

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

def test_cli_malformed_csv(tmp_path, monkeypatch):
    """Test CLI exits with error if the CSV file is malformed (bad header)."""
    import pytest
    from silver_garbanzo.cli import run_cli
    import io
    from contextlib import redirect_stdout
    # Create a malformed CSV (missing required headers)
    csv_path = tmp_path / "checking__2026-01.csv"
    csv_path.write_text("bad,header,only\n1,2,3\n")
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    rules_path = config_dir / "rules.json"
    rules_path.write_text('[{"category": "test", "pattern": ".*"}]')
    monkeypatch.setenv("SILVER_GARBANZO_CONFIG_DIR", str(config_dir))
    registry_path = tmp_path / "ingested_ranges.csv"
    monkeypatch.setenv("SILVER_GARBANZO_REGISTRY_PATH", str(registry_path))
    f = io.StringIO()
    with pytest.raises(SystemExit):
        with redirect_stdout(f):
            run_cli([str(csv_path)])
    output = f.getvalue()
    assert "header" in output.lower() or "invalid" in output.lower() or "schema" in output.lower()

def test_cli_profile_mode_outputs(tmp_path, monkeypatch):
    """Test CLI with --profile flag prints profiling output and succeeds."""
    import re
    from silver_garbanzo.cli import run_cli
    import io
    from contextlib import redirect_stdout
    csv_path = tmp_path / "checking__2026-01.csv"
    # Valid sample CSV
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    rules_path = config_dir / "rules.json"
    rules_path.write_text('[{"category": "test", "pattern": ".*"}]')
    monkeypatch.setenv("SILVER_GARBANZO_CONFIG_DIR", str(config_dir))
    registry_path = tmp_path / "ingested_ranges.csv"
    monkeypatch.setenv("SILVER_GARBANZO_REGISTRY_PATH", str(registry_path))
    f = io.StringIO()
    with redirect_stdout(f):
        run_cli([str(csv_path), "--profile"])
    output = f.getvalue()
    assert "[PROFILE] Profiling ingest performance and memory usage..." in output
    assert re.search(r"\[PROFILE\] Time elapsed: [0-9.]+ seconds", output)
    assert re.search(r"\[PROFILE\] Peak memory usage: [0-9.]+ KiB", output)

def test_cli_overlap_detection(tmp_path, monkeypatch):
    """Test CLI exits with error if ingested range overlaps an existing registry entry."""
    import pytest
    from silver_garbanzo.cli import run_cli
    import io
    from contextlib import redirect_stdout
    # Prepare registry with an existing range
    registry_path = tmp_path / "ingested_ranges.csv"
    registry_path.write_text(
        "account,start_date,end_date,source_file,ingested_at\n"
        "checking,2026-01-01,2026-01-31,checking__2026-01.csv,2026-02-01T00:00:00\n"
    )
    # Prepare a CSV with the same range
    csv_path = tmp_path / "checking__2026-01.csv"
    make_sample_csv(csv_path, ["2026-01-01", "2026-01-15", "2026-01-31"])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    rules_path = config_dir / "rules.json"
    rules_path.write_text('[{"category": "test", "pattern": ".*"}]')
    monkeypatch.setenv("SILVER_GARBANZO_CONFIG_DIR", str(config_dir))
    monkeypatch.setenv("SILVER_GARBANZO_REGISTRY_PATH", str(registry_path))
    f = io.StringIO()
    with pytest.raises(SystemExit):
        with redirect_stdout(f):
            run_cli([str(csv_path)])
    output = f.getvalue()
    assert "overlap" in output.lower() or "overlaps" in output.lower()

def test_cli_invalid_filename(tmp_path, monkeypatch):
    """Test CLI exits with error if the CSV filename does not match the expected pattern."""
    import pytest
    from silver_garbanzo.cli import run_cli
    import io
    from contextlib import redirect_stdout
    # Create a CSV with a bad filename
    csv_path = tmp_path / "badfile.csv"
    csv_path.write_text("Date,Description,Amount,Transaction_Type\n2026-01-01,desc,1.0,DEBIT\n")
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    rules_path = config_dir / "rules.json"
    rules_path.write_text('[{"category": "test", "pattern": ".*"}]')
    monkeypatch.setenv("SILVER_GARBANZO_CONFIG_DIR", str(config_dir))
    registry_path = tmp_path / "ingested_ranges.csv"
    monkeypatch.setenv("SILVER_GARBANZO_REGISTRY_PATH", str(registry_path))
    f = io.StringIO()
    with pytest.raises(SystemExit):
        with redirect_stdout(f):
            run_cli([str(csv_path)])
    output = f.getvalue()
    assert "filename" in output.lower() or "pattern" in output.lower() or "contract" in output.lower()
