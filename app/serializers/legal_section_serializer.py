from pydantic import BaseModel
import uuid
from datetime import datetime

# ==========================================
# FRONTEND SE AANE WALA DATA (Input)
# ==========================================
class LegalSectionCreate(BaseModel):
    case_id: uuid.UUID  # Kis case me lagani hai
    ipc_section: str
    bns_section: str
    reason: str
    # 🎯 Note: 'is_approved', 'source' (LLM), aur 'has_lawyer_verified' DB khud default set karega, isliye yahan nahi daale.

# ==========================================
# FRONTEND KO JANE WALA DATA (Output)
# ==========================================
class LegalSectionResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    ipc_section: str
    bns_section: str
    reason: str
    is_approved: bool | None = None
    source: str
    has_lawyer_verified: bool
    created_at: datetime