from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.core.config import settings
import app.models  # Ensure models are imported so SQLModel registers tables

db_url = settings.DATABASE_URL

if db_url.startswith("postgresql://"):
    db_url = db_url.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1,
    )

engine = create_async_engine(
    db_url,
    echo=True,
    future=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)




async def get_session() -> AsyncSession:
    """Dependency to provide a database session."""
    async with async_session() as session:
        yield session
