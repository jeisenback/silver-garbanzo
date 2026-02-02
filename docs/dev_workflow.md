# Development Workflow

This project is correctness-first and single-user.  
The workflow exists to prevent silent data corruption, scope creep, and drift.

If this workflow conflicts with a PRD/ESOD/TR requirement, follow the requirement and log an ADR if needed.

PRs are enforced via .github/pull_request_template.md.

---

## Branching

- `main`: stable, safe to run on real data
- `dev`: integration
- `feat/*`: feature branches (one issue per branch)
- `hotfix/*`: urgent fixes branched from `main`

Branch naming:
- `feat/<issue-number>-<short-slug>`
- `hotfix/<short-slug>`

---

## For every issue

1. Create a branch from `dev`
   - `feat/<issue-number>-<short-slug>`

2. Implement only what is in the issue scope
   - Do not combine issues
   - Do not add opportunistic refactors
   - If scope must change, update the issue and/or write an ADR

3. Keep logic pure and I/O at the edges
   - Core functions should be testable without touching the filesystem

4. Update tests when behavior changes
   - Contract changes require tests and sample fixtures

5. Update documentation when behavior/constraints change
   - TR/ESOD updated only when necessary
   - If a change alters contracts, failure behavior, state semantics, or tooling, add/update an ADR in `docs/decisions/`.


6. Open a PR into `dev`
   - Use the PR template checkboxes honestly
   - CI must pass

7. Merge when CI is green

---

## Feature Implementation Example

- For features like dry-run mode, create a dedicated feature branch (e.g., `feat/13-dry-run-mode`).
- Add CLI flags and ensure all contract checks run in dry-run mode, but no state/output files are written.
- Add tests to verify dry-run logic (no registry writes, all validations run).
- Update documentation to reflect new CLI options and behavior.

- For features like profile mode, create a dedicated feature branch (e.g., `feat/17-profile-mode`).
- Add CLI flags and ensure profiling logic (timing, memory usage) is integrated and tested.
- Add tests to verify profile output.
- Update documentation to reflect new CLI options and behavior.

---

## Merging to main

- Merge `dev` → `main` only at phase boundaries or after a coherent set of issues
- Tag releases from `main`

---

## Data safety rules

- Real data is never committed
- `data/raw/` and `state/` must remain git-ignored
- CI uses `data/sample/` only

---

## Required quality gates

- Lint + format checks pass
- Tests pass
- Coverage threshold enforced in CI

---

## Prohibited

- Direct commits to `main`
- Editing `state/ingested_ranges.csv` manually without logging it
- Weakening ingest hard-fail rules without an ADR
