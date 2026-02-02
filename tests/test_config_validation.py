import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from silver_garbanzo.config_validation import (
    validate_rules_json,
    validate_overrides_csv,
    validate_splits_csv,
)

def test_valid_rules_json(tmp_path):
    path = tmp_path / "rules.json"
    path.write_text('[{"category": "groceries", "pattern": "grocery"}]')
    validate_rules_json(str(path))

def test_invalid_rules_json_not_list(tmp_path):
    path = tmp_path / "rules.json"
    path.write_text('{"category": "groceries", "pattern": "grocery"}')
    with pytest.raises(RuntimeError):
        validate_rules_json(str(path))

def test_invalid_rules_json_bad_regex(tmp_path):
    path = tmp_path / "rules.json"
    path.write_text('[{"category": "groceries", "pattern": "["}]')
    with pytest.raises(RuntimeError):
        validate_rules_json(str(path))

def test_valid_overrides_csv(tmp_path):
    path = tmp_path / "overrides.csv"
    path.write_text("key,category\n123,groceries\n")
    validate_overrides_csv(str(path))

def test_invalid_overrides_csv_headers(tmp_path):
    path = tmp_path / "overrides.csv"
    path.write_text("bad,header\n123,groceries\n")
    with pytest.raises(RuntimeError):
        validate_overrides_csv(str(path))

def test_valid_splits_csv(tmp_path):
    path = tmp_path / "splits.csv"
    path.write_text("fingerprint,category,amount\nabc,groceries,42.5\n")
    validate_splits_csv(str(path))

def test_invalid_splits_csv_headers(tmp_path):
    path = tmp_path / "splits.csv"
    path.write_text("bad,header,amount\nabc,groceries,42.5\n")
    with pytest.raises(RuntimeError):
        validate_splits_csv(str(path))

def test_invalid_splits_csv_amount(tmp_path):
    path = tmp_path / "splits.csv"
    path.write_text("fingerprint,category,amount\nabc,groceries,notafloat\n")
    with pytest.raises(RuntimeError):
        validate_splits_csv(str(path))
