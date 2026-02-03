
"""
overlap.py — Overlap detection for ingested ranges.

This module provides logic to detect overlapping date ranges for account data during
ingestion. It ensures that no duplicate or conflicting data is ingested for the same account.
"""

import csv
import os
from datetime import datetime, timedelta


def check_range_overlap(
    account: str,
    start_date: datetime,
    end_date: datetime,
    registry_path: str = None
) -> None:
    """
    Check for overlapping ranges in the registry for the given account.
    Raises ValueError if overlap is detected, with details of the conflicting file and range.
    Touching edges (end == new_start or start == new_end) are allowed.
    """
    if registry_path is None:
        # Default to the canonical registry path if not provided
        registry_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'state',
            'ingested_ranges.csv',
        )
        registry_path = os.path.normpath(registry_path)
    if not os.path.isfile(registry_path):
        # If the registry does not exist, there can be no overlap
        return
    with open(registry_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only check for overlap with the same account
            if row['account'] != account:
                continue
            reg_start = datetime.strptime(row['start_date'], '%Y-%m-%d')
            reg_end = datetime.strptime(row['end_date'], '%Y-%m-%d')
            # Overlap logic: new_start <= existing_end AND new_end >= existing_start
            # This means the ranges touch or overlap in any way
            # Touching edges (adjacent, no overlap) are allowed:
            #   - new_end == existing_start - 1 day
            #   - new_start == existing_end + 1 day
            if (start_date <= reg_end and end_date >= reg_start):
                # Check for touching edge (adjacent, not overlapping)
                if (
                    end_date == reg_start - timedelta(days=1)
                    or start_date == reg_end + timedelta(days=1)
                ):
                    continue
                # If not just touching, this is a true overlap
                raise ValueError(
                    f"Range {start_date.date()} to {end_date.date()} for account '{account}' "
                    f"overlaps existing range {reg_start.date()} to {reg_end.date()} "
                    f"from file '{row['source_file']}'"
                )
