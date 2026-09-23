# Glossary

Terms as they are actually used in this repo's code and standards pack
(`app/domain`, `app/services`, `app/schemas`, `docs/adr`, `docs/standards`) —
not generic definitions.

## Domain entities (`app/domain/models.py`)

| Term | Meaning in this codebase |
|---|---|
| **User** | An account: `id`, `name`, `email`, `password_hash`, `role`, `avatar_url`, `theme`, plus optional `given_name`/`family_name`/`profile` kept for Task 4 registration compatibility. |
| **Project** | A named piece of work owned by a user (`owner_id`), with a `status`, optional `due_date`, and a set of tasks. |
| **Task** | A unit of work inside a project: `status`, `priority`, optional `assignee_id`, `due_date`, `completed_at`. |
| **Activity** | An immutable log entry recording something that happened to a project or task (`type`, `actor_id`, `at`). |
| **Progress** | A computed, read-only summary of a project: `total_tasks`, `done_tasks`, `percent`. |
| **Actor** | The authenticated caller of a request, used by the authorization rules in `app/services/authz.py` (`is_lead`, `require_lead`, `require_self_or_lead`, `require_project_manager`, `require_task_editor`). |

## Enum values (`app/domain/enums.py`)

| Enum | Values |
|---|---|
| **Role** | `developer`, `lead` |
| **Theme** | `light`, `dark`, `system` |
| **ProjectStatus** | `planned`, `active`, `on_hold`, `completed` |
| **TaskStatus** | `todo`, `in_progress`, `in_review`, `done` |
| **Priority** | `low`, `medium`, `high`, `urgent` |
| **ActivityType** | `created`, `status_changed`, `completed` |

## Task workflow (`app/domain/rules.py`, BR-204)

The allowed `TaskStatus` transitions are fixed and anything not listed is
rejected with a 409:

- `todo` → `in_progress`
- `in_progress` → `in_review`
- `in_review` → `in_progress` or `done`
- `done` → `in_progress`

## API / platform terms

| Term | Meaning |
|---|---|
| **FR / BR / NFR / TH / ADR** | Standards-pack reference codes used throughout code comments and `docs/adr/`: Functional Requirement, Business Rule, Non-Functional Requirement, Threat, Architecture Decision Record. |
| **PageOut / ListQuery** | The shared pagination contract (`app/schemas/common.py`, FR-229): `page` (≥1), `pageSize` (1–100), `sort`. |
| **requestId** | Correlation id attached to every error response (`{"error": {"code", "message", "details"?, "requestId"}}`), set by `RequestContextMiddleware`. |
| **Rate limiter / window** | The in-process sliding-window limiter (`app/core/ratelimit.py`, ADR-216) guarding `login` and `register` only; keyed by client and, for login, by email. |
| **Seed profile** | The scripted set of demo users/projects/tasks applied at startup in non-production environments (`app/seed/`). |
