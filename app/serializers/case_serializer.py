from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# FRONTEND SE AANE WALA DATA (Input)
class CaseCreate(BaseModel):
    case_number: str
    title: str
    description: Optional[str] = None
    created_by: uuid.UUID
    # status default 'open' hoga
    # created_by frontend nahi dega, hum token se nikalenge

# FRONTEND KO JANE WALA DATA (Output)
class CaseResponse(BaseModel):
    id: uuid.UUID
    case_number: str
    title: str
    description: Optional[str] = None
    status: str
    created_by: uuid.UUID
    created_at: datetime


   

