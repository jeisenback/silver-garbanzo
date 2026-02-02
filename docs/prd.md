PRD v2 — Personal Finance Ingest & Reporting Tool (Single-User)
1. Product overview

A local, CLI-driven tool that ingests monthly or explicitly ranged bank transaction CSVs, validates them against a strict filename-based date contract, categorizes transactions using editable rules, supports manual splits for ambiguous merchants, and produces period-based spend/income reports.

The tool prioritizes data correctness, auditability, and iteration speed over automation or intelligence.

2. Problem statement
You manage personal finances using CSV exports from financial institutions. These exports are easy to mis-ingest:
overlapping date ranges
inconsistent signs
ambiguous merchants
repeated re-imports
Silent ingestion errors destroy trust in the output.

You need a system that fails loudly when inputs are unsafe, makes decisions explicit, and allows fast correction without rewriting history.

3. Goals
Primary goals
Prevent accidental overlap or double ingestion
Enforce a clear ingest contract using filenames
Produce trustworthy monthly (and other period) summaries
Enable rapid categorization fixes
Maintain a durable decision trail

Secondary goals

Keep the system simple enough to maintain solo

Make future dedupe or recurrence detection possible without rewrites

4. Non-goals (explicit)

Automatic transaction-level deduplication (v2)

Bank API integrations

Cloud sync or multi-user support

Automatic item-level categorization (Amazon, Walmart, etc.)

Forecasting or budgeting enforcement

5. User & operating context

User: Single user (you)
Environment: Local machine
Usage pattern:

Download one transaction log per month (or explicit range)

Run tool manually

Inspect outputs

Adjust rules / splits

Re-run

No background jobs. No daemons.

6. Input contract (critical)
6.1 Required CSV header (enforced)
The following headers are required and validated for every ingest:

	Date,Description,Amount,Transaction_Type

If any are missing, the ingest fails immediately with a clear error message.

6.2 Filename contract (hard requirement)

Each CSV filename must encode its date range.

Supported formats:

Monthly
<account>__YYYY-MM.csv


Example:

checking__2026-01.csv


Implicit range:

start = first day of month

end = last day of month

Explicit range
<account>__YYYY-MM-DD__YYYY-MM-DD.csv


Example:

checking__2026-01-15__2026-02-14.csv

6.3 Ingest validation rules

The ingest fails if any of the following are true:

- Filename does not match a supported pattern
- Any CSV date falls outside the filename-declared range (hard fail)

CSV contains dates outside the declared filename range

The declared range overlaps a previously ingested range for the same account

Dates or amounts cannot be parsed reliably

There is no silent fallback.

7. Overlap prevention (MVP approach)
7.1 Range registry

The system maintains a local registry:

state/ingested_ranges.csv

Schema:

account,start_date,end_date,source_file,ingested_at

7.2 Overlap definition

Two ranges overlap if:

new_start <= existing_end AND new_end >= existing_start


Touching edges (end on Jan 31, start on Feb 1) are allowed.

7.3 Behavior

Overlap → hard fail

Registry is appended only after successful ingest

This replaces transaction-level dedupe for MVP.

8. Categorization model
8.1 Category taxonomy (MVP)

Top-level categories:

Mortgage

Utilities

TV/Phone/Internet

Insurance

Auto: Loans

Credit Cards

Subscriptions: Music

Subscriptions: Other

Groceries

Transportation

Car Maintenance

Home Maintenance

Kids

Pets

Shopping: Amazon

Transfer

Uncategorized

8.2 Classification layers (priority order)

Overrides (overrides.csv)

substring contains match

Rules (rules.json)

ordered regex rules

Uncategorized

No ML. No fuzzy matching beyond regex.

9. Manual splits
9.1 Purpose

Handle merchants that represent multiple real-world categories without guessing.

9.2 Split definition file

splits.csv

Schema:

fingerprint,category,amount

9.3 Rules

Splits replace the original transaction in reporting only

Ledger / raw ingest is unchanged

Tool warns if split totals ≠ original transaction amount

No auto-balancing in MVP

10. Reporting
10.1 Supported periods

Weekly

Monthly

Quarterly

Yearly

10.2 Outputs

Totals by period (spend, income, net, count)

Totals by period + category

Uncategorized transaction list

Optional export of cleaned, categorized stream

No averages (explicitly removed).

11. Decision logging (mandatory)
11.1 Architectural Decision Records (ADRs)

Location:

docs/decisions/


Format:

0001-short-title.md


Each ADR includes:

Context

Decision

Alternatives considered

Consequences

Status

An index file lists all ADRs.

11.2 Operational run log

Location:

docs/run-log.md


Each run records:

Date

Files ingested

Date ranges

Any warnings

Any rule/split changes made

This is the audit trail.

12. Branch & release strategy
Branches

main — production/stable

dev — integration

feat/* — short-lived feature branches

hotfix/* — production fixes

Rules

No direct commits to main

main requires PR + CI

Releases are tagged from main

Dev vs prod data

Real CSVs live outside git (data/raw/)

Sample/redacted CSVs live in repo (data/sample/)

CI never touches real data

13. Quality gates & CI/CD (MVP)
Required checks

Lint (ruff)

Format check

Unit tests (pytest)

Coverage threshold (70–80%)

Must-have tests

Filename range parsing

Overlap detection logic

CSV range validation

Transaction_Type sign mapping

Rule vs override precedence

Split replacement logic

CI scope

Runs on PRs to dev and main

Uses sample data only

14. MVP success criteria

The MVP is successful if:

You cannot ingest an overlapping or malformed CSV by accident

Monthly reports are trustworthy without manual reconciliation

Categorization fixes take <2 minutes

Every non-obvious behavior has a logged decision

You are comfortable building v2 features on top without regret