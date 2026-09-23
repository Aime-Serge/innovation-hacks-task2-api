# Contributing

This is Task 2 of the Innovation Hacks Full Stack Development Internship: a FastAPI backend for
users, projects and tasks. The notes below describe how this repository is actually worked on, so
a new contributor (or a future you) can pick it up without guessing.

## Setup

You need [uv](https://docs.astral.sh/uv/) (it installs Python 3.12 for you).

```bash
uv sync --frozen                                                                     # 1. install
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')      # 2. configure
SEED_PROFILE=default uv run uvicorn app.main:create_app --factory --reload           # 3. run
```

Open http://127.0.0.1:8000/docs. To keep settings in a file instead of exporting them, copy
`.env.example` to `.env` and fill in `SECRET_KEY`.

## Branch and commit conventions

Branches are named `<type>/<short-description>`, e.g. `feat/role-registration`,
`docs/screenshots`, `chore/render-service-name` (see `git log --oneline` for real examples from
this repo's history).

Commits follow `type(scope): description`, lower case, imperative, no trailing period. The types
actually used in this repository's history are `feat`, `fix`, `docs`, `test`, `chore`, `build`,
`refactor`, and `ci`. Scope is the area touched (`api`, `web`, `deploy`, `docs`, `auth`, `errors`,
`data`, `env`, ...). A scope is common but not strictly required (a handful of commits in this
repo's history are plain `feat:` or `docs:` with no scope). Examples from this repo:

```
feat(api): registration may set role=lead, defaults to developer
fix(auth): ...
docs(docs): add screenshots of the welcome page, Swagger UI and a 409 workflow error to the README
chore(deploy): rename the Render service to devdashapi
```

## Pull request process

1. Branch off `main`.
2. Make the change, keeping product code, tests, and docs in sync (see "Definition of done"
   below).
3. Open a PR into `main` using the PR template under `.github/pull_request_template.md`: it asks
   for the requirement ID(s) touched, which tests were added or changed, and screenshots for any
   user-visible change.
4. CI (`.github/workflows/ci.yml`) must pass: lint, typecheck, import-layer check, tests with
   coverage, OpenAPI spec check and diff, contract tests, security scan, gitleaks, Postman/Newman,
   load smoke test, and the Docker build.
5. Merge via the GitHub "Merge pull request" flow (this repo's history is entirely merge commits
   from PRs, not direct pushes to `main`).

## Definition of done

A change is done when:

- [ ] It maps to a real requirement ID from `docs/standards/task2-standards-pack.md` (FR-2xx /
      NFR-2xx), or is clearly a chore/docs change with no requirement ID.
- [ ] Tests cover the change and `make test` passes locally (coverage gate: 90%, see
      `pyproject.toml`).
- [ ] `make gate` passes locally, or CI is green on the PR, before merge.
- [ ] `docs/openapi.json` was regenerated with `make export-spec` if any endpoint changed.
- [ ] Any new architectural decision that isn't obvious from the code has an ADR added under
      `docs/adr/` (see the existing ADRs for the format).
- [ ] The README is updated if the change affects setup, configuration, or the endpoint list.
- [ ] No product code, test, or migration change is bundled into a docs-only commit, and vice
      versa.

## Quality gate reference

`make gate` runs, in order: `lint`, `typecheck`, `layers`, `test`, `spec-check`, `spec-diff`,
`contract`, `security`, `postman`, `load`. CI additionally runs `gitleaks/gitleaks-action@v2` and
`make docker`. See the README's "The quality gate" section for what each target checks.
