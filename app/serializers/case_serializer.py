from __future__ import annotations
from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID

class CaseCreate(SQLModel):
    title: str
    case_description: str
    user_id: UUID

class CaseUpdate(SQLModel):
    title: Optional[str] = None
    case_description: Optional[str] = None

class CaseResponse(SQLModel):
    id: UUID
    title: str
    case_description: str
    status: str
    user_id: UUID

class SummaryResponse(SQLModel):
    id: UUID
    title: str
    llm_summary: str

class ApproveRejectRequest(SQLModel):
    approved: bool

