from fastapi import FastAPI

from app.config import get_settings
from app.exceptions import register_exception_handlers

settings = get_settings()

app = FastAPI(
    title="Users, Projects & Tasks API",
    description="Task 2 — Innovation Hacks Full Stack Development Internship",
    version="0.1.0",
)

register_exception_handlers(app)


@app.get("/health", tags=["health"], summary="Service health check")
def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}
