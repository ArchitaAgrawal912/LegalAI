
from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship
from pydantic import EmailStr  # 🎯 Yeh naya import add karna hai
from app.models.base import BaseModel
from datetime import datetime, timezone  
# This prevents Circular Imports!
if TYPE_CHECKING:
    from app.models.legal_case import LegalCase

class User(BaseModel, table=True):
    name: str
    email: EmailStr = Field(unique=True, index=True)  # 🎯 str hata kar EmailStr laga diya
    phone_no: str 
    password_hash: str
    is_active: bool = Field(default=True)
    
    # Relationship: A user can have many Legal Cases
    cases: List["LegalCase"] = Relationship(back_populates="user")
















    # from typing import Optional->Database ki bhasha mein iska matlab hai NULL ALLOWED

    # (SQLModel, table=True): due to this line Python samajh jata hai ki "Oh, mujhe is class ko PostgreSQL ki table mein convert karna hai!"