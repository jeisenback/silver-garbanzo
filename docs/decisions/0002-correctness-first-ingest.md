# ADR 0002: Correctness-first ingest with hard failures

Status: Accepted  
Date: 2026-02-01

## Context
The tool ingests real financial data where silent errors (duplicates, misaligned ranges, schema drift) would produce misleading results that are difficult to detect later.

The user prefers explicit failures over permissive behavior that hides problems.

## Decision
The ingest pipeline will be correctness-first:
- Unsafe inputs cause hard failures (non-zero exit)
- Recoverable ambiguity produces explicit warnings
- No silent coercion or auto-correction of unsafe data

Hard failures include:
- Invalid filename date ranges
- CSV schema mismatches
- Date values exceeding declared ranges
- Overlapping ingest ranges

## Consequences
- Ingest is stricter and may require manual intervention
- Errors are detected early and locally
- Results can be trusted without downstream reconciliation

## Alternatives considered
- Permissive ingest with post-hoc validation: rejected due to high risk of silent error
- Automatic correction of ranges: rejected due to hidden assumptions
