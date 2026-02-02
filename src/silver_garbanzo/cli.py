import argparse
from .ingest import ingest

def main():
    parser = argparse.ArgumentParser(description="Silver Garbanzo CLI")
    parser.add_argument("csv_file", help="Path to CSV file to ingest")
    parser.add_argument("--dry-run", action="store_true", help="Run all validations but do not write any state or output files")
    # ...add other arguments as needed...
    args = parser.parse_args()

    # Indicate dry-run mode
    if args.dry_run:
        print("[DRY-RUN] No state or output files will be written.")
    ingest(args.csv_file, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
