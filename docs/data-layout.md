# Data Layout & Safety Conventions

This document describes the directory structure for data in the silver-garbanzo project and the safety rules that govern each directory.

## Directory Structure

```
data/
  raw/          ← Real bank data (gitignored)
  sample/       ← Sample/test data (committed)
state/          ← Operational state (gitignored)
```

---

## Directory Purposes

### `data/raw/` — Real Personal Financial Data

**Purpose:** Local storage for real bank transaction CSVs downloaded from financial institutions.

**Safety Rules:**
- **Gitignored:** Never committed to the repository.
- **Access:** Local-only; used only by the CLI running on your machine.
- **Retention:** Delete files after successful ingestion or retain locally as backup per your preference.
- **Audit:** All ingestions are logged in `state/ingested_ranges.csv` and in run-logs.

**Example contents:**
```
checking__2026-01.csv
checking__2026-02.csv
savings__2026-01.csv
```

### `data/sample/` — Sample & Test Data

**Purpose:** Committed sample data for CI, testing, and development without exposing real data.

**Safety Rules:**
- **Committed:** Included in git history; safe to share.
- **Synthetic:** Contains only fabricated or anonymized data (no real account numbers, balances, or merchants).
- **Usage:** Referenced in CI workflows, smoke tests, and documentation examples.
- **Format:** Mirrors the production CSV schema but with dummy values.

**Example contents:**
```
sample__2026-01.csv       ← Sample monthly data
sample-edge-cases.csv     ← Edge case test data (malformed dates, overlaps, etc.)
```

### `state/` — Operational State & Registry

**Purpose:** Local operational files that track ingestion history, configuration, and results.

**Safety Rules:**
- **Gitignored:** Never committed to the repository.
- **Atomic writes:** All state file updates are written atomically (all-or-nothing) to prevent corruption.
- **Local only:** Exists only on the user's machine.
- **Retention:** Preserved locally as the authoritative record of what has been ingested.

**Contents (directory structure):**
```
state/
  ingested_ranges.csv     ← Registry of ingested date ranges (prevents overlaps)
  run-logs/               ← Optional: individual run-log files per ingestion
    run-2026-01-15.log
    run-2026-02-10.log
  exports/                ← Output CSVs from the most recent run
    run-2026-02-10.csv
  rules.json              ← Category rules (local overrides or backups)
  splits.csv              ← Manual transaction splits (local edits)
  overrides.csv           ← Category overrides (local edits)
```

---

## Data Safety Principles

### Correctness First

- The ingest pipeline is **fail-fast**: it rejects unsafe input rather than silently ignoring or auto-correcting.
- All ingestion decisions are logged in the run-log for auditability.

### Immutability of Registry

- Once a range is recorded in `state/ingested_ranges.csv`, it is never deleted or modified.
- New ranges are only appended; the registry is the source of truth for what has been ingested.
- Atomic writes ensure the registry is never left in an inconsistent state.

### No Silent Data Mutation

- Real data (`data/raw/`) is never modified by the tool.
- Sample data (`data/sample/`) is never written to during normal operation.
- State files (`state/`) are only modified with explicit user intent (i.e., during a successful ingest run).

### Separation of Concerns

- **Real data** stays in `data/raw/`; tool reads but never modifies.
- **Test/sample data** in `data/sample/` is committed alongside code for reproducibility.
- **Operational state** in `state/` is local and gitignored; each user maintains their own ingestion history.

---

## Git Ignore Rules

The `.gitignore` file ensures:

```
# Real data (never committed)
data/raw/
data/raw/**

# Operational state (never committed)
state/
state/**

# Except: maintain .gitkeep files so directories are tracked
# (add exceptions as needed)
```

The `data/sample/` directory is **not** gitignored; all sample data is committed.

---

## Quick Reference

| Directory | Gitignored | Purpose | Example |
|-----------|-----------|---------|---------|
| `data/raw/` | ✅ Yes | Real bank CSVs | `checking__2026-01.csv` |
| `data/sample/` | ❌ No | Sample/test data | `sample__2026-01.csv` |
| `state/` | ✅ Yes | Ingestion registry & state | `ingested_ranges.csv` |

---

## Usage Examples

### Adding Real Data
1. Download a transaction CSV from your bank.
2. Place it in `data/raw/` (e.g., `checking__2026-01.csv`).
3. Run the ingest tool:
   ```bash
   silver-garbanzo ingest --freq monthly
   ```

### Adding Sample Data
1. Create a sample CSV in `data/sample/` with dummy data.
2. Add it to git:
   ```bash
   git add data/sample/sample-new.csv
   git commit -m "test: add sample data for edge case testing"
   ```

### Checking Ingestion History
1. View the registry to see what has been ingested:
   ```bash
   cat state/ingested_ranges.csv
   ```

---

## Troubleshooting

**Q: I accidentally committed real data to `data/raw/`. What do I do?**

A: Immediately revert the commit and purge the data from git history:
```bash
git reset HEAD <file>
git checkout -- <file>
git rm --cached <file>
git commit --amend -m "Revert: accidentally committed real data"
```

Then ensure `data/raw/` is in `.gitignore`.

**Q: The registry is missing or corrupted. Can I recover?**

A: `state/ingested_ranges.csv` is local and not backed up by git. If lost:
- Regenerate it manually with known ingested ranges, or
- Carefully re-ingest only new data and let the tool rebuild the registry.
- Always keep local backups of `state/` outside the repo if critical.

**Q: Can I share my `state/` directory with another user?**

A: Not recommended. Each user maintains their own ingestion history and local config (`rules.json`, `splits.csv`, `overrides.csv`). Share the committed data (`data/sample/`) and documented rules instead.

---

## References

- [.gitignore](../../.gitignore) — Data safety ignore rules
- [docs/dev_workflow.md](../dev_workflow.md) — Data safety rules in workflow
- [docs/esod.md](../esod.md#data-separation) — System design reference

### Dry-run Mode

- When running with `--dry-run`, no files in `state/` or `data/sample/` are written or modified.
- All contract checks, validations, and warnings are performed as normal.
- Output indicates dry-run status and what would have changed.
