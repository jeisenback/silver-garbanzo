# GitHub Copilot — Project-specific Instructions

Purpose

Provide clear, project-aware guidance for AI assistants (GitHub Copilot, copilots, or similar) working in this repository.

Role

Act as a concise, correctness-first pair programmer that: tests assumptions, avoids risky file I/O, and follows repository workflow and safety rules.

Big Picture & Architecture

- Silver Garbanzo is a correctness-first, single-user CLI tool for ingesting personal finance CSVs, enforcing strict contracts, categorizing transactions, and producing period-based reports.
- Key modules: `src/silver_garbanzo/contracts.py` (contract validation), `src/silver_garbanzo/` (CLI entry, ingest logic), `data/sample/` (synthetic test data), `state/` (local operational state, gitignored), `docs/decisions/` (ADRs for contract/safety/tooling changes).
- Data flow: CSV → filename/header validation → ingest/normalize/categorize → results/registry in `state/`.

Critical Developer Workflows

- Branching: `feat/<issue-number>-<short-slug>` for features, `hotfix/<short-slug>` for urgent fixes. PRs must address one issue only.
- Build/test: `poetry install`, `poetry run ruff check .`, `poetry run pytest -q`. CI runs lint/tests on PRs to `dev`/`main`.
- Data safety: Never commit real data (`data/raw/`, `state/` are gitignored). Use only synthetic data in `data/sample/` for tests/CI.

Project Conventions & Patterns

- All ingest logic must validate filename and CSV header contracts before processing. Required headers: `Date`, `Description`, `Amount`, `Transaction_Type`. Fail fast on contract violations.
- Update ADRs (`docs/decisions/`) for any contract, safety, or tooling changes. Update run-log template and technical requirements for contract changes.
- Tests must cover contract enforcement and edge cases (see `tests/test_headers.py`).

Integration Points & Dependencies

- Python 3.11+, pandas, pytest, ruff (see `pyproject.toml`). No external services, plugins, or background jobs.

Do (high priority)

- Target a single issue per branch and PR.
- Implement only the issue scope; avoid opportunistic refactors.
- Keep business logic pure and isolate I/O at edges.
- Create or update an ADR in `docs/decisions/` when changing contracts, safety rules, or invariants.
- Add or update tests for behavior changes; keep changes testable without file I/O when possible.
- Follow branch naming: `feat/<issue-number>-<short-slug>` or `hotfix/<short-slug>`.
- Respect data safety: do not add real data; `data/raw/` and `state/` are git-ignored.
- Make small, focused commits with descriptive messages.

Don't (forbidden)

- Commit real financial data or modify ignored paths.
- Make broad, cross-cutting changes unrelated to the issue.
- Silence or ignore warnings about overlapping ranges, malformed filenames, or CSV contract violations.
- Add heavyweight tooling or background services without an ADR.

PR checklist (automated or suggested prompts)

- Confirm PR addresses exactly one issue and references it.
- If behavior/contracts change, ensure an ADR is present and tests updated.
- Ensure CI passes (`ruff`, `pytest`) and linting expectations are met.

Example assistant prompt

"Make a small change that fixes <issue-number>: implement X. Use pure functions; add unit tests; update ADR if this changes the contract; create branch `feat/<issue-number>-x`; commit and push."

Notes

This file is a local project guideline for AI contributors. Keep it concise and update `docs/decisions/` if you change how AI assistants are used in the workflow.
