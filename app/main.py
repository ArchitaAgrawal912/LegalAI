from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import legal

def create_app() -> FastAPI:
    app = FastAPI(
        title="Legal AI API",
        version="v1.0.0",
        description="Production-grade API for extracting IPC and BNS sections from legal case facts."
    )

    # Standard security middleware for frontend communication
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict this to your actual frontend domain in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register the legal routing module
    app.include_router(legal.router, prefix="/api/v1")

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "operational", "service": "Legal AI API"}

    return app

app = create_app()