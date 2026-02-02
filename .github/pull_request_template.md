# Pull Request Checklist

> Before opening this PR, review:
> - `docs/dev_workflow.md`
> - `docs/technical_requirements.md`
> - `docs/data-layout.md` (data safety)

---

## What does this PR do?
<!-- Brief, concrete summary. Reference the issue number. -->

Closes #<issue-number>

---

## Scope check (must be true)
- [ ] This PR addresses **one issue only**
- [ ] Changes are limited to the issue's defined scope
- [ ] No opportunistic refactors or unrelated changes

---

## Contract & behavior changes
If this PR changes behavior, contracts, or invariants:
- [ ] An ADR was added or updated (`docs/decisions/`)
- [ ] Tests and fixtures updated for contract changes
- [ ] ESOD updated **only if** structure/responsibilities changed
- [ ] Technical Requirements updated **only if** constraints changed

(If none apply, leave unchecked.)

---

## Documentation & audit trail
- [ ] Run-log template reviewed and updated (if relevant to this change)
- [ ] Copilot instructions updated (if workflow changes)

---

## Data safety
- [ ] No real financial data added to the repo
- [ ] `data/raw/` and `state/` remain git-ignored
- [ ] Any sample data added is synthetic and appropriate for committed test data
- [ ] Dry-run mode used for validation (when applicable)

---

## Reviewer notes
<!-- Optional: add context for reviewers, known limitations, or follow-up tasks. -->
