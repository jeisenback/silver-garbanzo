# ADR 0001: Use Poetry for dependency management and Ruff for linting

Status: Accepted  
Date: 2026-02-01

## Context
The project is a local-only, correctness-first CLI tool. The development workflow must be reproducible across machines and CI with minimal tool sprawl.

## Decision
- Use Poetry to manage Python versions, virtual environments, and dependency locking.
- Use Ruff as the sole linter for early phases of the project.
- Do not introduce additional formatters/linters (e.g., Black, isort) during bootstrap unless required by a later ADR.

## Consequences
- Reproducible installs via `poetry.lock`.
- Single lint tool reduces configuration and CI failure modes.
- Formatting is not enforced beyond Ruff’s selected rules in early phases.

## Alternatives considered
- pip-tools: lighter, but more manual environment management.
- uv: fast, but adds a second mental model vs existing Poetry usage.
- Black + isort: more tooling and churn without increasing correctness in early phases.
