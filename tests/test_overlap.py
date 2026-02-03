
import csv
from datetime import datetime

import pytest

from silver_garbanzo.overlap import check_range_overlap


def write_registry(rows, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['account', 'start_date', 'end_date', 'source_file', 'ingested_at'])
        writer.writerows(rows)

def test_no_overlap(tmp_path):
    registry = tmp_path / 'ingested_ranges.csv'
    rows = [
        ['checking', '2026-01-01', '2026-01-31', 'file1.csv', '2026-02-01T00:00:00Z']
    ]
    write_registry(rows, registry)
    # New range after existing
    check_range_overlap('checking', datetime(2026,2,1), datetime(2026,2,28), str(registry))
    # New range before existing
    check_range_overlap('checking', datetime(2025,12,1), datetime(2025,12,31), str(registry))

def test_touching_edges(tmp_path):
    registry = tmp_path / 'ingested_ranges.csv'
    rows = [
        ['checking', '2026-01-01', '2026-01-31', 'file1.csv', '2026-02-01T00:00:00Z']
    ]
    write_registry(rows, registry)
    # Touching after
    check_range_overlap('checking', datetime(2026,2,1), datetime(2026,2,28), str(registry))
    # Touching before
    check_range_overlap('checking', datetime(2025,12,1), datetime(2025,12,31), str(registry))

def test_overlap_raises(tmp_path):
    registry = tmp_path / 'ingested_ranges.csv'
    rows = [
        ['checking', '2026-01-01', '2026-01-31', 'file1.csv', '2026-02-01T00:00:00Z']
    ]
    write_registry(rows, registry)
    # Overlap inside
    with pytest.raises(ValueError):
        check_range_overlap('checking', datetime(2026,1,15), datetime(2026,2,15), str(registry))
    # Overlap start
    with pytest.raises(ValueError):
        check_range_overlap('checking', datetime(2025,12,15), datetime(2026,1,15), str(registry))
    # Overlap end
    with pytest.raises(ValueError):
        check_range_overlap('checking', datetime(2026,1,15), datetime(2026,2,15), str(registry))
    # Overlap exact
    with pytest.raises(ValueError):
        check_range_overlap('checking', datetime(2026,1,1), datetime(2026,1,31), str(registry))

def test_different_account(tmp_path):
    registry = tmp_path / 'ingested_ranges.csv'
    rows = [
        ['checking', '2026-01-01', '2026-01-31', 'file1.csv', '2026-02-01T00:00:00Z']
    ]
    write_registry(rows, registry)
    # Different account should not raise
    check_range_overlap('savings', datetime(2026,1,1), datetime(2026,1,31), str(registry))

    def test_no_registry_file(tmp_path):
        # Should not raise if registry file does not exist
        missing_registry = tmp_path / 'does_not_exist.csv'
        check_range_overlap('checking', datetime(2026,1,1), datetime(2026,1,31), str(missing_registry))

    def test_default_registry_path(monkeypatch, tmp_path):
        # Patch os.path.join and os.path.normpath to use a temp file
        dummy_registry = tmp_path / 'ingested_ranges.csv'
        rows = [
            ['checking', '2026-01-01', '2026-01-31', 'file1.csv', '2026-02-01T00:00:00Z']
        ]
        write_registry(rows, dummy_registry)
        def fake_join(*args):
            return str(dummy_registry)
        def fake_normpath(path):
            return path
        monkeypatch.setattr('os.path.join', fake_join)
        monkeypatch.setattr('os.path.normpath', fake_normpath)
        # Should not raise for non-overlapping range
        check_range_overlap('checking', datetime(2026,2,1), datetime(2026,2,28))


    def test_missing_file_default_path(tmp_path):
        # Simulate missing registry file with default path
        import importlib
        mod = importlib.import_module('silver_garbanzo.overlap')
        orig_file = mod.__file__
        mod.__file__ = str(tmp_path / 'fake_overlap.py')
        try:
            check_range_overlap('checking', datetime(2026,1,1), datetime(2026,1,31))
        finally:
            mod.__file__ = orig_file


    def test_touching_edge_continue(tmp_path):
        registry = tmp_path / 'ingested_ranges.csv'
        rows = [
            ['checking', '2026-01-01', '2026-01-31', 'file1.csv', '2026-02-01T00:00:00Z']
        ]
        write_registry(rows, registry)
        # Touching after (start_date == reg_end + 1)
        check_range_overlap('checking', datetime(2026,2,1), datetime(2026,2,28), str(registry))
        # Touching before (end_date == reg_start - 1)
        check_range_overlap('checking', datetime(2025,12,1), datetime(2025,12,31), str(registry))
