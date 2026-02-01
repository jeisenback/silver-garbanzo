SETUP-SRS-0.1 Repository skeleton

Delivers: a place to work without chaos

Includes

GitHub repo created

.gitignore (Python, venv, data/raw/, state/)

Base README with project intent

Why releasable

You can now safely start work

No future work invalidates this

SETUP-SRS-0.2 Branch strategy enforced

Delivers: safety boundary between work and truth

Includes

main and dev branches

Branch protection on main

PRs required for main

Why releasable

Prevents accidental “prod” breakage immediately

SETUP-SRS-0.3 Python runtime & tooling pinned

Delivers: reproducible environment

Includes

pyproject.toml with:

Python version

dependencies (pandas, etc.)

Lockfile committed

Minimal src/ layout

Why releasable

Eliminates environment drift before logic exists

SETUP-SRS-0.4 CI skeleton (allowed to fail initially)

Delivers: future enforcement point

Includes

GitHub Actions workflow file

Steps:

install

lint placeholder

test placeholder

Why releasable

Establishes where quality gates will live

Can evolve without breaking behavior

SETUP-SRS-0.5 Decision logging framework

Delivers: memory outside your head

Includes

docs/decisions/

ADR template

ADR index

Why releasable

Prevents silent architectural drift

SETUP-SRS-0.6 Run log template

Delivers: operational audit trail

Includes

docs/run-log.md

Clear template

Why releasable

Ensures every ingest is traceable

SETUP-SRS-0.7 Data layout conventions

Delivers: file hygiene and safety

Includes

data/raw/ (gitignored)

data/sample/ (committed)

state/ (gitignored)

docs/data-layout.md

Why releasable

Prevents real data leaks

Prevents dev/prod confusion

POST-SETUP STORIES (REAL FUNCTIONALITY)

Once setup is done, every remaining story adds or tightens behavior.

INGEST CONTRACT
SRS-1.1 CSV header validation

Fail fast if headers don’t match required schema.

SRS-1.2 Filename range parsing

Parse <account>__YYYY-MM.csv and <account>__YYYY-MM-DD__YYYY-MM-DD.csv.

SRS-1.3 CSV date range validation

Fail if CSV dates fall outside filename-declared range.

OVERLAP PREVENTION
SRS-2.1 Range registry creation

Create and append state/ingested_ranges.csv after success.

SRS-2.2 Overlap detection

Fail ingest if new range overlaps existing range.

INGEST & NORMALIZATION
SRS-3.1 Minimal ingest echo

Print counts, date range, account.

SRS-3.2 Amount sign normalization

Apply Transaction_Type mapping.

CATEGORIZATION
SRS-4.1 Rules-based categorization

Apply ordered regex rules.

SRS-4.2 Overrides

Apply substring overrides.

SRS-4.3 Uncategorized output

Print uncategorized list.

SPLITS
SRS-5.1 Split replacement

Replace original txn with split rows.

SRS-5.2 Split validation warning

Warn on mismatched totals.

REPORTING
SRS-6.1 Monthly totals

Spend / income / net.

SRS-6.2 Monthly by category

Primary MVP output.

SRS-6.3 Export cleaned CSV

Portability.

CLI + QUALITY
SRS-7.1 Single command pipeline

One CLI invocation.

SRS-8.1 Ingest invariant tests

Filename, ranges, overlap.

SRS-8.2 Categorization & split tests

Rules, overrides, splits.

SRS-8.3 Coverage gate + v0.1.0

Freeze behavior.