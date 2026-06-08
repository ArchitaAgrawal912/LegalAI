from sqlmodel import Field, Relationship, Column
from sqlalchemy import JSON
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID
from enum import Enum
from app.models.base_model import BaseModel
if TYPE_CHECKING:
    from app.models.case_model import Case


class PrecedentCase(BaseModel, table=True):
    __tablename__ = "precedent_cases"

    case_id: UUID = Field(foreign_key="cases.id")

    title: str
    court: str
    year: str
    citation: str

    source: str = "indian_kanoon"

    case: "Case" = Relationship(back_populates="precedent_cases")