# Architecture Decision Records

Index of the ADRs recorded for Task 2 (the DevDash users/projects/tasks API). Each file is
numbered against the ADR IDs used in `docs/standards/task2-standards-pack.md`
(ADR-201 through ADR-211 there; this repository's own decisions continue the sequence from
ADR-212). Read the linked file for the full context, decision, and consequences.

| ADR | Title |
| --- | --- |
| [ADR-212](ADR-212-repo-layout.md) | The project lives at the repository root, not in `backend/` |
| [ADR-213](ADR-213-python-3-12.md) | Python 3.12, not the deployed 3.14 |
| [ADR-214](ADR-214-not-backward-compatible.md) | The rebuild is not backward compatible with the first deployed API |
| [ADR-215](ADR-215-landing-page-and-health.md) | No landing page; health is `/healthz` and `/readyz` (superseded in spirit by ADR-225, below) |
| [ADR-216](ADR-216-in-process-rate-limiter.md) | A small in-process rate limiter instead of slowapi |
| [ADR-217](ADR-217-activity-and-user-reads.md) | Activity `limit`, user reads, and `completed` events |
| [ADR-218](ADR-218-optional-due-date.md) | `Project.dueDate` is optional in Task 2 and required in Task 1 |
| [ADR-219](ADR-219-csp-and-body-limit.md) | CSP for the docs pages, and how the body limit works |
| [ADR-220](ADR-220-pydantic-mypy-alias-warning.md) | `warn_required_dynamic_aliases` is off for the pydantic mypy plugin |
| [ADR-221](ADR-221-render-demo-seeding.md) | The Render demo runs with seeded data and is not `APP_ENV=production` |
| [ADR-222](ADR-222-email-validation.md) | Email addresses are checked with a stated pattern |
| [ADR-223](ADR-223-clock-and-token-expiry.md) | Token expiry is checked against the injected clock |
| [ADR-224](ADR-224-camel-case-path-parameters.md) | Path parameters are camelCase too |
| [ADR-225](ADR-225-welcome-page.md) | A documented welcome page at `/` |

Note: ADR-215 (no landing page) and ADR-225 (a documented welcome page at `/`) read as opposite
decisions; ADR-225 is the later one (see the file dates under `docs/adr/`) and reflects current
behavior. Neither file has been edited here — this is a docs-only closeout pass and reconciling
or retiring ADR-215's text is left to the project author.

ADR-201 through ADR-211, referenced by ID in `docs/standards/task2-standards-pack.md`, are part of
the standards pack itself, not separate files in this directory.
