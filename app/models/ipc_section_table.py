import uuid
from sqlmodel import Field
from typing import Optional

# Base model ko import kar rahe hain
from app.models.base import CoreModel

class IpsSection(CoreModel, table=True):

    # if neeche vali line not comes then sql model class ke naam ko lower case me karke table bna deta hai , but we
    # explicitly convert that to table 
    __tablename__ = "ips_section"
    
    section_code: str = Field(index=True, unique=True, nullable=False)
    section_name: str = Field(nullable=False)
    description: Optional[str] = None
    penalty: Optional[str] = None
    
    # 🎯 Foreign Key type badalkar uuid.UUID kiya gaya hai taaki Cases table se match kare
    case_id: uuid.UUID = Field(foreign_key="cases.id", nullable=False)

   