echnical Requirements

This document defines the non-negotiable technical constraints for the Personal Finance Ingest & Reporting Tool.
If a choice conflicts with this document, the choice is wrong unless superseded by an ADR.

1. Runtime & environment
Language: Python 3.11+
Execution: Local machine only
Operating system: Any OS capable of running Python and pandas
Network: No network access required at runtime
User model: Single user
The system must run deterministically on a fresh clone with no external services.

2. Execution model
Mode: Batch CLI only
Invocation: User-initiated, synchronous execution
State:
Persistent state limited to:
range registry (state/ingested_ranges.csv; schema: account,start_date,end_date,source_file,ingested_at; append after every successful ingest)
No background processes
No daemons
No scheduled jobs
All side effects must be explicit and user-initiated.

3. Data handling & safety
Real financial data must never be committed to the repository
data/raw/ and state/ are git-ignored
CI must operate exclusively on committed sample data
All destructive operations must be:
explicit
opt-in
reversible where feasible (e.g., registry backup)

4. Dependencies
4.1 Required libraries
pandas — CSV ingest, normalization, grouping
pytest — testing
ruff (or equivalent) — linting/format enforcement

4.2 Standard library preferred
Use the Python standard library for:
CSV parsing (config files)
JSON parsing
Regex
Path handling
Argument parsing (argparse)

4.3 Explicitly excluded
Web frameworks
ORMs
Databases (SQLite, etc.)
Plugin systems
Background task frameworks

5. Performance expectations
Expected data volume:
Multiple years of monthly CSVs
Tens of thousands of rows total
Target runtime:
< 2 seconds for typical runs on local hardware
Memory usage:
Acceptable within pandas norms
No manual memory optimization required for MVP
Performance optimizations must not reduce correctness or clarity.

6. Error handling & exits
6.1 Hard failures (non-zero exit)
The system must fail immediately and clearly when:
- Filename contract is invalid
- Required CSV headers are missing (Date, Description, Amount, Transaction_Type)
- Dates cannot be parsed
- CSV dates exceed filename-declared range (hard fail)
- Ingested range overlaps prior ingested range
- Required config files are malformed
Error messages must include:
- File name
- Expected vs actual values
- Actionable guidance where possible

6.2 Warnings (exit zero)
Warnings are allowed (and expected) for:
Unknown Transaction_Type values
Uncategorized transactions
Split totals that do not match original amounts
Warnings must be visible in standard output.

7. Determinism & reproducibility
Given the same inputs and config, the system must:
produce the same outputs
produce the same warnings
No randomness
No time-dependent behavior except timestamps written to the range registry

8. Testability requirements
Core logic must be implemented as pure functions where possible
File I/O must be isolated at system boundaries
Sample datasets must exist for:
valid ingest
contract violations
overlap detection
unknown Transaction_Type handling

Tests must cover:
Filename parsing
Range validation
Overlap detection
Sign normalization
Categorization precedence
Split replacement logic

9. Quality gates
CI must run on all PRs to dev and main
Minimum test coverage: 70–80%
CI failures block merges to main

10. Documentation & governance
Development practices are defined in docs/dev_workflow.md.”
Architectural or behavioral changes require an ADR

Ingest behavior changes require updates to:

ESOD (if structural)

Technical Requirements (if constraints change)

Operational expectations must be reflected in the run-log template

11. Change policy

This document is stable by default.

Changes require:

An ADR

A clear justification tied to correctness, safety, or maintainability

Updated tests demonstrating compliance

## Related ADRs
- [0001](decisions/0001-use-poetry-and-ruff.md)
- [0002](decisions/0002-correctness-first-ingest.md)
- [0005](decisions/0005-local-single-user.md)


End of Technical Requirements