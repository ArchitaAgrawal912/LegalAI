from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# FRONTEND SE AANE WALA DATA (Input)
class IpsSectionCreate(BaseModel):
    section_code: str
    section_name: str
    description: Optional[str] = None
    penalty: Optional[str] = None
    case_id: uuid.UUID  # Frontend ko batana padega ki kis case me lagani hai

# FRONTEND KO JANE WALA DATA (Output)
class IpsSectionResponse(BaseModel):
    id: uuid.UUID
    section_code: str
    section_name: str
    description: Optional[str] = None
    penalty: Optional[str] = None
    case_id: uuid.UUID
    created_at: datetime