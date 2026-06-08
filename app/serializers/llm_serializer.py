from sqlmodel import SQLModel
from typing import List

class SummaryResponse(SQLModel):
    title: str
    summary: str

class SectionItem(SQLModel):
    ipc_section: str
    bns_section: str
    reason: str

class SectionResponse(SQLModel):
    sections: List[SectionItem]

# LLM OUTPUT MUST BE LIKE THIS