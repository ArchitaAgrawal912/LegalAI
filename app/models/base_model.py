from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, UTC
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime

class BaseModel(SQLModel, table=False):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    created_at: datetime = Field(
    default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = Field(
    default_factory=lambda: datetime.now(UTC)
)
    is_deleted: bool = Field(default=False)
    deleted_at : Optional[datetime] = None


    # updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    # -> a problem because it only run at creation time, not updation, because it don't know its meant for update dates

    # remove optional

    #table=False ==> ye class sirf parent hai, iska apna table mat banao. Columns sirf child tables mein jaayenge.

    # sa_column=Column(DateTime, ..) ek SQLAlchemy Column object h. jab User table inherit krta hai, basemodel se - to ye allowed nahi hota, kyunki ek Column ek hi table ka ho sakta h