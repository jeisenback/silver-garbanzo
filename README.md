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

### Phase A — Foundation (✅ COMPLETE)
- [x] Repository skeleton & branch strategy
- [x] Python runtime & dependencies pinned
- [x] CI workflow (placeholder lint/test)
- [x] ADR framework & documentation discipline
- [x] Data layout & safety conventions

### Phase B — Ingest Contract (🔄 IN PROGRESS)
- [x] Parse date range from filename
- [x] Validate CSV header schema (Date, Description, Amount, Transaction_Type)
- [x] Enforce filename-to-CSV date contract
- [x] Track ingested ranges in local registry
- [x] Atomic registry updates
- [x] Track & prevent overlaps (see `src/silver_garbanzo/overlap.py`)

### Phase C — Safety & Testing (⏳ PLANNED)
- [ ] Dry-run mode
- [ ] Profile mode
- [ ] Sample datasets & CI fixtures
- [ ] Config validation

## Quick Start

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
- Overlap detection is implemented in `src/silver_garbanzo/overlap.py` and enforced during ingest.
- Registry updates are atomic (write temp, replace original).
- All contract enforcement and overlap logic is covered by tests in `tests/test_contracts.py`.

## References
- [ESOD v3](docs/esod.md) — Complete system design
- [Epic breakdown](docs/epics.md) — Release planning
- [Branch strategy](docs/dev_workflow.md#branching) — Git workflow

