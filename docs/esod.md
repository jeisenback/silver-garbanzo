ESOD v3 — Personal Finance Ingest & Reporting Tool
1. Purpose

Define an engineering solution for a local, correctness-first CLI pipeline that ingests monthly or ranged bank CSVs under a strict filename contract, blocks overlaps, categorizes deterministically, supports manual splits, and produces period-based reports—while remaining simple, testable, and resistant to overengineering.

2. Guiding principles (non-negotiable)
2.1 DRY (practical)

Single definition of business rules:

filename → date range parsing

overlap detection

amount sign mapping

category precedence

One normalization pass. Downstream stages assume normalized inputs.

Config over code for extensibility (rules/overrides/splits).

2.2 SOLID (applied)

SRP: Each module has one reason to change.

OCP: New categories/rules/splits added without code changes.

LSP: Avoid inheritance; prefer functions.

ISP: Narrow function interfaces; no god-objects.

DIP: Pipeline depends on data/config passed in, not hardcoded paths.

2.3 Anti-goals

No plugin systems.

No frameworks.

No premature abstractions.

No classes unless there is state to protect.

3. Scope
In scope (MVP)

CSV ingest (monthly or explicit range)

Filename-declared date range enforcement

Overlap prevention via range registry

Amount sign normalization using Transaction_Type

Deterministic categorization (rules + overrides)

Manual splits for reporting

Period totals and period+category breakdown

Export cleaned stream

ADR + run-log templates

CI with quality gates

Out of scope (MVP)

Transaction-level dedupe

Persistent transaction ledger

Forecasting / recurrence detection

UI beyond CLI/CSV

Bank APIs

4. System architecture
4.1 Pipeline (primary pattern)

A linear, batch pipeline composed of pure-ish stages:

Discover inputs

Parse filename range

Validate overlap (registry)

Load CSV + validate header

Validate CSV dates within range

Normalize (description, amount sign)

Build fingerprint (for splits)

Categorize (overrides → rules)

Apply splits

Report + export

Append range to registry (atomic)

Each stage:

accepts a DataFrame + context

returns a DataFrame + warnings

does not perform I/O unless it is an edge stage

**Related ADRs:** [0002](decisions/0002-correctness-first-ingest.md), [0005](decisions/0005-local-single-user.md)


5. Module responsibilities (SRP boundaries)
contracts.py

Filename parsing

Date range validation

Overlap detection

Registry read/write (atomic)

normalize.py

Date parsing

contracts.py
	- Filename parsing
	- Date range validation
	- Registry read/write (atomic)
overlap.py
	- Range overlap detection (pure function, tested)
normalize.py
	- Date parsing
	- Amount parsing
	- Transaction_Type sign mapping
	- Description cleanup
	- Fingerprint generation
categorize.py
	- Load rules
	- Load overrides
	- Apply category precedence
splits.py
	- Load splits
	- Replace original rows for reporting
	- Validate split totals (warn)
report.py
	- Period totals
Uncategorized listing

CSV export

cli.py

Orchestration

Argument parsing

Exit codes

User-facing output

6. Canonical data schema (DRY anchor)

All downstream stages assume this schema after normalization:

Column	Type	Notes
date	datetime	Parsed, timezone-naive
description	string	Cleaned
amount	float	Signed
transaction_type	string	Raw
category	string	Assigned
fingerprint	string	Stable hash

Column names are defined once as constants.

7. Input contracts
7.1 CSV header (hard requirement)
Date,Description,Amount,Transaction_Type

7.2 Filename contract (hard requirement)

Supported:

<account>__YYYY-MM.csv

<account>__YYYY-MM-DD__YYYY-MM-DD.csv

Behavior:

Parse account + start/end dates

Fail on malformed names or invalid ranges

8. Range registry (overlap prevention)
File

All config files are validated on startup; malformed files cause hard failure with clear error reporting.
state/ingested_ranges.csv (gitignored)

Config files are loaded from `config/` and validated before any ingest or reporting.
Schema
account,start_date,end_date,source_file,ingested_at
Overrides (`config/overrides.csv`, substring; optional, validated if present)
Rules (`config/rules.json`, ordered regex; required, validated on startup)
Rules

`config/splits.csv` (optional, validated if present)
Overlap detection per account

Hard fail (exit non-zero) on:
- Invalid filename
- Missing CSV columns
- Unparseable dates
- CSV dates outside filename range
- Range overlap
- Unreadable files
- Malformed config files (rules.json, overrides.csv, splits.csv)

Append only after successful run

Atomic write

9. Normalization rules
9.1 Date parsing

Use pandas.to_datetime

Any unparseable date → hard fail

9.2 Amount parsing

Strip currency symbols, commas

Support parentheses negatives

9.3 Sign mapping (Strategy-lite)

Debit-like Transaction_Type → negative

Credit-like → positive

Unknown types:

fallback to numeric sign

emit warning with counts

Mapping is defined once.

10. Categorization
Priority

Overrides (overrides.csv, substring)

Rules (rules.json, ordered regex)

Uncategorized

Determinism

First match wins

No randomness

No cross-row inference

11. Splits (reporting only)
Input

splits.csv

fingerprint,category,amount

Behavior

If fingerprint appears:

exclude original row from reporting

include split rows

Warn if split totals ≠ original amount

No enforcement in MVP

12. Reporting
Frequencies

Weekly / Monthly / Quarterly / Yearly

Outputs

Totals by period (spend, income, net, count)

Totals by period + category

Uncategorized list

Optional cleaned CSV export (split-applied)

13. Error handling & exits
Hard fail (exit non-zero)

Invalid filename

Missing CSV columns

Unparseable dates

CSV dates outside filename range

Range overlap

Unreadable files

Warnings (exit zero)

Unknown Transaction_Type

Split mismatch totals

Uncategorized transactions present

14. Repo & workflow
Branching

main (stable)

dev (integration)

feat/*, hotfix/*

Data separation

data/raw/ (gitignored)

data/sample/ (committed)

state/ (gitignored)

15. CI & quality gates
Required checks

Lint (ruff)

Format check

Tests (pytest)

Coverage threshold (70–80%)

Required tests

Filename parsing

Range validation

Overlap detection

Sign mapping

Category precedence

Split replacement + warnings

Technical Requirements (next)
TR-1 Environment

Python 3.11+

Reproducible install via pyproject.toml + lockfile

No OS-specific assumptions

TR-2 CLI

One primary command

Flags:

--freq

--top-uncat

--export-clean

Deterministic output

TR-3 Performance

Handle several years of monthly CSVs in <2 seconds

Memory use acceptable for pandas in local execution

TR-4 Testability

Core logic implemented as pure functions

File I/O isolated to edges

Sample data committed for CI

TR-5 Maintainability

No duplicated business rules

No hidden state

Changes isolated to one module per concern

TR-6 Auditability

ADR framework present

Run-log template present

Registry records source files and timestamps

**Related ADRs:** [0002](decisions/0002-correctness-first-ingest.md), [0003](decisions/0003-filename-date-range-contract.md)
