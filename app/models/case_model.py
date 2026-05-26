from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Case(SQLModel, table=True):
    __tablename__ = "case"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    ai_conclusion: Optional[str] = None
    reasoning: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)