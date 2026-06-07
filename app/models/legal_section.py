import uuid
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from datetime import datetime, timezone 

# This prevents Circular Imports!
if TYPE_CHECKING:
    from app.models.legal_case import LegalCase

class LegalSection(BaseModel, table=True):
    # Foreign Key pointing to the Case UUID
    case_id: uuid.UUID = Field(foreign_key="legalcase.id")
    
    ipc_section: str
    bns_section: str
    reason: str
    
    
    title: str = Field(default="Unknown Offense") 
    probability: float = Field(default=0.0)
    
    
    # True = Approved, False = Rejected, None = Pending Action
    is_approved: bool | None = Field(default=None) 
    has_lawyer_verified: bool = Field(default=False) # Naya field for lawyer verification status
    
    
    # Jab lawyer reject karega (is_approved=False), toh yahan reason aayega
    rejection_reason: str | None = Field(default=None)
    
    # Source: "LLM" ya "Lawyer" (Kahan se generate hua)
    source: str = Field(default="LLM") 
    
    # Soft Delete Flags
  
    
    # Relationship linking back to the Case
    legal_case: "LegalCase" = Relationship(back_populates="sections")
    
    
    #  has lawer verified , key , tyaaki state maintaine ho sake  single query  ki kisis case ka false hai toh no refence 
    