from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime

class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime, 
            default=func.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime,
            default=func.now(),
            onupdate=func.now()
        )
    )
    is_deleted: bool = Field(default=False)
    deleted_at : Optional[datetime] = None


    # updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    # -> a problem because it only run at creation time, not updation, because it don't know its meant for update dates

    # remove optional