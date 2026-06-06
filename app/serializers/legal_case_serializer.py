from pydantic import BaseModel
import uuid
from datetime import datetime

# ==========================================
# FRONTEND SE AANE WALA DATA (Input)
# ==========================================
class CaseCreate(BaseModel):
    # title: str
    raw_description: str
    user_id: uuid.UUID
    # 🎯 Note: 'case_number' hata diya gaya hai kyunki DB Model mein nahi hai.
    # 🎯 Note: 'status' DB automatically "pending" set kar dega.

# ==========================================
# FRONTEND KO JANE WALA DATA (Output)
# ==========================================
class CaseResponse(BaseModel):
    # id: uuid.UUID
    
    title: str
    # raw_description: str  # <-- DB model se add kiya
    llm_summary: str | None = None
    # lawyer_approved_summary: str | None = None  # <-- DB model se add kiya
    status: str
    # user_id: uuid.UUID
    # created_at: datetime


   

