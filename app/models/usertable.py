from sqlmodel import Field
from typing import Optional
from app.models.base import CoreModel # Base model import kiya

class User(CoreModel, table=True):
    __tablename__ = "user"
    
    # id, created_at, updated_at khud ba khud aa jayenge!
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)


























    # from typing import Optional->Database ki bhasha mein iska matlab hai NULL ALLOWED

    # (SQLModel, table=True): due to this line Python samajh jata hai ki "Oh, mujhe is class ko PostgreSQL ki table mein convert karna hai!"