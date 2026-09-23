# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project does not yet publish
semantic-version releases; the tag below is the actual tag in this repository
(`git tag -l`), used as the heading in place of a semver number.

## [task-2-submission] - 2026-09-22

Tagged submission of Task 2: the DevDash users/projects/tasks API.

### Added

- Users, projects and tasks REST API under `/api/v1` (FastAPI, Pydantic v2), with bearer-token
  authentication, role-based authorization, and the shared error envelope.
- Task status workflow (`todo` → `in_progress` → `in_review` → `done`, with defined reopen
  transitions) enforced server-side, returning `409 INVALID_STATUS_TRANSITION` on an invalid move.
- Welcome page at `GET /` with its own CSP, `GET /healthz` and `GET /readyz`.
- Activity feed (`GET /activity`) and dashboard summary (`GET /dashboard/summary`).
- OpenAPI document exported to `docs/openapi.json`, with a CI check that it matches the running
  app and a diff check against `origin/main` for breaking changes.
- Postman collection under `postman/`, run against the live server with Newman in CI.
- Seed data command (`python -m app.seed`), refused when `APP_ENV=production`.
- Architecture decision records under `docs/adr/` (ADR-212 through ADR-225).
- CI workflow (`.github/workflows/ci.yml`): lint, mypy strict, import-linter layers, pytest with
  coverage (90% gate), spec check/diff, Schemathesis contract tests, bandit + pip-audit, gitleaks,
  Postman/Newman, Locust load smoke test, and a Docker build.
- README with a 3-command quickstart, configuration table, curl walkthrough, endpoint table, and
  screenshots of the welcome page, Swagger UI, and a 409 status-transition error.
- Live demo deployment on Render (see README "Deploying" and ADR-221).

### Notes

- State is held in memory (single worker); Task 3 is expected to add a database.
- Full list of known, intentional limitations: see the README's "Known limitations" section.

## [Unreleased]

Commits on `main` after the `task-2-submission` tag (`git log --oneline task-2-submission..main`
at the time of this closeout pass):

### Added

- `feat(api): registration may set role=lead, defaults to developer` (0491bae) — registration can
  now set `role=lead` explicitly; still defaults to `developer`.
- `feat: support registration profile fields` (8e700a7) — extended registration payload
  (`givenName`, `familyName`, `profile`, `avatarUrl`); see the README's "Full-registration
  compatibility" section.

This closeout/documentation pass (LICENSE, SECURITY.md, CONTRIBUTING.md, this file, issue/PR
templates, CODEOWNERS, dependabot config, ADR index, and README audit fixes) is not a product
change and is not itemized here beyond this note.
