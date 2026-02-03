
"""
cli.py — Command-line interface entry point.

This module provides the CLI for Silver Garbanzo, handling argument parsing, config validation,
and invoking the ingestion process. It is the user-facing entry point for all operations.
"""

import argparse
import os
import time
import tracemalloc

from .ingest import ingest


def main():
    parser = argparse.ArgumentParser(description="Silver Garbanzo CLI")
    parser.add_argument("csv_file", help="Path to CSV file to ingest")
    parser.add_argument("--dry-run", action="store_true", help="Run all validations but do not write any state or output files")
    parser.add_argument("--profile", action="store_true", help="Profile ingest performance and memory usage")
    args = parser.parse_args()

    # Validate config files before proceeding
    from .config_validation import validate_overrides_csv, validate_rules_json, validate_splits_csv
    config_dir = os.environ.get("SILVER_GARBANZO_CONFIG_DIR")
    if not config_dir:
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    errors = []
    # rules.json (required)
    rules_path = os.path.join(config_dir, "rules.json")
    if os.path.exists(rules_path):
        try:
            validate_rules_json(rules_path)
        except Exception as e:
            errors.append(str(e))
    else:
        errors.append("Missing required config: rules.json")
    # overrides.csv (optional)
    overrides_path = os.path.join(config_dir, "overrides.csv")
    if os.path.exists(overrides_path):
        try:
            validate_overrides_csv(overrides_path)
        except Exception as e:
            errors.append(str(e))
    # splits.csv (optional)
    splits_path = os.path.join(config_dir, "splits.csv")
    if os.path.exists(splits_path):
        try:
            validate_splits_csv(splits_path)
        except Exception as e:
            errors.append(str(e))
    # Report errors and exit if any
    if errors:
        print("[CONFIG VALIDATION FAILED]")
        for err in errors:
            print(f"  - {err}")
        exit(1)

    # Indicate dry-run mode
    if args.dry_run:
        print("[DRY-RUN] No state or output files will be written.")

    if args.profile:
        print("[PROFILE] Profiling ingest performance and memory usage...")
        tracemalloc.start()
        start_time = time.perf_counter()
        ingest(args.csv_file, dry_run=args.dry_run)
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"[PROFILE] Time elapsed: {end_time - start_time:.3f} seconds")
        print(f"[PROFILE] Peak memory usage: {peak / 1024:.1f} KiB")
    else:
        ingest(args.csv_file, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
