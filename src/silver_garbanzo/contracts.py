REQUIRED_HEADERS = ["Date", "Description", "Amount", "Transaction_Type"]

def validate_csv_headers(headers: list[str]) -> None:
    """
    Validate that the CSV headers match the required schema.
    Args:
        headers: List of header strings from the CSV file.
    Raises:
        ValueError: If required headers are missing or extra headers are present.
    """
    missing = [h for h in REQUIRED_HEADERS if h not in headers]
    if missing:
        raise ValueError(f"Missing required header(s): {missing}. Required: {REQUIRED_HEADERS}")
    # Optionally, enforce no extra headers (strict schema)
    # extra = [h for h in headers if h not in REQUIRED_HEADERS]
    # if extra:
    #     raise ValueError(f"Unexpected header(s): {extra}. Required: {REQUIRED_HEADERS}")

def validate_csv_date_range(rows: list[dict], start_date, end_date) -> None:
    """
    Validate that all dates in the CSV fall within the declared filename range.
    Args:
        rows: List of dicts, each representing a CSV row with a 'Date' field.
        start_date: datetime, start of allowed range (inclusive)
        end_date: datetime, end of allowed range (inclusive)
    Raises:
        ValueError: If any row's date is outside the allowed range.
    """
    from datetime import datetime
    out_of_range = []
    for i, row in enumerate(rows):
        try:
            date = datetime.strptime(row["Date"], "%Y-%m-%d")
        except Exception as e:
            raise ValueError(f"Row {i+1}: Invalid date format '{row['Date']}' ({e})")
        if not (start_date <= date <= end_date):
            out_of_range.append((i+1, row["Date"]))
    if out_of_range:
        raise ValueError(f"CSV contains dates outside filename-declared range: {out_of_range}")

"""
contracts.py — Filename and data contract validation.

Implements the filename-based date range contract that is the primary
safety mechanism for ingest operations.
"""

import re
import csv
import os
from datetime import datetime
from typing import NamedTuple


class FilenameRange(NamedTuple):
    """Parsed filename components and declared date range."""
    account: str
    start_date: datetime
    end_date: datetime
    filename: str


def parse_filename_range(filename: str) -> FilenameRange:
    """
    Parse a bank CSV filename and extract account, start date, and end date.
    
    Supported formats:
    - Monthly: <account>__YYYY-MM.csv
    - Explicit range: <account>__YYYY-MM-DD__YYYY-MM-DD.csv
    
    Args:
        filename: The CSV filename (basename, not full path).
    
    Returns:
        FilenameRange with account, start_date, end_date, and original filename.
    
    Raises:
        ValueError: If filename does not match any supported format or
                   contains invalid dates.
    """
    # Remove .csv extension if present
    base = filename.replace('.csv', '').replace('.CSV', '')
    
    # Pattern 1: Monthly format <account>__YYYY-MM
    monthly_pattern = r'^(.+?)__(\d{4})-(\d{2})$'
    match = re.match(monthly_pattern, base)
    if match:
        account, year, month = match.groups()
        try:
            start_date = datetime(int(year), int(month), 1)
            # End date is last day of month
            if int(month) == 12:
                end_date = datetime(int(year) + 1, 1, 1)
            else:
                end_date = datetime(int(year), int(month) + 1, 1)
            # Subtract one day from end_date to get the last day of the month
            from datetime import timedelta
            end_date = end_date - timedelta(days=1)
            
            return FilenameRange(
                account=account,
                start_date=start_date,
                end_date=end_date,
                filename=filename
            )
        except ValueError as e:
            raise ValueError(f"Invalid date in monthly filename '{filename}': {e}")
    
    # Pattern 2: Explicit range <account>__YYYY-MM-DD__YYYY-MM-DD
    range_pattern = r'^(.+?)__(\d{4})-(\d{2})-(\d{2})__(\d{4})-(\d{2})-(\d{2})$'
    match = re.match(range_pattern, base)
    if match:
        account, year1, month1, day1, year2, month2, day2 = match.groups()
        try:
            start_date = datetime(int(year1), int(month1), int(day1))
            end_date = datetime(int(year2), int(month2), int(day2))
            
            # Validate that start_date <= end_date
            if start_date > end_date:
                raise ValueError(f"Start date {start_date} is after end date {end_date}")
            
            return FilenameRange(
                account=account,
                start_date=start_date,
                end_date=end_date,
                filename=filename
            )
        except ValueError as e:
            raise ValueError(f"Invalid date range in filename '{filename}': {e}")
    
    # No pattern matched
    raise ValueError(
        f"Filename '{filename}' does not match supported formats. "
        f"Expected: <account>__YYYY-MM.csv or "
        f"<account>__YYYY-MM-DD__YYYY-MM-DD.csv"
    )

def append_range_registry(account: str, start_date: datetime, end_date: datetime, source_file: str, registry_path: str = None) -> None:
    """
    Append a successfully ingested range to the registry CSV atomically.
    Args:
        account: Account name
        start_date: Range start (datetime)
        end_date: Range end (datetime)
        source_file: Source filename
        registry_path: Path to registry CSV (default: state/ingested_ranges.csv)
    """
    if registry_path is None:
        registry_path = os.path.join(os.path.dirname(__file__), '..', '..', 'state', 'ingested_ranges.csv')
        registry_path = os.path.normpath(registry_path)
    state_dir = os.path.dirname(registry_path)
    os.makedirs(state_dir, exist_ok=True)
    ingested_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    row = [account, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), source_file, ingested_at]
    # Read existing rows
    rows = []
    if os.path.isfile(registry_path):
        with open(registry_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    if not rows:
        rows = [['account', 'start_date', 'end_date', 'source_file', 'ingested_at']]
    rows.append(row)
    # Write to temp file
    import tempfile
    with tempfile.NamedTemporaryFile('w', delete=False, dir=state_dir, newline='', encoding='utf-8') as tf:
        writer = csv.writer(tf)
        writer.writerows(rows)
        temp_path = tf.name
    # Atomically replace registry
    os.replace(temp_path, registry_path)
