# Silver Garbanzo (Personal Finance Ingest & Reporting)

Local CLI tool to ingest bank transaction CSV exports, validate strict filename date ranges, categorize deterministically, and report spend/income by period and category.

## Purpose
- Prevent silent ingestion mistakes (bad ranges, overlaps, schema drift)
- Enable fast category iteration via editable rules and overrides
- Produce trustworthy summaries for personal finance review

## Scope
- Single-user
- Local-only execution
- Correctness-first: fail fast on unsafe inputs, warn on recoverable issues

## Data safety
Real financial data is never committed to this repository.
- Put real exports in `data/raw/` (gitignored)
- Use `data/sample/` for synthetic/redacted fixtures (committed later)
- Local ingest state lives in `state/` (gitignored)

## Status
Bootstrapping. No ingestion logic implemented yet.
