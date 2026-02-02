# Run Log (Manual Ingestion)

Use this template to record a manual ingestion run. Each run should be appended as a new entry in a single file or stored as a separate run file under `state/run-logs/` depending on your team's preference.

---

## Run: YYYY-MM-DD HH:MM UTC

- **Operator:** [name or initials]
- **Date:** YYYY-MM-DD
- **Files ingested:**
  - `filename1.csv` (source description)
  - `filename2.csv`

- **Declared ranges:**
  - `filename1.csv`: 2024-01-01 → 2024-01-31
  - `filename2.csv`: 2024-02-01 → 2024-02-28

- **Warnings / Notes:**
  - Unknown `Transaction_Type` values: 3 rows (see details below)
  - CSV dates outside declared range: 0 rows
  - Overlap detection: none / overlap with `state/ingested_ranges.csv` on account XYZ

- **Rule changes / Split edits applied during run:**
  - `rules.json` changed: added regex `...` → category `Groceries` (brief rationale)
  - `splits.csv` updated: fingerprint `abc123` split into 2 rows (total preserved)

- **Validation checks performed:**
<<<<<<< HEAD
  - Header validation (Date, Description, Amount, Transaction_Type): passed/failed
  - Date parsing (filename range): passed/failed
  - Amount normalization: passed/failed
  - Split totals match original: yes/no (if no, explain)

- **Post-run actions:**
  - `state/ingested_ranges.csv` appended: yes/no (audit registry for all prior ingests; updates are atomic and never leave partial writes)
  - Exports written to: `state/exports/run-YYYY-MM-DD.csv`
  - PR/Issue created for manual follow-up: #[number]

### Details
- Attach or paste small samples of warnings, diffs, or rows requiring follow-up here.

---

## Usage / Guidance
- Record every manual ingestion run to preserve an audit trail.
- Include any temporary rule/split changes and link the PR or file that contains the change.
- If a run triggers warnings that require follow-up, reference the issue or PR created.

## Acceptance
- Template exists (this file).
- Usage guidance is documented above.

