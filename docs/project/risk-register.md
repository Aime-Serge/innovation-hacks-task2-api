# Risk Register — Top 5

Real, code-verified risks specific to this repo. Kept to 5 because that is
what can be honestly substantiated from the codebase in this pass — not
padded to a round number.

| # | Risk | Evidence | Impact | Likelihood | Mitigation / status |
|---|---|---|---|---|---|
| 1 | JWT access tokens cannot be revoked before they expire. No logout/blacklist mechanism was found (`grep -ri "logout\|revoke\|blacklist" app/` returns nothing). | `app/core/security.py` (`TokenCodec`), `app/services/auth.py` | A stolen or leaked token remains valid for its full TTL with no way to invalidate it server-side. | Medium | None found in this repo. Accepted design trade-off for a stateless API; document TTL and treat as an open item. |
| 2 | The rate limiter is in-process and per-worker ("Counts per worker, so it is only accurate with one worker", `app/core/ratelimit.py` docstring, ADR-216). | `app/core/ratelimit.py`; `Dockerfile` currently pins `--workers 1` | If ever deployed with more than one worker/process (e.g. a future scale-up), each worker gets its own counter and the effective rate limit is multiplied by worker count, silently weakening brute-force protection. | Low today (single worker pinned), Medium if scaled | Currently mitigated by `--workers 1` in `Dockerfile`. No distributed limiter (e.g. shared store) exists. |
| 3 | Rate limiting only guards `login` and `register`. Other write endpoints have no rate limiting. | `grep -rn "enforce_rate_limit" app/api` shows only `app/api/v1/auth.py` (login) and `app/api/v1/users.py` (register) call it. | Authenticated users can call project/task/activity-writing endpoints without any request-rate control, allowing abuse or accidental load from a single account. | Medium | Not mitigated in this repo; scoped to auth endpoints per ADR-216. |
| 4 | All application state is kept in memory only; there is no database in this repo. | `app/repositories/memory/*`; `app/main.py` docstring: "State is kept in memory and resets on restart" | Any process restart, redeploy, or crash loses all users/projects/tasks/activity data. Acceptable for a Task 2 demo/API-contract scope, but a real risk if an instance is mistaken for a durable environment. | High (by design) | By design for Task 2; Task 3 (separate repo) adds PostgreSQL persistence. |
| 5 | `User.profile` is an unconstrained `dict[str, Any] | None` with no schema validation. | `app/domain/models.py` | Arbitrary, unvalidated data can be stored under `profile`, with no guarantee about its shape, size, or content — including potentially sensitive data a client chooses to put there. | Low–Medium | Not validated or size-limited in this repo; kept for Task 4 registration compatibility per the code comment. |

## Out of scope for this register

Anything requiring a live penetration test, load test at scale, or review of
a specific deployment's infrastructure (e.g. actual Render configuration,
TLS termination, secret rotation practice) is a manual step, not claimed
here.
