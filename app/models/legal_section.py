from uuid import UUID
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.legal_case import LegalCase

class LegalSection(BaseModel, table=True):
    case_id: UUID = Field(foreign_key="legalcase.id")
    ipc_section: str
    bns_section: str
    reason: str  # Hum isme hi AI reason aur Rejection reason dono manage karenge
    is_approved: bool | None = Field(default=None)
    source: str = Field(default="LLM")
    has_lawyer_verified: bool = Field(default=False)
    
    # Notice: rejection_reason aur confidence dono hata diye hain DB safety ke liye
    
    legal_case: "LegalCase" = Relationship(back_populates="sections")