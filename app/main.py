from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.exceptions import register_exception_handlers
from app.landing import public_base_url, render_landing
from app.routers import projects, tasks, users

settings = get_settings()

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
        )
    )
