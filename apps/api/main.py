"""FastAPI Application Entry Point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routes import router
from pharma_platform.agents.bootstrap import register_all_agents
from pharma_platform.configuration.settings import get_settings
from pharma_platform.observability.logger import setup_observability_logging
from pharma_platform.persistence.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown."""
    settings = get_settings()
    setup_observability_logging(level=settings.log_level)
    init_db()
    register_all_agents()
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "Enterprise Pharmaceutical Agentic AI Ecosystem. "
        "Provides CEO conversational executive support, specialist agent framework, "
        "observability, evaluation, and controlled continuous improvement."
    ),
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Mount Routes
app.include_router(router)

# Serve static frontend build if present (for single-container free deployments)
web_dist = Path(__file__).resolve().parent.parent / "web" / "dist"
if web_dist.exists() and (web_dist / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=web_dist / "assets"), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(web_dist / "index.html")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith(("api", "docs", "redoc", "openapi.json")):
            raise HTTPException(status_code=404, detail="Not found")
        file_path = web_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(web_dist / "index.html")
else:
    @app.get("/")
    def root():
        return {
            "app": settings.app_name,
            "version": settings.version,
            "api_docs": "/docs",
            "api_prefix": settings.api_prefix,
            "data_mode": "synthetic",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=True)
