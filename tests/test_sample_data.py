import os

import pandas as pd
import pytest

from silver_garbanzo.contracts import (
    parse_filename_range,
    validate_csv_date_range,
    validate_csv_headers,
)


def load_sample_csv(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample', filename)
    df = pd.read_csv(path, comment='#')
    return df

def test_valid_monthly_sample():
    df = load_sample_csv('checking__2026-01.csv')
    validate_csv_headers(list(df.columns))
    rows = df.to_dict(orient='records')
    info = parse_filename_range('checking__2026-01.csv')
    validate_csv_date_range(rows, info.start_date, info.end_date)

def test_valid_explicit_range_sample():
    df = load_sample_csv('checking__2026-01-15__2026-02-14.csv')
    validate_csv_headers(list(df.columns))
    rows = df.to_dict(orient='records')
    info = parse_filename_range('checking__2026-01-15__2026-02-14.csv')
    validate_csv_date_range(rows, info.start_date, info.end_date)

def test_out_of_range_sample():
    df = load_sample_csv('checking__2026-01.csv.out_of_range')
    validate_csv_headers(list(df.columns))
    rows = df.to_dict(orient='records')
    info = parse_filename_range('checking__2026-01.csv')
    with pytest.raises(ValueError, match='outside filename-declared range'):
        validate_csv_date_range(rows, info.start_date, info.end_date)

def test_unknown_transaction_type_sample():
    df = load_sample_csv('checking__2026-01-unknown-type.csv')
    validate_csv_headers(list(df.columns))
    assert 'REFUND' in df['Transaction_Type'].values

# Overlap scenario is tested via ingest logic and registry, not pure contract validation
