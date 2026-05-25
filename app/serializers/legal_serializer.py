from pydantic import BaseModel
from typing import List


class LegalQueryRequest(BaseModel):
    query: str


class LegalQueryResponse(BaseModel):
    ipc_sections: List[str]
    bns_sections: List[str]
    legal_concepts: List[str]