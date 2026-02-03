
"""
ingest.py — Ingestion orchestration.

This module coordinates the ingestion process, including loading CSVs, validating
headers and date ranges, checking for overlaps, and updating the registry. It acts as
the main entry point for ingest operations, delegating validation and contract logic to
other modules.
"""

import os

import pandas as pd

from .contracts import (
    append_range_registry,
    parse_filename_range,
    validate_csv_date_range,
    validate_csv_headers,
)
from .overlap import check_range_overlap


def ingest(csv_path, dry_run=False, registry_path=None):
    # Extract filename and parse the declared date range and account
    filename = os.path.basename(csv_path)
    range_info = parse_filename_range(filename)
    account = range_info.account
    start_date = range_info.start_date
    end_date = range_info.end_date
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    # Validate that the headers match the required schema
    validate_csv_headers(list(df.columns))
    # Convert DataFrame rows to dicts for validation
    rows = df.to_dict(orient="records")
    # Ensure all dates in the CSV are within the declared filename range
    validate_csv_date_range(rows, start_date, end_date)
    # Check for overlapping date ranges in the registry for this account
    check_range_overlap(account, start_date, end_date, registry_path)
    # If dry-run, do not write to the registry, just report what would happen
    if dry_run:
        print(
            f"[DRY-RUN] Would append to registry: {account}, "
            f"{start_date.date()}-{end_date.date()}, {filename}"
        )
        return True
    # Write the ingested range to the registry (atomic update)
    append_range_registry(account, start_date, end_date, filename, registry_path)
    print(f"Ingested: {filename} ({start_date.date()}-{end_date.date()})")
    return True
