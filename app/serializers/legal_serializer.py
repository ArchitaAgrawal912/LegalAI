from pydantic import BaseModel
from typing import List

class CaseReference(BaseModel):
    title: str
    court: str
    year: str
    citation: str


class LegalQueryRequest(BaseModel):
    query: str


class LegalQueryResponse(BaseModel):
    ipc_sections: List[str]
    bns_sections: List[str]
    reason: List[str]
    # case_references: List[CaseReference]  # UPDATED: was List[str]
    # next_steps: List[str]

