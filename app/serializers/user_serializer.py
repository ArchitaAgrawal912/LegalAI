from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

# FRONTEND SE AANE WALA DATA (Input)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Frontend plain text bhejega, hum route me hash karenge
    full_name: Optional[str] = None

# FRONTEND KO JANE WALA DATA (Output)
class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    # 🎯 Notice: Yahan password_hash missing hai, for security!