# Sample Data for CI and Contract Testing

This directory contains synthetic CSV files for contract validation, edge case testing, and CI workflows. Each file is safe to commit and contains only fabricated data.

## Files
- `checking__2026-01.csv`: Valid monthly file for contract validation
- `checking__2026-01-15__2026-02-14.csv`: Valid explicit range file for contract validation
- `checking__2026-01.csv.out_of_range`: Contains a date outside the filename range (contract violation)
- `checking__2026-01.csv.overlap`: Overlap scenario for same account (overlap detection)
- `checking__2026-01-unknown-type.csv`: Contains unknown Transaction_Type value (warning scenario)

See issue #16 for acceptance criteria and test coverage requirements.
