# Demo Video Script

Target length: **2:00–2:30** (within the guide's 2–5 minute range —
this is a backend-only task, so there's no UI to walk through beyond
Swagger UI itself).

Record against a locally running server (`uvicorn app.main:app --reload`)
using the Swagger UI at `http://localhost:8000/docs` — it's a real,
executable client, not a slide, so every request in this script should
actually be sent and its real response shown.

| Time | Beat | Say | Show |
| --- | --- | --- | --- |
| 0:00–0:15 | Cold open | "This is the Users, Projects & Tasks API — the backend Task 1's dashboard and Task 4's platform will consume. Built with FastAPI and Pydantic v2, in-memory storage for this task, real database comes in Task 3." | Swagger UI overview at `/docs`, scrolled to show all three route groups. |
| 0:15–0:45 | Create a user | "Passwords are hashed with PBKDF2 before they're ever stored — they're never returned in any response." | Expand `POST /users`, "Try it out", fill in a real name/email/password, Execute. Point at the response body: no `password` or `password_hash` field. |
| 0:45–1:05 | Validation & conflict | "Creating a second user with the same email is a 409, not a 500 — and an invalid payload is a clean 422 with field-level detail." | POST the same email again (409); then POST with `"email": "not-an-email"` (422), point at the `error.code` field in both. |
| 1:05–1:35 | Projects and tasks, relationships enforced | "A project has to reference a real user — try a random UUID as owner_id and it's a 404, not a crash. Same rule for a task's project_id." | `POST /projects` with the real user's id (201); then with a random UUID as `owner_id` (404). `POST /tasks` against the real project, then the dedicated `PATCH /tasks/{id}/status` endpoint to move it to `done`. |
| 1:35–2:00 | Centralized errors, even framework-level ones | "Every error response shares one shape — `{"error": {code, message, details}}` — and that's true even for errors FastAPI raises itself, like hitting a route that doesn't exist." | Hit a nonexistent path directly in the browser or via curl in a terminal split, e.g. `GET /nope` — show the wrapped `not_found` shape, not FastAPI's default `{"detail": ...}`. |
| 2:00–2:20 | Close | "41 tests, all passing against this exact behavior — full source, README, and API docs are in the repo linked below." | Quick cut to a passing `pytest -v` run, then back to the repo's GitHub page. |

## Notes for whoever records this

- No auth on this task (deliberate — Task 4 adds it) and no database
  (deliberate — Task 3 adds it), so don't apologize for either on
  camera; the README explains both as intentional scope.
- The `error.code` field (not just the status code) is worth pointing
  at explicitly on screen — it's the detail most likely to get missed
  in a quick read of the response body.
- If recording in one take gets awkward around the 409/422 beat,
  it's fine to have both request bodies pre-typed in separate tabs
  before hitting record, so the video doesn't sit on typing.
