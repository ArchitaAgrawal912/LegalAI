import uuid
from sqlmodel import Field
from typing import Optional
from app.models.base import CoreModel

class Case(CoreModel, table=True):
    __tablename__ = "cases"
    
    # id, created_at, updated_at inherited hain
    case_number: str = Field(index=True, unique=True, nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    status: str = Field(default="open")
    
    created_by: uuid.UUID = Field(foreign_key="user.id", nullable=False)






















