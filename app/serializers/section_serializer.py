from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional
from app.models.legal_sections import SectionSource

class LegalSectionCreate(SQLModel):
    case_id: UUID
    ipc_section: Optional[str] = None
    bns_section: Optional[str] = None
    reason: str
    source: SectionSource

class LegalSectionUpdate(SQLModel):
    ipc_section: Optional[str] = None
    bns_section: Optional[str] = None
    reason: Optional[str] = None
    has_lawyer_verified: Optional[bool] = None

class LegalSectionResponse(SQLModel):
    id: UUID
    case_id: UUID
    ipc_section: Optional[str]
    bns_section: Optional[str]
    reason: str
    source : SectionSource
    has_lawyer_verified: bool