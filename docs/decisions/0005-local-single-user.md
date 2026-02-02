# ADR 0005: Local-only, single-user execution model

Status: Accepted  
Date: 2026-02-01

## Context
The tool is designed for personal use on local financial data.
Introducing multi-user or networked features increases risk and complexity without clear benefit.

## Decision
The system is explicitly:
- single-user
- local-only
- batch CLI driven
- stateful only via local files

No network access, background services, or shared state are introduced.

## Consequences
- Simplified threat model
- Easier reasoning about correctness
- Reduced operational overhead

## Alternatives considered
- Multi-user or hosted service: rejected as out of scope
- Database-backed architecture: rejected for MVP
