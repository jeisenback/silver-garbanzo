import pandas as pd
from .contracts import validate_csv_headers, validate_csv_date_range, parse_filename_range, append_range_registry
from .overlap import check_range_overlap
import os

def ingest(csv_path, dry_run=False, registry_path=None):
    filename = os.path.basename(csv_path)
    range_info = parse_filename_range(filename)
    account = range_info.account
    start_date = range_info.start_date
    end_date = range_info.end_date
    # Load CSV
    df = pd.read_csv(csv_path)
    validate_csv_headers(list(df.columns))
    rows = df.to_dict(orient="records")
    validate_csv_date_range(rows, start_date, end_date)
    # Overlap check
    check_range_overlap(account, start_date, end_date, registry_path)
    # Dry-run: do not write registry
    if dry_run:
        print(f"[DRY-RUN] Would append to registry: {account}, {start_date.date()}-{end_date.date()}, {filename}")
        return True
    # Write registry
    append_range_registry(account, start_date, end_date, filename, registry_path)
    print(f"Ingested: {filename} ({start_date.date()}-{end_date.date()})")
    return True
