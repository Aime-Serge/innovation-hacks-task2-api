# Privacy / Data Map

## Scope

This document describes what personal data the Task 2 API's own domain
models actually store, based on `app/domain/models.py`. This repo has no
database (state is in-memory only, see `docs/architecture/README.md`); Task 3
adds PostgreSQL persistence in a separate repository, which is out of scope
here.

## Personal data stored (`app/domain/models.py::User`)

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Internal identifier, not personal on its own. |
| `name` | `str` | Display name. |
| `email` | `str` | Used as login identifier; validated per ADR-222. |
| `password_hash` | `str` | Argon2id hash (`app/core/security.py`) — the plaintext password is never stored. |
| `role` | `Role` enum | `developer` or `lead`; not personal data but access-control metadata. |
| `avatar_url` | `str \| None` | Optional link to a profile image. |
| `theme` | `Theme` enum | UI preference, not personal data. |
| `given_name` / `family_name` | `str \| None` | Optional, kept on the account for Task 4 registration compatibility (see comment in `app/domain/models.py`). |
| `profile` | `dict[str, Any] \| None` | Optional free-form profile block carried over for Task 4; its actual contents are not constrained by this repo's schema, so no further claim is made about what it may contain. |
| `created_at` / `updated_at` | `datetime` | Record timestamps. |

No other domain entity (`Project`, `Task`, `Activity`, `Progress`) stores
personal data beyond a `owner_id` / `actor_id` / `assignee_id` UUID reference
back to a `User`.

## Where it is stored

- **At rest**: nowhere persistent in this repo. `app/repositories/memory/*`
  holds all data in process memory; it is lost on restart. There is no
  database connection, file store, or external storage client in `app/`.
- **In transit**: over whatever transport the deployment uses (HTTPS is
  expected in production per `render.yaml` / deployment docs; this repo does
  not itself terminate TLS).
- **In logs**: `app/core/logging.py` was not audited line-by-line for this
  pass; treat log redaction of `email`/`password_hash` as **UNVERIFIED** —
  a manual step, not a claim made here.

## Third-party / AI data flow

Verified by grepping `app/` for AI/LLM and outbound-HTTP-client identifiers
(`openai|anthropic|httpx|requests\.|aiohttp|llm|gpt`): **zero matches**. This
repo has no AI provider integration and makes no outbound third-party HTTP
calls, so there is no third-party data flow to document for Task 2.

## Retention

Not applicable in the literal sense: because storage is in-memory only, all
data is retained only for the life of the running process and is erased on
restart. There is no long-term retention policy to state for this repo.

## Data subject contact

For data-subject requests regarding any deployed instance of this API:
<set-me>.
