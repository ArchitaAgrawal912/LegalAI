import uuid
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.legal_case import LegalCase

class ReferenceCase(BaseModel, table=True):
    case_id: uuid.UUID = Field(foreign_key="legalcase.id")
    
    title: str
    summary: str
    ipc_bns_applied: str  # Isme hum save karenge ki us past case me kya laws lage the
    
    # Relationship with main LegalCase
    legal_case: "LegalCase" = Relationship(back_populates="reference_cases")