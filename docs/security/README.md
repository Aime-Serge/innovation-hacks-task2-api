# Security / API Specification

This repo generates and commits a real OpenAPI document at
[`docs/openapi.json`](../openapi.json). It is produced by
`scripts/export_openapi.py` from the live FastAPI app (`app/main.py`,
ADR-211, NFR-221) — it is not hand-written and not a separate source of
truth from the code.

- Regenerate: `python scripts/export_openapi.py` (or `make export-spec`).
- Verify it matches the running app: `python scripts/export_openapi.py --check`
  (or `make spec-check`); this is enforced in CI so the committed spec cannot
  drift from the actual endpoints.
- After changing any endpoint, run `make export-spec` and commit the updated
  `docs/openapi.json`.

For the broader security posture of this repo (threat model references,
vulnerability reporting process, dependency scanning), see
[`SECURITY.md`](../../SECURITY.md) at the repo root, which was added in the
prior documentation pass.

Relevant, code-verified security controls already in this repo (for
reference, not re-documented in depth here):

- Passwords hashed with argon2id, off the event loop (`app/core/security.py`).
- JWT (HS256) access tokens with pinned algorithm, required claims, issuer
  and audience checks (`app/core/security.py`).
- In-process sliding-window rate limiting on `login` and `register` only
  (`app/core/ratelimit.py`, ADR-216) — see the known limitation of this
  approach in `docs/project/risk-register.md`.
- `SecurityHeadersMiddleware` and `BodyGuardMiddleware` (`app/core/middleware.py`,
  ADR-219: CSP and body size limit).
