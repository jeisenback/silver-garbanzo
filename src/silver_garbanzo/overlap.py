import os
import csv
from datetime import datetime, timedelta

def check_range_overlap(account: str, start_date: datetime, end_date: datetime, registry_path: str = None) -> None:
    """
    Check for overlapping ranges in the registry for the given account.
    Raises ValueError if overlap is detected, with details of the conflicting file and range.
    Touching edges (end == new_start or start == new_end) are allowed.
    """
    if registry_path is None:
        registry_path = os.path.join(os.path.dirname(__file__), '..', '..', 'state', 'ingested_ranges.csv')
        registry_path = os.path.normpath(registry_path)
    if not os.path.isfile(registry_path):
        return  # No registry, no overlap
    with open(registry_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['account'] != account:
                continue
            reg_start = datetime.strptime(row['start_date'], '%Y-%m-%d')
            reg_end = datetime.strptime(row['end_date'], '%Y-%m-%d')
            # Overlap: new_start <= existing_end AND new_end >= existing_start
            # Touching edges allowed: (new_start == reg_end+1 or new_end == reg_start-1)
            if (start_date <= reg_end and end_date >= reg_start):
                # Touching edge check
                if end_date == reg_start - timedelta(days=1) or start_date == reg_end + timedelta(days=1):
                    continue
                raise ValueError(
                    f"Range {start_date.date()} to {end_date.date()} for account '{account}' overlaps "
                    f"existing range {reg_start.date()} to {reg_end.date()} from file '{row['source_file']}'"
                )
