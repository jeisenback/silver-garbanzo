# ADR 0004: Range registry with overlap prevention

Status: Accepted  
Date: 2026-02-01

## Context
Statements may be re-exported with overlapping periods.
Without persistent state, duplicate ingestion is difficult to detect.

## Decision
Maintain a local range registry (`state/ingested_ranges.csv`) that records:
- account identifier
- declared date range
- ingest timestamp

Before ingest, the tool checks for overlapping ranges and fails if any overlap exists.

Registry updates must be atomic.

## Consequences
- Simple, auditable ingest history
- Manual intervention required to override mistakes
- No hidden deduplication logic

## Alternatives considered
- Transaction fingerprint deduplication: deferred
- Database-backed ledger: rejected as overkill for scope
