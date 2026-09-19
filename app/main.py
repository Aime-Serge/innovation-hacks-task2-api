from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.exceptions import register_exception_handlers
from app.landing import public_base_url, render_landing
from app.routers import projects, tasks, users

settings = get_settings()

# The Task 2 brief's requirements, each mapped to where it is met — shown on
# the landing page and verifiable there with "Run live checks".
TASK_REQUIREMENTS = [
    ("User management endpoints", "Create, list, get, update and delete: /users"),
    ("Project creation and retrieval", "POST, list and get by id: /projects. The owner must exist."),
    ("Task creation, update and deletion", "POST, PATCH and DELETE: /tasks"),
    ("Task status management", "PATCH /tasks/{id}/status. Values: todo, in-progress, done."),
    ("Centralized error handling", "Every error uses one JSON shape, including unknown routes and wrong methods."),
    ("Input validation on all writes", "Pydantic models. Invalid input returns 422 with field-level detail."),
    ("Correct HTTP status codes", "201 created, 204 deleted, 404 not found, 405 wrong method, 409 duplicate, 422 invalid."),
    ("Environment variables for configuration", "Settings come from the environment; .env.example is documented and no secrets are committed."),
    ("Clear API documentation", "Swagger UI (/docs), ReDoc (/redoc), OpenAPI JSON, and a README route table."),
]

app = FastAPI(
    title="Users, Projects & Tasks API",
    description="Task 2 — Innovation Hacks Full Stack Development Internship",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/health", tags=["health"], summary="Service health check")
def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    base = public_base_url(request.headers.get("host", "localhost"), request.url.scheme)
    return HTMLResponse(
        render_landing(
            app,
            base_url=base,
            environment=settings.app_env,
            repo_url="https://github.com/Aime-Serge/innovation-hacks-task2-api",
            label="Task 2",
            requirements=TASK_REQUIREMENTS,
        )
    )
