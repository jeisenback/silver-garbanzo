# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the silver-garbanzo project. ADRs document important architectural, design, and technical decisions made during development.

## Purpose

ADRs help the team:
- Record decisions at the time they are made
- Explain context and alternatives considered
- Document consequences and tradeoffs
- Enable onboarding of new contributors
- Establish a decision log for future reference

## Format

Each ADR follows a standard template with the following sections:

- **Status**: Proposed, Accepted, Deprecated, or Superseded
- **Context**: The issue or situation that motivated the decision
- **Decision**: The chosen solution or approach
- **Alternatives**: Other options considered and why they were rejected
- **Consequences**: Positive and negative impacts of the decision

## Naming Convention

ADRs are named with a four-digit number (0000, 0001, etc.) followed by a slug describing the decision:

```
NNNN-short-title.md
```

Example: `0001-use-pandas-for-csv-processing.md`

## Creating a New ADR

1. Copy `0000-adr-template.md` to a new file with the next sequential number
2. Replace `[Decision Title]` with your decision title
3. Fill in all sections: Status, Context, Decision, Alternatives, Consequences
4. Set Status to `Proposed` initially
5. Submit as part of a PR for team review
6. Update Status to `Accepted` once approved

## Architecture Decision Records

| ADR | Title | Status |
|-----|-------|--------|
| [0000](0000-adr-template.md) | ADR Template | Accepted |
| [0001](0001-use-poetry-and-ruff.md) | Use Poetry for dependency management and Ruff for linting | Accepted |
| [0002](0002-correctness-first-ingest.md) | Correctness-first ingest with hard failures | Accepted |
| [0003](0003-filename-date-range-contract.md) | Filename-declared date ranges as ingest contract | Accepted |
| [0004](0004-range-registry.md) | Range registry with overlap prevention | Accepted |
| [0005](0005-local-single-user.md) | Local-only, single-user execution model | Accepted |


*This ADR framework is inspired by [Documenting Architecture Decisions](https://adr.github.io/)*
