# from __future__ import annotations
from sqlmodel import Field, Relationship, Column
from sqlalchemy import JSON
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID
from enum import Enum
from app.models.base_model import BaseModel
if TYPE_CHECKING:
    from app.models.user_model import User
    from app.models.legal_sections import LegalSection

class CaseStatus(str, Enum):
    pending = "pending"
    inprogress = "inprogress"
    completed = "completed"

class Case(BaseModel, table=True):
    __tablename__ = "cases"

    title: str
    case_description: str
    llm_summary: Optional[str] = Field(default=None, sa_column=Column(JSON))
    lawyer_approved_summary: Optional[str] = None
    status: CaseStatus = Field(default=CaseStatus.pending)
    user_id: UUID = Field(foreign_key="users.id")

    # Relationship
    user: "User" = Relationship(back_populates="cases")
    legal_sections: list["LegalSection"] = Relationship(back_populates="case")

    # Optional tab hota hai jab field ki value future me aayegi ya absent ho sakti hai
    # *cases -> variable name
    # *case -> variable name
    # case <-> legal_sections
    # cases <-> user