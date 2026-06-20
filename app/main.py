import logging
import contextlib
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Local module imports
from app.core.config import settings
from app.db.database import init_db, engine, get_session
from app.core.logging_config import setup_logging
from app.middleware.logging import APILoggingMiddleware

# Routers
from app.api.routes import legal, cases, auth

# Initialize custom logging
setup_logging()
logger = logging.getLogger(__name__)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Production lifecycle manager. 
    Handles startup and shutdown events securely.
    """
    logger.info(f"⏳ Starting {settings.PROJECT_NAME} ({settings.API_VERSION})...")
    
    logger.info("⏳ Initializing PostgreSQL Database...")
    # await init_db()  # commented because alembic is handling the creation of db
    logger.info("✅ Database connection pool ready!")
    
    yield  # Application is live and serving requests here
    
    logger.info("🛑 Server shutting down. Cleaning up database connections...")
    if engine:
        await engine.dispose()
        logger.info("✅ Database connections safely closed.")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        description="Production-grade API for extracting IPC and BNS sections from legal case facts.",
        lifespan=lifespan, 
    )

    # Standard security middleware for frontend communication
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
        ],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(APILoggingMiddleware)

    # Register the routing modules
    app.include_router(legal.router, prefix="/api/v1")
    app.include_router(cases.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1/auth")

    # Upgraded Health Check that pings the RDS database
    @app.get("/health", tags=["System"])
    async def health_check(db: AsyncSession = Depends(get_session)):
        try:
            # Ping the database to ensure connection is active
            await db.execute(text("SELECT 1"))
            return {
                "status": "operational", 
                "service": settings.PROJECT_NAME,
                "database": "connected to RDS AWS"
            }
        except Exception as e:
            logger.error(f"Health check failed to connect to DB: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service unhealthy: Database connection failed. Error: {str(e)}"
            )

    return app


app = create_app()