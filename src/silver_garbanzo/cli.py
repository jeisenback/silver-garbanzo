import argparse
import time
import tracemalloc
from .ingest import ingest

def main():
    parser = argparse.ArgumentParser(description="Silver Garbanzo CLI")
    parser.add_argument("csv_file", help="Path to CSV file to ingest")
    parser.add_argument("--dry-run", action="store_true", help="Run all validations but do not write any state or output files")
    parser.add_argument("--profile", action="store_true", help="Profile ingest performance and memory usage")
    args = parser.parse_args()

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
