# Silver Garbanzo (Personal Finance Ingest & Reporting)

![CI](https://github.com/jeisenback/silver-garbanzo/actions/workflows/ci.yml/badge.svg?branch=dev)

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

See [docs/data-layout.md](docs/data-layout.md) for detailed conventions.

## Documentation

### Core References
- **[ESOD v3](docs/esod.md)** — Engineering solution & architecture
- **[PRD](docs/prd.md)** — Product requirements & user context
- **[Technical Requirements](docs/technical_requirements.md)** — Implementation constraints

### Workflow & Development
- **[Development Workflow](docs/dev_workflow.md)** — Branching, PRs, CI gates
- **[Data Layout](docs/data-layout.md)** — Directory structure & safety rules
- **[Copilot Instructions](docs/copilot_instructions.md)** — AI assistant guidelines

### Decisions & Operations
- **[Architecture Decision Records](docs/decisions/)** — Design decisions (ADRs)
- **[Run Log Template](docs/run-log.md)** — Manual ingestion audit trail

## Status

### Phase A — Foundation (COMPLETE)
- [x] Repository skeleton & branch strategy
- [x] Python runtime & dependencies pinned
- [x] CI workflow (placeholder lint/test)
- [x] ADR framework & documentation discipline
- [x] Data layout & safety conventions

### Phase B — Ingest Contract (IN PROGRESS)
- [x] Parse date range from filename
- [x] Validate CSV header schema (Date, Description, Amount, Transaction_Type)
- [x] Enforce filename-to-CSV date contract
- [x] Track ingested ranges in local registry
- [x] Atomic registry updates
- [x] Track & prevent overlaps (see src/silver_garbanzo/overlap.py)

### Phase C — Safety & Testing (IN PROGRESS)
- [x] Dry-run mode (--dry-run CLI flag: validates all contracts, prevents state/output writes)
- [x] Profile mode (--profile CLI flag: reports ingest timing and peak memory usage)
- [x] Sample datasets & CI fixtures
- [x] Config validation (rules.json, overrides.csv, splits.csv; hard failure on malformed files, clear error reporting)

## Quick Start
## Config Files

Config files live in the `config/` directory:
- `rules.json` (required): List of objects with `category` and `pattern` (regex, validated on startup)
- `overrides.csv` (optional): Must have headers `key,category`
- `splits.csv` (optional): Must have headers `fingerprint,category,amount` (amount must parse as float)


### Environment Variable Override

You can override the config directory location by setting the environment variable `SILVER_GARBANZO_CONFIG_DIR`. This is useful for testing and CI:

```bash
export SILVER_GARBANZO_CONFIG_DIR=/path/to/custom/config
poetry run python -m silver_garbanzo.cli data/sample/checking__2026-01.csv --dry-run
```

Malformed config files cause hard failure with clear error messages. Missing optional files do not fail unless required for the operation.


```bash
# Install dependencies
poetry install

# Run lint
poetry run ruff check .

# Run tests
poetry run pytest -q
```

See [docs/dev_workflow.md](docs/dev_workflow.md) for full development instructions.

## Overlap Detection & Registry
## Error Handling

All config validation errors are reported with file name and specific details. The CLI exits with a non-zero status on any malformed config file.
- Overlap detection is implemented in `src/silver_garbanzo/overlap.py` and enforced during ingest.
- Registry updates are atomic (write temp, replace original).
- All contract enforcement and overlap logic is covered by tests in `tests/test_contracts.py`.

## References
- [ESOD v3](docs/esod.md) — Complete system design
- [Epic breakdown](docs/epics.md) — Release planning
- [Branch strategy](docs/dev_workflow.md#branching) — Git workflow

