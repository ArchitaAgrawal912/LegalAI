from pydantic import BaseModel

class LawyerDecision(BaseModel):
    decision: str