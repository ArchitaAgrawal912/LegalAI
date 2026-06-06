import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    # Automatically generates a unique UUID
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # Automatically sets the time when created
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    # Automatically updates timestamp whenever the row is modified
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc)
        }
    )
    
    # 🎯 Soft Delete Fields
    is_deleted: bool = Field(default=False, nullable=False)
    deleted_at: datetime | None = Field(default=None, nullable=True)