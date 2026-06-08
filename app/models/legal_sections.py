# from __future__ import annotations
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from enum import Enum
from app.models.base_model import BaseModel
if TYPE_CHECKING:
    from app.models.case_model import Case

class SectionSource(str, Enum):
    lawyer = "Lawyer"
    llm = "LLM"

class LegalSection(BaseModel, table=True):
    __tablename__ = "legal_sections"

    case_id: UUID = Field(foreign_key="cases.id")
    ipc_section: Optional[str] = None
    bns_section: Optional[str] = None 
    reason: str 
    source: SectionSource
    has_lawyer_verified: bool = Field(default=False)

    case: "Case" = Relationship(back_populates="legal_sections")

    # *case -> variable name