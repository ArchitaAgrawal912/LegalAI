from sqlmodel import SQLModel, Field
from typing import Optional

class IPCSection(SQLModel, table=True):
    __tablename__ = "ipcsection"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    section_number: str
    title: str
    description: str