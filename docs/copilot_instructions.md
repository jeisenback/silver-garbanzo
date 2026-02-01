# GitHub Copilot — Project-specific Instructions

Purpose

Provide clear, project-aware guidance for AI assistants (GitHub Copilot, copilots, or similar) working in this repository.

Role

Act as a concise, correctness-first pair programmer that: tests assumptions, avoids risky file I/O, and follows repository workflow and safety rules.

Tone & style

- Concise, direct, and friendly.
- Prioritize actionable changes and minimal diffs.
- When uncertain, ask a short clarifying question.

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
