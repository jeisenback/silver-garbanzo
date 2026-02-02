# ADR 0003: Filename-declared date ranges as ingest contract

Status: Accepted  
Date: 2026-02-01

## Context
Bank statements often overlap in time and may be re-exported.
Relying on CSV contents alone makes it difficult to detect duplicates or partial re-ingests.

## Decision
Each CSV filename must declare the date range it covers.
The filename is treated as a contract that:
- defines the expected date bounds
- is validated against CSV contents
- is used for overlap detection

CSV rows outside the declared range cause ingest failure.

## Consequences
- File naming discipline is required
- Overlap detection becomes simple and deterministic
- No transaction-level deduplication is required for MVP

## Alternatives considered
- Infer range from CSV contents: rejected due to ambiguity
- Transaction-level deduplication: deferred due to complexity
