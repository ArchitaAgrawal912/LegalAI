# from __future__ import annotations
from sqlmodel import Field, Relationship
from typing import List, TYPE_CHECKING
from app.models.base_model import BaseModel
if TYPE_CHECKING:
    from app.models.case_model import Case

class User(BaseModel, table=True):
    __tablename__ = "users"

    name: str
    email: str = Field(unique=True, nullable=False) #index=True (duplicates allowed)-> unique=True(no duplicates as well as fast searching)
    phone_no: str
    password_hash: str
    is_active: bool = Field(default=True)

    cases: List["Case"] = Relationship(back_populates="user")

    # *cases -> variable name
    # *user -> variable name